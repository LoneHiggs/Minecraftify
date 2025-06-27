# Minecraftify-Images

Converts colors into textures from the Minecraft atlas.
Useful for pixelart.

## Features

 - Finds the closest block to a color of your choice
 - Converts all pixels in an image into Minecraft textures
 - Allows for any texture atlas, including non-minecraft ones, and of any tile size
 - Fast processing
 - Convert a .gif with speed

## Getting started

1. Clone the repository:

git clone https://github.com/LoneHiggs/Minecraftify
cd Minecraftify

2. Install all libraries in requirements.txt

pip install -r requirements.txt

## Usage

python minecraftify.py -i image.png/jpg/jpeg
python minecraftify.py -i image.png -sf savetohere.png
python minecraftify.py -i image.png -af alternativealtas.png

python minecraft_colors.py -hex hexcode

minecraftify_video.py input.gif outputfilename.gif

## Notes

This started as a fun sideproject, then a reddit post, then whatever it is now.
This probably isn't going to turn into a real tool and definitely won't be updated that much.
Feel free to make your own, with the rise of AI it shouldn't be that hard. 
Or use my code, I don't have anything against that as long as you credit me.
Thanks to ChatGPT for a few functions; those should have a comment mentioning they are from ChatGPT or with help from him.
Enjoy!