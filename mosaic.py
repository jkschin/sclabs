import cv2
import os
import numpy as np
import math
import sys

'''
To implement: Padding in mosaicking.
'''

'''
Input: 
	numpy array with format [length, width, depth]
	integer pad size
Output: 
	padded numpy array with format [length, width, depth]
'''
def pad_colour_image(arr, pad_size):
	transposed = np.transpose(arr, (2,0,1))
	padded = np.pad(transposed, pad_width=((0,0),(pad_size,pad_size),(pad_size,pad_size)), mode='constant', constant_values=0)
	padded = np.transpose(padded, (1,2,0))
	return padded

'''
Input: 
	numpy array with format [height, width]
	integer pad size
Output:
	padded numpy array with format [height, width]
'''
def pad_grayscale_image(arr, pad_size):
	expanded = np.expand_dims(arr, axis=2)
	padded = pad_colour_image(expanded, pad_size)
	squeezed = np.squeeze(padded, axis=2)
	return squeezed
	
def save_numpy_array_as_image(arr, filename):
	norm = cv2.normalize(arr, 0, 255, norm_type=cv2.NORM_MINMAX)
	norm.astype(np.uint8)
	cv2.imwrite(filename, norm)

'''
Helper method for brevity in code. Checks if the element in an array is the last one
'''
def last_item(cur, end):
	return (cur+1) == end

'''
Input:
	numpy array with format [num_images, height, width, depth]
Output:
	numpy array with format [height, width*num_images, depth]
Example:
	Input: 	numpy array with shape [2, 100, 100, 3]
	Output: numpy array with shape [100, 200, 3]
	The images are now horizontally stacked.
'''
def reshape_row(arr):
	return reduce(lambda x, y: np.concatenate((x,y), axis=1), arr)

'''
Input:
	numpy array with format [num_images, height, width, depth]
Output:
	numpy array with format [height*num_images, width, depth]
Example:
	Input: 	numpy array with shape [2, 100, 100, 3]
	Output:	numpy array with shape [200, 100, 3]
	The images are now vertically stacked.
'''
def reshape_col(arr):
	return reduce(lambda x, y: np.concatenate((x,y), axis=0), arr)

'''
Input:
	arr
Output:
	numpy array that is mosaicked into a square.
Example:
	Input:	numpy array with format [103, 100, 100, 3]
			103 Images of size [100 x 100] and depth [3].
	Output:	numpy array with format [1000, 1100, 3]
			A mosaic of the images. Empty space is greyed out.
'''
def square(arr, gray=False):
	num_images, height, width, depth = arr.shape
	sides = int(math.ceil(math.sqrt(num_images)))
	num_rows, num_cols = int(math.ceil(num_images/float(sides))), sides
	rows = []
	for i in range(num_rows):
		row_image = arr[i*num_cols:i*num_cols+num_cols]
		r_n, r_h, r_w, r_d = row_image.shape
		row_image = reshape_row(row_image)
		if last_item:
			for _ in range(num_cols-r_n):
				row_image = np.concatenate((row_image,np.zeros((height,width,depth))), axis=1) 
		rows.append(row_image)
	mosaic = reshape_col(rows)
	if gray:
		mosaic = np.squeeze(mosaic, axis=2)
	return mosaic

'''
Input:
	directory: string
Output:
	numpy array of all images in the directory
Example:
	Input: /home/directory with 1000 images of [100 x 100 x 3]
	Output: numpy array with format [1000 x 100 x 100 x 3]
'''
def build_array_from_directory(directory):
	arr = []
	image_name_list = []
	for image_name in os.listdir(directory):
		try:
			image_name_list.append(int(image_name[:-4]))
		except ValueError:
			image_name_list.append(image_name[:-4])
	image_name_list = sorted(image_name_list)
	for image_name in image_name_list:
		arr.append(cv2.imread(os.path.join(directory, str(image_name) + ".jpg")))
	return np.array(arr)

def run_sample():
	run("images", "")

def run(input_directory, output_directory):
	arr = build_array_from_directory(input_directory)
	img = square(arr, gray=False)
	save_numpy_array_as_image(img, os.path.join(output_directory, "square.jpg"))

if __name__ == "__main__":
	if sys.argv[1] == "test":
		run_sample()
	elif len(sys.argv) != 3:
		print "Usage: python mosaic.py input_directory output_directory"
	else:
		input_directory = sys.argv[1]
		output_directory = sys.argv[2]
		run(input_directory, output_directory)

