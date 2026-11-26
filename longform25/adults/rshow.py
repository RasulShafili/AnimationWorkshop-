"""python3 show.py stills "c05:0.5,3;c23:2" /prefix  |  render [c05 …]   (gravity/show.py with this project's data)"""
import os, sys
D = "/home/rasul/Desktop/Animations/longform25/adults"; os.environ["SHOW_DATA"] = D + "/out"; os.environ["SHOW_VO"] = D + "/vo16"
src = open("/home/rasul/Desktop/Animations/longform25/gravity/show.py").read().replace('D = "/home/rasul/Desktop/Animations/longform25/gravity"', f'D = "{D}"').replace('sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/gravity")', f'sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/gravity"); sys.path.insert(0, "{D}")')
src = src.replace('scenes_*.py', 'adults_*.py')
exec(compile(src, __file__, "exec"))
