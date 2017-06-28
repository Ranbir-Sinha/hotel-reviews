import json

class ReviewData:
    reviewObj = {}
    hotelinfo = {}
    reviews = {}

    def __init__(self, filename):
        with open(filename) as data_file:    
            self.reviewObj = json.load(data_file)

        self.hotelinfo = self.reviewObj['HotelInfo']
        self.reviews = self.reviewObj['Reviews']

    def getHotelInfo(self):
        return self.hotelinfo

    def getReviews(self):
        return self.reviews
