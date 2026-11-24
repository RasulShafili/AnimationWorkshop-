import sys
from PIL import Image
fs=sys.argv[2:];W,H=800,450;im=Image.new('RGB',(W*2,H*((len(fs)+1)//2)))
for k,f in enumerate(fs): im.paste(Image.open(f).resize((W,H)),(k%2*W,k//2*H))
im.save(sys.argv[1],quality=88)
