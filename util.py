from PIL import Image
import numpy as np
import pygame
import cv2

def pixel_list(image):
    """
    Turns an image into a list of all of its pixels (represented as tuples)
    -----------------------------------------------------------------------
    If image is a str, uses that as filepath for Image.open()
    If image is a ndarray or PIL Image, uses that as the image
    If image is a list, it is used as what you would get from np.tolist() on an image represented as a numpy array
    Does not care about what format the image is stored (RGB, RGBA, CMYK, HSL, etc.); whatever is used is preserved
    
    Parameters
    ----------
    image: str | np.ndarray | Image.Image | list
        Image or filepath as input
    Returns
    -------
    list
        A single list of tuples containing all pixels in the image.
    """
    if type(image) == str:
        image = np.asarray(Image.open(image))
    elif type(image) == Image.Image:
        image = np.asarray(image)
    elif type(image) == np.ndarray:
        pass
    elif type(image) == list:
        pass

    if type(image) == np.ndarray:
        image = image.tolist()
    return [tuple(pixel) for row in image for pixel in row]

def split_tiles(image, w, h):
    """
    Cuts an image a list of smaller images (np.ndarrays)
    ----------------------------------------------------
    If image is a str, uses that as filepath for Image.open()
    If image is a ndarray or PIL Image, uses that as the image
    Does not care about what format the image is stored (RGB, RGBA, CMYK, HSL, etc.); whatever is used is preserved
    
    Parameters
    ----------
    image: str | np.ndarray | Image.Image
        Image or filepath as input
    w: int
        Width
    h: int
        Height
    Returns
    -------
    """
    if type(image) == str:
        image = np.asarray(Image.open(image))
    elif type(image) == Image.Image:
        image = np.asarray(image)
    elif type(image) == np.ndarray:
        pass
    return [image[x:x+w,y:y+h] for x in range(0,image.shape[0],w) for y in range(0,image.shape[1],h)]


def avg_color(img):
    img = pixel_list(img)
    output = [0, 0, 0]
    for pixel in img:
        output[0] += pixel[0]
        output[1] += pixel[1]
        output[2] += pixel[2]
    output[0] /= len(img)
    output[1] /= len(img)
    output[2] /= len(img)
    return output

def contrast(img):
    output = 0
    avg = avg_color(img)
    img = pixel_list(img)
    for pixel in img:
        output += abs(avg[0]-pixel[0])+abs(avg[1]-pixel[1])+abs(avg[2]-pixel[2])
    output /= 255
    return output

def hex_to_rgb(hex):
    return tuple(int(hex.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))

def pil_to_surface(image):
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    size = image.size
    data = image.tobytes()
    expected_bytes = size[0] * size[1] * 4
    actual_bytes = len(data)
    
    if actual_bytes != expected_bytes:
        raise ValueError(f"Buffer size mismatch: expected {expected_bytes} bytes for size {size}, got {actual_bytes} bytes")
    
    return pygame.image.fromstring(data, size, "RGBA").convert_alpha()

def array_to_surface(image, mode=None):
    pil_image = Image.fromarray(image, mode)
    return pil_to_surface(pil_image)

#by ChatGPT
def rgb_to_hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = (df/mx)*100
    v = mx*100
    return h, s, v

import numpy as np

#by ChatGPT
def np_rgb_to_hsb_fast(rgb_img: np.ndarray) -> np.ndarray:
    # Normalize RGB to [0, 1]
    rgb = rgb_img.astype(np.float32) / 255.0
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]

    maxc = np.maximum(np.maximum(r, g), b)
    minc = np.minimum(np.minimum(r, g), b)
    delta = maxc - minc

    # Hue
    hue = np.zeros_like(maxc)
    mask = delta != 0

    # Conditions for max color channel
    r_max = (maxc == r) & mask
    g_max = (maxc == g) & mask
    b_max = (maxc == b) & mask

    hue[r_max] = ((g[r_max] - b[r_max]) / delta[r_max]) % 6
    hue[g_max] = ((b[g_max] - r[g_max]) / delta[g_max]) + 2
    hue[b_max] = ((r[b_max] - g[b_max]) / delta[b_max]) + 4

    hue = (hue / 6.0) % 1.0  # Normalize to [0,1)
    hue = (hue * 255).astype(np.uint8)

    # Saturation
    sat = np.zeros_like(maxc)
    sat[maxc != 0] = delta[maxc != 0] / maxc[maxc != 0]
    sat = (sat * 255).astype(np.uint8)

    # Brightness = max(R, G, B)
    val = (maxc * 255).astype(np.uint8)

    # Stack into HSB image
    hsb = np.stack((hue, sat, val), axis=-1)
    return hsb

def np_rgb_to_hsb_fast(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
