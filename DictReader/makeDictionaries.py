import sys, types, time, random, os

stopWordSet = set(line.split()[0].lower() for line in open("stop-words.txt").readlines())

class MakeSentimentDicts:
	"""
	Creates three separate files- pos-words.txt, neg-words.txt and neut-words.txt - for each of the different
	types of words in the sentiment dictionary and extracts just to word. Words are organized in the appropiate 
	file line by line.
	"""

	def readWords(self):
		pos_words = open("pos-words.txt", "w")
		neg_words = open("neg-words.txt", "w")
		neut_words = open("neut-words.txt", "w")
		for line in open("full-dict.txt", "r").readlines():
			key1 = 'word1='
			before1, key1, after1 = line.partition(key1)
			key2 = ' pos1='
			word, key2, after2 = after1.partition(key2)
			key3 = 'priorpolarity='
			before3, key3, word_type = after2.partition(key3)

			word_type = word_type.strip()
			
			if word in stopWordSet:
				print word
			else:
				if word_type == "positive":
					pos_words.write(word)
					pos_words.write("\n")
				elif word_type == "negative":
					neg_words.write(word)
					neg_words.write("\n")
				elif word_type == "neutral":
					neut_words.write(word)
					neut_words.write("\n")

		pos_words.close()
		neg_words.close()
		neut_words.close()

def main(argv):
    
    better_dict = MakeSentimentDicts()

    test = better_dict.readWords()

if __name__ == '__main__':
    main(sys.argv[1:])

