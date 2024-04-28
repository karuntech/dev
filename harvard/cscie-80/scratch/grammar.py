import nltk

# Print the formatted context-free grammar tree

grammar = nltk.CFG.fromstring("""
        S -> NP V
        NP -> N | A NP
        A -> "small" | "white"
        N -> "cats" | "trees"
        V -> "climb" | "run"
""")

parser = nltk.ChartParser(grammar)

s = input("Sentence: ").split()

try:
    for tree in parser.parse(s):
        tree.pretty_print()
except:
    print("Cannot parse sentence. No parse tree possible")