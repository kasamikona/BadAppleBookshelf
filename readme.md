# Bad Apple on Chiseled Bookshelves
A data pack built for Minecraft 22w46a, may not work in newer snapshots!
I don't intend to update this again during snapshots but will check if it still works when 1.20 releases.

Does not play the music, only the animation!
The animation plays in realtime (20fps video at 1 frame per tick)

## Requirements
- Minecraft snapshot 22w46a
- FFmpeg
- Python 3.7+
- [Pillow](https://pillow.readthedocs.io/en/stable/) library for Python
- A copy of the Bad Apple video

## Building data pack
**You can skip this and download the zip file from [releases](https://github.com/kasamikona/BadAppleBookshelf/releases) if you want!**
1. Clone this repository into a working folder
1. Place the Bad Apple video in the working folder as input.mp4
1. Run make_frames.bat (or make_frames.sh on Linux) and wait
1. Count how many files are in the newly created "frames" directory
1. Edit make_datapack.py and make sure num_frames matches
1. Run make_datapack.py and wait
1. The newly created BadShelfPack directory is the built data pack.

## Using the data pack
**If using the self-built folder version without zipping, remove** `.zip` **from the commands**
1. Start creating a new world with creative superflat on the default preset, don't click create yet.
1. In data packs menu, select the 1.20 experimental features data pack (important!)
1. Open the data packs folder and copy BadShelfPack into it
1. Finish creating the world
1. Set any gamerules and other things you like (daylight cycle, time of day etc.)
1. Set your FOV to 70 or higher
1. Run `/datapack enable "file/BadShelfPack.zip"` to make sure it's enabled
1. Run `/function badshelf:start` to begin the animation
1. To stop, run `/datapack disable "file/BadShelfPack.zip"`. You'll need to enable it again to replay.

## Notes
The python script looks at which blocks need to change each frame and only updates those that changed.
This means the files are smaller and shouldn't have any trouble loading, and should also minimize lag.

By default, the python script generates blocks at x=0 y=-60 z=0 in a default superflat world.
To change this, edit origin_x/origin_y/origin_z at the top of the script and rerun it.
The block resolution can also be changed, but you'll need to edit make_frames to generate the right frame size.
