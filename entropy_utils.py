# -*- coding: utf-8 -*- 

from math import log

def find_information_entropy(*distribution):
    """
    Finds value of entropy according to Shannon for a given distribution.

    *distibution - probability values of some ditribution
    """
    entropy = 0
    for probability in distribution:
        entropy -=  (probability * log(probability, 2.))
    return entropy


if __name__ == '__main__':
    print find_information_entropy(4./11, 4./11, 3./11)
