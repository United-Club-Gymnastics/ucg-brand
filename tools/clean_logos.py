"""Clean UCG logo SVGs in place: swap the traced mark for the constructed one (tools/mark_geometry.py)
and drop artboard clip paths that don't clip anything.

How the mark is found, in any file, at any size, position or rotation:
1. Every closed subpath that is a near-circle is a candidate dot.
2. Around each dot, subpaths that match the ideal V (scaled by the dot's size, rotated to their own
   axis) within MATCH_TOL mark units, both ways (so a V cut by other art is not mistaken for a whole
   one), are V's. A dot with at least 3 matching V's is a mark.
3. Each matched V is replaced by the ideal V on the nearest exact 60-degree axis (allowing a
   whole-mark rotation), the dot by a true circle, keeping each subpath's winding direction so
   knockouts stay knockouts. Other subpaths of the same <path> are kept as they are.

Clip paths: an Illustrator export wraps the art in a clip the size of the artboard. They clip
nothing while the art stays inside, but crop anything that grows (a stroke, an effect). Run with
--verify to render each file before and after in Chrome and keep any clip whose removal changes
the picture.

Usage: python tools/clean_logos.py [--dry-run] [--verify] [--keep-clips] file.svg ...
"""
import argparse, math, re, sys
from pathlib import Path

import numpy as np
from lxml import etree
from scipy.spatial import cKDTree
from svgpathtools import parse_path, Path as SPath

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mark_geometry as MG  # noqa: E402

SVG = "http://www.w3.org/2000/svg"
SKIP = {"defs", "clipPath", "mask", "pattern", "symbol", "marker", "metadata"}
MATCH_TOL = 1.0      # mark units (the mark is 125 units across)
MAX_OFFSET = 8.0     # a V may sit this far from its standard spot (the crest's side V's: ~5)
DOT_ROUND = 0.02     # max (rmax - rmin) / r for a dot


# ---------- affine helpers (a, b, c, d, e, f) as in SVG matrix() ----------

def mul(m, n):
    a, b, c, d, e, f = m; A, B, C, D, E, F = n
    return (a * A + c * B, b * A + d * B, a * C + c * D, b * C + d * D, a * E + c * F + e, b * E + d * F + f)


def inv(m):
    a, b, c, d, e, f = m
    det = a * d - b * c
    return (d / det, -b / det, -c / det, a / det, (c * f - d * e) / det, (b * e - a * f) / det)


def parse_transform(s):
    m = (1, 0, 0, 1, 0, 0)
    for name, args in re.findall(r"(\w+)\s*\(([^)]*)\)", s or ""):
        v = [float(x) for x in re.split(r"[\s,]+", args.strip()) if x]
        if name == "matrix": t = tuple(v)
        elif name == "translate": t = (1, 0, 0, 1, v[0], v[1] if len(v) > 1 else 0)
        elif name == "scale": t = (v[0], 0, 0, v[1] if len(v) > 1 else v[0], 0, 0)
        elif name == "rotate":
            r = math.radians(v[0]); co, si = math.cos(r), math.sin(r)
            t = (co, si, -si, co, 0, 0)
            if len(v) == 3:
                t = mul((1, 0, 0, 1, v[1], v[2]), mul(t, (1, 0, 0, 1, -v[1], -v[2])))
        elif name == "skewX": t = (1, 0, math.tan(math.radians(v[0])), 1, 0, 0)
        elif name == "skewY": t = (1, math.tan(math.radians(v[0])), 0, 1, 0, 0)
        else: raise ValueError(name)
        m = mul(m, t)
    return m


def ctm(el):
    m = (1, 0, 0, 1, 0, 0)
    for a in reversed(list(el.iterancestors())):
        m = mul(m, parse_transform(a.get("transform")))
    return mul(m, parse_transform(el.get("transform")))


def apply(m, z):
    a, b, c, d, e, f = m
    return complex(a * z.real + c * z.imag + e, b * z.real + d * z.imag + f)


# ---------- geometry ----------

def sample(sp, n=400):
    return np.array([sp.point(t / n) for t in range(n)])


def signed_area(pts):
    x, y = pts.real, pts.imag
    return 0.5 * np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y)


_CANON_V = None


