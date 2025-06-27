from util import *
import argparse
from minecraftify import *
import pygame

def main():
    parser = argparse.ArgumentParser("minecraftify_video.py", "python minecraftify_video.py gif_filepath output_file", 
                                     "Takes the Minecraft texture atlas, splits it into blocks, " + 
                                     "finds the average color and contrast of each one, " +
                                     "and uses those to replace pixels in the input image.")
    parser.add_argument("vid", help="File to convert to minecraft blocks")
    parser.add_argument("saveto", help="Save to file name")
    parser.add_argument("-af", "--atlasfile", dest="af", 
                        help="Input file for the minecraft texture atlas", 
                        default = "25w20a_atlas_cropped.png")
    parser.add_argument("-as", "--atlastilesize", dest="ats", 
                        help="Size for tiles in atlas (for non-minecraft and compressed atlas compat)",
                        type=int, default=16)
    parser.add_argument("-f", "--fps", dest="fps", help="Output gif framerate", type=int, default=60)
    args = parser.parse_args()
    pygame.init()
    pygame.display.set_mode()
    tiles = split_tiles(args.af, args.ats, args.ats)
    colordata = generate_colordata(tiles, False, 100, args.ats)
    print("Collecting and processing frames...")
    frames = [minecraftify(frame.convert("RGB"), tiles, colordata) for frame in gif_to_list(args.vid)]
    print("Creating gif...")
    make_gif([pygame.surfarray.array3d(frame).transpose(1, 0, 2) for frame in frames], args.saveto, args.fps)

if __name__ == "__main__":
    main()