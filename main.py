import os
import sys
import argparse
from mosaic import Mosaic

def main():
    args = parse_arguments()

    if args is not None:
        img = args.input
        out = args.output
        tiles = args.tiles

        Mosaic().create(img_name=img, out=out, dir=tiles)

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Image to create a mosaic")
    parser.add_argument("-o", "--output", help="Mosaic to be saved as")
    parser.add_argument("-t", "--tiles",
                                help="Directory of images for creating tiles")

    options = parser.parse_args()
    if len(sys.argv) not in [4, 7]:
        parser.print_help()
        return None
    return options

if __name__ == "__main__":
    main()
