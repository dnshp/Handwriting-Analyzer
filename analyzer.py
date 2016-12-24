from PIL import Image
import numpy as np
import os

#charset = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z','0','1','2','3','4','5','6','7','8','9']
charset = map(chr, range(65,91))

# "Data" is abstracted as [imgmap, character] where imgmap is a 100-length array and character is a 1-length string

# DATA ABSTRACTIONS
def imgmap(point): #returns the grayscale map from a data pair
	return point[0]

def character(point): #returns the character string from a data pair
	return point[1]

def pair(lst, letter): #constructs a data pair from a grayscale map and a character string
	return [lst, letter]

# PROCESSING FUNCTIONS

def load_image(filename): #The character represented will be the first character in the filename
	print("Loading image "+filename)
	return pair(arrayToList(grayscale(np.array(Image.open(os.getcwd() + '/Samples/' + filename)))), filename[0])

def load_all_images():
	return [load_image(file) for file in os.listdir(os.getcwd() + '/Samples/') if file.endswith('.jpg')]

def grayscale(arr): #converts an RGB image array to a grayscale array
	gray = np.full(arr.shape[:2],None)
	for row in range(arr.shape[0]):
		for element in range(arr.shape[1]):
			gray[row, element] = sum(arr[row][element])/3
	print("Grayscaling...")
	return gray

def arrayToList(arr): #reshapes a grayscale array into a vector
	print("Reshaping...")
	return list(arr.reshape(1, arr.shape[0]*arr.shape[1])[0])

def listsum(lst): #sums the terms of a list of lists
	print("Summing list terms...")
	return [sum(x) for x in zip(*lst)]

def distance(a,b):
	return sum([abs((a[i] - b[i])**2) for i in range(len(a))])

# MAPPING EXECUTION

def find_centroids(): #finds the centroids for each character in the data set
	data = load_all_images()
	centroids = {}
	for char in charset:
		filtered_images = [imgmap(d) for d in data if character(d) == char]
		centroid = [elem/len(filtered_images) for elem in listsum(filtered_images)]
		centroids[char] = centroid
	print("Centroids found.")
	return centroids

def write_to_file(centroids):
	file = open("centroids.txt","w")
	for key in centroids:
		file.write("{k}|{v}\n".format(k=key,v=centroids[key]))
	print("File written.")

# PREDICTING EXECUTION

def load_centroids():
	file = open("centroids.txt","r")
	line, centroids = file.readline(), {}
	while line:
		centroids[line[0]] = eval(line[2:])
		line = file.readline()
	return centroids

def predict(vec, centroids):
	squaredDiff = {}
	for i in centroids:
		squaredDiff[i] = distance(vec, centroids[i])
	return min(squaredDiff, key = squaredDiff.get)

def generate_centroid(character, centroids):
	rescaled = np.array(centroids[character]).reshape((40,40)).astype(np.uint8)
	Image.fromarray(rescaled).save(os.getcwd() + "/Centroids/" + "{char}Centroid.jpg".format(char=character))