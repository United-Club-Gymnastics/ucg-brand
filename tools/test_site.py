"""Test the brand site the way the public sees it (Saira Condensed + Arial, no licensed fonts).

Checks every page at desktop and phone width: WCAG AA contrast of all text, palette pairs the
design guide rejects at that size (DG p42-43, via tools/contrast.py), horizontal
overflow, broken same-site links/images, noindex tag, console errors. Saves screenshots.
Usage: python tools/test_site.py http://127.0.0.1:8123/ucg-brand/ <screenshot dir>
"""
import json
import re
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urljoin, urlparse

from playwright.sync_api import sync_playwright

BASE = sys.argv[1].rstrip("/") + "/"
SHOTS = Path(sys.argv[2]) if len(sys.argv) > 2 else None
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_site import PAGES  # noqa: E402
import contrast  # noqa: E402

# palette pairs the guide rejects: "rgb" strings of (fg, bg) -> "small" (not for small text) or "all"
def _rgb(h):
    return ",".join(str(int(h[i:i + 2], 16)) for i in (1, 3, 5))
GUIDE_BAN = {}
for (fg, bg), g in contrast.GUIDE.items():
    if g in ("large", "small-no", "no"):
        GUIDE_BAN[_rgb(contrast.C[fg][1]) + "|" + _rgb(contrast.C[bg][1])] = "all" if g == "no" else "small"

URLS = [BASE] + [BASE + p[0] + "/" for p in PAGES] + [BASE + "templates/email/example-announcement.html", BASE + "site/email-example-dark.html"]

