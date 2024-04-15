import json
import os
import random

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

def choose_random_entry():
    #choose random json file by choosing random letter and opening file with that name (which contains list of words beginning with that letter)
    random_letter = letters[random.randrange(26)]
    with open(os.path.join(__location__, f'data/{random_letter}.json'), encoding='cp437') as user_file:
        letter_dict = json.load(user_file)
    #choose random entry in json file and extract word, defintion and part of speech
    random_index = random.randrange(len(letter_dict))
    random_entry = list(letter_dict.items())[random_index]
    word = random_entry[0]
    meanings = random_entry[1]['meanings']
    #if word has multiple meanings, select one at random to use as definition
    if len(meanings) > 1:
        meaning = meanings[random.randrange(len(meanings))]
    else:
        meaning = meanings[0]
    definition = meaning['def']
    part_of_speech = meaning['speech_part']
    #make sure word does not contain spaces or hyphens and is an adjective/ adverb/ noun/ verb (to keep game simple by limiting scope)
    if " " in random_entry[0] or "-" in random_entry[0] or part_of_speech not in ["adjective", "adverb", "noun", "verb"]:
        return choose_random_entry()
    else:
        return word, definition, part_of_speech