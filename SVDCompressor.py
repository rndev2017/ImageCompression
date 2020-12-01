import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import imageio
import os, math
from skimage.metrics import normalized_root_mse

THRESHOLD = 1e-6


class NoImageProvided(Exception):
    __cause__ = "No image path was provided"


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
    def __init__(self, k: int = None, image_path: str = None):
        try:
            if image_path is not None:
                self.image_path = image_path
                self.image_name = self.image_path[self.image_path.find("/") + 1:self.image_path.find(".")]
                if k is None:
                    self.__find_optimium_k()
                else:
                    print(f"K value initialized to {k}")
                    self.__k = k
            else:
                raise NoImageProvided
        except NoImageProvided as error:
            print(error.__cause__)

    def __find_optimium_k(self):
        # Open ground truth image
        ground_truth_img = imageio.imread(self.image_path)
        # Intialize binary search paramters
        range_of_k = [1, ground_truth_img.shape[0]]
        self.__k = 1
        count_of_repeated_metric = 0
        # Compress image with start parameters
        compress_img = self.compress()
        nrmse = normalized_root_mse(ground_truth_img, compress_img)
        while nrmse > THRESHOLD:
            self.__k = int(0.5 * (range_of_k[0] + range_of_k[1]))
            compress_img = self.compress()
            new_nrmse = normalized_root_mse(ground_truth_img, compress_img)
            if new_nrmse > nrmse:
                range_of_k[1] = self.__k
            else:
                range_of_k[0] = self.__k
            if math.fabs(new_nrmse - nrmse) < THRESHOLD and count_of_repeated_metric <= 3:
                count_of_repeated_metric += 1

            if count_of_repeated_metric >= 3:
                print("converged")
                break

            nrmse = new_nrmse
            print(nrmse, count_of_repeated_metric)

    def __calculate_compression_ratio(self, shape: tuple):
        uncompressed_num_pixels = shape[0] * shape[1]
        compressed_num_pixels = (shape[0] * self.__k) + self.__k + (self.__k * shape[1])

        return uncompressed_num_pixels / compressed_num_pixels

    def SVD(self, channel: np.array):
        U, sigma, V = np.linalg.svd(channel.copy())
        compressed = np.dot(U[:, :self.__k], np.dot(np.diag(sigma[:self.__k]), V[:self.__k, :]))
        return compressed

    def compress(self, verbose: bool = False):
        # Read image
        image = imageio.imread(self.image_path)
        # Copy original image and get layers
        img_layers = np.zeros(image.shape)
        for i in range(3):
            img_layers[:, :, i] = self.SVD(image[:, :, i]).astype(np.uint8)
        # Displays metrics and saves images
        if verbose:
            # Image paths
            og_path = f"images/{self.image_name}.jpg"
            compress_path = f"compressed_images/{self.image_name}-{self.__k}.jpg"
            # Save image
            result = Image.fromarray(img_layers.astype(np.uint8))
            result.save(compress_path)
            # Calculate compression metrics
            compression_ratio = self.__calculate_compression_ratio(image.shape)
            print(f"Compression Ratio: {compression_ratio}")
            print(f"Original file size: {os.path.getsize(og_path) / 1000} kB")
            print(f"Compressed file image: {os.path.getsize(compress_path) / 1000} kB")
            # Save Figure with Annotations
            plt.title(f"{os.path.getsize(compress_path) / 1000} kB (k={self.__k})")
            plt.imshow(img_layers.astype(np.uint8))
            plt.savefig(f"compressed_images/{self.image_name}-{self.__k}.jpg")

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
