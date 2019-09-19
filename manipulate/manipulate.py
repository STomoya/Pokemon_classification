"""
Data manipulation

What's in here?
    - remaking png files to jpg
    - moving images to folders
    - data augmentation
"""

import os
import shutil
import pandas as pd
from PIL import Image
from PIL import ImageOps
from pathlib import Path

class ManipulationError(Exception):
    """manipulation error class"""
def _raise_not_in_dir_error(req_dir):
    raise ManipulationError('You must run this file under \'{}\' folder'.format(req_dir))
def _raise_existance_error(dir):
    raise ManipulationError('You do not have \'{}\''.format(dir))
def _raise_already_ready_error():
    raise ManipulationError('You have already ran this file')

def check_current_directory():
    """
    check the current directory
    """
    current = Path().resolve()
    folder_name = 'manipulate'
    if not str(current)[-10:] == folder_name:
        _raise_not_in_dir_error(folder_name)

def check_existance():
    """
    check the existance of folders and files
    does not check all of them.
    """
    path = Path('../data/')
    if not path.exists():
        _raise_existance_error('data directory')
    path = Path('../data/images/')
    if not path.exists():
        _raise_existance_error('data/images/ directory')
    path = Path('../data/pokemon.csv')
    if not path.exists():
        _raise_existance_error('pokemon.csv file')

def check_already_ready():
    """
    check if the manipulation is already done
    not a good algorithm...
    """
    path = Path('../data/images/')
    image_paths = path.glob('*.jpg')
    file_count = len(list(image_paths))
    if file_count == 0:
        _raise_already_ready_error()

def png_to_jpg(pokemon_names):
    """
    convert png images to jpg image

    argument
        pokemon_names : list
            the name sof the pokemons
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

def reshape_dataframe(pokemon):
    """
    reshapes the input dataframe
    
    flow
        melt 'Type1' and 'Type2'
        erase 'variable' column
        drop rows that has NaN in 'Type'

    argument
        pokemon : dataframe
            columns : Name, Type1, Type2
    
    return
        pokemon : dataframe
            columns : Name, Type
    """
    melt_pokemon = pd.melt(pokemon, id_vars=['Name'], value_vars=['Type1', 'Type2'], value_name='Type')
    pokemon = melt_pokemon.dropna()
    return pokemon

def place_image_by_type(pokemon_names, pokemon_types, variables):
    """
    replace images to folders that represents types

    arguments
        pokemon_names : list
            Names of pokemons
        pokemon_types : list
            Types of pokemons
    """
    # make new directory
    print('   ##      making new directory     ##   ')
    try:
        path = Path('../data/images/train/')
        path.mkdir()
        path = Path('../data/images/test/')
        path.mkdir()
    except:
        pass
    unique_type = pokemon_types.unique()
    for folder in unique_type:
        train_path = Path('../data/images/train/'+folder)
        test_path = Path('../data/images/test/'+folder)
        try:
            train_path.mkdir()
            test_path.mkdir()
        except:
            pass
    print('   ##           finished            ##   ')
    # place images to the directory
    print('   ##       replacing images        ##   ')
    for name, typ, v in zip(pokemon_names, pokemon_types, variables):
        path = Path('../data/images/'+name+'.jpg')
        if path.exists():
            train_path = Path('../data/images/train/'+typ+'/'+name+'.jpg')
            shutil.copy(str(path), str(train_path))
            if 'Type1' == v:
                test_path = Path('../data/images/test/'+typ+'/'+name+'.jpg')
                shutil.copy(str(path), str(test_path))
    print('   ##           finished            ##   ')
    # erase images(one rsrc file exists in the dataset)
    print('   ##        erasing images         ##   ')
    path = Path('../data/images/')
    ## png
    png_file_paths = path.glob('*.png')
    for png_file in png_file_paths:
        os.remove(str(png_file))
    ## jpg
    jpg_file_paths = path.glob('*.jpg')
    for jpg_path in jpg_file_paths:
        os.remove(str(jpg_path))
    ## rsrc
    path = Path('../data/images/fletchling.png.rsrc')
    if path.exists():
        os.remove(str(path))
    print('   ##           finished            ##   ')
        
def augment():
    """
    data augmentation

    generated images
        original                (filename)
        flip                    (filename_f)
        mirror                  (filename_m)
        flip + mirror           (filename_fm)
        rot90                   (filename_r)
        rot90 + flip            (filename_rf)
        rot90 + mirror          (filename_rm)
        rot90 + flip + mirror   (filename_rfm)
    """
    path = Path('../data/images/train/')
    img_paths = path.glob('*/*.jpg')

    for path in img_paths:
        filename = path.stem
        folder = str(path.parent)

        img = Image.open(path)
        # flip
        f_img = ImageOps.flip(img)
        f_img.save(folder+'/'+filename+'_f.jpg')
        # mirror
        m_img = ImageOps.mirror(img)
        m_img.save(folder+'/'+filename+'_m.jpg')
        # flip + image
        fm_img = ImageOps.mirror(f_img)
        fm_img.save(folder+'/'+filename+'_fm.jpg')
        # rotate90
        r_img = img.rotate(90)
        r_img.save(folder+'/'+filename+'_r.jpg')
        # rotate + flip
        rf_img = ImageOps.flip(r_img)
        rf_img.save(folder+'/'+filename+'_rf.jpg')
        # rotate + mirror
        rm_img = ImageOps.mirror(r_img)
        rm_img.save(folder+'/'+filename+'_rm.jpg')
        # rotate + flip + mirror
        rfm_img = ImageOps.mirror(rf_img)
        rfm_img.save(folder+'/'+filename+'_rfm.jpg')

def erase_test_img_in_train():
    """
    erase test images(original images) from the training folders
    """
    ## test image in training data
    path = Path('../data/images/train/')
    train_file_paths = path.glob('*/*.jpg')
    for file_path in train_file_paths:
        if not '_' in file_path.stem:
            os.remove(str(file_path))

def update_csv(pokemon, filename='pokemon_alpha.csv'):
    """
    updates csv, in order of the argumentation

    argument
        pokemon : dataframe
            columns : Name, Type
        filename : str (default : 'pokemon_alpha.csv')
            filename of the updated output
    """
    names = pokemon['Name']
    types = pokemon['Type']
    for name, typ in zip(names, types):
        for id in ['_f', '_m', '_fm', '_r', '_rf', '_rm', '_rfm']:
            pokemon = pokemon.append({'Name':name+id, 'Type':typ}, ignore_index=True)
    pokemon.to_csv('../data/'+filename)


def main():
    print('------------DATA MANIPULATION------------')
    check_current_directory()
    check_existance()
    check_already_ready()

    print(' #  generating jpg files for png files # ')
    pokemon = pd.read_csv('../data/pokemon.csv')
    png_to_jpg(pokemon_names=pokemon['Name'])
    print(' #              finished               # ', end='\n\n')

    print(' #            reshaping csv            # ')
    pokemon = reshape_dataframe(pokemon)
    print(' #              finished               # ', end='\n\n')

    print(' #  image replacement to class folder  # ')
    place_image_by_type(pokemon['Name'], pokemon['Type'], pokemon['variable'])
    print(' #              finished               # ', end='\n\n')

    print(' #          data augmentation          # ')
    augment()
    print(' #              finished               # ', end='\n\n')

    print(' #      erasing test image in train    # ')
    erase_test_img_in_train()
    print(' #              finished               # ', end='\n\n')

    # print(' #         update on csv file          # ')
    # update_csv(pokemon)
    # print(' #              finished               # ')
    print('----------------FINISHED-----------------')

if __name__ == '__main__':
    main()