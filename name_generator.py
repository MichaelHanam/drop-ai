import string, random

def name_gen(length):
    letters = set(string.ascii_lowercase)
    vowels = ["a","e","i","o","u"]
    h_letters = ["s", "c", "t"]
    for i in vowels:
        letters.remove(i)
    temp_name = ""
    names = []

    for j in range(int(length)):
        if temp_name != "" and temp_name[-1] in h_letters and random.random() > 0.5:
            temp_name += "h"
        elif j % 2 or temp_name != "" and temp_name[-1] == "h":
            temp_name += str(random.choice(vowels))
        else:
            temp_name += str(random.choice(list(letters)))

    return temp_name