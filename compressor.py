# -*- coding: utf-8 -*-

from coding_algorithms import HuffmanCoding

class FileCompressionUtility(object):
    """
    Class that compresses the file using different coding algorithms.

    _filename - name of a file to compress
    """
    def __init__(self, filename):
        self._filename = filename

    def get_filename(self):
        """Getter of a filename."""
        return self._filename

    def set_filename(self, new_filename):
        """Setter of a filename."""
        self._filename = new_filename

    def compress(self):
        """Makes compressed copy of a file."""
        self._write_string(self._compose_compressed_strings(self._filename))

    def _compose_compressed_strings(self, filename):
        """
        Makes list of compressed strings of file's contents.

        filename - name of fileto make compressed string
        """
        with open(filename, 'rb') as file_to_compress:
            strings_list = file_to_compress.readlines() 
            alphabet = self._create_alphabet(strings_list)
            coder = HuffmanCoding(alphabet)
            coded_alphabet = dict(coder.get_coded_alphabet())
            result = self._code_strings(strings_list, coded_alphabet)
            return result

    def _write_string(self, strings_list):
        """
        Writes string to file.

        strings_list - list of strings read from a file
        """
        with open(self._filename.rpartition('.')[0] + '.' + 'ctf', 'wb') \
                as file_to_write:
                    for string in strings_list:
                        file_to_write.write(string)

    def _create_alphabet(self, strings_list):
        """
        Creates alphabet from given list of strings.

        strings_list - list of initial strings   
        """
        letters_count = {}
        quantity_of_letters = 0.
        for string in strings_list:
            for letter in string:
                quantity_of_letters += 1
                letters_count.setdefault(letter, 0)
                letters_count[letter] += 1
        alphabet = {}
        for letter in letters_count.iterkeys():
            alphabet[letter] = letters_count[letter] / quantity_of_letters
        return alphabet

    def _code_strings(self, strings_list, coded_alphabet):
        """
        Codes given strings list with coded alphabet and returns list of
        coded strings.

        strings_list - list of initial strings
        coded_alphabet - dictionary of letters and their codes
        """
        coded_strings_list = []
        for string in strings_list:
            coded_string = ''
            for symbol in string: 
                coded_string += coded_alphabet[symbol]
            coded_strings_list.append(coded_string)
        return coded_strings_list


if __name__ == '__main__':
    compresing_utility = FileCompressionUtility('initial_file.txt')
    compresing_utility.compress()
