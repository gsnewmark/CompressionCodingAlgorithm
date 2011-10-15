# -*- coding: utf-8 -*-

from decimal import Decimal
from dba import db
from math import log, ceil

class ArithmeticCoding(object):
    """
    Represents arithmetic coding algorithm.

    symbols_probability - dictitonary with letters and their probabilities 
    input_string - string to be coded
    """
    def __init__(self, symbols_probability, input_string=None):
        super(ArithmeticCoding, self).__init__() 
        self._alphabet_distribution = symbols_probability
        self._input_string = input_string
        self._coded_string = None

    def get_alphabet(self):
        """Returns current alphabet."""
        return self._alphabet_distribution.keys()

    def get_alphabet_with_probabilities(self):
        """Returns current alphabet with probabilities of symbols."""
        raise self._alphabet_distribution

    def get_input_string(self):
        """Returns current string to encode."""
        return self._input_string

    def set_input_string(self, new_string):
        """Sets current string to encode."""
        self._input_string = new_string

    def get_coded_string(self):
        """Returns encoded string (codes it if needed)."""
        if not self._coded_string:
            self._coded_string = self._encode_string(self._input_string) 
        return self._coded_string

    def _encode_string(self, input_string):
        """Encodes string and returns it's code."""
        # interval for calculations (initial value)
        current_interval = (Decimal(0.), Decimal(1.))
        for letter in self._input_string:
            current_interval = self._algorithm_step(
                    self._alphabet_distribution,
                    current_interval,
                    letter
                    )
        # point that are used to produce code    
        code_point = (current_interval[1] + current_interval[0]) /Decimal(2)
        # how much symbols in code 
        precision = int(ceil(
                -log(
                    (current_interval[1] - current_interval[0]), 2
                    )
                )) + 1
        #convert to binary, discard first three symbols, slice to precision 
        code = db(code_point)[3:3 + precision]
        return code
            
    def _algorithm_step(self, alphabet, interval, letter):
        """
        Makes one step of algorithm: divides interval and chooses new.
        Returns new interval.

        alphabet - dictionary with keys-symbols and values-probabilities
        interval - tuple of left and right borders of interval   
        letter - letter which interval is to be returned
        """
        letter_intervals = self._divide_interval(alphabet, interval)
        print letter_intervals
        print 
        return letter_intervals[letter]

    def _divide_interval(self, alphabet, interval):
        """
        Divides interval according to letters probabilities.
        Retunrs dictionary with symbols (keys) and respective intervals-
        tuples (values).

        alphabet - dictionary with keys-symbols and values-probabilities
        interval - tuple of left and right borders of interval
        """
        intervals = {}
        # start and end of initial interval
        c = interval[0]
        d = interval[1]
        # for storing start and end of letter's interval
        ci = c
        di = Decimal(0)
        for char in sorted(alphabet):
            di = ci + Decimal(alphabet[char]) * (d - c)
            intervals.setdefault(char, (ci, di))
            ci = di
        return intervals


if __name__ == '__main__':
    alphabet = {
            'a': 0.41,
            'b': 0.23,
            'c': 0.1,
            'd': 0.26,
            }
    initial_string = "acbaa"
    coder = ArithmeticCoding(alphabet, initial_string)
    print coder.get_coded_string()
