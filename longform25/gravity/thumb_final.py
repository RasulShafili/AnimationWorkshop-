"""owner's Gemini art + our words → 1280×720"""
import sys; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/gravity")
from PIL import Image, ImageEnhance, ImageDraw, ImageFont, ImageFilter
im = Image.open("/home/rasul/Downloads/Gemini_Generated_Image_dw4eqkdw4eqkdw4e.jpeg").convert("RGB"); w, h = im.size; cw = h * 16 // 9; im = im.crop((0, 0, cw, h)).resize((2560, 1440), Image.LANCZOS); im = ImageEnhance.Color(im).enhance(1.18); im = ImageEnhance.Contrast(im).enhance(1.06)
sh = Image.new("L", im.size, 0); d = ImageDraw.Draw(sh); d.ellipse((-500, -520, 1350, 980), fill=120); sh = sh.filter(ImageFilter.GaussianBlur(220)); im.paste(Image.new("RGB", im.size, (8, 40, 70)), (0, 0), sh)
L = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L); F = "/home/rasul/.local/share/fonts/MontserratXB.ttf"
for s, size, y, col in (("DON'T", 318, 40, (255, 255, 255)), ("JUMP!", 340, 350, (255, 216, 24))):
    f = ImageFont.truetype(F, size); d.text((74, y + 18), s, font=f, fill=(0, 0, 0, 150), stroke_width=40, stroke_fill=(0, 0, 0, 150)); d.text((60, y), s, font=f, fill=col, stroke_width=34, stroke_fill=(0, 0, 0)); d.text((60, y), s, font=f, fill=col)
L = L.rotate(3, resample=Image.BICUBIC, center=(640, 380)); im.paste(L, (0, 0), L); im = im.resize((1280, 720), Image.LANCZOS); im.save("out/thumbnail_final.jpg", quality=94); print(im.size)
