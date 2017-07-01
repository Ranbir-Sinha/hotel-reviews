import argparse
from algo.nlpalgorithm import ReviewMiner
from output.displayResult import Display

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", nargs='+', required=True)
    parser.add_argument("--topic", "-t", type=str, required=True)
    args = parser.parse_args()
    #args.file contains list of filenames, e.g., [reviews1.json, reviews2.json], etc.
    #args.topic contains the topic to be rated, e.g., room, staff, food, etc.

    #process the files for the "topic" in the reviews
    reviewAlgo = ReviewMiner(args.file, args.topic)
    reviewAlgo.process()

    #display the result - hotel with best rating on "topic" & other statistics
    print 'Best Hotel: ', Display.hotelIDNameMap[Display.getBestHotel()]
    print 'Topic Rating: ', Display.hotelScore[Display.getBestHotel()][0]
    Display.displayAvgRating(Display.hotelScore[Display.getBestHotel()][1])

if __name__ == '__main__':
    #Usage: python main.py -f reviews1.json reviews2.json reviews3.json reviews4.json reviews5.json -t food
    main()