def canon_v_points():
    global _CANON_V
    if _CANON_V is None:
        d = MG.to_d(MG.placed(MG.v_canonical(), 90, (1, 0, 0, 1, 0, 0)), nd=6)  # axis along +y
        pts = sample(parse_path(d), 4000)
        _CANON_V = (np.column_stack([pts.real, pts.imag]), cKDTree(np.column_stack([pts.real, pts.imag])))
    return _CANON_V


def match_v(pts_root, c, k):
    """If pts (root coords) form a whole V near a dot centred at c with scale k, return its pose
    (axis angle in SVG degrees, offset of the V's origin from c in mark units); else None.
    The pose is fitted freely (rigid: angle + offset), so V's arranged differently from the
    standard mark (as in the crest) still match."""
    from scipy.optimize import least_squares
    m = (pts_root - c) / k
    cen = m.mean()
    if not 25 < abs(cen) < 60:
        return None
    ref, tree = canon_v_points()
    phi0 = math.degrees(math.atan2(cen.imag, cen.real))

    def to_canon(x):
        ph, tx, ty = x
        rot = complex(math.cos(math.radians(90 - ph)), math.sin(math.radians(90 - ph)))
        q = (m - complex(tx, ty)) * rot
        return np.column_stack([q.real, q.imag])

    res = least_squares(lambda x: tree.query(to_canon(x))[0], [phi0, 0.0, 0.0], loss="soft_l1", f_scale=0.1)
    Q = to_canon(res.x)
    off = complex(res.x[1], res.x[2])
    e1, e2 = tree.query(Q)[0].max(), cKDTree(Q).query(ref)[0].max()
    if e1 < MATCH_TOL and e2 < MATCH_TOL and abs(off) < MAX_OFFSET:
        return float(res.x[0]), off, max(e1, e2)
    return None


def cmds_to_local(cmds, m):
    return [(k[0],) + tuple((lambda z: (z.real, z.imag))(apply(m, complex(*p))) for p in k[1:]) for k in cmds]


