import draw
import pygame
from util import *
import argparse
from numba import njit

def main():
    parser = argparse.ArgumentParser("minecraft_block_colors.py", "", 
                                     "Takes the Minecraft texture atlas, splits it into blocks, " + 
                                     "finds the average color and contrast of each one, " +
                                     "and finds the block that most closely matches your request.")
    parser.add_argument("-af", "--atlasfile", dest="af", help="Input file for the minecraft texture atlas")
    parser.add_argument("-hsb", "--HSB", dest="hsb", help="Compares HSB instead of RGB (input color is still HEX RGB)", action="store_true")
    parser.add_argument("-hex", "--color", dest="hex", help="Hex code to match")
    parser.add_argument("-r", "--reverse", dest="reverse", help="Reverses sorting", action="store_true")
    parser.add_argument("-c", "--contrast", dest="c", help="Contrast limit")
    parser.add_argument("-as", "--atlastilesize", dest="ats", 
                        help="Size for tiles in atlas (for non-minecraft and compressed atlas compat)",
                        type=int, default=16)
    args = parser.parse_args()
    screenWidth = 800
    screenHeight = 400
    pygame.init()
    pygame.display.set_mode((screenWidth, screenHeight))
    if args.af:
        tiles = split_tiles(args.af, args.ats, args.ats)
    else:
        tiles = split_tiles("25w20a_blocks.png-atlas.png", args.ats, args.ats)
    avg_color_data = {}
    contrast_data = {}
    for i in range(len(tiles)):
        tile = tiles[i]
        if pixel_list(tile).count((0, 0, 0, 0)) > 0:
            pass
            continue
        avg_color_data.update({i: avg_color(tile)})
        if args.hsb:
            avg_color_data[i] = rgb_to_hsv(avg_color_data[i][0], avg_color_data[i][1], avg_color_data[i][2])
        contrast_data.update({i: contrast(tile)})
        if args.c and contrast_data[i] > int(args.c):
            avg_color_data.pop(i)
    color = hex_to_rgb(args.hex) if args.hex else hex_to_rgb(input("Color hex: "))
    if args.hsb:
        color = rgb_to_hsv(color[0], color[1], color[2])
    print(color)
    if args.hsb:
        s=sorted(avg_color_data.keys(), 
                reverse = args.reverse,
                key=lambda i: 
                abs(avg_color_data[i][0]-color[0]) + 
                abs(avg_color_data[i][1]-color[1]) + 
                abs(avg_color_data[i][2]-color[2]))
    else:
        s=sorted(avg_color_data.keys(), 
                reverse = args.reverse,
                key=lambda i: 
                abs(avg_color_data[i][0]-color[0]) + 
                abs(avg_color_data[i][1]-color[1]) + 
                abs(avg_color_data[i][2]-color[2]))
    print(contrast(tiles[s[1]]))
    draw.init(screenWidth, screenHeight, center=(0, 0))
    draw.run(things=[draw.thing(array_to_surface(tiles[s[i]]), 
                                array_to_surface(tiles[s[i]]).get_rect(topleft=(i*args.ats%screenWidth, 
                                                                       int(i*args.ats/screenWidth)*args.ats))) for i in range(len(s))])

if __name__ == "__main__":
    main()

def generate_colordata(atlas = "25w20a_blocks.png-atlas.png", hsb = False, contrast_limit = None, tilesize=16):
    if type(atlas) == list:
        tiles = atlas
    else:
        tiles = split_tiles(atlas, tilesize, tilesize)
    avg_color_data = {}
    contrast_data = {}
    for i in range(len(tiles)):
        tile = tiles[i]
        if pixel_list(tile).count((0, 0, 0, 0)) > 0:
            pass
            continue
        avg_color_data.update({i: avg_color(tile)})
        if hsb:
            avg_color_data[i] = rgb_to_hsv(avg_color_data[i][0], avg_color_data[i][1], avg_color_data[i][2])
        contrast_data.update({i: contrast(tile)})
        if contrast_limit and contrast_data[i] > contrast_limit:
            avg_color_data.pop(i)
    return avg_color_data

def find_closest_from_colordata(colordata, color, tiles, hsb = False, outputcount = None, reverse = False):
    if type(color) == str:
        color = hex_to_rgb(color)
    if hsb:
        color = rgb_to_hsv(color)
    if hsb:
        s=sorted(colordata.keys(), 
                reverse = reverse,
                key=lambda i: 
                abs(colordata[i][0]-color[0]) + 
                abs(colordata[i][1]-color[1]) + 
                abs(colordata[i][2]-color[2]))
    else:
        s=sorted(colordata.keys(), 
                reverse = reverse,
                key=lambda i: 
                abs(colordata[i][0]-color[0]) + 
                abs(colordata[i][1]-color[1]) + 
                abs(colordata[i][2]-color[2]))
    if outputcount:
        return [tiles[s[i]] for i in range(outputcount)]
    else:
        return tiles[s[0]]

def match_tiles(image, colordata):
    colordata_list = np.array([colordata[i] for i in sorted(colordata.keys())], dtype=np.uint32)
    colordata_indices = sorted(colordata.keys())
    indices = match_tiles_inner(np.asarray(image), colordata_list)
    height, width = indices.shape
    for y in range(height):
        for x in range(width):
            indices[y, x] = colordata_indices[indices[y, x]]
    return indices


#by ChatGPT
@njit
def match_tiles_inner(image_pixels, tile_colors):
    height, width, _ = image_pixels.shape
    indices = np.empty((height, width), dtype=np.int32)
    for y in range(height):
        for x in range(width):
            r, g, b = image_pixels[y, x]
            best_i = 0
            best_dist = 1e9
            for i in range(len(tile_colors)):
                tr, tg, tb = tile_colors[i]
                dist = (r - tr)**2 + (g - tg)**2 + (b - tb)**2
                if dist < best_dist:
                    best_dist = dist
                    best_i = i
            indices[y, x] = best_i
    return indices

#Spruce: #725430
#Packed Ice: #8bb4fc