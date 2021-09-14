import numpy as np

def listify(string):
    string = string.split('\n')

    for i in range(0, len(string)):
        string[i] = list(string[i])

    return string

def getShape(arr):
    return [len(arr), len(arr[0])]
