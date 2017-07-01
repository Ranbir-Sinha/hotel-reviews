from nltk import RegexpParser
from nltk import pos_tag
from nltk import Tree
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from data_parser.semanticsParser import SemanticsParser
from data_parser.reviewParser import ReviewData
from output.displayResult import Display

#Algorithm to process the reviews against a topic
class ReviewMiner:
    fileList = []       #list of files to be processed
    topic = ""          #topic to be mined
    positiveAdj = {}    #dictionary of positive adjectives
    negativeAdj = {}    #dictionary of negative adjectives
    intensifiers = {}   #dictionary of intensifiers
    #patterns made from pos_tags
    patterns = """
        P: {<DT>?<NN><VBD><RB>?<JJ>(<CC><JJ>)?}
        {<DT>?<NNS><VBD><RB>?<JJ>(<CC><JJ>)?}
        {<DT>?<NN><RB>?<JJ>}
        {<DT>?<NNS><RB>?<JJ>}
        {<RB>?<JJ><NN>}
        {<RB>?<JJ><NNS>}
        """

    def __init__(self, fileList, topic):
        self.fileList = fileList
        self.topic = topic
        semantics = SemanticsParser()
        self.positiveAdj = semantics.getPositives()
        self.negativeAdj = semantics.getNegatives()
        self.intensifiers = semantics.getIntensifiers()

    def calculateAvgRating(self, reviewObj, data_on_ratings):
        ratings = reviewObj['Ratings']
        if 'Service' in ratings.keys():
            data_on_ratings['Service'] += int(ratings['Service'])
        if 'Cleanliness' in ratings.keys():
            data_on_ratings['Cleanliness'] += int(ratings['Cleanliness'])
        if 'Overall' in ratings.keys():
            data_on_ratings['Overall'] += float(ratings['Overall'])
        if 'Value' in ratings.keys():
            data_on_ratings['Value'] += int(ratings['Value'])
        if 'Sleep Quality' in ratings.keys():
            data_on_ratings['Sleep Quality'] += int(ratings['Sleep Quality'])
        if 'Rooms' in ratings.keys():
            data_on_ratings['Rooms'] += int(ratings['Rooms'])
        if 'Location' in ratings.keys():
            data_on_ratings['Location'] += int(ratings['Location'])

        return data_on_ratings

    def calculateTopicRating(self, reviewObj):
        totalscore = 0
        content = reviewObj['Content']
        tokenizedContents = sent_tokenize(content)
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = []
        for tokenContent in tokenizedContents:
            tokens = tokenizer.tokenize(tokenContent)
            if tokens != []:
                pChunker = RegexpParser(self.patterns)
                # identify parts of speech by tagging the tokens
                sentenceTree = pChunker.parse(pos_tag(tokens))

                for subtree in sentenceTree:
                    if isinstance(subtree, Tree):
                        if subtree.label() == 'P': #if subtree matches the pattern
                            wordTagPair = subtree.leaves()

                            if self.topic in [word for (word,tag) in wordTagPair]:
                                individualScore = 0
                                multiplier = 0

                                #calculate the score for each adjective and adverb associated with the topic
                                for (word,tag) in wordTagPair:
                                    if (tag == 'JJ') & (word.lower() in self.positiveAdj.keys()):
                                        individualScore += self.positiveAdj[word.lower()]
                                    elif (tag == 'JJ') & (word.lower() in self.negativeAdj.keys()):
                                        individualScore += (self.negativeAdj[word.lower()] * -1)
                                    elif (tag == 'RB') & (word.lower() in self.intensifiers.keys()):
                                        multiplier = self.intensifiers[word.lower()]
                                totalscore += individualScore * (1 if multiplier == 0 else multiplier)
                                #print wordTagPair, '==>', individualScore * (1 if multiplier == 0 else multiplier)
        return totalscore

    def process(self):
        for fileName in self.fileList:
            qualifiedFileName = 'input/' + fileName
            print 'Processing file: ', fileName

            rootJson = ReviewData(qualifiedFileName)
            totalReviewObjs = rootJson.getReviews()
            totalScore = 0 #total score of topic in reviews
            data_on_ratings=dict((k, 0) for k in Display.data_on_ratings) #additional ratings

            #process each review
            for reviewObj in totalReviewObjs:
                data_on_ratings = self.calculateAvgRating(reviewObj, data_on_ratings)
                totalScore += self.calculateTopicRating(reviewObj)
            data_on_ratings = self.calculate(data_on_ratings, len(totalReviewObjs))

            #create a map of 'hotelID' as key and scores as value
            Display.hotelScore[rootJson.getHotelInfo()['HotelID']] = [int(round(totalScore)), data_on_ratings]

            #create a map of 'hotelID' as key and 'hotelName' as value
            if 'Name' in rootJson.getHotelInfo():
                Display.hotelIDNameMap[rootJson.getHotelInfo()['HotelID']] = rootJson.getHotelInfo()['Name']
            else:
                Display.hotelIDNameMap[rootJson.getHotelInfo()['HotelID']] = 'Hotel Name not available'

    # function to calculate the average of the rating for different parameters
    def calculate(self, data_on_ratings, totalSize):
        data_on_ratings['Service'] /= totalSize
        data_on_ratings['Cleanliness'] /= totalSize
        data_on_ratings['Overall'] /= totalSize
        data_on_ratings['Value'] /= totalSize
        data_on_ratings['Sleep Quality'] /= totalSize
        data_on_ratings['Rooms'] /= totalSize
        data_on_ratings['Location'] /= totalSize
        return data_on_ratings
