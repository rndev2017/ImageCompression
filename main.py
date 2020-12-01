import argparse, imageio
from SVDCompressor import SVDImageCompressor
import matplotlib.pyplot as plt
import os


class IncorrectImageFormatException(Exception):
    __cause__ = ".jpg file suffix was expected"


def get_all_possible_compressed_images(step: int, total: int, image_path: str):
    k = step
    compressor = SVDImageCompressor(k=k, image_path=image_path)
    while k < total:
        compressor.compress(verbose=True)
        k += step
        compressor.k = k


def display_original_image(image_path: str):
    image = imageio.imread(image_path)
    title = f"Original Image {os.path.getsize(image_path) / 1000} kB"
    plt.title(title)
    plt.imshow(image)
    plt.savefig("compressed_images/og_image.jpg")


def main(file_path: str):
    """
    Retrieves the path to an .jpg image file and compresses
    the image based on Singular Value Decomposition.
    :param file_path: file path to .jpg image
    """
    # get_all_possible_compressed_images(2, 512, file_path)
    compressor = SVDImageCompressor(image_path=file_path)
    compressor.compress(verbose=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--Input", help="Input directory to image file", required=False)
    args = parser.parse_args()
    try:
        if args.Input and args.Input.endswith(".jpg"):
            print(f"Got {args.Input}")
            main(args.Input)
        elif not args.Input.endswith(".jpg"):
            raise IncorrectImageFormatException
    except IncorrectImageFormatException as error:
        print(error.__cause__)