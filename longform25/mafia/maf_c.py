"""mafia c09–c12: how the FBI won, the raid, a new life, the letter"""
import sys; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/mafia")
from maf_a import crib_scene, bassinet, MAROON
from maf_b import playpen
from mlib import *
SC = {}
w = wt
def cuffs2d(c, x, y, s, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s); c.set_line_width(10); c.set_source_rgb(*C("c0c8d4"))
    for sg in (-1, 1): c.new_path(); c.arc(sg * 45, 0, 32, 0, 7); c.stroke()
    c.move_to(-15, 0); c.line_to(15, 0); c.stroke(); c.restore()
def stair_cast(sc, t, faces=None):
    for k, ch in enumerate(MEN[:5]): stand(ch, t, (-2.6 + k * 1.3, .6, .5), 0, k); ch.face = FACE["neutral"]
    stand(MEN[5], t, (-1.2, 1.8, 1.0), 0, 5); stand(MEN[6], t, (1.2, 1.8, 1.0), 0, 6); stand(SAL, t, (-.9, 3.0, 1.5), 0, 1); stand(OLD, t, (.9, 3.0, 1.5), 0, 2); stand(DON, t, (0, 4.6, 2.0), 0, 3)
    DON.face = FACE[(faces or {}).get("DON", "smug")]
    for ch in MEN[:7] + [SAL, OLD, DON]: sc.at(sc.cam.depth(ch.hip), lambda ch=ch: (ch.draw(sc), fedora(sc, ch) if ch is DON else None, ring(sc, ch) if ch is DON else None))
def c09(t):
    D = CH["c09"]["dur"]
    n, u, s = shot(t, [(0, "dana"), (lt("c09_n2") - .1, "rico"), (w("c09_n2", "Before") - .1, "before"), (w("c09_n2", "With") - .1, "after"), (lt("c09_n3") - .1, "court"),
                       (w("c09_n3", "Eight") - .1, "eight"), (w("c09_n3", "Most") - .1, "paper"), (lt("c09_n4") - .1, "proof"), (w("c09_n4", "proof", 1) - .2, "crib")], D)
    if n == "dana":
        sc = Scene(K(u, (1.2, -1.2, 1.6), (.9, -.8, 1.6), (-.3, 2.6, 1.7), (-.3, 2.6, 1.75), 1050)); office_fbi(sc, t); stand(DANA, t, (.4, 1.9, 0), 200, 3); DANA.face = FACE["det"]
        DANA.hands[1] = V(-.1, 2.5, 1.9 - .2 * ss(u, .2, .6)); sc.at(sc.cam.depth(DANA.hip), lambda: DANA.draw(sc)); sc.flush(); sc.c.set_source_rgba(.02, .03, .1, .2); sc.c.paint(); sc.vignette(.4); return sc
    if n == "rico":
        sc = Scene(Cam((0, -2, 2), (0, 0, 0))); vgrad(sc, "2a2f3a", "15171c"); doc2d(sc, W / 2, H / 2 + 20, 620, "RICO ACT|1970", ["Racketeer Influenced and", "Corrupt Organizations Act", "", "A boss can be charged", "for the crimes of his", "organization."], "LAW", t, lt("c09_n2") + .8); sc.vignette(.4); return sc
    if n in ("before", "after"):
        sc = Scene(K(u, (3.0, -3.8, 3.2), (2.6, -3.4, 3.1), (0, 2.4, 2.1), (0, 2.4, 2.1), 1000)); stairs(sc, t, 4, .6); stair_cast(sc, t, {"DON": "smug" if n == "before" else "shock"}); sc.flush(); sc.vignette(.35)
        tgt = sc.cam.pr(V(-2.6, .6, 1.4)) if n == "before" else sc.cam.pr(V(0, 4.6, 3.0)); start = (W * .1, H * .9); uu = ss(u, .1, .6); x = start[0] + (tgt[0] - start[0]) * uu; y = start[1] + (tgt[1] - start[1]) * uu
        cuffs2d(sc.c, x, y, 1.4, -.3 + .6 * uu); label(sc, W / 2, 110, "BEFORE RICO: ARREST THE SOLDIER" if n == "before" else "WITH RICO: ARREST THE BOSS", 52, "ffd21e"); return sc
    if n in ("court", "eight"):
        sc = Scene(K(u, (0, -5.5, 2.2), (0, -4.8, 2.1), (0, 2.4, 1.4), (0, 2.4, 1.4), 1050) if n == "court" else K(u, (2.6, -1.6, 1.6), (2.2, -1.4, 1.55), (-1.0, 1.6, 1.1), (-1.0, 1.6, 1.1), 1050))
        courtroom(sc, t); stand(OLD if False else MEN[9], t, (0, 2.9, .5), 0, 9); MEN[9].face = FACE["det"]; sc.at(sc.cam.depth(V(0, 3.0, .5)) + .2, lambda: MEN[9].draw(sc))
        for k in range(8): ch = (MEN + [SAL, DON])[k]; sit(ch, t, (-2.6 + .75 * k, 1.1, .45), 0, k); ch.face = FACE["sad" if k % 2 else "angry"]; sc.at(sc.cam.depth(V(-2.6 + .75 * k, 1.1, .5)), lambda ch=ch: (ch.draw(sc), fedora(sc, ch, "3a3a40")))
        sc.at(sc.cam.depth(V(.5, 2.4, 1.45)) - .1, lambda: gavel(sc, (.5, 2.4, 1.45), t, lt("c09_n3") + 1.2))
        sc.flush(); sc.vignette(.35)
        if n == "court": stamp(sc, "NEW YORK, 1986", clamp(s * 3))
        if n == "eight": label(sc, W / 2, 110, "8 MOB BOSSES CONVICTED", 56, "ffd21e")
        return sc
    if n == "paper":
        sc = Scene(Cam((0, -2, 2), (0, 0, 0))); vgrad(sc, "2a2f3a", "15171c"); c = sc.c; c.save(); c.translate(W * .38, H * .52); c.scale(.9 + .1 * u, .9 + .1 * u); c.translate(-W * .38, -H * .52)
        paper2d(sc, W * .38, H * .52, 600, "MOB BOSSES|GET 100 YEARS", "8 convicted in the Commission case", t, -.04, "JAN. 13, 1987"); c.restore(); bigcount(sc, W * .76, H * .45, "100", 220, "YEARS IN PRISON", "ffd21e", clamp(s * 3)); sc.vignette(.4); return sc
    if n in ("proof", "crib"):
        sc = Scene(K(u, (.8, -.9, 1.7), (.4, -.3, 1.4), (.2, 1.4, .75), (.35, 1.45, .7), 1100, 1400)); nursery(sc, t); crib_scene(sc, t, who=lambda: baby(sc, V(-.15, 1.4, .62), 0, t, "sleep", 0, 1.0, ax=(-1, 0, 0)), bear_=True, mobile=True)
        sc.flush(); sc.c.set_source_rgba(.02, .04, .15, .5); sc.c.paint(); X, Y = sc.cam.pr(V(.45, 1.5, .7)); sc.glow(X, Y, 220, "ffe0a0", .4 * ss(u, .2, .8)); sc.vignette(.5); return sc