css = urllib.request.urlopen(urllib.request.Request(
    "https://fonts.googleapis.com/css2?family=Saira+Condensed:wght@700",
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120 Safari/537.36"})).read().decode()
saira = re.search(r"url\((https://[^)]+)\)", css).group(1)
# Shadow the locally installed licensed fonts so screenshots match what visitors see
FALLBACK = f"""@font-face{{font-family:"Greed Condensed";src:url({saira});font-weight:100 900}}
@font-face{{font-family:"Suisse Intl";src:local("Arial");font-weight:100 500}}
@font-face{{font-family:"Suisse Intl";src:local("Arial Bold");font-weight:600 900}}"""

CHECK_JS = r"""(ban) => {
  const rgba = s => { const m = s.match(/rgba?\(([^)]+)\)/); if (!m) return null;
    const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number); return [p[0], p[1], p[2], p.length > 3 ? p[3] : 1]; };
  const lum = c => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2]); };
  const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
  const blend = (top, bot) => { const a = top[3]; return [0,1,2].map(i => top[i] * a + bot[i] * (1 - a)).concat([1]); };
  function bgOf(el) {
    const stack = [];
    for (let e = el; e && e.nodeType === 1; e = e.parentElement) {
      const cs = getComputedStyle(e);
      if (cs.backgroundImage && cs.backgroundImage !== 'none' && !cs.backgroundImage.startsWith('linear-gradient') && !cs.backgroundImage.startsWith('repeating')) return {img: true};
      const c = rgba(cs.backgroundColor);
      if (c && c[3] > 0) { stack.push(c); if (c[3] >= 1) break; }
    }
    let col = [255, 255, 255, 1];
    for (let i = stack.length - 1; i >= 0; i--) col = blend(stack[i], col);
    return {col};
  }
  const out = [], photo = [];
  const all = document.querySelectorAll('body *');
  for (const el of all) {
    if (el.closest('[data-contrast-skip],svg,script,style,noscript,[aria-hidden="true"]')) continue;
    const own = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (!own) continue;
    const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
    if (r.width === 0 || r.height === 0 || cs.visibility === 'hidden' || cs.display === 'none') continue;
    if (el.closest('details:not([open])') && !el.closest('summary')) continue;
    const fg = rgba(cs.color); const b = bgOf(el);
    if (b.img) { photo.push(el.textContent.trim().slice(0, 40)); continue; }
    const fgc = fg[3] < 1 ? blend(fg, b.col) : fg;
    const size = parseFloat(cs.fontSize), w = parseInt(cs.fontWeight);
    const large = size >= 24 || (size >= 18.66 && w >= 700);
    const need = large ? 3 : 4.5, got = ratio(fgc, b.col);
    const bgs = 'rgb(' + b.col.slice(0,3).map(Math.round).join(',') + ')';
    if (got < need - 0.01) out.push({text: el.textContent.trim().slice(0, 50), fg: cs.color, bg: bgs, ratio: +got.toFixed(2), need});
    const key = fgc.slice(0,3).map(Math.round).join(',') + '|' + b.col.slice(0,3).map(Math.round).join(',');
    if (ban[key] === 'all' || (ban[key] === 'small' && !large)) out.push({text: el.textContent.trim().slice(0, 50), fg: cs.color, bg: bgs, guide: 'not approved at this size (DG p42-43)'});
  }
  const over = document.documentElement.scrollWidth > window.innerWidth + 1;
  const wide = over ? [...all].filter(e => e.getBoundingClientRect().right > window.innerWidth + 1 && !e.closest('.matrix-scroll,.table-wrap,pre'))
                         .slice(0, 6).map(e => e.tagName + '.' + (e.className || '').toString().slice(0, 40)) : [];
  const refs = [...document.querySelectorAll('a[href],img[src],source[src],iframe[src],link[href],video[poster],script[src]')]
     .map(e => e.getAttribute('href') || e.getAttribute('src') || e.getAttribute('poster'));
  ['data-src-light','data-src-white','data-src-bw','data-href-light','data-href-white','data-href-bw'].forEach(a =>
     document.querySelectorAll('[' + a + ']').forEach(e => refs.push(e.getAttribute(a))));
  const robots = document.querySelector('meta[name=robots]');
  return {fails: out, photo, overflow: over, wide, refs, noindex: !!(robots && /noindex/.test(robots.content))};
}"""

problems, checked, seen = [], set(), {}
with sync_playwright() as p:
    br = p.chromium.launch(channel="chrome")
    for vw, vh, tag in ((1280, 900, "desktop"), (390, 844, "mobile")):
        ctx = br.new_context(viewport={"width": vw, "height": vh}, device_scale_factor=1)
        for url in URLS:
            page = ctx.new_page()
            errors = []
            page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.goto(url, wait_until="networkidle")
            page.add_style_tag(content=FALLBACK)
            page.evaluate("document.fonts.ready")
            page.wait_for_timeout(300)
            # scroll through so lazy images load before screenshots
            page.evaluate("async () => { for (let y = 0; y < document.body.scrollHeight; y += 700) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 40)); } window.scrollTo(0, 0); }")
            page.wait_for_timeout(500)
            r = page.evaluate(CHECK_JS, GUIDE_BAN)
            name = urlparse(url).path.replace("/ucg-brand/", "").strip("/").replace("/", "_") or "home"
            if r["fails"]:
                problems.append((tag, name, "contrast", r["fails"][:8]))
            if r["overflow"]:
                problems.append((tag, name, "overflow", r["wide"]))
            if "email" not in name and not r["noindex"]:
                problems.append((tag, name, "noindex missing", ""))
            errs = [e for e in errors if "favicon" not in e]
            if errs:
                problems.append((tag, name, "console", errs[:3]))
            if tag == "desktop":
                seen[name] = r["photo"]
                for ref in r["refs"]:
                    if not ref or ref.startswith(("#", "mailto:", "data:", "javascript:")):
                        continue
                    full = urljoin(url, ref).split("#")[0]
                    if urlparse(full).netloc != urlparse(BASE).netloc or full in checked:
                        continue
                    checked.add(full)
                    resp = page.request.get(full)
                    if resp.status != 200:
                        problems.append((tag, name, f"broken {resp.status}", ref))
            if SHOTS:
                SHOTS.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(SHOTS / f"{name}_{tag}.png"), full_page=True)
            page.close()
        ctx.close()
    br.close()

print(f"checked {len(URLS)} pages x 2 widths, {len(checked)} same-site URLs")
for p_ in problems:
    print("PROBLEM", p_[0], p_[1], p_[2], json.dumps(p_[3])[:600])
print("text over photos to eyeball:", {k: v[:4] for k, v in seen.items() if v})
print("OK" if not problems else f"{len(problems)} problems")
