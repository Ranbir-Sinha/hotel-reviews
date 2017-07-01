# hotel-reviews

## How to run?
python main.py -f "filenames" -t "topic"

* filenames - number of filenames separated by space

* topic     - topic to be searched

**Example:**
```
$> python main.py -f reviews1.json reviews2.json reviews3.json reviews4.json reviews5.json -t spa
```

## Insight
There is a list of reviews about each hotel. Let's start looking at an example review:
```
This hotel is just minutes away from LAX with a convenient shuttle. The staff was friendly and check-in easy. The room was large and recently renovated with stylish drapes and wallpaper. The flatscreen TV had great reception and good recent movie selections. I did not like the squishiness of the foam top on the mattress, which was adequately firm in its base, nor did I like the lack of choice in pillows. The door to the hallway is not sound-proof so you have to put up with hearing slamming of doors throughout the night. There is a $16.00 charge for parking, but the lot and garage seem very safe in an area that is a little sketchy.
```
As we can see, this is mainly a mixed review about a hotel.

Sometimes we don't want an overall rating of the review but a little more detail. We want the postive/negative sentiments towards some entities. For example,
```
* The staff was friendly and check-in easy.
* I did not like the squishiness of the foam top on the mattress
```

This kind of detailed detection can be quite challenging. An example is the opinion "The staff was friendly", where the (positive) opinion is about the staff, etc.

## Logic
1. Tokenize review contents (sentences)
2. Tokenize words
3. Find the noun (topic) in the sentence (POS tagging)
4. Find the sentiment about that topic (adverb, adjectives)

## Rationale for the logic
In natural languages, a large percentage of word-forms are ambiguous. Some words can represent more than one part of speech at different times and some parts of speech are complex. For example,
```
Fear and "Loathing" in Las Vegas
I was absolutely "loathing" every minute of it.
```
‘loathing’ appears as a gerund in “Fear and Loathing in Las Vegas”, but as a verb in “I was absolutely loathing every minute of it.”
So, POS tags are well suited for identifying and treating differently the different meanings of polysemous words.
