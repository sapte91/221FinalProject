import sys

posWordSet = set(line.split()[0].lower() for line in open("pos-words.txt").readlines())
negWordSet = set(line.split()[0].lower() for line in open("neg-words.txt").readlines())
neutWordSet = set(line.split()[0].lower() for line in open("neut-words.txt").readlines())
negFilesSet = set(line.split()[0].lower() for line in open("negative-files-list.txt").readlines())
posFilesSet = set(line.split()[0].lower() for line in open("positive-files-list.txt").readlines())

class ReviewExtractor:

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
    numPosReviews = 0
    numNegReviews = 0
    reviewExtractor = ReviewExtractor()

    totalPosClass = []
    # loop thru positive reviews
    for posFile in posFilesSet:
        posData = reviewExtractor.readData(posFile)
        # array of classifications for each text file
        posClass = reviewExtractor.classifyData(posData)
        totalPosClass.append(posClass)
        numPosReviews += len(posClass)

    posScore = reviewExtractor.scoreClassification(totalPosClass, 'positive')
    print "POSITIVE SCORE: ", posScore

    totalNegClass= []
    # loop thru negative reviews
    for negFile in negFilesSet:
        negData = reviewExtractor.readData(negFile)
        negClass = reviewExtractor.classifyData(negData)
        totalNegClass.append(negClass)
        numNegReviews += len(negClass)

    negScore = reviewExtractor.scoreClassification(totalNegClass, 'negative')
    print "NEGATIVE SCORE: ", negScore
    print "\n"
    print "NUMERICAL DATA"
    print "--------------"
    numReviews = numPosReviews + numNegReviews
    print "NUMBER OF POS REVIEWS: ", numPosReviews
    print "NUMBER OF NEG REVIEWS: ", numNegReviews
    print "TOTAL NUMBER OF REVEIWS: ", numReviews
    print "NUM POS WORDS: ", len(posWordSet)
    print "NUM NEG WORDS: ", len(negWordSet)



if __name__ == '__main__':
    main(sys.argv[1:])
