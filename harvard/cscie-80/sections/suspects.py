# Three suspects have been brought in for a murder: Albert, George, And William.
# One of the three suspects is the murderer. The other two are innocent. Innocent suspects always tell the truth. 
# Albert, George, and William all say that they are not the murderer.
# Albert additionally says that "William is the murderer"
# William additionally says that "Albert or George is innocent"

from logic import *

AlbertMurderer = Symbol("Albert is the murderer")
GeorgeMurderer = Symbol("George is the murderer")
WilliamMurderer = Symbol("William is the murderer")

Albert = Symbol("Albert is innocent")
George = Symbol("George is innocent")
William = Symbol("William is innocent")

symbols = [Albert, George, William, AlbertMurderer, GeorgeMurderer, WilliamMurderer]

knowledge = And(
    # One of them is murderer
    Biconditional(AlbertMurderer, And(George, William)),
    Biconditional(GeorgeMurderer, And(Albert, William)),
    Biconditional(WilliamMurderer, And(Albert, George)),
    Biconditional(Albert, Not(AlbertMurderer)),
    Biconditional(George, Not(GeorgeMurderer)),
    Biconditional(William, Not(WilliamMurderer)),
    
    Biconditional(Albert, And(WilliamMurderer)),
    Biconditional(William, Or(William, George))
    
)

for symbol in symbols:
    if model_check(knowledge, symbol):
        print(f"    {symbol}")