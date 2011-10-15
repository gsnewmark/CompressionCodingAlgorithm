 # -*- coding: utf-8 -*-

from math import log, ceil

class LZ78Coding(object):
    """
    Represents lz78 coding algorithm.

    input_string - string to be coded
    """ 
    def __init__(self, input_string):
        super(LZ78Coding, self).__init__()    
        self._input_string = input_string
        self._coded_string = None
        self._codes = None

    def get_input_string(self):
        """Returns current string to encode."""
        return self._input_string

    def set_input_string(self, new_string):
        """Sets current string to encode."""
        self._input_string = new_string
        self._coded_string = None
        self._codes = None

    def get_coded_string(self):
        """Returns encoded string (codes it if needed)."""
        if not self._coded_string:
            self._coded_string, self._codes = \
                    self._encode_string(self._input_string) 
        return self._coded_string 

    def get_codes(self):
        """Returns list of codes for words."""
        if not self._codes:
            self._coded_string, self._codes = \
                    self._encode_string(self._input_string)
        return self._codes

    def _encode_string(self, input_string):
        """Encodes string and returns its code and list of codes."""
        words = self._divide_to_words(input_string)
        words_copy = words[::]
        codes = {'':'0'}
        coded_string = ''
        last_code = 0

        # adding first word to dict and resulting string
        last_code += 1
        codes[words[0]] = self._get_code_from_number(last_code)
        coded_string += words[0]
        words.pop(0)

        # adding rest of words to dict and resulting string
        for word in words:
            if not codes.has_key(word):
                check_word_len = len(word) - 1
                check_word = word[:check_word_len]
                coded_string += (codes[check_word] + word[check_word_len:])
                last_code += 1
                codes.setdefault(word, 
                        self._get_code_from_number(last_code))
                codes = self._add_prefix_zeros_to_code(codes)
            else:
                coded_string += codes[word]
            
        codes_list = self._get_codes_list(words_copy, codes)

        return coded_string, codes_list

    def _divide_to_words(self, input_string):
        """
        Divides string to words.
        Returns list of such words.
        """
        result = []
        working_string = input_string[::]
        word_length = 1
        while working_string:
            word = working_string[:word_length]
            if result.count(word) == 0 or word == working_string:
                result.append(word)
                working_string = working_string[word_length:]
                word_length = 1
            else:
                word_length += 1
        return result

    def _get_code_from_number(self, number):
        return bin(number)[2:]

    def _add_prefix_zeros_to_code(self, codes):
        """Adds prefix zeroz to codes to make their lengths equal."""
        new_codes = {}
        code_length = ceil(log(len(codes), 2.))
        for key in codes.iterkeys():
            new_code = codes[key]
            new_code_len = len(new_code)
            if new_code_len < code_length:
                new_code = '0' * int(code_length - new_code_len) + new_code
            new_codes[key] = new_code
        return new_codes

    def _get_codes_list(self, words_list, codes_dict):
        """
        Returns list of tuples (word, code) with preserved word_list's
        order.
        """
        result = []
        for word in words_list:
            tmp_dict = dict(result)
            if not tmp_dict.has_key(word):
                result.append((word, codes_dict[word]))
        return result

    
if __name__ == '__main__':
    """First argument - string to encode."""
    from sys import argv

    if len(argv) >= 2:
        input_string = argv[1]
    else:
        input_string = '11010000001001'

    coder = LZ78Coding(input_string)
    print coder.get_coded_string()
    print coder.get_codes()


    
