from PIL import Image
import os, sys

numframes = 4382
blocks_x = 16
blocks_y = 12

origin_x = 0
origin_y = -60
origin_z = 0

view_distance = 8.7 # Determined for 16x12 blocks at FOV=70

packname="BadShelfPack"
packdesc="Bad Apple Bookshelf by KasamiKona"
packformat=10
namespace="badshelf"

startbits = 0
endbits = 0
startdelay = 20

blockbits_last = [[startbits]*blocks_y for x in range(blocks_x)]

def getblockbits(pix, x, y):
	xx = x*3
	yy = y*2
	bit0 = pix[xx+0,yy+0]>>7
	bit1 = pix[xx+1,yy+0]>>7
	bit2 = pix[xx+2,yy+0]>>7
	bit3 = pix[xx+0,yy+1]>>7
	bit4 = pix[xx+1,yy+1]>>7
	bit5 = pix[xx+2,yy+1]>>7
	return bit0*1 + bit1*2 + bit2*4 + bit3*8 + bit4*16 + bit5*32

def bools(bit):
	return "true" if (bit&1 == 1) else "false"

def bitstostate(bits):
	state = "minecraft:chiseled_bookshelf[facing=south"
	for i in range(6):
		state += ",slot_{}_occupied={}".format(i, bools(bits>>i))
	state += "]"
	return state

def setblock(x, y, z, state):
	return "setblock {} {} {} {}\n".format(x, y, z, state)

os.makedirs("{}/data/{}/functions".format(packname, namespace), exist_ok=True)

# Make pack.mcmeta
meta = '{{"pack":{{"pack_format":{:d},"description":"{}"}}}}\n'.format(packformat, packdesc)

with open("{}/pack.mcmeta".format(packname), "w") as ff:
	ff.write(meta)

# Make start function
function = "fill {} {} {} {} {} {} {} replace\n".format(origin_x, origin_y, origin_z, origin_x+blocks_x-1, origin_y+blocks_y-1, origin_z, bitstostate(startbits))
function += "gamemode spectator @p\n"
function += "teleport @p {:.2f} {:.2f} {:.2f} 180 0\n".format(origin_x+(blocks_x/2), origin_y+(blocks_y/2)-1.62, origin_z+view_distance)
function += "schedule function {}:frame_{:04d} {:d}t\n".format(namespace, 1, startdelay)
with open("{}/data/{}/functions/start.mcfunction".format(packname, namespace), "w") as ff:
	ff.write(function)

# Make end function
function = "fill {} {} {} {} {} {} {} replace\n".format(origin_x, origin_y, origin_z, origin_x+blocks_x-1, origin_y+blocks_y-1, origin_z, bitstostate(endbits))
with open("{}/data/{}/functions/end.mcfunction".format(packname, namespace), "w") as ff:
	ff.write(function)

# Make frame functions
for fn in range(1, numframes+1):
	im = Image.open("frames/frame_{:04d}.png".format(fn))
	pix = im.convert('L').load()
	blockbits = [[0]*blocks_y for x in range(blocks_x)]
	function = ""
	for x in range(blocks_x):
		for y in range(blocks_y):
			blockbits[x][y] = getblockbits(pix, x, y)
			changed = (blockbits[x][y] != blockbits_last[x][y])
			if changed:
				function += setblock(origin_x+x, origin_y+blocks_y-1-y, origin_z, bitstostate(blockbits[x][y]))
	if fn < numframes:
		function += "schedule function {}:frame_{:04d} 1t\n".format(namespace, fn+1)
	else:
		function += "schedule function {}:end 1t\n".format(namespace)
	with open("{}/data/{}/functions/frame_{:04d}.mcfunction".format(packname, namespace, fn), "w") as ff:
		ff.write(function)
	blockbits_last = blockbits
