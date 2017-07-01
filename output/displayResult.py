class Display(object):
    #contains the average rating across various parameters
    data_on_ratings = {
        "Service": 0,
        "Cleanliness": 0,
        "Overall": 0,
        "Value": 0,
        "Sleep Quality": 0,
        "Rooms": 0,
        "Location": 0
    }

    hotelScore = {} #dictionary of hotelID and totalscore on a 'topic'
    hotelIDNameMap = {} #dictionary of hotelID and hotelName

    @staticmethod
    def displayAvgRating(data_on_ratings):
        for (key,value) in data_on_ratings.items():
            print key, ': ', value

    @staticmethod
    def getBestHotel():
        maxRating = 0
        bestHotelID = ''
        for (key,value) in Display.hotelScore.items():
            if int(value[0]) > int(maxRating):
                maxRating = int(value[0])
                bestHotelID = key
        return bestHotelID
