import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP

AP -> Adj | Adj AP
PP -> P NP
CP -> Conj | Conj N
NP -> N | CP N | Det N | Det AP N | NP PP
VP -> V | VP Adv | Adv VP | V NP | VP PP | VP CP VP
"""


grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    
    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    
    # Convert sentense to lower case
    sentence = sentence.lower()
    
    # Tokennize the sentence
    list_of_words = nltk.tokenize.word_tokenize(sentence)
    
    # Loop through the list, remove words without at least one alphabetic chracter
    cleaned_list_of_words = [ word for word in list_of_words if containsAlpha(word)]
    
    return cleaned_list_of_words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    list_of_np_chunks = []
   
    for s in tree.subtrees(lambda t: t.label() == "NP"):  # Restrict subtrees with the label NP
        # Check if they contain any NPs in them.
        nps = s.subtrees(lambda t: t.label() == "NP")
        next(nps)  # subtress function also returns the root node. We need to skip it.
        len = sum(1 for _ in nps)  # Since subtree returns a generator, use sum to find the length
        if len == 0:
            list_of_np_chunks.append(s)

    return list_of_np_chunks

def containsAlpha(word):
    """
    Returns true if the word contains at least one alphabet.
    False otherwise.
    """
    return any(char.isalpha() for char in word)

if __name__ == "__main__":
    main()
