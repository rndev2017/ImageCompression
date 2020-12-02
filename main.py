import argparse
import imageio
import os

import matplotlib.pyplot as plt

from SVDCompressor import SVDImageCompressor

ACCEPTABLE_FILE_FORMATS = ["jpg", "jpeg"]


class IncorrectImageFormatException(Exception):
    __cause__ = ".jpg or jpeg file suffix was expected"


def main(input_path: str, output_path: str, k: int, verbose: bool):
    """
    Retrieves the path to an .jpg image file and compresses
    the image based on Singular Value Decomposition.
    :param k: the number of singular values to approximate the ground truth image
    :param input_path: file path to .jpg image
    :param verbose: Output metrics and save compressed images?
    :param output_path: Where should the compressed image be stored?
    """
    compressor_instance = SVDImageCompressor(k=k, image_path=input_path)
    compressor_instance.compress(output_path=output_path, verbose=verbose)


if __name__ == '__main__':
    # Creates the command line argument parser
    parser = argparse.ArgumentParser(description="CLI for SVD Image Compressor")
    parser.add_argument("-i", "--input", help="Path to input image", required=True)
    parser.add_argument("-o", "--output",
                        help="Path to location where the compressed image should be stored",
                        required=True)
    parser.add_argument("-k", "--k", help="Number of singular values used by compressor", required=True, type=int)
    parser.add_argument("-v", "--verbose", help="Verbose?", required=True, type=int, default=0)
    args = parser.parse_args()
    try:
        # I/O Checks
        input_path = args.input
        file_format = input_path[input_path.find(".") + 1:]
        if os.path.isfile(input_path):
            if file_format in ACCEPTABLE_FILE_FORMATS:
                num_singular_values = args.k if args.k > 0 else None
                verbose = True if args.verbose == 1 else False
                output_path = args.output
                main(input_path=input_path, output_path=output_path, k=num_singular_values, verbose=verbose)
            else:
                raise IncorrectImageFormatException
        else:
            raise FileNotFoundError(f"{input_path} does not exist")
    except FileNotFoundError as error:
        print(error)
