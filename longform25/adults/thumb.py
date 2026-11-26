"""thumbnails 1280×720: A hero drives the school bus (NO ADULTS!)  B empty kitchen, Mom's warm mug (MOM?!)"""
import os, sys
D = "/home/rasul/Desktop/Animations/longform25/adults"; os.environ["SHOW_DATA"] = D + "/out"; os.environ["SHOW_VO"] = D + "/vo16"; sys.path.insert(0, D)
from adults_a import *
from PIL import Image
def big(sc, x, y, s, size, col, rot=0.0):
    c = sc.c; c.save(); c.translate(x, y); c.rotate(rot); c.select_font_face("Montserrat XB"); c.set_font_size(size); e = c.text_extents(s); c.move_to(-e.width / 2 - e.x_bearing, -e.height / 2 - e.y_bearing); c.text_path(s); p = c.copy_path(); c.set_line_join(cairo.LINE_JOIN_ROUND)
    c.save(); c.translate(8, 12); c.set_source_rgba(0, 0, 0, .55); c.set_line_width(size * .30); c.stroke(); c.restore(); c.new_path(); c.append_path(p); c.set_source_rgb(0, 0, 0); c.set_line_width(size * .21); c.stroke(); c.append_path(p); g = cairo.LinearGradient(0, -size * .4, 0, size * .4); g.add_color_stop_rgb(0, *mul(col, 1.15)); g.add_color_stop_rgb(1, *mul(col, .88)); c.set_source(g); c.fill(); c.restore()
def A(text=True):
    t = 1.0; sc = Scene(Cam((.6, -.55, 2.0), (-.25, .7, 1.9), 1150)); bus_int(sc, t, 1.0, pigeons=.4); h = HERO; stand(h, t, (-.35, .2, 1.0), 110, 1); h.face = FACE["laugh"]; h.hyaw = 50; h.hpitch = 5; wp = V(-.35, .55, 1.4); a = .5
    h.hands = [wp + V(-.26 * math.cos(a), -.05, .26 * math.sin(a)), wp + V(.26 * math.cos(a), -.05, -.26 * math.sin(a))]; h.draw(sc); wheel(sc, wp, t, 30); sc.vignette(.35)
    if text: big(sc, 1430, 250, "NO", 200, "ffffff", -.05); big(sc, 1400, 470, "ADULTS!", 180, "ffd21e", -.05)
    return sc
def B(text=True):
    t = 1.0; sc = Scene(Cam((-.2, -1.2, 1.25), (.2, .5, .95), 1100)); KIT.kitchen(sc, .3); KIT.table(sc); mug(sc, (.35, .3, .74), t); flatphone(sc, (-.05, .35, .745), 20, 1); h = HERO; stand(h, t, (-.55, -.2, 0), 20, 1); h.face = FACE["shock"]; reach(h, 0, h.joints()[4] + V(-.2, -.1, -.05)); reach(h, 1, h.joints()[4] + V(.2, -.1, -.05)); h.draw(sc); sc.vignette(.35)
    if text: big(sc, 1380, 250, "MOM?!", 230, "ffd21e", -.05)
    return sc
for n, fn in (("A_no_adults", A), ("A_layout", lambda: A(False)), ("B_mom", B)):
    s = fn().surf; a = np.ndarray((H, W, 4), np.uint8, s.get_data()); Image.fromarray(a[:, :, 2::-1]).resize((1280, 720), Image.LANCZOS).save(f"{D}/out/thumb_{n}.jpg", quality=94)
