from nltk import RegexpParser
from nltk import pos_tag
from nltk import Tree
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from data_parser.semanticsParser import SemanticsParser
from data_parser.reviewParser import ReviewData

#Algorithm to process the reviews against a topic
class ReviewMiner:
    fileList = []       #list of files to be processed
    topic = ""          #topic to be mined
    positiveAdj = {}    #dictionary of positive adjectives
    negativeAdj = {}    #dictionary of negative adjectives
    intensifiers = {}   #dictionary of intensifiers

    def __init__(self, fileList, topic):
        self.fileList = fileList
        self.topic = topic
        semantics = SemanticsParser()
        self.positiveAdj = semantics.getPositives()
        self.negativeAdj = semantics.getNegatives()
        self.intensifiers = semantics.getIntensifiers()

    def process(self):
        #fill the process