def clean_paths(root, report):
    """Find marks and replace their subpaths. Returns the number of marks replaced."""
    items = []  # (element, subpath index, subpath, root sample points)
    elems = {}
    for el in root.iter(f"{{{SVG}}}path"):
        if any(etree.QName(a).localname in SKIP for a in el.iterancestors()):
            continue
        d = el.get("d")
        if not d:
            continue
        try:
            subs = parse_path(d).continuous_subpaths()
        except Exception as exc:  # noqa: BLE001
            report.append(f"  ! unparsable path {el.get('id')}: {exc}")
            continue
        M = ctm(el)
        elems[el] = (subs, M)
        for i, sp in enumerate(subs):
            if len(sp) == 0 or not sp.isclosed():
                continue
            pts = sample(sp)
            items.append((el, i, sp, np.array([apply(M, z) for z in pts])))

    # pass 1: every (dot, V) candidate pair with its fit error
    dots = []
    for el, i, sp, P in items:
        c = P.mean(); r = np.abs(P - c)
        if r.mean() < 1e-6 or (r.max() - r.min()) / r.mean() > DOT_ROUND:
            continue
        dots.append((el, i, sp, c, r.min() / MG.DOT_R))
    dot_keys = {(d[0], d[1]) for d in dots}
    cands = {}  # V key -> list of (err, dot index, pose)
    for di, (el, i, sp, c, k) in enumerate(dots):
        for el2, j, sp2, P2 in items:
            if (el2, j) in dot_keys or np.abs(P2.mean() - c) > 70 * k:
                continue
            pose = match_v(P2, c, k)
            if pose is not None:
                cands.setdefault((el2, j), []).append((pose[2], di, pose[:2], sp2))
    # pass 2: each V belongs to the dot it fits best
    per_dot = {}
    for key, lst in cands.items():
        err, di, pose, sp2 = min(lst, key=lambda t: t[0])
        per_dot.setdefault(di, []).append((key[0], key[1], sp2) + pose)

    replaced = {}  # (el, i) -> (local commands, original subpath)
    marks = 0
    for di, found in sorted(per_dot.items()):
        el, i, sp, c, k = dots[di]
        if len(found) < 3:
            report.append(f"  ! dot at ({c.real:.2f}, {c.imag:.2f}) has only {len(found)} V's: left alone")
            continue
        marks += 1
        # a V within SNAP of the standard layout (exact 60-degree axes, no offset) is snapped to it;
        # anything else (a custom arrangement) keeps its fitted pose, rounded to 0.01 degree / unit
        offs = np.array([((f[3] - 30 + 30) % 60) - 30 for f in found])
        delta = math.degrees(math.atan2(np.mean(np.sin(np.radians(offs * 6))), np.mean(np.cos(np.radians(offs * 6))))) / 6
        if abs(delta) < 0.5:
            delta = 0.0
        aff_root = (k, 0, 0, k, c.real, c.imag)
        poses, kinds = [], []
        for el2, j, sp2, phi, off in found:
            grid = 30 + 60 * round((phi - 30 - delta) / 60) + delta
            if abs(off) < 0.6 and abs(phi - grid) < 0.6:
                poses.append([grid, 0j, True])
            else:
                poses.append([phi, off, False])
        # custom V's that mirror each other across the dot's vertical axis are made exact mirrors,
        # with the angle snapped to the nearest 0.5 degree when it is within 0.25
        snap = lambda a: round(a * 2) / 2 if abs(a - round(a * 2) / 2) < 0.25 else a
        for a in range(len(poses)):
            for b in range(a + 1, len(poses)):
                pa, pb = poses[a], poses[b]
                if pa[2] or pb[2]:
                    continue
                if abs(pa[0] + pb[0] - 180) < 1 and abs(pa[1].real + pb[1].real) < 0.3 and abs(pa[1].imag - pb[1].imag) < 0.3:
                    ang = snap((pa[0] + 180 - pb[0]) / 2)
                    ox, oy = (pa[1].real - pb[1].real) / 2, (pa[1].imag + pb[1].imag) / 2
                    pa[0], pa[1] = ang, complex(ox, oy)
                    pb[0], pb[1] = 180 - ang, complex(-ox, oy)
        for (el2, j, sp2, _phi, _off), (axis, off, std) in zip(found, poses):
            kinds.append("std" if std else f"custom axis {axis:.3f} deg, offset ({off.real:.3f}, {off.imag:.3f})")
            local = mul(inv(elems[el2][1]), mul(aff_root, (1, 0, 0, 1, off.real, off.imag)))
            cmds = cmds_to_local(MG.placed(MG.v_canonical(), axis, (1, 0, 0, 1, 0, 0)), local)
            replaced[(el2, j)] = (cmds, sp2)
        local = mul(inv(elems[el][1]), aff_root)
        replaced[(el, i)] = (cmds_to_local(MG.placed(MG.dot_canonical(), -90, (1, 0, 0, 1, 0, 0)), local), sp)
        std = kinds.count("std")
        report.append(f"  mark: centre ({c.real:.2f}, {c.imag:.2f}) scale {k:.4f} V's {len(found)} ({std} standard) rotation {delta:+.2f}"
                      + "".join(f"\n     {x}" for x in kinds if x != "std"))

    # write back, keeping each subpath's winding
    touched = {el for el, _ in replaced}
    for el in touched:
        subs, _M = elems[el]
        parts = []
        for i, sp in enumerate(subs):
            if (el, i) in replaced:
                cmds, orig = replaced[(el, i)]
                new = parse_path(MG.to_d(cmds, nd=6))
                if np.sign(signed_area(sample(new))) != np.sign(signed_area(sample(orig))):
                    parts.append(re.sub(r"(-?\d+\.\d{3})\d+", r"\1", new.reversed().d()) + " Z")
                else:
                    parts.append(MG.to_d(cmds, nd=3))
            else:
                parts.append(sp.d() + ("Z" if sp.isclosed() else ""))
        el.set("d", " ".join(parts))
    return marks


TINY = 0.02  # file units: straight segments shorter than this are seams left by tracing, not drawing


