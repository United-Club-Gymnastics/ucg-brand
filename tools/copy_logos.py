"""Copy logo SVG + PNG files from the designer's toolkit into assets/logos with
URL-safe names. Files are copied byte for byte (never redrawn or re-exported).
Usage: python tools/copy_logos.py "<path to 01_Design ToolKit/01_Assets/01_Logo>" """
import shutil
import sys
from pathlib import Path

SRC = Path(sys.argv[1])
DST = Path(__file__).resolve().parent.parent / "assets" / "logos"
DST.mkdir(parents=True, exist_ok=True)

# designer folder name -> colorway slug
COLORWAYS = {"_Primary": "navy", "Light": "light", "ᆞBlack": "black", "ᆞWhite": "white"}
# (folder under 01_Logo, optional subfolder, file stem) -> family slug
FAMILIES = [
    ("01_Primary Logo", None, "UCG - Primary Logo", "primary"),
    ("02_Secondary Logo", None, "UCG - Secondary Logo", "secondary"),
    ("03_Logotype", "Logotype", "UCG - Logotype", "logotype"),
    ("03_Logotype", "Logotype Alt1", "UCG - Logotype Alt1", "wordmark-full-name"),
    ("03_Logotype", "Logotype Alt2", "UCG - Logotype Alt2", "wordmark-ucg"),
    ("04_Mark", None, "UCG - Mark", "mark"),
    ("05_Badge", "Badge - Circle", "UCG - Badge - Circle", "badge-circle"),
    ("05_Badge", "Badge - Crest", "UCG - Badge - Crest", "badge-crest"),
]
n = 0
for folder, sub, stem, fam in FAMILIES:
    for cw_dir, cw in COLORWAYS.items():
        base = SRC / folder / cw_dir
        if sub:
            base = base / sub
        for ext in ("svg", "png"):
            f = base / f"{stem}.{ext}"
            if f.exists():
                shutil.copyfile(f, DST / f"ucg-{fam}-{cw}.{ext}")
                n += 1
            else:
                print("missing", f)
extras = {
    SRC / "04_Mark" / "Mark - White on Dark Blue Green - Socials Profile - Circle.svg": "ucg-avatar-circle.svg",
    SRC / "06_Document Header" / "UCG - Document Header.svg": "ucg-document-header.svg",
    SRC / "06_Document Header" / "UCG - Document Header.png": "ucg-document-header.png",
    SRC / "04_Mark" / "UCG - Mark - Social Media Profiles and Avatars - Circle.png": "ucg-avatar-circle.png",
    SRC / "04_Mark" / "UCG - Mark - Social Media Profiles and Avatars - Square.png": "ucg-avatar-square.png",
    SRC / "04_Mark" / "UCG - Mark - in circle - white on dark blue green Favicon.png": "ucg-favicon.png",
    SRC / "04_Mark" / "UCG - Mark - in circle - light blue on navy blue.png": "ucg-mark-in-circle-light-on-navy.png",
}
for f, name in extras.items():
    shutil.copyfile(f, DST / name)
    n += 1
# social and digital files (sources: the "05 Social & Digital" artboards in All UCG Assets.svg)
SOCIAL = DST.parent / "social"
social = {
    "UCG_Facebook_Cover_Photo.png": "ucg-facebook-cover.png",
    "ucg-youtube-banner-2048x1152.png": "ucg-youtube-banner-2048x1152.png",
    "UCG Zoom Background.png": "ucg-zoom-background.png",
    "UCG Zoom Background (mirror).png": "ucg-zoom-background-mirrored.png",
    "ucg-email-header-logo.png": "ucg-email-header.png",
}
for f, name in social.items():
    shutil.copyfile(SRC.parent / f, SOCIAL / name)
    n += 1
print("copied", n, "files to", DST)
