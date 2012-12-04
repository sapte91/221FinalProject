import sys
import ReviewExtractor

numEpochs = 10000

class LogisticRegression {

	# train model with training data
	def trainModel(numInputVars, numDataVects, betas, gradients, inputVars, classes):
	    z = 0.0
	    for e in range(0, numEpochs):
			# initialize gradients to 0
			for g in range(0, numInputVars + 1):
				gradients[g] = 0

			# loop through training
			for  i in range(0, numDataVects):
				z = findZ(i, numInputVars, betas, inputVars)
				# compute "batch" gradient for each variable j in vector i
				for g in range(0, numInputVars + 1):
					gradients[g] += inputVars[i][g]
					                * (classes[i] - 1 / (1 + Math.exp(z * -1)))

			# reset z to 0
			z = 0.0
			updateBetas(numInputVars, betas, gradients)
	    }


	# find z for data vector i
	def findZ(i, numInputVars, betas, inputVars):
		# initialize z for vector i
		z = betas[0] * inputVars[i][0]

		# loop through input variables of vector i
		for j in range(1, numInputVars + 1):
			# update z with beta j and input variable j of vector i
			z += betas[j] * inputVars[i][j]
		return z

	# loop through betas array to update all betas
	def updateBetas(numInputVars, betas, gradients):
		learnRate = 1 / numEpochs

		# update betas
		for b in range(0, numInputVars + 1):
			betas[b] += learnRate * gradients[b]

    # testing data
	def testData(betas):
		# read in data
		# TODO ********

		# classifyData
		classifyData(inputVars, classes, betas)

    # classify data
    def classifyData(inputVars, classes, betas):
		z = 0.0
		p = 0.0
		correct0 = 0
		correct1 = 0
		total0 = 0
		total1 = 0
        accuracy

		# find z for vector i
		for i in range(0, len(classes):
			z = findZ(i, len(inputVars[0]) - 1, betas, inputVars)
			# find P(Y=1|X)
			for j in range(0, len(inputVars[0] + 1):
				p = 1 / (1 + Math.exp(z * -1))

			# classify vector
			if p > 0.5:
				classification = 'positive'
				# if correct
				if classification == classes[i]:
					correct1 += 1
			else:
				classification = 'negative'
				# if correct
				if classification == classes[i]:
					correct0 += 1

			# increment totals
			if classes[i] == 'positive':
				total1 += 1
            else:
				total0 += 1

        print "negative: tested ", total0, ", correctly classified ", correct0
        print "positive: tested ", total1, ", correctly classified " + correct1
        print "Overall: tested ", total0 + total1, ", correctly classified ", correct0 + correct1

		accuracy = (correct0 + correct1 + 0.0) / (total0 + total1)
		print "Accuracy: ", accuracy

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

    # totalPosClass now has all positive/negative classifications for all reviews in positive review file
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

#####

	# variables to store file data
	betas = []
	gradients = []
	inputVars = [][]
	classes = []

    # numDataVects should be numReviews
    # numInputVars should be numWords
    trainModel(numInputVars, numDataVects, betas, gradients, inputVars, classes);
    testData(betas);
