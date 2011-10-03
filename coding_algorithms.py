# -*- coding: utf-8 -*- 

from operator import itemgetter
from math import fabs
from entropy_utils import find_information_entropy

class CodingAlgorithm(object):
    """Describes basic interface for coding algorithms."""
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

    def _sort_alphabet(self, alphabet):
        """
        Returns alphabet sorted increasingly according to probabilities of
        symbols.
        """
        return sorted(alphabet.iteritems(), key=itemgetter(1))  

    def _calculate_average_length(self):
        """Calculates average length of code."""
        coded_dict = dict(self.get_coded_alphabet())
        avr_length = 0
        for letter in coded_dict:
            avr_length += len(coded_dict[letter]) * \
                    self._alphabet_distribution[letter]
        return avr_length  


class FanoCoding(CodingAlgorithm):
    """
    Represents Fano's compression algorithm for obtaining prefix code.

    **symbols_probability - letters with their probabilities
    """
    def __init__(self, **symbols_probability):
        super(FanoCoding, self).__init__() 
        self._alphabet_distribution = symbols_probability
        self._coded_alphabet = None
        self._average_length = None

    def get_alphabet(self):
        return self._alphabet_distribution.keys()

    def get_alphabet_with_probabilities(self):
        return self._alphabet_distribution

    def get_coded_alphabet(self):
        if not self._coded_alphabet:
            res = {}
            self._code_alphabet(res,
                    self._sort_alphabet(self._alphabet_distribution)
                    )
            res = sorted(res.iteritems())
            self._coded_alphabet = res
        return self._coded_alphabet

    def get_average_length(self):
        if not self._average_length:
            self._average_length = self._calculate_average_length()
        return self._average_length 

    def _code_alphabet(self, result, tmp_alph):
        """Creates compression code for alphabet acording to algorithm."""
        left, right = self._coding_step(tmp_alph)
        for letter in left:
            result.setdefault(letter[0], '')
            result[letter[0]] += '1'
        for letter in right:
            result.setdefault(letter[0], '')
            result[letter[0]] += '0'

        if len(left) != 1:
            self._code_alphabet(result, left)
        if len(right) != 1:
            self._code_alphabet(result, right)

    def _coding_step(self, tmp_alph):
        """
        One iteration of Fano's algorithm.
        
        tmp_alph - list of letters sorted according to probabilities
        """
        left_tmp = []
        right_tmp = []
        # Sorted alphabet
        left = []
        right = tmp_alph[::] 
        for i in range(len(tmp_alph)):
            left.append(tmp_alph[i])
            if len(right) != 0:
                right.pop(0)
            left_prob = self._calculate_total_probability(left)
            right_prob = self._calculate_total_probability(right)
            delta = right_prob - left_prob
            if i != (len(tmp_alph) - 1):
                left_tmp = left[::]
                left_tmp.append(tmp_alph[i+1])
                right_tmp = right[::]
                if len(right_tmp) != 0:
                    right_tmp.pop(0)
                left_tmp_p = self._calculate_total_probability(left_tmp)
                right_tmp_p = self._calculate_total_probability(right_tmp) 
                delta_tmp = left_tmp_p - right_tmp_p
                if delta_tmp > 0:
                    if fabs(delta_tmp) > fabs(delta):
                        break
                    else:
                        left = left_tmp[::]
                        right = right_tmp[::] 
                        break
        return left, right

    def _calculate_total_probability(self, list_of_symbols):
        """Returns sum of probabilities of letters in alphabet."""
        sum = 0
        for letter in list_of_symbols:
            sum += self._alphabet_distribution[letter[0]]
        return sum
        

class HuffmanCoding(CodingAlgorithm):
    """
    Represents Huffman's compression algorithm for obtaining prefix code.

    **symbols_probability - letters with their probabilities
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


if __name__ == '__main__':
    eng_alphabet = {}
    
    eng_coder = HuffmanCoding(
            a = 0.08167,
            b = 0.01492,
            c = 0.02782,
            d = 0.04253,
            e = 0.12702,
            f = 0.02228,
            g = 0.02015,
            h = 0.06094,
            i = 0.06966,
            j = 0.00153,
            k = 0.00772,
            l = 0.04025,
            m = 0.02406,
            n = 0.06749,
            o = 0.07507,
            p = 0.01929,
            q = 0.00095,
            r = 0.05987,
            s = 0.06327,
            t = 0.09056,
            u = 0.02758,
            v = 0.00978,
            w = 0.02360,
            x = 0.00150,
            y = 0.01974,
            z = 0.00074,  
            )
    print u'Huffman:'
    print eng_coder.get_coded_alphabet()
    print u'Average length ' + unicode(eng_coder.get_average_length())  

    print
    eng_coder_f = FanoCoding(
            a = 0.08167,
            b = 0.01492,
            c = 0.02782,
            d = 0.04253,
            e = 0.12702,
            f = 0.02228,
            g = 0.02015,
            h = 0.06094,
            i = 0.06966,
            j = 0.00153,
            k = 0.00772,
            l = 0.04025,
            m = 0.02406,
            n = 0.06749,
            o = 0.07507,
            p = 0.01929,
            q = 0.00095,
            r = 0.05987,
            s = 0.06327,
            t = 0.09056,
            u = 0.02758,
            v = 0.00978,
            w = 0.02360,
            x = 0.00150,
            y = 0.01974,
            z = 0.00074,  
            )
    print u'Fano:'
    print eng_coder_f.get_coded_alphabet()
    print u'Average length ' + unicode(eng_coder_f.get_average_length())

    print
    print u'Entropy ' + unicode(find_information_entropy(
        0.08167,
        0.01492,
        0.02782,
        0.04253,
        0.12702,
        0.02228,
        0.02015,
        0.06094,
        0.06966,
        0.00153,
        0.00772,
        0.04025,
        0.02406,
        0.06749,
        0.07507,
        0.01929,
        0.00095,
        0.05987,
        0.06327,
        0.09056,
        0.02758,
        0.00978,
        0.02360,
        0.00150,
        0.01974,
        0.00074,    
       ))   
    """
    coder = HuffmanCoding(
            a=0.35, 
            b=0.17, 
            c=0.16, 
            d=0.16, 
            e=0.16, 
            )
    print u'Huffman:'
    print coder.get_coded_alphabet()
    print u'Average length ' + unicode(coder.get_average_length())
    f_coder = FanoCoding(
            a=0.35, 
            b=0.17, 
            c=0.16, 
            d=0.16, 
            e=0.16, 
            )
    print
    print u'Fano'
    print f_coder.get_coded_alphabet()
    print u'Average length ' + unicode(f_coder.get_average_length())
    print u'Entropy ' + unicode(find_information_entropy(
            0.35, 0.17, 0.16, 0.16, 0.16
            ))
    """

