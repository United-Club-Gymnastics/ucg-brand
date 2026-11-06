"""The UCG mark, built from its construction instead of the designer's traced outlines.

The delivered files drew the six V's by hand: each one a little different, not exactly 60 degrees
apart, with extra nodes and a tiny flat notch at every inner point, and the whole mark stretched
0.55% sideways (the dot is an ellipse). Fitting all six V's gives one clean construction:

- each V is two straight legs, 22.5 degrees either side of its axis, LEG_W wide;
- the rounded base is a circle centred on the V's inner point, radius LEG_W;
- each leg ends square to the leg, with a slight outward arc (sagitta END_SAG);
- six identical V's at exactly 60 degree steps (axes at 30, 90, ... 330 degrees, y down);
- the dot is a true circle.

Each V has 8 nodes: the base apex, the two points where the base meets the outer edges, the two
corners at the end of each leg, and the inner point. Units: the 126 x 126 frame of
`UCG - Mark.svg`, centre (CX, CY). The fit is within 0.21 units of all six original V's once the
stretch is removed, and within 0.35 units of the original outline.
"""
import math

THETA = math.radians(22.5)  # leg angle from the V's axis
LEG_W = 13.93852            # leg width; also the base-arc radius
INNER_D = 32.79597          # mark centre -> inner point of each V
LEG_L = 62.48772            # leg ends: projection along the leg from the mark centre
END_SAG = 0.48088           # outward bulge of each leg end
DOT_R = 10.88386            # dot radius
CX = CY = 62.53441          # mark centre in the 126 x 126 frame
V_AXES = [-90, -30, 30, 90, 150, 210]  # SVG degrees (y down): top, then clockwise


def _arc(c, r, a0, a1):
    """One cubic Bezier for a circular arc from angle a0 to a1 (radians, under 90 degrees)."""
    k = 4 / 3 * math.tan((a1 - a0) / 4)
    p0 = (c[0] + r * math.cos(a0), c[1] + r * math.sin(a0))
    p3 = (c[0] + r * math.cos(a1), c[1] + r * math.sin(a1))
    p1 = (p0[0] - k * r * math.sin(a0), p0[1] + k * r * math.cos(a0))
    p2 = (p3[0] + k * r * math.sin(a1), p3[1] - k * r * math.cos(a1))
    return p1, p2, p3


def v_canonical():
    """One V as path commands, in a frame with the mark centre at the origin, +y outward along
    the V's axis and x across it. Commands: ("M", p), ("L", p), ("C", c1, c2, p)."""
    th, w, d, L, s = THETA, LEG_W, INNER_D, LEG_L, END_SAG
    u = (math.sin(th), math.cos(th))      # along the right leg
    n = (math.cos(th), -math.sin(th))     # across it, inner edge -> outer edge
    dot = lambda a, b: a[0] * b[0] + a[1] * b[1]
    V0 = (0.0, d)
    T = (V0[0] + w * n[0], V0[1] + w * n[1])
    Ei = tuple(V0[i] + (L - dot(V0, u)) * u[i] for i in range(2))
    Eo = tuple(T[i] + (L - dot(T, u)) * u[i] for i in range(2))
    R = (w * w / 4 + s * s) / (2 * s)
    mid = ((Eo[0] + Ei[0]) / 2, (Eo[1] + Ei[1]) / 2)
    ce = (mid[0] - (R - s) * u[0], mid[1] - (R - s) * u[1])
    a_o = math.atan2(Eo[1] - ce[1], Eo[0] - ce[0]); a_i = math.atan2(Ei[1] - ce[1], Ei[0] - ce[0])
    end = _arc(ce, R, a_o, a_i)                     # Eo -> Ei
    base = _arc(V0, w, -math.pi / 2, -th)           # apex -> T
    m = lambda p: (-p[0], p[1])
    apex = (0.0, d - w)
    return [("M", apex), ("C",) + base, ("L", Eo), ("C",) + end, ("L", V0), ("L", m(Ei)),
            ("C", m(end[1]), m(end[0]), m(Eo)), ("L", m(T)), ("C", m(base[1]), m(base[0]), apex)]


def dot_canonical():
    r = DOT_R
    pts = [(0, -r), (r, 0), (0, r), (-r, 0)]
    cmds = [("M", pts[0])]
    for i in range(4):
        a0 = -math.pi / 2 + i * math.pi / 2
        cmds.append(("C",) + _arc((0, 0), r, a0, a0 + math.pi / 2))
    return cmds


def placed(cmds, axis_deg, affine):
    """Rotate canonical commands so +y points along axis_deg (SVG degrees), then apply
    affine = (a, b, c, d, e, f) mapping mark-frame units (origin = mark centre) to output."""
    ph = math.radians(axis_deg)
    ax, ac = (math.cos(ph), math.sin(ph)), (-math.sin(ph), math.cos(ph))
    a, b, c, d, e, f = affine
    def T(p):
        x = p[0] * ac[0] + p[1] * ax[0]; y = p[0] * ac[1] + p[1] * ax[1]
        return (a * x + c * y + e, b * x + d * y + f)
    return [(k[0],) + tuple(T(p) for p in k[1:]) for k in cmds]


def to_d(cmds, nd=3):
    def num(v):
        s = f"{v:.{nd}f}".rstrip("0").rstrip(".")
        return "0" if s in ("-0", "") else s
    return "".join(k[0] + " ".join(f"{num(p[0])} {num(p[1])}" for p in k[1:]) for k in cmds) + "Z"


# Outlines (expressive use). The tightest gap in the mark is between neighbouring V's: V_GAP units
# (about 4% of the mark's width). A centred stroke as wide as that gap makes neighbouring outlines
# touch, so keep it well under: about 3% of the mark's width reads as a clean outline.
V_GAP = 4.918
STROKE_GOOD = 3.6          # units: about 2.9% of the 124-unit mark width
STROKE_TOO_THICK = 9.0     # units: wider than V_GAP, so outlines merge (the "don't")


def outline_svg(color="#DBEBEE", width=STROKE_GOOD):
    """The mark as an outline only (no fill), with a margin so the stroke is never cropped."""
    aff = (1, 0, 0, 1, CX, CY)
    ds = [to_d(placed(v_canonical(), ax, aff)) for ax in V_AXES] + [to_d(placed(dot_canonical(), -90, aff))]
    m = width / 2 + 1
    return (f'<svg viewBox="{-m:.2f} {-m:.2f} {126 + 2 * m:.2f} {126 + 2 * m:.2f}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">'
            f'<path d="{"".join(ds)}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linejoin="miter" stroke-miterlimit="10"/></svg>')


def mark_svg(fill="#1E2B38"):
    """The mark alone in the original 126 x 126 frame."""
    aff = (1, 0, 0, 1, CX, CY)
    ds = [to_d(placed(v_canonical(), ax, aff)) for ax in V_AXES] + [to_d(placed(dot_canonical(), -90, aff))]
    return ('<svg width="126" height="126" viewBox="0 0 126 126" fill="none" xmlns="http://www.w3.org/2000/svg">\n'
            + "".join(f'<path d="{d}" fill="{fill}"/>\n' for d in ds) + "</svg>\n")


if __name__ == "__main__":
    print(mark_svg())
