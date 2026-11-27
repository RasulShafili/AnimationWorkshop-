"""python3 show.py stills "c05:0.5,3;c23:2" /prefix  |  render [c05 …]   (gravity/show.py with this project's data)"""
import os, sys
D = "/home/rasul/Desktop/Animations/longform25/mafia"; os.environ["SHOW_DATA"] = D + "/out"; os.environ["SHOW_VO"] = D + "/vo16"
src = open("/home/rasul/Desktop/Animations/longform25/gravity/show.py").read().replace('D = "/home/rasul/Desktop/Animations/longform25/gravity"', f'D = "{D}"').replace('sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/gravity")', f'sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/gravity"); sys.path.insert(0, "{D}")')
src = src.replace('scenes_*.py', 'maf_*.py'); src = src.replace("Pool(8)", "Pool(int(os.environ.get(\"SP\", 3)))")
src = src.replace('\nif __name__ == "__main__":', "\nimport mlib as _M\nfor _n, _c in vars(_M).items():\n    if isinstance(_c, EN.Char): NAME[id(_c)] = _n\nfor _k, _c in enumerate(getattr(_M, \"MEN\", [])): NAME[id(_c)] = f\"MEN{_k}\"\nif __name__ == \"__main__\":")
exec(compile(src, __file__, "exec"))

