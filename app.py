import nltk, magic
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
from pathlib import Path
from comment_parser import comment_parser
import csv

porter_stemmer = PorterStemmer()
# summaryList = list()
# descriptionList = list()
reportList = list()
reportFileList = list()
fileList = list()
fileContentList = list()
fileNames = list()
ranklist = list()
bugidList = list()
inputFile = ".\CIS580_Assignment_BugLocalization\AspectJ_Dataset.txt"
inputDir = ".\CIS580_Assignment_BugLocalization\sourceFile_aspectj\org.aspectj"
stopWordList = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]


def stemList(l):
	stemList = list()
	for i in l:
		stemmedLine = ""
		words = i.split(" ")
		stemmedWords = [porter_stemmer.stem(word) for word in words]
		for w in stemmedWords:
			stemmedLine = stemmedLine + " " + w
		stemList.append(stemmedLine)

	return stemList

def removeStopWords(l):
	newList = list()
	for i in l:
		item = i
		for j in stopWordList:
			item = i.replace(j, "")
		newList.append(item)
	return newList

def list_files_recursive(path='.'):
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            list_files_recursive(full_path)
        else:
            fileList.append(full_path)

def extractComments(fileContent):
	print(fileContent.search('/*(.*)*/'))

with open(inputFile, 'r') as f:
	lines = f.read().splitlines()
	headerFlag = True
	for l in lines:
		if(headerFlag != True):
			items = l.split("\t")
			reportList.append(items[2] + " " + items[3])
			reportFileList.append(items[9])
			bugidList.append(items[1])
		headerFlag = False


reportList = removeStopWords(reportList)
reportList = stemList(reportList)

tfidf = TfidfVectorizer()
tfidfResult = tfidf.fit_transform(reportList)

list_files_recursive(inputDir)

for file in fileList:
	end = str(file).split(" ")[1]
	beginning = str(file).rsplit('\\', 1)[0]
	fileNames.append(beginning + "\\" + end)
	with open(file, 'r') as f:
		content = f.read()
		try:
			p = comment_parser.extract_comments_from_str(content, 'text/x-java-source')
			for i in p:
				fileContentList.append(str(i))
		except:
			print("Error found when parsing")

fileContentList = removeStopWords(fileContentList)
fileContentList = stemList(fileContentList)

tfidfFileResult = tfidf.transform(fileContentList)
cosineOutput = cosine_similarity(tfidfResult, tfidfFileResult, dense_output=True)

iter = 0
for i in cosineOutput:
	ranklist.append([i[0], bugidList[iter]])
	iter = iter + 1

sortedList = sorted(ranklist, reverse=True)


with open("bug_localization_ranks.csv", 'w', newline='') as f:
	fieldNames = ['BugID', 'Rank']
	writer = csv.DictWriter(f, fieldnames=fieldNames)
	writer.writeheader()
	for i in sortedList:
		writer.writerow({'BugID':i[1], 'Rank':i[0]})

with open("debug.txt", "w") as f:
	for i in sortedList:
		f.write(str(i) + "\n")