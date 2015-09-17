from random import random

def generate_message(letters, probabilities, length):
    thresholds = [sum(probabilities[:i+1]) for i in range(len(probabilities))]
    symbols = []
    for i in range(length):
        threshold = random()
        symbols.append([letters[i] for i in range(len(letters)) if thresholds[i] >= threshold][0])
    return ''.join(symbols)
