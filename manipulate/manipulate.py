"""
Data manipulation

What's in here?
    - remaking png files to jpg
    - moving images to folders
    - data augmentation
"""

import pandas as pd
from PIL import Image
from pathlib import Path

def png_to_jpg(pokemon_names):
    """
    convert png images to jpg image
    """
    for name in pokemon_names[:]:
        path = Path('../data/images/'+name+'.png')
        if path.exists():
            # load image as RGBA
            png_img = Image.open(path).convert('RGBA')
            # make new RGBA image
            rgba_img = Image.new('RGBA', png_img.size, (255,255,255))
            # paste png image to the new image
            rgba_img.paste(png_img, png_img.split()[-1])
            # convert to RGB
            rgb_img = rgba_img.convert('RGB')
            rgb_img.save('../data/images/'+name+'.jpg')

def place_image_by_type(pokemon_names, pokemon_types):
    # make new directory
    unique_type = pokemon_types.unique()
    for folder in unique_type:
        path = Path('../data/images/'+folder)
        path.mkdir()
    # place images to the directory
    for name, typ in zip(pokemon_names, pokemon_types):
        path = Path('../data/images/'+name+'.jpg')
        new_path = Path('../data/images/'+typ+'/'+name+'.jpg')
        path.rename(new_path)
        
def augment():
    pass

def main():
    pokemon = pd.read_csv('../data/pokemon.csv')
    # png_to_jpg(pokemon_names=pokemon['Name'])
    # place_image_by_type(pokemon['Name'], pokemon['Type1'])

if __name__ == '__main__':
    main()