SC["c09"] = c09
# ------------------------------------------------------------------ c10 the raid (first birthday, 6 a.m.)
def banner(sc, t):
    onplane(sc, (-1.4, 3.18, 3.2), (2.8, 0, 0), (0, 0, -.45), 700, 110, lambda c, w_, h: (c.set_source_rgb(*C("ffd24a")), c.paint(), txt2d(c, w_ / 2, 76, "HAPPY 1ST BIRTHDAY NICO!", 52, "c0303a")))
    for k in range(5): sc.ball((-3.2 + .25 * k, 2.9, 2.6 + .2 * (k % 2) + .05 * wob(t, .4, k)), .2, ("e8392e", "3d86e0", "ffc93a", "57c785", "8f5ad0")[k], .008)
def agents_in(sc, t, t0, n=3, aim=None):
    for k in range(n):
        ch = AGENTS[k]; tt = t - t0 - .25 * k; x = (-.5 + .5 * k) * clamp(tt); walk(ch, t, [(t0 + .25 * k, 0, 3.6), (t0 + .25 * k + 1.2, x, 1.8 - .5 * k)], k, run=True); ch.face = FACE["det"]
        if tt > 1.1: stand(ch, t, (x, 1.8 - .5 * k, 0), (-30, 0, 30)[k], k); ch.face = FACE["det"]
        ch.hands[1] = ch.hip + dirv(ch.yaw) * .35 + V(0, 0, .35); sc.at(sc.cam.depth(ch.hip), lambda ch=ch: (ch.draw(sc), fbi(sc, ch), flashlight(sc, ch, 1, t, ch.hip + dirv(ch.yaw) * 4 + V(0, 0, -.6))))
