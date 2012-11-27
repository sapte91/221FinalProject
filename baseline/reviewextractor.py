#<product_type>, <helpful>, <rating>, <title>, <review_text>

#search for things btw <review> </review>

#extract above features

#array of reviews: # pos, # neg

import sys

stopWordSet = set(line.split()[0].lower() for line in open("stop-words.txt").readlines())
posWordSet = set(line.split()[0].lower() for line in open("pos-words.txt").readlines())
negWordSet = set(line.split()[0].lower() for line in open("neg-words.txt").readlines())
neutWordSet = set(line.split()[0].lower() for line in open("neut-words.txt").readlines())
negFilesSet = set(line.split()[0].lower() for line in open("negative-files-list.txt").readlines())
posFilesSet = set(line.split()[0].lower() for line in open("positive-files-list.txt").readlines())

class ReviewExtractor:
    """
    Words is a list of the words in the sentence, previousLabel is the label
    for position-1 (or O if it's the start of a new sentence), and position
    is the word you are adding features for.
    """

    def computeFeatures(self, words, previousLabel, position):
        features = []
        currentWord = words[position]
        lowerWord = currentWord.lower()
        previousWord = words[position-1].lower()
        # if all letters in word aren't either alpha or common name symbol
        for letter in currentWord:
            if letter.lower() not in alphabet and letter != "." and letter != "'" and letter != "-":
                features.append("wordNotNameChar")
                return features

        # original features
        features.append("word=" + currentWord);
        features.append("prevLabel=" + previousLabel);
        features.append("word=" + currentWord + ", prevLabel=" + previousLabel);

        return features

    def setFeaturesTrain(self, data):
        newData = []
        words = []

        for datum in data:
            words.append(datum.word)

        ## This is so that the feature factory code doesn't
        ## accidentally use the true label info
        previousLabel = "O"
        for i in range(0, len(data)):
            datum = data[i]

            newDatum = Datum(datum.word, datum.label)
            newDatum.features = self.computeFeatures(words, previousLabel, i)
            newDatum.previousLabel = previousLabel
            newData.append(newDatum)

            previousLabel = datum.label

        return newData

    """
    Compute the features for all possible previous labels
    """
    def setFeaturesTest(self, data):
        newData = []
        words = []
        labels = []
        labelIndex = {}

        for datum in data:
            words.append(datum.word)
            if not labelIndex.has_key(datum.label):
                labelIndex[datum.label] = len(labels)
                labels.append(datum.label)

        ## This is so that the feature factory code doesn't
        ## accidentally use the true label info
        for i in range(0, len(data)):
            datum = data[i]

            if i == 0:
                previousLabel = "O"
                datum.features = self.computeFeatures(words, previousLabel, i)

                newDatum = Datum(datum.word, datum.label)
                newDatum.features = self.computeFeatures(words, previousLabel, i)
                newDatum.previousLabel = previousLabel
                newData.append(newDatum)
            else:
                for previousLabel in labels:
                    datum.features = self.computeFeatures(words, previousLabel, i)

                    newDatum = Datum(datum.word, datum.label)
                    newDatum.features = self.computeFeatures(words, previousLabel, i)
                    newDatum.previousLabel = previousLabel
                    newData.append(newDatum)

        return newData

    # read in review text, return list of lists: each index has list of # pos/neg words
    def readData(self, filename):
        allReviews = []
        isReview = False
        numPos = 0
        numNeg = 0
        for line in open(filename, 'r'):
            if "<review_text>" in line:
                isReview = True
            if "</review_text>" in line:
                isReview = False
                allReviews.append([numPos, numNeg])
                numPos = 0
                numNeg = 0
            if isReview == True:
                splitLine = line.split()
                if len(splitLine) < 2:
                    continue
                for word in splitLine:
                    if word in posWordSet:
                        numPos += 1
                    if word in negWordSet:
                        numNeg += 1

        return allReviews

    # classify array of reviews as positive or negative
    # return array of classifications
    def classifyData(self, reviewArray):
        classifiedData = []
        for review in reviewArray:
            if review[0] > review[1]:
                classifiedData.append('positive')
            else:
                classifiedData.append('negative')
      #  print classifiedData
        return classifiedData

    # read in array (all text files) of array of classifications (all reviews per text file)
    # score classification and return percentage
    def scoreClassification(self, fileClassArray, actual):
        numRight = 0.0
        numWrong = 0.0
        for reviewClassArray in fileClassArray:
            for classification in reviewClassArray:
                if classification == actual:
                    numRight += 1
                else:
                    numWrong += 1
        return numRight / (numRight + numWrong)


def main(argv):

    posScore = 0.0
    negScore = 0.0
    reviewExtractor = ReviewExtractor()

    totalPosClass = []
    for posFile in posFilesSet:
        posData = reviewExtractor.readData(posFile)
        posClass = reviewExtractor.classifyData(posData)
        totalPosClass.append(posClass)

    posScore = reviewExtractor.scoreClassification(totalPosClass, 'positive')
    print "POSITIVE SCORE: ", posScore

    totalNegClass= []
    for negFile in negFilesSet:
        negData = reviewExtractor.readData(negFile)
        negClass = reviewExtractor.classifyData(negData)
        totalNegClass.append(negClass)

    negScore = reviewExtractor.scoreClassification(totalNegClass, 'negative')
    print "NEGATIVE SCORE: ", negScore


    # add the features
 #   trainDataWithFeatures = reviewExtractor.setFeaturesTrain(trainData);
 #   testDataWithFeatures = reviewExtractor.setFeaturesTest(testData);

    # write the updated data into JSON files
   # reviewExtractor.writeData(trainDataWithFeatures, "trainWithFeatures");
    #reviewExtractor.writeData(testDataWithFeatures, "testWithFeatures");

if __name__ == '__main__':
    main(sys.argv[1:])
