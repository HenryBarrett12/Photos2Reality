

import py360convert as p360
import argparse
from pathlib import Path
import numpy as np
from PIL import Image
import os



def get_args():
    parser = argparse.ArgumentParser(description='Extract flattened images from 360 images.')
    parser.add_argument('--images', default='images', help='Path to the folder containing 360 images.')
    parser.add_argument('--output', default='output', help='Path to the folder where the flattened images will be saved.')
    parser.add_argument('--hfov', default=90, help='Horizontal field of view of the flattened images.')
    parser.add_argument('--vfov', default=90, help='Vertical field of view of the flattened images.')
    parser.add_argument('--hcount', default=4, help='Number of horizontal images to extract.')
    parser.add_argument('--cubemap', default=True, help='Overrite settings, use cubemap projection.')
    parser.add_argument('--scale', default=1, help='Scale the images by this factor.')
    args = parser.parse_args()
    return args


def cube_map(image, image_id, args):
    face_w = int(image.shape[0]/4 * args.scale)
    cube_dict = p360.e2c(image, cube_format='dict', face_w=face_w)
    for direction, img in cube_dict.items():
        img = Image.fromarray(img)

        p = Path(output_path.joinpath(direction))
        if not p.exists():
            p.mkdir()

        img.save(output_path / f'{direction}\{image_id}.jpg')


if __name__ == '__main__':
    args = get_args()
    images_path = Path(os.path.join(args.images))
    output_path = Path(os.path.join(args.output))
    hfov = int(args.hfov)
    vfov = int(args.vfov)

    if not output_path.exists():
        output_path.mkdir()
    
    for i, image_path in enumerate(images_path.glob('*.jpg')):
        image360 = np.array(Image.open(image_path))
        if args.cubemap:
            cube_map(image360, i, args)
    print("Done!")
        