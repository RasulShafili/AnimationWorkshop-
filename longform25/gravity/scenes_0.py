"""c01–c02: the approved cold open (proto.py)"""
import sys; sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/gravity")
import proto as KIT
from show25 import CH
class _F:
    def __init__(s, surf): s.surf = surf
SC = {c: (lambda t, c=c: _F(KIT.frame(min(CH[c]["off"] + t, KIT.END - .01)))) for c in ("c01", "c02")}
