import xml.etree.ElementTree as ET
from data.data_utils import Dataset

from configuration.config_json import Config
from data.sentiment import SentimentDataset
from data.data_utils import preprocess_word, process_line

INPUT = "resources/sentiment/CorpusTweets_Clean.csv" #"results/tass2019/intertass_all_texts"
OUTPUT = "resources/sentiment/chars100.txt"
TOP=100

def main():

    # Build and save char vocab (it takes into account emojis!)
    with open(INPUT, 'r', encoding='utf8') as f:
        vocab_chars, freq_chars = get_char_vocab(f)
        if TOP == -1:
            write_vocab(vocab_chars, OUTPUT)
        else:
            write_vocab_more_freq(freq_chars, OUTPUT, TOP)

        print("CHARS saved")

    f.close()
    '''
    with open(OUTPUT, 'r', encoding='utf8') as check:
        for line in check:
            print(line)
    '''

def get_char_vocab(file):
    """Build char vocabulary from an iterable of datasets objects
    """
    print("Building CHAR vocab...")
    vocab_char = set()
    freq_char = {}
    for line in file:
        for word in line.strip().split(' '):
            for char in word:
                #word2 = remove_emoji(word)
                if char in freq_char:
                    freq_char[char] += 1
                else:
                    freq_char[char] = 1
                vocab_char.update(char) #update(each character of the word)

    return vocab_char, freq_char


def write_vocab(vocab, filename):
    """Writes a vocab to a file
    Writes one word per line.
    """
    print("Writing vocab...")
    with open(filename, "w", encoding="utf8") as f:
        for i, word in enumerate(vocab):
            if i != len(vocab) - 1:
                f.write("{}\n".format(word))
            else:
                f.write(word)
    f.close()
    print("- done. {} tokens".format(len(vocab)))

def write_vocab_more_freq(freqs, filename, ntop=100):
    """Writes a vocab to a file
    Writes one word per line.
    """
    print("Writing vocab...")
    with open(filename, "w", encoding="utf8") as f:
        for i, word in enumerate(freqs):
            if i < ntop:
                f.write("{}\n".format(word))
            else:
                f.write(word)
                break

    print("- done. {} tokens".format(len(freqs)))


if __name__ == "__main__":
    main()