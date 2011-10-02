# -*- coding: utf-8 -*- 

from operator import itemgetter

class CodingAlgorithm(object):
    """Descrbes basic interface for coding algorithms."""
    def get_alphabet(self):
        """Return current alphabet."""
        raise NotImplementedError("Should be implemented in child class.")

    def get_alphabet_with_probabilities(self):
        """Return current alphabet with probabilities of symbols."""
        raise NotImplementedError("Should be implemented in child class.")  

    def get_coded_alphabet(self):
        """Returns coded alphabet."""
        raise NotImplementedError("Should be implemented in child class.")

    def get_average_length(self):
        """Return average length of coded alphabet's symbols."""
        raise NotImplementedError("Should be implemented in child class.")
        

class HuffmanCoding(CodingAlgorithm):
    """
    Represents Huffman's compression algorithm for obtaining prefix code.
    """
    def __init__(self, **symbols_probability):
        super(HuffmanCoding, self).__init__() 
        self._alphabet_distribution = symbols_probability
        self._coded_alphabet = None
        self._average_length = None

    def get_alphabet(self):
        return self._alphabet_distribution.keys()

    def get_alphabet_with_probabilities(self):
        return self._alphabet_distribution

    def get_coded_alphabet(self):
        if not self._coded_alphabet:
            self._coded_alphabet = self._code_alphabet()
        return self._coded_alphabet

    def get_average_length(self):
        if not self._average_length:
            self._average_length = self._calculate_average_length()
        return self._average_length

    def _sort_alphabet(self, alphabet):
        """
        Returns alphabet sorted increasingly according to probabilities of
        symbols.
        """
        return sorted(alphabet.iteritems(), key=itemgetter(1))       

    def _code_alphabet(self):
        """Creates compression code for alphabet acording to algorithm."""
        result = {}
        # Sorted alphabet
        tmp_alph = self._sort_alphabet(self._alphabet_distribution)

        while len(tmp_alph) >= 2:
            # Getting symbols with smallest probabilities
            smallest_letter = tmp_alph[0][0] 
            smallest_letter_prob = tmp_alph[0][1]
            second_smallest_letter = tmp_alph[1][0]  
            second_smallest_letter_prob = tmp_alph[1][1]

            # Adding code symbol to code of alphabet's letters
            # according to algorithm
            for letter in smallest_letter:
                result.setdefault(letter, '')
                if smallest_letter_prob > second_smallest_letter_prob or \
                    (smallest_letter < second_smallest_letter and \
                    smallest_letter_prob == second_smallest_letter_prob):
                        result[letter] += '0'
                else:
                    result[letter] += '1'

            for letter in second_smallest_letter:
                result.setdefault(letter, '')
                if smallest_letter_prob > second_smallest_letter_prob or \
                    (smallest_letter < second_smallest_letter and \
                    smallest_letter_prob == second_smallest_letter_prob):
                        result[letter] += '1'
                else:
                    result[letter] += '0'

            # Merging letters
            new_letter = smallest_letter + second_smallest_letter
            total_probability = smallest_letter_prob + \
                    second_smallest_letter_prob

            # Cleaning alphabet from used letters
            tmp_alph.pop(0)
            tmp_alph.pop(0)

            # Adding merged symbol (word, actually)
            tmp_alph.append((new_letter, total_probability))

            # Sorting newly acquired alphabet
            tmp_alph = self._sort_alphabet(dict(tmp_alph))

        # Reversing acquired codes
        for k in result.keys():
            result[k] = result[k][::-1]

        return sorted(result.iteritems())

    def _calculate_average_length(self):
        """Calculates average length of code."""
        coded_dict = dict(self.get_coded_alphabet())
        avr_length = 0
        for letter in coded_dict:
            avr_length += len(coded_dict[letter]) * \
                    self._alphabet_distribution[letter]
        return avr_length


if __name__ == '__main__':
    coder = HuffmanCoding(
            a=1./64, 
            b=1./32, 
            c=3./64, 
            d=1./2, 
            e=3./32, 
            f=3./16, 
            g=1./16, 
            h=1./16,
            )
    print coder.get_coded_alphabet()
    print coder.get_average_length()

