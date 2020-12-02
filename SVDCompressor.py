import math
import os

import imageio
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from skimage.metrics import normalized_root_mse

THRESHOLD = 1e-6


class NoImageProvided(Exception):
    """An exception that is raised when SVDImageCompressor class is not provided an image path"""
    __cause__ = "No image path was provided"


class InvalidRankProvidedException(Exception):
    __cause__ = "The rank or number of singular value used is less or equal to 0"


def show_distinct_channels(image_path: str):
    rgb_channels = extract_RGB_channels(imageio.imread(image_path))
    img_name = image_path[image_path.find("/") + 1:image_path.find(".")]
    # Set up plot
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey="all", sharex="all")
    ax1.set_title("Red Channel")
    ax2.set_title("Green Channel")
    ax3.set_title("Blue Channel")
    # Show channel images
    ax1.imshow(rgb_channels[0])
    ax2.imshow(rgb_channels[1])
    ax3.imshow(rgb_channels[2])
    fig.suptitle(f"RGB Decomposition of {img_name}.jpg")
    plt.savefig(f"analysis/{img_name}RGBChannels.jpg", bbox_inches="tight")
    plt.close()


def extract_RGB_channels(image: imageio.core.util.Array) -> np.array:
    return np.array([
        image[:, :, 0],
        image[:, :, 1],
        image[:, :, 2]
    ], dtype=np.uint8)


class SVDImageCompressor:
    """Compresses images using singular value decomposition"""

    def __init__(self, k: int = None, image_path: str = None):
        try:
            if image_path is not None:
                self.image_path = image_path
                self.image_name = self.image_path[self.image_path.find("/") + 1:self.image_path.find(".")]
                if k is None:
                    self.__k = 1
                    raise InvalidRankProvidedException
                else:
                    print(f"Number of singular values initialized to {k}")
                    self.__k = k
            else:
                raise NoImageProvided
        except NoImageProvided as error:
            print(error.__cause__)
        except InvalidRankProvidedException as error:
            print(error.__cause__)
            print(f"Automatically set number of singular values to {self.__k}")

    def __calculate_compression_ratio(self, shape: tuple):
        """
        :param shape: The shape of the original image as a tuple
        :return: The compression ratio as computed using sizes of compressed image and original image
        """
        uncompressed_num_pixels = shape[0] * shape[1]
        compressed_num_pixels = (shape[0] * self.__k) + self.__k + (self.__k * shape[1])

        return uncompressed_num_pixels / compressed_num_pixels

    def __SVD(self, channel: np.array):
        """
        :param channel: A matrix corresponding to one of 3 color channels (R, G, B)
        :return: The compressed image of a color channel (R, G, or B)
        """
        U, sigma, V = np.linalg.svd(channel.copy())
        compressed = np.dot(U[:, :self.__k], np.dot(np.diag(sigma[:self.__k]), V[:self.__k, :]))
        return compressed

    def compress(self, output_path: str = None, verbose: bool = False):
        """
        Compresses the image and stores that image in a user provided output directory. If verbose is true
        then compression metrics will be computed and outputed
        :param output_path: The output directory in which the compressed file should be saved in
        :param verbose: Whether or not to display compression metrics
        :return: The compressed image as a matrix
        """
        # Read image
        image = imageio.imread(self.image_path)
        # Copy original image and get layers
        img_layers = np.zeros(image.shape)
        for i in range(3):
            img_layers[:, :, i] = self.__SVD(image[:, :, i]).astype(np.uint8)

        if output_path is not None:
            # If the directory doesn't exist create it
            if not os.path.isdir(output_path[:output_path.rfind("/")]):
                os.mkdir(output_path[:output_path.rfind("/")])
            # Save image
            result = Image.fromarray(img_layers.astype(np.uint8))
            result.save(output_path)
        if verbose:
            # Calculate compression metrics
            compression_ratio = self.__calculate_compression_ratio(image.shape)
            print(f"Current rank: {self.__k}")
            print(f"Compression Ratio: {compression_ratio}")
            print(f"Original file size: {os.path.getsize(self.image_path) / 1000} kB")
            print(f"Compressed file image: {os.path.getsize(output_path) / 1000} kB")
        return img_layers.astype(np.uint8)

    @property
    def k(self):
        return self.__k

    @k.setter
    def k(self, k):
        try:
            if k > 0:
                self.__k = k
            else:
                msg = "Number of singular values can't be less than or equal to 0."
                raise ValueError(msg)
        except ValueError as error:
            print(error)

    def __repr__(self):
        return f"Image Compressor is using {self.k} singular values"
