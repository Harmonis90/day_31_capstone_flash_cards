import pandas
import random

word_df = pandas.read_csv("./data/french_words.csv").to_dict(orient="records")

def get_random_word_pair():
    return random.choice(word_df)


