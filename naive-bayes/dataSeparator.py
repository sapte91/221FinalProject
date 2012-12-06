#<product_type>, <helpful>, <rating>, <title>, <review_text>

#search for things btw <review> </review>

#extract above features

#array of reviews: # pos, # neg

import sys
import math

class DataSeparator:
	
	def readData(self, fileSet):
		allReviews = []
		isReview = False
		textString = ''
		for filename in fileSet:
			for line in open("data/"+filename, 'r'):
				if "<review_text>" in line:
					isReview = True
				if "</review_text>" in line:
					isReview = False
					if len(textString) != 0:
						allReviews.append(textString)
					textString = ''
				if isReview == True:
					splitLine = line.split()
					if len(splitLine) < 2:
						continue
					for i in range(len(splitLine)):
						textString += splitLine[i]
						textString += " "
		return allReviews

	def separateReviews(self, reviews):
		train = []
		test = []
		train_test = []
		numTest = (len(reviews) / 4) / 100
		numTrain = (len(reviews) - numTest) / 100
		train = reviews[:numTrain]
		test = reviews[numTrain:numTrain+numTest]
		train_test.append(train)
		train_test.append(test)
		return train_test

"""
def main(argv):
	dataSeparator = DataSeparator()

	posReviews = dataSeparator.readData(posFilesSet)
	negReviews = dataSeparator.readData(negFilesSet)

	train_test_pos = dataSeparator.separateReviews(posReviews)
	train_test_neg = dataSeparator.separateReviews(negReviews)

	print len(posReviews)
	print len(negReviews)
	print train_test_pos[0][0]


if __name__ == '__main__':
    main(sys.argv[1:])
"""
