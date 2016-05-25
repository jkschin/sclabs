from PIL import Image as PILImage
import numpy as np

'''
Input: numpy array with format [length, width, depth], pad size.
Output: padded numpy array with format [length, width, depth].
'''
def pad_colour_image(arr, pad_size):
	transposed = np.transpose(arr, (2,0,1))
	padded = np.pad(transposed, pad_width=((0,0),(pad_size,pad_size),(pad_size,pad_size)), mode='constant', constant_values=0)
	padded = np.transpose(padded, (1,2,0))
	return padded

def pad_grayscale_image(arr, pad_size):
	expanded = np.expand_dims(arr, axis=2)
	padded = pad_colour_image(expanded, pad_size)
	squeezed = np.squeeze(padded, axis=2)
	return squeezed

	

arr = np.array(PILImage.open("cat.jpg").convert('L'))
# padded = arr
# padded = pad_grayscale_image(arr, 100)
padded = pad_colour_image(arr, 100)
img = PILImage.fromarray(padded.astype(np.uint8))
img.save('lol.jpg')