def close_seams(root):
    """Collapse tiny straight segments (seams where two curves almost meet, e.g. 0.01-unit steps at
    the outer edge of the C and G): the neighbours are joined at the segment's midpoint, moving their
    adjacent control points by the same amount so the curves keep their direction. Returns how many."""
    from svgpathtools import Line, CubicBezier
    n = 0
    for el in root.iter(f"{{{SVG}}}path"):
        if any(etree.QName(a).localname in SKIP for a in el.iterancestors()) or not el.get("d"):
            continue
        M = ctm(el); sc = math.sqrt(abs(M[0] * M[3] - M[1] * M[2])) or 1
        subs = parse_path(el.get("d")).continuous_subpaths()
        changed = False
        out = []
        for sp in subs:
            segs = list(sp)
            i = 0
            while len(segs) > 3 and i < len(segs):
                s = segs[i]
                a, b = segs[i - 1], segs[(i + 1) % len(segs)]
                if (isinstance(s, Line) and 0 < s.length() * sc < TINY and sp.isclosed()
                        and isinstance(a, (Line, CubicBezier)) and isinstance(b, (Line, CubicBezier))):
                    mid = (s.start + s.end) / 2
                    da, db = mid - a.end, mid - b.start
                    a = CubicBezier(a.start, a.control1, a.control2 + da, mid) if isinstance(a, CubicBezier) else Line(a.start, mid)
                    b = CubicBezier(mid, b.control1 + db, b.control2, b.end) if isinstance(b, CubicBezier) else Line(mid, b.end)
                    segs[i - 1] = a; segs[(i + 1) % len(segs)] = b
                    del segs[i]
                    n += 1; changed = True
                    continue
                i += 1
            out.append(SPath(*segs))
        if changed:
            el.set("d", " ".join(re.sub(r"(-?\d+\.\d{4})\d+", r"\1", p.d()) + " Z" for p in out))
    return n


def strip_page_masks(root):
    """Remove masks whose only shape is one rectangle covering the whole canvas. They come from PDF
    extraction (a soft mask that meant 'show everything'); in SVG an unfilled one is black, which
    hides the art completely (the event pattern rendered blank). Returns how many uses were removed."""
    vb = [float(v) for v in re.split(r"[\s,]+", (root.get("viewBox") or "0 0 0 0").strip())]
    masks = {}
    for m in root.iter(f"{{{SVG}}}mask"):
        shapes = [e for e in m.iter() if isinstance(e.tag, str) and etree.QName(e).localname in ("path", "rect", "circle", "ellipse", "image", "use", "text")
                  and not any(etree.QName(a).localname == "clipPath" for a in e.iterancestors())]
        if len(shapes) != 1 or etree.QName(shapes[0]).localname not in ("path", "rect"):
            continue
        s = shapes[0]
        fill = None
        for a in [s] + list(s.iterancestors()):
            if a is m:
                break
            fm = re.search(r"fill:\s*([^;]+)", a.get("style") or "")
            fill = fill or (fm.group(1).strip() if fm else a.get("fill"))
        if fill in (None, "#000", "#000000", "black", "rgb(0,0,0)"):
            masks[m.get("id")] = m   # an unfilled (black) mask hides everything it touches: always broken
            continue
        pts = _shape_points(s, mul(ctm(s), (1, 0, 0, 1, 0, 0)))
        if pts is None:
            continue
        if fill.lower() in ("#fff", "#ffffff", "white") and pts.real.min() <= vb[0] + 0.5 and pts.imag.min() <= vb[1] + 0.5 \
                and pts.real.max() >= vb[0] + vb[2] - 0.5 and pts.imag.max() >= vb[1] + vb[3] - 0.5:
            masks[m.get("id")] = m   # a white mask over the whole canvas does nothing
    n = 0
    for el in root.iter():
        if isinstance(el.tag, str):
            ref = re.search(r"url\(#([^)]+)\)", el.get("mask") or "")
            if ref and ref.group(1) in masks:
                del el.attrib["mask"]; n += 1
    for m in masks.values():
        m.getparent().remove(m)
    return n


CLIP_TOL = 0.05  # file units the art may poke past a clip and still count as "not clipped"


