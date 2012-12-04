#<product_type>, <helpful>, <rating>, <title>, <review_text>

#search for things btw <review> </review>

#extract above features

#array of reviews: # pos, # neg

import sys
from dataSeparator import DataSeparator
import re

negFilesSet = set(line.split()[0].lower() for line in open("data/negative-files-list.txt").readlines())
posFilesSet = set(line.split()[0].lower() for line in open("data/positive-files-list.txt").readlines())

class FeaturesCreator:
	def computeFeatures(self, reviews, currentFeaturesSet):
		features = currentFeaturesSet
		lastIndex = 0
		for review in reviews:
			lastIndex = 0
			wordList = review.split()
			for i in range(len(wordList)):
				wordList[i] = wordList[i].lower()
				# if all letters in word aren't either alpha or common name symbol
		        wordList[i] = wordList[i].strip('.,/\(\)!? ')
		        if i != 0:
		        	features.add((wordList[lastIndex],wordList[i]))
		        	lastIndex += 1
	   	# original features
	   	return features
	
	def createFeatureVector(self, review, featuresSet, type):
		feature_value = {}
		for item in featuresSet:
			feature_value[item] = 0
		if type == 0:
			feature_value["type"] = 0
		else:
			feature_value["type"] = 1
		wordList = review.split()[0].lower().strip('.,/\(\)!? ')
		lastIndex = 0
		for i in range(len(wordList)):
			if i != 0:
				if (wordList[lastIndex],wordList[i]) in featuresSet:
					feature_value[(wordList[lastIndex],wordList[i])] = 1
		    	lastIndex += 1

		return feature_value
	

def main(argv):
	dataSeparator = DataSeparator()

	posReviews = dataSeparator.readData(posFilesSet)
	negReviews = dataSeparator.readData(negFilesSet)

	train_test_pos = dataSeparator.separateReviews(posReviews)
	train_test_neg = dataSeparator.separateReviews(negReviews)

	featuresCreator = FeaturesCreator()
	allFeatures = set()
	allFeatures = featuresCreator.computeFeatures(train_test_pos[0],allFeatures)
	allFeatures = featuresCreator.computeFeatures(train_test_neg[0],allFeatures)
	
	train_data = []
	for review in train_test_pos[0]:
		train_data.append(featuresCreator.createFeatureVector(review,allFeatures,1))
	for review in train_test_neg[0]:
		train_data.append(featuresCreator.createFeatureVector(review,allFeatures,0))


if __name__ == '__main__':
    main(sys.argv[1:])