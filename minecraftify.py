import draw
import pygame
from util import *
import argparse
from minecraft_colors import *
from screeninfo import get_monitors
import numpy as np

def main():
    parser = argparse.ArgumentParser("minecraft_block_colors.py", "", 
                                     "Takes the Minecraft texture atlas, splits it into blocks, " + 
                                     "finds the average color and contrast of each one, " +
                                     "and uses those to replace pixels in the input image.")
    parser.add_argument("-af", "--atlasfile", dest="af", 
                        help="Input file for the minecraft texture atlas", 
                        default = "25w20a_blocks.png-atlas.png")
    parser.add_argument("-i", "--image", dest="img", help="File to convert to minecraft blocks", default="rickroll_first_frame.png")
    parser.add_argument("-s", "--save", dest="s", help="Save full image (not scaled down)", action="store_true")
    parser.add_argument("-sf", "--saveto", dest="sf", help="Save to specific file name")
    parser.add_argument("-as", "--atlastilesize", dest="ats", 
                        help="Size for tiles in atlas (for non-minecraft and compressed atlas compat)",
                        type=int, default=16)
    args = parser.parse_args()
    tiles = split_tiles(args.af, args.ats, args.ats)
    colordata = generate_colordata(tiles, False, 100, args.ats)
    img = Image.open(args.img).convert("RGB")
    pygame.init()
    pygame.display.set_mode()
    surf = minecraftify(img, tiles, colordata)
    if args.s or args.sf:
        #Done twice to unmorror image
        Image.fromarray(pygame.surfarray.array3d(pil_to_surface(
            Image.fromarray(pygame.surfarray.array3d(surf))))).save(args.sf if args.sf else
                f"minecraftified_{args.img.replace(".jpg", ".png").replace(".jpeg", ".png")}")
        
    draw.init(get_monitors()[0].width, get_monitors()[0].height, center = (0, 0), margin = 0)
    surf = pygame.transform.scale_by(surf, min(draw.screen.get_size()[0]/surf.get_size()[0], draw.screen.get_size()[1]/surf.get_size()[1]))
    draw.run(things=[draw.thing(surf, draw.get_rect(surf, "topleft", 0, 0))])
    #img.resize()

def minecraftify(image, tiles, colordata):
    if type(image) == np.ndarray:
        output = pygame.surface.Surface((image.shape[1], image.shape[0]))
        #print(image.tolist())
        print(image.shape)
    else:
        output = pygame.surface.Surface((image.width*tiles[0].shape[0], image.height*tiles[0].shape[1]))
    indices = match_tiles(image, colordata)
    height, width = indices.shape
    for y in range(height):
        for x in range(width):
            output.blit(array_to_surface(tiles[indices[y, x]]), (x*tiles[0].shape[0], y*tiles[0].shape[1]))
    return output
    

if __name__ == "__main__":
    main()