def c10(t):
    D = CH["c10"]["dur"]
    n, u, s = shot(t, [(0, "foyer"), (w("c10_n1", "explodes") - .1, "door"), (lt("c10_dana1") - .1, "dana"), (lt("c10_n7") - .1, "robe"), (w("c10_n7", "Sal") - .1, "sal"),
                       (lt("c10_n2") - .1, "office"), (w("c10_n2", "walls") - .1, "walls"), (w("c10_n2", "cars") - .1, "cars"), (w("c10_n2", "freezer") - .1, "freezer"), (w("c10_n2", "nothing") - .1, "nothing"),
                       (lt("c10_n3") - .1, "pickup"), (lt("c10_don1") - .1, "whisper"), (lt("c10_n4") - .1, "memory"), (lt("c10_n5") - .1, "lookbear"), (w("c10_n5", "father") - .1, "lookdad"),
                       (w("c10_n5", "throw") - .1, "throw"), (lt("c10_n6") - .1, "lands"), (w("c10_n6", "feels") - .1, "feels"), (w("c10_n6", "looks") - .1, "stare"), (lt("c10_dana2") - .1, "thanks")], D)
    T_door = w("c10_n1", "explodes")
    if n in ("foyer", "door", "dana", "nothing", "pickup", "lookbear", "lookdad", "throw", "lands", "stare"):
        door = ss(t, T_door, T_door + .25)
        cam = {"foyer": lambda: K(u, (2.4, -4.6, 2.2), (2.0, -4.0, 2.0), (0, 2.8, 1.4), (0, 2.8, 1.4), 1000), "door": lambda: K(u, (.6, -2.8, 1.5), (.5, -2.6, 1.5), (0, 3.2, 1.3), (0, 3.2, 1.3), 1000, hh=.03, t=t),
               "dana": lambda: K(u, (.4, -.6, 1.6), (.3, -.4, 1.6), (0, 2.2, 1.5), (0, 2.2, 1.5), 1100), "nothing": lambda: K(u, (1.6, -2.4, 1.7), (1.4, -2.2, 1.65), (0, 2.6, 1.2), (0, 2.6, 1.2), 1000),
               "pickup": lambda: K(u, (1.8, -2.0, 1.6), (1.5, -1.8, 1.6), (-1.6, .6, 1.2), (-1.6, .6, 1.2), 1050), "lookbear": lambda: K(u, (-1.3, .25, 1.35), (-1.3, .3, 1.32), (-1.35, .9, .05), (-1.35, .9, .05), 1000, 1250),
               "lookdad": lambda: K(u, (-1.25, .15, 1.3), (-1.27, .2, 1.3), (-1.6, .62, 1.42), (-1.6, .62, 1.44), 950, 1100), "throw": lambda: K(u, (1.8, -3.6, 1.6), (1.8, -3.6, 1.6), (-.3, 1.2, .9), (.2, 1.6, .5), 950),
               "lands": lambda: K(u, (.9, -.4, .6), (.85, -.35, .6), (.6, 1.6, .2), (.6, 1.6, .2), 1100), "stare": lambda: K(u, (-.5, .9, 1.55), (-.4, .95, 1.55), (.6, 1.6, 1.5), (.6, 1.6, 1.52), 1300, 1450)}[n]()
        sc = Scene(cam); foyer(sc, t, door=door if n in ("door",) else (1.0 if n != "foyer" else 0.0), dawn=True); banner(sc, t)
        if n == "foyer":
            sit(SAL, t, (-2.6, .8, .45), 90, 2); SAL.face = FACE["sleep"]; sc.at(sc.cam.depth(V(-2.6, .8, .45)), lambda: (sc.box((-2.6, .8, .22), (1.6, .7, .45), "8a2a2a", 0, .01), SAL.draw(sc), cannoli(sc, SAL.hip + V(.25, -.15, .3), 30)))
            sc.flush(); sc.c.set_source_rgba(.1, .12, .3, .35); sc.c.paint(); sc.vignette(.4); stamp(sc, "1ST BIRTHDAY · 6:00 A.M.", clamp(s * 3)); return sc
        if n == "door": agents_in(sc, t, T_door + .15, 3)
        if n == "dana":
            for k in range(3): ch = AGENTS[k]; stand(ch, t, (-1.2 + 1.2 * k, 2.7 - .2 * (k % 2), 0), (-20, 0, 20)[k], k); ch.face = FACE["det"]; ch.hands[1] = ch.hip + dirv(ch.yaw) * .35 + V(0, 0, .35); sc.at(sc.cam.depth(ch.hip), lambda ch=ch: (ch.draw(sc), fbi(sc, ch), flashlight(sc, ch, 1, t, ch.hip + dirv(ch.yaw) * 4 + V(0, 0, -.6))))
        if n in ("door", "dana", "nothing", "pickup", "lookbear", "lookdad", "throw", "lands", "stare"):
            dp = (.6, 1.6) if n in ("lands", "stare", "throw", "lookbear", "lookdad", "pickup") else ((0, 2.6) if n in ("door",) else (0, 1.9)); walkin = n in ("door",)
            if walkin and t < T_door + .3: pass
            else:
                stand(DANA, t, (dp[0], dp[1], 0), {"lands": 295, "stare": 295, "throw": 295, "lookbear": 295, "lookdad": 295, "pickup": 295}.get(n, 0), 3); DANA.face = FACE[{"dana": "angry", "nothing": "sad", "lands": "shock", "stare": "neutral"}.get(n, "det")]; DANA.talk = talk("c10_dana1", t)
                if n == "dana": DANA.hands[1] = DANA.hip + V(.2, -.3, .5)
                if n == "nothing": walk(DANA, t, [(lt("c10_n2") + 4, 0, 1.9), (lt("c10_n2") + 9, .1, 3.0)], 3); DANA.face = FACE["sad"]
                sc.at(sc.cam.depth(DANA.hip), lambda: (DANA.draw(sc), fbi(sc, DANA)))
        if n in ("pickup", "lookbear", "lookdad", "throw", "lands", "stare"):
            stand(DON, t, (-1.6, .6, 0), 30, 3); DON.face = FACE[{"pickup": "sad", "lookdad": "sad", "throw": "shock", "stare": "shock"}.get(n, "sad")]; bp = carry(DON, NICO, t, 1); look(DON, NICO.joints()[4])
            NICO.face = FACE[{"lookbear": "focus", "lookdad": "sad", "throw": "det", "stare": "neutral"}.get(n, "neutral")]
            bt = ss(t, w("c10_n5", "throw"), w("c10_n5", "throw") + 1.0); bear_in = n in ("pickup", "lookbear", "lookdad") or (n == "throw" and bt == 0)
            if n == "lookbear": look(NICO, (-1.35, .9, .1))
            if n == "lookdad": look(NICO, DON.joints()[4]); look(DON, sc.cam.p)
            if n == "throw": look(NICO, (.6, 1.4, 0)); NICO.hands[1] = NICO.hip + V(.15, .1 if bt < .05 else .2, .35 if bt < .05 else .15)
            if n == "lookbear": pass
            elif n == "lookdad": sc.at(sc.cam.depth(DON.hip), lambda: DON.draw(sc))
            else: sc.at(sc.cam.depth(DON.hip), lambda: (DON.draw(sc), NICO.draw(sc), ring(sc, DON)))
            if n in ("pickup", "lookbear", "lookdad"): sc.at(sc.cam.depth(V(-1.35, .9, .1)), lambda: bear(sc, (-1.35, .9, 0), 30, .9))
            if n == "throw" and bt > 0:
                a = V(-1.35, .5, 1.3); b = V(.55, 1.4, 0); q = a + (b - a) * bt + V(0, 0, 1.2 * math.sin(math.pi * bt)); sc.at(sc.cam.depth(q), lambda: bear(sc, q - V(0, 0, .15), 360 * bt, .9))
            if n in ("lands",): sc.at(sc.cam.depth(V(.55, 1.4, 0)) - .05, lambda: bear(sc, (.55, 1.4, 0), 200, .9))
        if n == "stare": sc.at(sc.cam.depth(DANA.hip) - .2, lambda: bear(sc, DANA.hip + V(.05, -.3, .2), 200, .8))
        for k in range(2):
            if n in ("nothing", "pickup", "throw"): ch = AGENTS[k]; stand(ch, t, (2.6 - .8 * k, 1.8 + .6 * k, 0), 200, k); ch.face = FACE["det"]; sc.at(sc.cam.depth(ch.hip), lambda ch=ch: (ch.draw(sc), fbi(sc, ch)))
        sc.flush(); sc.c.set_source_rgba(.1, .12, .3, .2); sc.c.paint()
        if n == "door" and t > T_door: sc.c.set_source_rgba(1, 1, 1, .5 * math.exp(-(t - T_door) * 5)); sc.c.paint()
        sc.vignette(.35); return sc
    if n in ("robe",):
        sc = Scene(K(u, (1.2, -1.6, 1.6), (1.0, -1.3, 1.6), (-.2, 1.6, 1.3), (-.2, 1.6, 1.3), 1150)); KIT.kitchen(sc, .3); stand(LUCIA, t, (-.2, 1.3, 0), 20, 2); LUCIA.body = "f0b0c8"; LUCIA.face = FACE["shock"]
        LUCIA.hands = [LUCIA.hip + V(-.25, -.1, .9), LUCIA.hip + V(.25, -.1, .9)]; sc.at(1, lambda: (LUCIA.draw(sc), robe(sc, LUCIA))); sc.flush(); LUCIA.body = "c0304a"; sc.c.set_source_rgba(.1, .12, .3, .2); sc.c.paint(); sc.vignette(.35); return sc
    if n == "sal":
        sc = Scene(K(u, (.6, -1.0, 1.0), (.5, -.9, .95), (-.3, .9, .15), (-.3, .9, .15), 1150)); foyer(sc, t, 1.0); onplane(sc, (-1.4, 1.8, .004), (2.4, 0, 0), (0, -1.8, 0), 480, 360, lambda c, w_, h: (c.set_source_rgb(*C("7a1a22")), c.paint(), c.set_source_rgb(*C("c9a040")), c.set_line_width(10), c.rectangle(20, 20, w_ - 40, h - 40), c.stroke()))
        lying(SAL, t, (0, .9, .2), "down", 0, 2); SAL.face = FACE["sad"]; SAL.hands[1] = V(.45, .55, .06); sc.at(1, lambda: (draw_lying(sc, SAL), cannoli(sc, (.5, .5, .06), 60))); sc.flush(); sc.c.set_source_rgba(.1, .12, .3, .2); sc.c.paint(); sc.vignette(.35); return sc
    if n in ("office", "walls", "cars", "freezer"):
        if n == "office":
            sc = Scene(K(u, (1.6, -1.6, 1.8), (1.4, -1.4, 1.75), (0, 1.8, 1.0), (0, 1.8, 1.0), 1050)); mansion_office(sc, t, False, .6)
            for k in range(14): q = V(-.5 + .07 * k, 1.5, 1.0 + 1.5 * ((t * .8 + k * .13) % 1)); sc.box(q, (.2, .14, .005), "ffffff", 40 * k + 200 * t, .003)
            stand(AGENTS[0], t, (.4, 1.4, 0), 160, 0); AGENTS[0].hands = [V(.1, 1.75, .85), V(.5, 1.75, .9)]; AGENTS[0].face = FACE["det"]; sc.at(sc.cam.depth(V(.4, 1.4, 0)), lambda: AGENTS[0].draw(sc))
        elif n == "walls":
            sc = Scene(K(u, (1.0, -1.4, 1.6), (.9, -1.2, 1.6), (-.6, 2.0, 1.4), (-.6, 2.0, 1.4), 1050)); foyer(sc, t, 1.0); stand(AGENTS[1], t, (-.6, 2.4, 0), 180, 1); AGENTS[1].face = FACE["det"]
            hit = abs(wob(t, 2.5)); AGENTS[1].hands = [V(-.8, 2.9, 1.3 + .15 * hit), V(-.4, 2.9, 1.5)]; sc.at(1, lambda: (AGENTS[1].draw(sc), sc.line([V(-.8, 2.9, 1.3 + .15 * hit), V(-.8, 3.05, 1.5 + .15 * hit)], "6a4a2a", .03), sc.box(V(-.8, 3.08, 1.5 + .15 * hit), (.14, .05, .05), "5a5f6a", 0, .006)))
            for k in range(6): sc.box((-.9 + .2 * k, 3.15, 1.0 + .25 * (k % 3)), (.12, .02, .1), "c8b8a0", 20 * k, .004)
        elif n == "cars":
            sc = Scene(K(u, (3, -5, 2.2), (2.6, -4.6, 2.1), (0, 1, .8), (0, 1, .8), 1000)); S25.room(sc, wall=("8a8f98", "9aa0a8"), floor=("6a6e78", "626670"), side_="7a7e88", x0=-4, x1=4, y1=4, z1=3.2, base="4a4e58")
            q = V(0, 1.5, 0); sc.at(sc.cam.depth(q), lambda: car(sc, q, 90, "1c1e24", lights=False)); stand(AGENTS[2], t, (2.2, 1.2, 0), 250, 2); AGENTS[2].face = FACE["det"]; AGENTS[2].hands[1] = V(1.9, 1.3, 1.0)
            sc.at(sc.cam.depth(V(2.2, 1.2, 0)), lambda: (AGENTS[2].draw(sc), fbi(sc, AGENTS[2]), flashlight(sc, AGENTS[2], 1, t, V(.5, 1.5, .6))))
        else:
            sc = Scene(K(u, (.9, -1.4, 1.6), (.8, -1.2, 1.55), (-.4, 1.8, 1.0), (-.4, 1.8, 1.0), 1100)); KIT.kitchen(sc, .3); fz = V(-.4, 2.0, 0)
            sc.at(sc.cam.depth(fz), lambda: (sc.box(fz + V(0, 0, .45), (.9, .7, .9), "e8ecf0", 0, .012), sc.poly([fz + V(-.45, -.35, .9), fz + V(.45, -.35, .9), fz + V(.45, -.6, 1.6), fz + V(-.45, -.6, 1.6)], "dfe6ec", .01),
                                         [sc.box(fz + V(-.25 + .17 * k, -.1, .85 + .05 * (k % 2)), (.14, .2, .08), ("e8392e", "3d86e0", "ffffff", "57c785")[k], 10 * k, .005) for k in range(4)], [sc.ball(fz + V(-.3 + .1 * k, 0, .95), .03, "dff4ff", .003) for k in range(7)]))
            stand(AGENTS[0], t, (.4, 1.3, 0), 210, 0); AGENTS[0].face = FACE["sick"]; AGENTS[0].hands = [V(.0, 1.7, 1.0), V(.2, 1.6, 1.1)]; sc.at(sc.cam.depth(V(.4, 1.3, 0)), lambda: (AGENTS[0].draw(sc), sc.box(V(.1, 1.62, 1.1), (.3, .2, .03), "e8a040", 20, .005)))
            sc.flush(); label(sc, W / 2, 110, "FROZEN PIZZA. NO PROOF.", 50, "ffd21e"); sc.vignette(.35); return sc
        sc.flush(); sc.vignette(.35); return sc
    if n == "whisper":
        sc = Scene(K(u, (-.9, -.35, 1.6), (-.95, -.25, 1.58), (-1.5, .55, 1.4), (-1.5, .55, 1.4), 1250)); foyer(sc, t, 1.0); stand(DON, t, (-1.6, .6, 0), 30, 3); bp = carry(DON, NICO, t, 1)
        DON.face = FACE["sad"]; DON.talk = talk("c10_don1", t); look(DON, NICO.joints()[4]); NICO.face = FACE["sad"]; sc.at(1, lambda: (DON.draw(sc), NICO.draw(sc), ring(sc, DON))); sc.flush(); sc.c.set_source_rgba(.1, .12, .3, .2); sc.c.paint(); sc.vignette(.45); return sc
    if n == "memory":                                          # he sang to you every night
        sc = Scene(K(u, (1.3, -.9, 1.5), (1.1, -.7, 1.48), (0, 1.4, .9), (0, 1.4, .9), 1100)); nursery(sc, t); crib_scene(sc, t, who=lambda: baby(sc, V(-.1, 1.4, .62), 0, t, "sleep", 0, 1.0, ax=(-1, 0, 0)), mobile=True)
        sit(DON, t, (.9, 1.2, .45), 250, 3); DON.face = FACE["smile"]; DON.talk = .4 * max(0, wob(t, 1.2)); DON.hands[0] = V(.35, 1.4, .95); sc.at(sc.cam.depth(V(.9, 1.2, .5)), lambda: (kchair(sc, (.9, 1.2, 0), 250, "6a3a22", "4a2a18"), DON.draw(sc)))
        sc.flush(); sc.c.set_source_rgba(.25, .15, .05, .45); sc.c.paint(); X, Y = sc.cam.pr(V(.6, 1.2, 1.6))
        for k in range(3): tx(sc, X + 80 * k - 60, Y - 60 - 40 * ((t * .5 + k * .33) % 1), "♪" if False else "~", 70, "fff0c0", INK, .1, a=.8)
        sc.vignette(.55); return sc
    if n == "feels":
        sc = Scene(Cam((0, -2, 2), (0, 0, 0))); vgrad(sc, "3a3442", "1c1a22"); c = sc.c; c.save(); c.translate(W / 2, H / 2 + 40); c.scale(1.5, 1.5)
        for k, (bx, by, r) in enumerate(((0, 60, 150), (0, -110, 100), (-90, -190, 40), (90, -190, 40), (-150, 40, 50), (150, 40, 50))): c.new_path(); c.arc(bx, by, r, 0, 7); c.set_source_rgb(*C("a0683a")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
        c.new_path(); c.arc(0, 60, 100, 0, 7); c.set_source_rgb(*C("e8c79a")); c.fill(); sq = .5 + .5 * abs(wob(t, 1.3)); c.rectangle(-55, 0, 110, 150); c.set_source_rgba(.1, .1, .12, .35 + .3 * sq); c.set_line_width(6); c.set_dash([12, 8]); c.stroke(); c.set_dash([])
        for sg in (-1, 1): c.new_path(); c.save(); c.translate(sg * 150, 90 + 10 * sq); c.rotate(sg * .4); c.scale(55, 38); c.arc(0, 0, 1, 0, 7); c.restore(); c.set_source_rgb(*C("f3d6b8")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
        c.restore(); label(sc, W / 2, 110, "SOMETHING HARD INSIDE...", 52, "ffd21e"); sc.vignette(.4); return sc
    if n == "thanks":
        sc = Scene(K(u, (-.45, .95, 1.6), (-.4, 1.0, 1.6), (.6, 1.6, 1.5), (.6, 1.6, 1.52), 1350)); foyer(sc, t, 1.0); stand(DANA, t, (.6, 1.6, 0), 295, 3); DANA.face = FACE["smile"]; DANA.talk = talk("c10_dana2", t)
        DANA.hands = [DANA.hip + V(-.1, -.3, .25), DANA.hip + V(.1, -.3, .25)]; sc.at(1, lambda: (DANA.draw(sc), fbi(sc, DANA), bear(sc, DANA.hip + V(0, -.32, .15), 200, .8))); sc.flush(); sc.c.set_source_rgba(.1, .12, .3, .15); sc.c.paint(); sc.vignette(.4); return sc
SC["c10"] = c10
# ------------------------------------------------------------------ c11 a new life
DANNY = Char("8fc8f0", .62, cap="e8392e")                    # Nico at ~3, then 6 (scaled at use)
KIDS2 = [Char(c_, .7, cap=cp, skin=sk) for c_, cp, sk in (("e05a5a", "2f3a4a", "f0c49a"), ("3aa0a8", "ffc93a", "a8714a"), ("8f5ad0", "e8392e", "fffaf2"), ("57c785", "3d86e0", "e8b88a"))]
def people_grid(sc, t, u, n=200):
    c = sc.c; cols = 25; k_on = int(n * clamp(u * 1.3))
    for k in range(n):
        x = W * .12 + (k % cols) * W * .03; y = H * .36 + (k // cols) * 62
        if k < k_on: c.new_path(); c.arc(x, y - 14, 11, 0, 7); c.set_source_rgb(*C(("ffd21e", "ffffff", "7ad0ff")[k % 3])); c.fill(); rrect(c, x - 11, y, 22, 26, 8); c.fill()
def c11(t):
    D = CH["c11"]["dur"]
    n, u, s = shot(t, [(0, "gavel"), (w("c11_n1", "Uncle") - .1, "witness"), (w("c11_n1", "witness") - .1, "marshals"), (lt("c11_n2") - .1, "count"), (w("c11_n2", "They") - .1, "zero"),
                       (lt("c11_n3") - .1, "id"), (w("c11_n3", "live") - .1, "town"), (w("c11_n3", "mom") - .1, "bakery"), (w("c11_n3", "Uncle") - .1, "league"), (w("c11_n3", "Nobody") - .1, "highfive"),
                       (lt("c11_n4") - .1, "dana")], D)
    if n in ("gavel", "witness"):
        sc = Scene(K(u, (0, -2.0, 1.9), (0, -1.6, 1.85), (0, 2.6, 1.5), (0, 2.6, 1.5), 1100) if n == "gavel" else K(u, (1.6, -.6, 1.7), (1.4, -.4, 1.68), (-1.9, 2.3, 1.2), (-1.9, 2.3, 1.2), 1150))
        courtroom(sc, t); stand(MEN[9], t, (0, 2.9, .5), 0, 9); MEN[9].face = FACE["det"]; sc.at(sc.cam.depth(V(0, 3.0, .5)) + .2, lambda: MEN[9].draw(sc)); sc.at(sc.cam.depth(V(.5, 2.4, 1.45)) - .1, lambda: gavel(sc, (.5, 2.4, 1.45), t, lt("c11_n1") + 1.0))
        if n == "gavel": stand(DON, t, (-1.6, 1.1, 0), 0, 3); DON.face = FACE["sad"]; DON.hands = [DON.hip + V(-.08, -.25, .05), DON.hip + V(.08, -.25, .05)]; sc.at(sc.cam.depth(DON.hip), lambda: (DON.draw(sc), cuffs3 := None))
        if n == "witness":
            sc.at(sc.cam.depth(V(-1.9, 2.4, .6)), lambda: (sc.box((-1.9, 2.4, .55), (.9, .7, 1.1), "5a3a22", 0, .012)))
            sit(SAL, t, (-1.9, 2.6, .5), 0, 2); SAL.face = FACE["sad"]; SAL.talk = .5 * max(0, wob(t, 2)); sc.at(sc.cam.depth(V(-1.9, 2.6, .5)) + .1, lambda: SAL.draw(sc))
        sc.flush(); sc.vignette(.35)
        if n == "gavel": bigcount(sc, W * .74, H * .3, "100", 170, "YEARS", "ffd21e", clamp(s * 3))
        if n == "witness": label(sc, W / 2, 110, "SAL TESTIFIES", 56, "ffd21e")
        return sc
    if n == "marshals":
        sc = Scene(K(u, (5, -6, 1.8), (4.5, -5.6, 1.8), (0, 1, 1), (0, 1, 1), 1000)); foyer(sc, t, 0) if False else None
        city_night(sc, t, 0, 30, parked=()); q = V(0, 1.0, 0); sc.at(sc.cam.depth(q), lambda: car(sc, q, 90, "1c1e24", beams=1))
        for k, (ch, x) in enumerate(((LUCIA, -1.8), (SAL, 2.6), (AGENTS[1], 3.4))):
            stand(ch, t, (x, -.6, 0), 180 if ch is not AGENTS[1] else 220, k); ch.face = FACE["sad" if ch is not AGENTS[1] else "det"]
            if ch is LUCIA: bp = carry(LUCIA, NICO, t, 1); NICO.face = FACE["neutral"]
            if ch is SAL: SAL.hands[1] = SAL.hip + V(.2, 0, -.1)
            sc.at(sc.cam.depth(ch.hip), lambda ch=ch: (ch.draw(sc), NICO.draw(sc) if ch is LUCIA else None, sc.box(ch.hands[1] + V(0, 0, -.15), (.4, .15, .3), "6a4a3a", 0, .008) if ch is SAL else None))
        sc.flush(); label(sc, W / 2, 110, "WITNESS PROTECTION", 58, "ffd21e"); sc.vignette(.35); return sc
    if n in ("count", "zero"):
        sc = Scene(Cam((0, -2, 2), (0, 0, 0))); vgrad(sc, "1c2a44", "0e1626")
        if n == "count": tx(sc, W / 2, H * .17, "U.S. MARSHALS · SINCE 1971", 56, "ffffff", INK, .14); people_grid(sc, t, u); bigcount(sc, W / 2, H * .88, f"{int(19000 * ss(u, 0, .8)):,}+", 110, "", "ffd21e")
        else: tx(sc, W / 2, H * .42, "0", 300, "57e08a", INK, .14, a=clamp(s * 3)); tx(sc, W / 2, H * .7, "HURT, IF THEY FOLLOWED THE RULES", 64, "ffffff", INK, .16, a=clamp(s * 3)); tx(sc, W / 2, H * .86, "(the Marshals' own record)", 36, "c8d0dc", INK, .12)
        sc.vignette(.35); return sc
    if n == "id":
        sc = Scene(Cam((0, -2, 2), (0, 0, 0))); vgrad(sc, "e8e4d8", "c8c0b0"); c = sc.c; c.save(); c.translate(W / 2, H / 2); c.scale(.9 + .15 * u, .9 + .15 * u); c.translate(-W / 2, -H / 2); idcard2d(sc, W / 2, H / 2, 760, t, "DANNY"); c.restore(); sc.vignette(.3); return sc
    if n in ("town", "bakery", "dana"):
        cam = {"town": lambda: K(u, (-1, -9, 2.4), (1, -8.5, 2.2), (0, 4, 1.8), (0, 4, 1.8), 1000), "bakery": lambda: K(u, (-1.4, -.3, 1.5), (-1.4, .1, 1.5), (-1.4, 3.9, 1.3), (-1.4, 3.9, 1.3), 1100),
               "dana": lambda: K(u, (-1.2, -.6, 1.6), (-1.2, -.3, 1.6), (-1.3, 3.2, 1.1), (-1.3, 3.2, 1.1), 1000)}[n]()
        sc = Scene(cam); town(sc, t)
        stand(LUCIA, t, (-1.4, 4.2, 0), 0, 2); LUCIA.face = FACE["smile"]; sc.at(sc.cam.depth(V(-1.4, 4.2, 0)) + .01, lambda: (LUCIA.draw(sc), robe(sc, LUCIA)))
        def stall():
            sc.box((-1.4, 3.7, .5), (2.4, .5, 1.0), "c97a5a", 0, .01); sc.box((-1.4, 3.7, 1.02), (2.4, .55, .04), "f6e6d0", 0, .006); [sc.ball((-2.3 + .25 * k, 3.7, 1.1), .07, ("e8c080", "c08a4a", "f0d8b0")[k % 3], .005) for k in range(8)]
            sc.poly([(-2.7, 3.3, 2.2), (-.1, 3.3, 2.2), (-.1, 4.5, 2.5), (-2.7, 4.5, 2.5)], "e8392e", .01); [sc.line([(x, 3.45, 0), (x, 3.45, 2.2)], "8a6a4a", .03) for x in (-2.6, -.2)]
        sc.at(sc.cam.depth(V(-1.4, 3.7, .5)), stall)
        if n == "dana":
            stand(DANA, t, (-2.1, 2.9, 0), 120, 3); DANA.face = FACE["smile" if u < .6 else "laugh"]; DANA.blink = 1.0 if .55 < u < .75 else 0; sc.at(sc.cam.depth(DANA.hip), lambda: (DANA.draw(sc), cannoli(sc, DANA.hip + V(.25, -.2, .3), 0)))
            sk = .9; stand(DANNY, t, (-.7, 2.7, 0), 250, 6); DANNY.face = FACE["smile"]; sc.at(sc.cam.depth(DANNY.hip), lambda: DANNY.draw(sc))
        sc.flush(); sc.vignette(.25)
        if n == "town": stamp(sc, "SOMEWHERE SMALL. NEW NAMES.", clamp(s * 3))
        return sc
    if n in ("league", "highfive"):
        sc = Scene(K(u, (3, -3, 1.6), (2.6, -2.6, 1.55), (0, 2.5, 1.0), (0, 2.5, 1.0), 1050) if n == "league" else K(u, (1.2, .4, 1.3), (1.1, .5, 1.28), (-.2, 2.4, 1.0), (-.2, 2.4, 1.0), 1200)); ballfield(sc, t)
        stand(SAL, t, (-.6, 2.6, 0), 40, 2); SAL.body = "2a5aa0"; SAL.coat = None; SAL.tie = None; SAL.face = FACE["laugh"]; SAL.cap = "2a5aa0"
        for k, ch in enumerate(KIDS2): stand(ch, t, (.4 + .6 * k, 2.0 + .3 * (k % 2), 0), 220, k); ch.face = FACE["happy"]; cheer(ch, t, k) if n == "league" and k % 2 else None
        if n == "highfive":
            hf = V(-.1, 2.3, 1.15 + .1 * ss(u, .3, .5)); SAL.hands[1] = hf + V(-.04, 0, 0); KIDS2[0].hands[0] = hf + V(.04, 0, 0); stand(KIDS2[0], t, (.25, 2.0, 0), 230, 0); KIDS2[0].hands[0] = hf + V(.04, 0, 0); KIDS2[0].face = FACE["laugh"]
        for ch in [SAL] + KIDS2: sc.at(sc.cam.depth(ch.hip), lambda ch=ch: ch.draw(sc))
        sc.flush(); SAL.body = "4a505e"; SAL.coat = "ffffff"; SAL.tie = "2a2f3a"; SAL.cap = None
        if n == "highfive": X, Y = sc.cam.pr(V(-.1, 2.3, 1.2)); sc.glow(X, Y, 80, "ffffff", .7 * ss(u, .35, .5) * (1 - ss(u, .6, .9))); label(sc, W / 2, 110, "NOBODY KISSES ANYBODY'S RING", 52, "ffd21e")
        sc.vignette(.25); return sc
SC["c11"] = c11
# ------------------------------------------------------------------ c12 the letter (cliffhanger)
KID6 = Char("8fc8f0", .82, cap="e8392e")
def c12(t):
    D = CH["c12"]["dur"]
    n, u, s = shot(t, [(0, "cake"), (w("c12_n1", "letter") - .1, "mailbox"), (w("c12_n1", "Inside") - .1, "drawing"), (lt("c12_n2") - .1, "words"), (lt("c12_don1") - .1, "cell"),
                       (lt("c12_n3") - .1, "kid"), (w("c12_n3", "subscribe") - .1, "gate")], D)
    if n == "cake":
        sc = Scene(K(u, (1.0, -1.6, 1.5), (.8, -1.3, 1.45), (-.2, 1.4, 1.0), (-.2, 1.4, 1.0), 1100)); KIT.kitchen(sc, .3)
        sc.at(sc.cam.depth(V(-.2, 1.0, .7)), lambda: (sc.box((-.2, 1.0, .74), (1.6, .9, .06), "e07a3f", 0, .01), cake(sc, (-.2, .95, .77), t)))
        stand(KID6, t, (.75, 1.0, 0), 270, 2); KID6.face = FACE["laugh"]; look(KID6, (-.2, .95, .9)); stand(LUCIA, t, (-1.1, 1.8, 0), 20, 3); LUCIA.face = FACE["happy"]; cheer(LUCIA, t)
        for ch in (KID6, LUCIA): sc.at(sc.cam.depth(ch.hip) + .3, lambda ch=ch: ch.draw(sc))
        sc.flush(); sc.vignette(.3); stamp(sc, "5 YEARS LATER", clamp(s * 3)); return sc
    if n == "mailbox":
        sc = Scene(K(u, (1.6, -2.4, 1.3), (1.3, -2.0, 1.28), (0, 1.0, 1.0), (0, 1.0, 1.05), 1050)); town(sc, t); mailbox(sc, (.4, 1.0, 0), 1.0)
        stand(KID6, t, (-.2, .9, 0), 80, 2); KID6.face = FACE["ooh"]; KID6.hands[1] = V(.15, .8, .95); sc.at(sc.cam.depth(V(-.2, .9, 0)), lambda: (KID6.draw(sc), sc.box(V(.18, .78, .95), (.25, .02, .14), "fbf7ee", 80, .006)))
        sc.flush(); sc.vignette(.3); return sc
    if n in ("drawing", "words"):
        sc = Scene(Cam((0, -2, 2), (0, 0, 0))); vgrad(sc, "3a3442", "1c1a22"); wd = 0 if n == "drawing" else clamp((t - lt("c12_n2") - .5) / 1.2)
        if n == "words" and t > lt("c12_n2", 1): wd = 1
        letter2d(sc, W / 2, H / 2 - 40, 680 + 30 * u, t, 1, wd); sc.vignette(.45); return sc
    if n == "cell":
        sc = Scene(K(u, (0, -1.6, 1.3), (0, -1.2, 1.3), (0, 1.0, 1.25), (0, 1.0, 1.25), 1150)); cell(sc, t); sit(DON, t, (-1.0, 1.2, .45), 0, 3); DON.body = "e08a2a"; DON.coat = None; DON.tie = None
        DON.face = FACE["smug"]; DON.talk = talk("c12_don1", t); DON.hands = [DON.hip + V(-.15, -.25, .2), DON.hip + V(.15, -.25, .2)]; sc.at(1, lambda: DON.draw(sc)); sc.flush(); DON.body = "262a33"; DON.coat = "ffffff"; DON.tie = "b3202a"
        bars(sc, -.3); sc.c.set_source_rgba(0, .02, .08, .45); sc.c.paint(); X, Y = sc.cam.pr(V(0, 2.1, 2.1)); sc.glow(X, Y, 300, "c8d8ff", .3); sc.vignette(.55); return sc
    if n == "kid":
        sc = Scene(K(u, (.8, -1.2, 1.2), (.6, -1.0, 1.15), (0, 1.0, 1.0), (0, 1.0, 1.0), 1150)); KIT.kitchen(sc, .3); stand(KID6, t, (0, 1.0, 0), 0, 2); KID6.face = FACE["scared" if u < .5 else "det"]
        KID6.hands = [KID6.hip + V(-.12, -.25, .12), KID6.hip + V(.12, -.25, .12)]; sc.at(1, lambda: (KID6.draw(sc), sc.box(KID6.hip + V(0, -.28, .12), (.26, .02, .2), "fbf7ee", 0, .006))); sc.flush()
        sc.c.set_source_rgba(.05, .05, .2, .35); sc.c.paint(); sc.vignette(.45); return sc
    if n == "gate":
        sc = Scene(K(u, (0, -9, 1.8), (0, -7.5, 1.7), (0, 4, 2.2), (0, 4, 2.2), 1000)); skyline(sc, t); P = sc.poly
        P([(-30, -20, 0), (30, -20, 0), (30, 30, 0), (-30, 30, 0)], "3a3e48", 0); P([(-20, 4, 0), (20, 4, 0), (20, 4, 7), (-20, 4, 7)], "5a5e68", .012)
        for k in range(-20, 21, 2): sc.line([(k, 3.9, 7), (k, 3.9, 7.6)], "2a2d34", .04)
        op = ss(u, .2, .9)
        for sg in (-1, 1): x0 = sg * (1.6 + 2.6 * op); [sc.line([(x0 + sg * .2 * k_, 3.95, 0), (x0 + sg * .2 * k_, 3.95, 4.5)], "2a2d34", .05) for k_ in range(14)]
        sc.poly([(-1.6, 4.01, 0), (1.6, 4.01, 0), (1.6, 4.01, 4.5), (-1.6, 4.01, 4.5)], "0a0c12", 0) if op < .05 else None
        wtx(sc, (0, 3.9, 5.6), "STATE PRISON", .9, "e8e8e8", INK, .12); [sc.line([(-20, 3.95, 7.6 + .15 * (k % 2)), (20, 3.95, 7.6 + .15 * (k % 2))], "8a8f98", .02) for k in range(2)]
        for x in (-9, 9): sc.box((x, 5, 4), (2, 2, 8), "4a4e58", 0, .012); sc.box((x, 5, 8.3), (2.6, 2.6, .6), "3a3e48", 0, .012); Xl, Yl = sc.cam.pr(V(x, 4, 8.6)); sc.glow(Xl, Yl, 160, "fff2c0", .35)
        X, Y = sc.cam.pr(V(0, 6, 1.5)); sc.glow(X, Y, 500, "fff2c0", .45 * op); sc.vignette(.5); label(sc, W / 2, 110, "NEXT TIME: HE GETS OUT", 60, "ffd21e"); return sc
SC["c12"] = c12
