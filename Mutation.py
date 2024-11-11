# A series of mutation operations.Be aware that the functions are still very much unfinished
# and should be used only for testing. - Mitch
from random import randrange, shuffle
import numpy as np


def TwoRandNum(size: int):
    """
    Returns two ints between 0 and size where a!=b
    """
    a = randrange(size)
    b = randrange(size)

    while (a == b):
        b = randrange(size)

    return a, b

# Selects two points in list and moves second next to first


def Insert(listin):
    listin = list(listin)
    if len(listin) < 2:
        return np.array(listin)

    a, b = TwoRandNum(len(listin))

    if a < b:
        temp = listin[b]
        listin[a+2:b+1] = listin[a+1:b]
        listin[a+1] = temp
    else:
        temp = listin[b]
        listin[b:a-1] = listin[b+1:a]
        listin[a-1] = temp

    return np.array(listin)


def Swap(listin: list) -> list:
    """
    Selects two points in list and swaps elements
    """

    a, b = TwoRandNum(len(listin))

    temp = listin[a]
    listin[a] = listin[b]
    listin[b] = temp

    return np.array(listin)

# Selects two points in list and inverts subsection


def Inversion(listin):
    listin = list(listin)
    if len(listin) < 2:
        return np.array(listin)

    a = randrange(len(listin))
    b = randrange(len(listin))

    while (a == b):
        b = randrange(len(listin))

    if (a < b):
        listin[a:b] = reversed(listin[a:b])
    else:
        listin[b:a] = reversed(listin[b:a])

    return np.array(listin)


def Scramble(listin: list) -> list:
    """
    Selects two points in list and randomizes subsection
    """

    a, b = TwoRandNum(len(listin))

    if (a < b):
        temp = listin[a:b]
        shuffle(temp)
        listin[a:b] = temp
    else:
        temp = listin[b:a]
        shuffle(temp)
        listin[b:a] = temp

    return np.array(listin)
