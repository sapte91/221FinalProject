#<product_type>, <helpful>, <rating>, <title>, <review_text>

#search for things btw <review> </review>

#extract above features

#array of reviews: # pos, # neg

from dataSeparator import DataSeparator
import re
import sys, types, time, random, os

posWordSet = set(line.split()[0].lower() for line in open("data/pos-words.txt").readlines())
negWordSet = set(line.split()[0].lower() for line in open("data/neg-words.txt").readlines())
negFilesSet = set(line.split()[0].lower() for line in open("data/negative-files-list.txt").readlines())
posFilesSet = set(line.split()[0].lower() for line in open("data/positive-files-list.txt").readlines())
stopWords = set(line.split()[0].lower() for line in open("stop-words.txt").readlines())

class FeaturesCreator:
	def computeFeaturePairs(self, reviews, currentFeaturesSet):
		features = currentFeaturesSet
		lastIndex = 0
		for review in reviews:
			lastIndex = 0
			wordList = review.split()
		#	print wordList
			for i in range(len(wordList)):
				wordList[i] = wordList[i].lower().strip(" ,.?/:;\(\)!")
				# if all letters in word aren't either alpha or common name symbol
				#features.add(wordList[i])
				
				if i != 0:
					if wordList[lastIndex] in posWordSet or wordList[lastIndex] in negWordSet or wordList[i] in posWordSet or wordList[i] in negWordSet:
						features.add((wordList[lastIndex],wordList[i]))
					lastIndex = lastIndex + 1

	   	# original featuresd
	   	return features
	
	def computeFeatureWords(self, reviews, currentFeaturesSet):
		features = currentFeaturesSet
		lastIndex = 0
		for review in reviews:
			wordList = review.split()
			for i in range(len(wordList)):
				wordList[i] = wordList[i].lower().strip(" ,.?/:;\(\)!")
				# if all letters in word aren't either alpha or common name symbol
				#features.add(wordList[i])
				if wordList[i] not in stopWords:
				#if wordList[i] in posWordSet or wordList[i] in negWordSet:
					features.add(wordList[i])

	   	# original features
	   	return features

	def createFeatureVector(self, review, featuresPairs, featureWords, type):
		#print featuresSet
		all_features = {}
		#for item in featuresPairs:
		#	all_features[item] = 0
		for item in featureWords:
			all_features[item] = 0
		if type == 0:
			all_features["type"] = 0
		else:
			all_features["type"] = 1
		wordList = review.split()
		lastIndex = 0
		count = 0
		for i in range(len(wordList)):
			wordList[i] = wordList[i].lower().strip(" ,.?/:;\(\)!")
			#if i != 0:
				#if (wordList[lastIndex],wordList[i]) in featuresPairs:
				#	all_features[(wordList[lastIndex],wordList[i])] = 1
				#	count = count + 1
		   		#lastIndex = lastIndex + 1
		   	if wordList[i] in featureWords:
		   		all_features[wordList[i]] = 1
		   		count = count + 1
		   		#if wordList[i] in featuresSet:
		  		#	feature_value[wordList[i]] = 1
		return all_features
	
	def convertDictToList(self,allDataDicts):
		featuresList = []
		train_data_list = []
		for key in allDataDicts[0].keys():
			if key != "type":
				featuresList.append(key)
		for reviewDict in allDataDicts:
			reviewList = []
			for i in range(len(featuresList)):
				reviewList.append(reviewDict[featuresList[i]])
			reviewList.append(reviewDict["type"])
			train_data_list.append(reviewList)
		return train_data_list

def main(argv):
	dataSeparator = DataSeparator()

	posReviews = dataSeparator.readData(posFilesSet)
	negReviews = dataSeparator.readData(negFilesSet)

	train_test_pos = dataSeparator.separateReviews(posReviews)
	train_test_neg = dataSeparator.separateReviews(negReviews)

	featuresCreator = FeaturesCreator()
	allFeaturesPairs = set()
	allFeaturePairs = featuresCreator.computeFeaturePairs(train_test_pos[0],allFeaturesPairs)
	allFeaturesPairs = featuresCreator.computeFeaturePairs(train_test_neg[0],allFeaturesPairs)

	allFeaturesWords = set()
	allFeatureWords = featuresCreator.computeFeatureWords(train_test_pos[0],allFeaturesWords)
	allFeaturesWords = featuresCreator.computeFeatureWords(train_test_neg[0],allFeaturesWords)
	
	train_data_dicts = []
	for review in train_test_pos[0]:
		train_data_dicts.append(featuresCreator.createFeatureVector(review,allFeaturesPairs,allFeaturesWords,1))
	for review in train_test_neg[0]:
		train_data_dicts.append(featuresCreator.createFeatureVector(review,allFeaturesPairs,allFeaturesWords,0))

	test_data_dicts = []
	for review in train_test_pos[1]:
		test_data_dicts.append(featuresCreator.createFeatureVector(review,allFeaturesPairs,allFeaturesWords,1))
	for review in train_test_neg[1]:
		test_data_dicts.append(featuresCreator.createFeatureVector(review,allFeaturesPairs,allFeaturesWords,0))
	
	train_data_list = featuresCreator.convertDictToList(train_data_dicts)
	test_data_list = featuresCreator.convertDictToList(test_data_dicts)
	
	trainfile = open("train_stopw_0.txt", "w")
	trainfile.write(str(len(train_data_list[0])-1))
	trainfile.write("\n")
	trainfile.write(str(len(train_data_list)))
	trainfile.write("\n")
	for review in train_data_list:
		for i in range(len(review)):
			if i < len(review)-1:
				trainfile.write(str(review[i]))
				trainfile.write(" ")
			else:
				if review[i] == 1:
					trainfile.write(":1")
					trainfile.write("\n")
				else:
					trainfile.write(":0")
					trainfile.write("\n")

	testfile = open("test_stopw_0.txt", "w")
	testfile.write(str(len(test_data_list[0])-1))
	testfile.write("\n")
	testfile.write(str(len(test_data_list)))
	testfile.write("\n")
	for review in test_data_list:
		for i in range(len(review)):
			if i < len(review)-1:
				testfile.write(str(review[i]))
				testfile.write(" ")
			else:
				if review[i] == 1:
					testfile.write(":1")
					testfile.write("\n")
				else:
					testfile.write(":0")
					testfile.write("\n")
	
	

if __name__ == '__main__':
    main(sys.argv[1:])