import nltk
from nltk.stem import PorterStemmer

porter_stemmer = PorterStemmer()
summaryList = list()
descriptionList = list()
inputFile = ".\CIS580_Assignment_BugLocalization\AspectJ_Dataset.txt"
stopWordList = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
stemList = [

]

def stemList(list):
	newList = list()
	for i in l:
		item = i
		for j in stopWordList:
			item = i.replace(j, "")
		newList.append(item)
	return newList

def removeStopWords(l):
	newList = list()
	for i in l:
		item = i
		for j in stopWordList:
			item = i.replace(j, "")
		newList.append(item)
	return newList

with open(inputFile, 'r') as f:
	lines = f.read().splitlines()
	for l in lines:
		items = l.split("\t")
		summaryList.append(items[2])
		descriptionList.append(items[3])

	summaryList = removeStopWords(summaryList)
	descriptionList = removeStopWords(descriptionList)



