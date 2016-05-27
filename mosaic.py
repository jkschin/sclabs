import cv2
import numpy as np
import math

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

class Mosaic:
	def __init__(self, arr, gray=False):
		self.arr = arr
		self.gray = gray
		if self.gray:
			self.arr = np.expand_dims(self.arr, axis=3)
		self.num_images, self.height, self.width, self.depth = self.arr.shape

	'''
	Helper method for brevity in code. Checks if the element in an array is the last one
	'''
	def last_item(self, cur, end):
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
	def reshape_row(self, arr):
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
	def reshape_col(self, arr):
		return reduce(lambda x, y: np.concatenate((x,y), axis=0), arr)

	'''
	Input:
		self.arr
	Output:
		numpy array that is mosaicked into a square.
	Example:
		Input:	numpy array with format [103, 100, 100, 3]
				103 Images of size [100 x 100] and depth [3].
		Output:	numpy array with format [1000, 1100, 3]
				A mosaic of the images. Empty space is greyed out.
	'''
	def square(self):
		sides = int(math.ceil(math.sqrt(self.num_images)))
		num_rows, num_cols = int(math.ceil(self.num_images/float(sides))), sides
		rows = []
		for i in range(num_rows):
			row_image = self.arr[i*num_cols:i*num_cols+num_cols]
			r_n, r_h, r_w, r_d = row_image.shape
			row_image = self.reshape_row(row_image)
			if self.last_item:
				for _ in range(num_cols-r_n):
					row_image = np.concatenate((row_image,np.zeros((self.height,self.width,self.depth))), axis=1) 
			rows.append(row_image)
		mosaic = self.reshape_col(rows)
		if self.gray:
			mosaic = np.squeeze(mosaic, axis=2)
		return mosaic
		# save_numpy_array_as_image(mosaic, "square.jpg")

					




# arr = np.array(PILImage.open("cat.jpg").convert("L"))
# arr = np.expand_dims(arr, axis=0)
# arr = np.concatenate((arr,arr,arr,arr,arr), axis=0)
# print arr.shape
# m = Mosaic(arr, True)
# m.square()
