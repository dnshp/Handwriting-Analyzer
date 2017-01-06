import numpy as np
from PIL import Image
from analyzer import grayscale

def slice(arr, slice_height, slice_width):
	arr_height, arr_width = arr.shape
	height_divs, width_divs = arr_height // slice_height, arr_width // slice_width
	row_start, col_start = 0, 0
	while row_start < arr_height:
		while col_start < arr_width:
			yield arr[row_start:row_start + slice_height, col_start:col_start + slice_width]
			col_start += slice_width
		row_start += slice_height
		col_start = 0

def autoslice(img, slice_height, slice_width):
	im = Image.open(img)
	im = grayscale(np.array(im))
	slices = list(slice(im, slice_height, slice_width))
	slices = [Image.fromarray(i.astype(np.uint8)) for i in slices]
	for i in range(len(slices)):
		slices[i].save(str(i) + ".jpg")