def _shape_points(el, M):
    """Sample points of a basic shape in root coords, or None if it isn't one we can measure."""
    tag = etree.QName(el).localname
    f = lambda k, dflt=0.0: float(el.get(k, dflt) or dflt)
    if tag == "path" and el.get("d"):
        return np.array([apply(M, z) for z in sample(parse_path(el.get("d")), 2000)])
    if tag == "rect":
        x, y, w, h = f("x"), f("y"), f("width"), f("height")
        return np.array([apply(M, complex(a, b)) for a, b in ((x, y), (x + w, y), (x + w, y + h), (x, y + h))])
    if tag in ("circle", "ellipse"):
        cx, cy = f("cx"), f("cy")
        rx = f("r") if tag == "circle" else f("rx"); ry = f("r") if tag == "circle" else f("ry")
        t = np.linspace(0, 2 * np.pi, 360)
        return np.array([apply(M, complex(cx + rx * math.cos(a), cy + ry * math.sin(a))) for a in t])
    return None


def _clip_ref(el, css_clip):
    v = el.get("clip-path") or ""
    m = re.search(r"url\(#([^)]+)\)", v) or re.search(r"clip-path\s*:\s*url\(#([^)]+)\)", el.get("style") or "")
    if m:
        return m.group(1)
    for cls in (el.get("class") or "").split():
        if cls in css_clip:
            return css_clip[cls]
    return None


def strip_clips(root):
    """Remove clip paths that clip nothing: a rectangle clip whose content (every shape inside the
    clipped element, in the same coordinates) lies within it, within CLIP_TOL. Clips that cut real
    art, or wrap content we can't measure (text, images), are kept.
    Returns (uses removed, list of kept clip ids with the reason)."""
    css_clip = {}
    for st in root.iter(f"{{{SVG}}}style"):
        for cls, ref in re.findall(r"\.([\w-]+)\s*\{[^}]*clip-path\s*:\s*url\(#([^)]+)\)", st.text or ""):
            css_clip[cls] = ref
    clips = {cp.get("id"): cp for cp in root.iter(f"{{{SVG}}}clipPath")}
    removed, kept = 0, []
    dead_classes = set()
    for el in list(root.iter()):
        if not isinstance(el.tag, str) or any(etree.QName(a).localname in SKIP for a in el.iterancestors()):
            continue
        ref = _clip_ref(el, css_clip)
        if not ref or ref not in clips:
            continue
        M = ctm(el)
        cp = clips[ref]
        if cp.get("clipPathUnits") == "objectBoundingBox":
            kept.append((ref, "objectBoundingBox units")); continue
        clip_pts = []
        ok = True
        for ch in cp:
            if not isinstance(ch.tag, str):
                continue
            if etree.QName(ch).localname != "rect":
                ok = False; break
            clip_pts.append(_shape_points(ch, mul(M, parse_transform(ch.get("transform")))))
        if not ok or not clip_pts:
            kept.append((ref, "not a rectangle")); continue
        C = np.concatenate(clip_pts)
        x0, x1, y0, y1 = C.real.min(), C.real.max(), C.imag.min(), C.imag.max()
        inside = True
        for d in el.iter():
            if not isinstance(d.tag, str) or etree.QName(d).localname in ("g", "title", "desc"):
                continue
            pts = _shape_points(d, ctm(d))
            if pts is None:
                inside = False; kept.append((ref, f"wraps a <{etree.QName(d).localname}>")); break
            if (pts.real.min() < x0 - CLIP_TOL or pts.real.max() > x1 + CLIP_TOL or
                    pts.imag.min() < y0 - CLIP_TOL or pts.imag.max() > y1 + CLIP_TOL):
                inside = False
                kept.append((ref, f"cuts art: content x {pts.real.min():.2f}..{pts.real.max():.2f} y {pts.imag.min():.2f}..{pts.imag.max():.2f}"
                                  f" vs clip x {x0:.2f}..{x1:.2f} y {y0:.2f}..{y1:.2f}"))
                break
        if not inside:
            continue
        if el.get("clip-path"):
            del el.attrib["clip-path"]
        st = el.get("style")
        if st and "clip-path" in st:
            el.set("style", ";".join(p for p in st.split(";") if not p.strip().startswith("clip-path")))
        for cls in (el.get("class") or "").split():
            if cls in css_clip:
                dead_classes.add(cls)
        removed += 1
    # a CSS class whose only job was the dead clip: drop the rule (only if no kept clip uses it)
    kept_refs = {k for k, _ in kept}
    for st in root.iter(f"{{{SVG}}}style"):
        for cls in dead_classes:
            if css_clip[cls] not in kept_refs and st.text:
                st.text = re.sub(rf"\s*\.{re.escape(cls)}\s*\{{\s*clip-path\s*:\s*url\([^)]*\)\s*;?\s*\}}", "", st.text)
    # clipPath defs nothing refers to any more
    used = set()
    for el in root.iter():
        if isinstance(el.tag, str):
            used |= set(re.findall(r"url\(#([^)]+)\)", (el.get("clip-path") or "") + (el.get("style") or "")))
    for st in root.iter(f"{{{SVG}}}style"):
        used |= set(re.findall(r"url\(#([^)]+)\)", st.text or ""))
    for cid, cp in clips.items():
        if cid not in used and cp.getparent() is not None:
            cp.getparent().remove(cp)
    return removed, kept


