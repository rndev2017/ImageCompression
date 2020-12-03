# Image Compression Using Singular Value Decomposition

## Why is image compression so important?
Firstly, what is image compression? Image compression is an application of data compression that is used to minimize redundancy in an image, thereby reducing the amount of data/information it hold, thus minimizing the file sizes. An effecient image compression algorithm is certainly behenficial for an era where sharing and accessing images and other media files are commonplace [1.8 billion photos are added to social media platforms **daily**.](https://www.businessinsider.com/were-now-posting-a-staggering-18-billion-photos-to-social-media-every-day-2014-5) For our MATH 214 Final Project, we wanted to delve into understanding the basics of image compression with a simple algorithm known as singular value decomposition or SVD which has its foundations in various linear algebra concepts that we have learned throughout this semester. 

## How do I use this software?
This project is built entirely with the Python programming langugage and uses a number of scientific libraries that should be installed before using otherwise the code won't work on your machine. I won't go over how to install Python here, but here is a [resource](https://realpython.com/installing-python/) that might help! This program is designed to run completely through the command line so you don't have to deal with any code.

### Get the code
If you are seeing this on GitHub, on the main screen there should be a **green** button that shows that says "Code". When you click that there should be a dropdown menu of which there are 3 options, _Clone_, _Open in Github Desktop_, _Download Zip_. Click the _Download Zip_ option and you should see a download start. Depending on your browser, the location of this will be different. After the download has completed, extract its content into whatever directory (i.e. folder) you want this code to be in.

### Installing dependencies
Dependencies are other pieces of software that my project uses in order for it to function properly. In this case, its a suite of scientific software that allows us to compute matrix and linear algebra operations faster than if we were to write all that code by ourselves. The list of dependencies are listed in a file called _requirements.txt_. In order to install the dependencies listed in the file run the following command in your terminal and in the folder where the code is. ```pip install -r requirements.txt```
There might be errors if Python is install incorrectly, so if you encounter any issues make sure to check ur installation of Python and use the internet as a secondary resource. 

### Running the code
This project comes with 3 test images in the [images/](https://github.com/rndev2017/ImageCompression/tree/master/images) directory of varying size. You can test out the program with these 3 test images if you would like, but you can add your own images as well. If you want to compress your own images, simply drop them into the aforementioned directory and it should be availabe for the program to compress. As you might have seen there is another folder called [_compressed_images/_](https://github.com/rndev2017/ImageCompression/tree/master/compressed_images), this folder contains some tests that I ran on the 3 of the test images, if you would like you can go ahead and delete them, they won't stop the code from running :) Once you have your image that you want to compress, its time to actually run the program to compress your image! Yay!

#### Pre-Run Check
- [ ] I have installed Python successfully with no errors or issues
- [ ] I have installed all the dependecies as highlighted above
- [ ] I am in the directory where the project files are
 
#### What to type into the terminal
```
python main.py -i [LOCATION OF UNCOMPRESSED IMAGE] -o [LOCATION WHERE COMPRESSED IMAGE SHOULD BE SAVED] -k [INTEGER GREATER THAN 0 AND LESS THAN THE WIDTH OF IMAGE IN PIXELS] -v [0 OR 1]
```

This should run the program with the specific input that you give it. If it seems like its hung, its probably because you inputed a really large image and its taking a while to crunch the numbers. Be patient, if it doesn't work after a while, try resizing the image so that its smaller and easier to work with. If you have issues where it takes a while, create an issue on Github and I'll take a look at it and see how to fix it. The code files are set up for basic functionality: it will compress your desired image given the number of singular values you give it. There are some functions that are not used when you run the program that you can look at and mess around with. 

## Results
Here is a GIF where you can observe the increase in quality of the compressed image as the number of singular values are used increases. Additionally, you can also see the file size of the image change as the number of singular values increase

<p align="center">
  <img src="https://github.com/rndev2017/ImageCompression/blob/master/compressed_images/bird.gif" alt="Bird Compressed GIF" style="width:100%">
</p>
