#!/usr/bin/env python3
"""Render a 1200x630 social-preview (Open Graph) PNG for one digital product.

Used by build_digital_products.py so every shareable product page gets its own
theTechMentor-branded LinkedIn/WhatsApp preview instead of the generic site cover.
Needs Pillow (and cairosvg for the logo); if they are missing the build keeps
any image already on disk and falls back to the site cover.
"""
import io
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1200, 630
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
LOGO_SVG = os.path.join(REPO, "public", "images", "logo-mark.svg")
FONT_DIRS = ["/usr/share/fonts/opentype/inter", "/usr/share/fonts/truetype/inter", "/Library/Fonts", os.path.expanduser("~/Library/Fonts")]


def font(weight, size):
    names = {"black": ["Inter-Black.otf", "Inter-ExtraBold.otf", "Inter-Bold.otf"],
             "bold": ["Inter-Bold.otf", "Inter-SemiBold.otf"],
             "semibold": ["Inter-SemiBold.otf", "Inter-Medium.otf"],
             "regular": ["Inter-Regular.otf", "Inter-Medium.otf"]}[weight]
    for d in FONT_DIRS:
        for n in names:
            p = os.path.join(d, n)
            if os.path.exists(p):
                return ImageFont.truetype(p, size)
    for fallback in ("DejaVuSans-Bold.ttf" if weight != "regular" else "DejaVuSans.ttf",):
        try:
            return ImageFont.truetype(fallback, size)
        except OSError:
            pass
    return ImageFont.load_default(size)


def wrap(draw, text, f, max_w, max_lines):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while draw.textlength(lines[-1] + "…", font=f) > max_w and " " in lines[-1]:
            lines[-1] = lines[-1].rsplit(" ", 1)[0]
        lines[-1] += "…"
    return lines


def glow(img, xy, r, color):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).ellipse((xy[0] - r, xy[1] - r, xy[0] + r, xy[1] + r), fill=color)
    img.alpha_composite(layer.filter(ImageFilter.GaussianBlur(r * 0.45)))


def render(p, cat_label, out_path, domain="youronementor.com"):
    free = p["price"] == 0
    img = Image.new("RGBA", (W, H), (6, 5, 26, 255))
    # background: vertical gradient + soft glows
    grad = Image.linear_gradient("L").resize((W, H)).rotate(0)
    top, bottom = Image.new("RGBA", (W, H), (8, 6, 34, 255)), Image.new("RGBA", (W, H), (22, 10, 60, 255))
    img = Image.composite(bottom, top, grad)
    glow(img, (1040, 90), 300, (124, 58, 237, 150))
    glow(img, (120, 640), 260, (34, 211, 238, 70))
    glow(img, (760, 560), 220, (236, 72, 153, 60))
    # subtle grid, faded towards the bottom-left
    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    for x in range(0, W, 60):
        gd.line([(x, 0), (x, H)], fill=(255, 255, 255, 14))
    for y in range(0, H, 60):
        gd.line([(0, y), (W, y)], fill=(255, 255, 255, 14))
    fade = Image.linear_gradient("L").rotate(135, expand=False).resize((W, H))
    grid.putalpha(Image.composite(grid.getchannel("A"), Image.new("L", (W, H), 0), fade))
    img.alpha_composite(grid)
    d = ImageDraw.Draw(img)

    pad = 72
    # brand row: logo + "theTechMentor"
    x = pad
    try:
        import cairosvg
        png = cairosvg.svg2png(url=LOGO_SVG, output_width=56, output_height=56)
        logo = Image.open(io.BytesIO(png)).convert("RGBA")
        img.alpha_composite(logo, (x, 58))
        x += 70
    except Exception:
        pass
    fb = font("bold", 34)
    for part, col in (("the", (244, 242, 255)), ("Tech", (167, 139, 250)), ("Mentor", (244, 242, 255))):
        d.text((x, 64), part, font=fb, fill=col)
        x += d.textlength(part, font=fb)

    # badge pill (top right)
    badge = ("FREE " + ("STUDY GUIDE" if p["category"] == "notes" else "DOWNLOAD")) if free else f"₹{p['price']:,}"
    fbadge = font("bold", 24)
    bw = d.textlength(badge, font=fbadge) + 44
    bx = W - pad - bw
    d.rounded_rectangle((bx, 60, bx + bw, 108), radius=24, fill=(16, 185, 129, 255) if free else (139, 92, 246, 255))
    d.text((bx + 22, 70), badge, font=fbadge, fill=(255, 255, 255))

    # category eyebrow
    fe = font("semibold", 24)
    d.text((pad, 170), cat_label.split(" (")[0].upper(), font=fe, fill=(167, 139, 250))

    # title (auto-size to fit 3 lines)
    title = p["title"]
    for size in (68, 62, 56, 50, 46):
        ft = font("black", size)
        lines = wrap(d, title, ft, W - 2 * pad, 3)
        if not lines[-1].endswith("…") or size == 46:
            break
    y = 212
    for ln in lines:
        d.text((pad, y), ln, font=ft, fill=(255, 255, 255))
        y += int(size * 1.14)

    # accent bar
    d.rounded_rectangle((pad, y + 18, pad + 120, y + 24), radius=3, fill=(34, 211, 238))

    # footer: facts + domain
    ff = font("semibold", 26)
    facts = " · ".join(x for x in ("Free" if free else f"₹{p['price']:,}", p.get("format", ""), f"{p.get('pages')} pages" if p.get("pages") else "") if x)
    d.text((pad, H - 92), facts, font=ff, fill=(205, 201, 234))
    fd = font("bold", 26)
    dw = d.textlength(domain, font=fd)
    d.text((W - pad - dw, H - 92), domain, font=fd, fill=(167, 139, 250))

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.convert("RGB").save(out_path, "PNG", optimize=True)
    return out_path