def render(pg, svg_text, px=1600):
    import io
    from PIL import Image
    vb = [float(v) for v in re.split(r"[\s,]+", re.search(r'viewBox="([^"]+)"', svg_text).group(1).strip())]
    w, h = px, max(1, round(px * vb[3] / vb[2]))
    body = re.sub(r"<\?xml[^>]*\?>", "", svg_text)
    pg.set_viewport_size({"width": w, "height": h})
    pg.set_content(f'<body style="margin:0"><div style="width:{w}px;height:{h}px">{body}</div></body>')
    pg.evaluate("() => { const s = document.querySelector('svg'); s.setAttribute('width','100%'); s.setAttribute('height','100%'); }")
    return np.array(Image.open(io.BytesIO(pg.screenshot(omit_background=True))).convert("RGBA")).astype(int), vb


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--keep-clips", action="store_true")
    a = ap.parse_args()
    pg = None
    if a.verify:
        from playwright.sync_api import sync_playwright
        pw = sync_playwright().start(); br = pw.chromium.launch(); pg = br.new_page()
    for f in a.files:
        raw = Path(f).read_bytes()
        tree = etree.fromstring(raw, etree.XMLParser(remove_blank_text=False, huge_tree=True))
        report = []
        marks = clean_paths(tree, report)
        seams = close_seams(tree)
        if seams:
            report.append(f"  closed {seams} seam(s) under {TINY} units")
        pm = strip_page_masks(tree)
        if pm:
            report.append(f"  removed {pm} whole-canvas mask(s)")
        seams += pm
        after_marks = etree.tostring(tree, xml_declaration=raw.lstrip().startswith(b"<?xml"), encoding="UTF-8").decode("utf-8")
        clips, kept = (0, []) if a.keep_clips else strip_clips(tree)
        out = etree.tostring(tree, xml_declaration=raw.lstrip().startswith(b"<?xml"), encoding="UTF-8").decode("utf-8")
        note = "".join(f"\n  kept clip {cid}: {why}" for cid, why in kept)
        if pg is not None and clips:
            # belt and braces: removing dead clips must not change coverage anywhere (anti-aliasing
            # noise from compositing a clipped group is ignored: only pixels that flip in/out count)
            A, vb = render(pg, after_marks); B, _ = render(pg, out)
            flips = int((np.abs(A[:, :, 3] - B[:, :, 3]) > 128).sum())
            if flips:
                out = after_marks; note += f"\n  clips KEPT: removing them flips {flips} px"; clips = 0
        if pg is not None and marks:
            A, vb = render(pg, raw.decode("utf-8")); B, _ = render(pg, after_marks)
            alpha = lambda X: X[:, :, 3] > 127
            x = alpha(A) ^ alpha(B)
            from scipy import ndimage
            edge = alpha(A) ^ ndimage.binary_erosion(alpha(A))
            dist = ndimage.distance_transform_edt(~edge)
            unit = A.shape[1] / vb[2]
            note += f" | max outline shift {dist[x].max() / unit if x.any() else 0:.3f} file units"
        print(f"{f}: marks {marks}, clip uses removed {clips}{note}")
        for line in report:
            print(line)
        if not a.dry_run and (marks or clips or seams):
            Path(f).write_text(out, encoding="utf-8", newline="\n")
    if pg is not None:
        br.close(); pw.stop()


if __name__ == "__main__":
    main()
