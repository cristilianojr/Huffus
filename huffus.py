"""
HUFFUS

This lib working with a huffman codification, to compress and decompress texts.

Author: Cristiliano Junior
Linkedin: https://www.linkedin.com/in/cristilianojr/
Github: https://github.com/cristilianojr


Repository:
Link: https://github.com/cristilianojr/Huffus
"""

class Huffus:
    def __init__(self, text: str) -> None:
        self.text: str = text
        self.compress_data: dict = {
            'tree': [],
            'code': '',
        }

    def count_each_character(self, text: str = None) -> dict[str, int]:
        """
        The function initializes an empty dictionary, iterates through each character in the input 
        string, and increments the count for that character in the dictionary.

        @param text (str): A text in which all its characters will be counted

        Returns:
            A new dictionary with each letter and number of repetitions in text
        """

        dictionary: dict[str, int] = {}

        for char in text:
            #  if the character not in variable dictionary, init the counter with 1
            if not (char in dictionary):
                dictionary[char] = 1
            # Else increase +1
            else:
                dictionary[char] += 1
        
        dictionary = self.sort_dict_tree(dictionary)

        return dictionary


    def sort_dict_tree(self, tree: dict) -> dict:
        """Sorts a dictionary in ascending order based on its values. 

        @param tree (dict): A dictionary to be sorted.

        Returns:
            dict: A new dictionary with the same keys as the input dictionary, sorted in ascending order based on the values.
        """
        return dict(sorted(tree.items(), key=lambda x: x[1]))


    def sort_list_tree(self, tree: list) -> list:
        """Sorts a list of tuples in ascending order based on the second element (value) of each tuple.

        @param list_tree (list): A list of tuples to be sorted.

        Returns:
            list: A new list with the same tuples as the input list, sorted in ascending order based on the second element (value) of each tuple.
        """
        return sorted(tree, key=lambda x: x[1])


    def build_huffman_tree(self, char_freq_dict: dict) -> list:
        """
        Builds a Huffman coding tree from a dictionary of character frequencies.

        @param char_dict (dict): A dictionary containing character frequencies.

        Returns:
            tuple: A tuple representing the root of the Huffman coding tree.
        """

        char_freq_list: list = list(char_freq_dict.items())

        while len(char_freq_list) != 1:
            node_0 = list(char_freq_list.pop(0))

            node_1 = list(char_freq_list.pop(0))

            child_node = [[node_0, node_1], node_0[1] + node_1[1]]

            char_freq_list.append(child_node)

            char_freq_list = self.sort_list_tree(char_freq_list)

        return char_freq_list   
    

    def encode(self, huffman_tree: list, sequence: str = '', code_words: dict = {}) -> str:
        _code_words: dict = code_words
        
        if isinstance(huffman_tree[0], str):
            _code_words[huffman_tree[0]] = sequence
        else:
            left, right = huffman_tree[0]
            _code_words.update(self.encode(left, sequence+'0', _code_words))
            _code_words.update(self.encode(right, sequence+'1', _code_words))

        return _code_words


    def decode(self, huffman_tree: list, code: str) -> str:
        current = huffman_tree[0]
        decoded: str = ''
        for bit in code:
            direction = 0 if bit == '0' else 1
            current = current[0][direction]

            if isinstance(current[0], str):
                decoded += current[0]
                current = huffman_tree[0]

        return decoded


    def get_code(self, code_words: dict, text: str) -> str:
        return ''.join([code_words[char] for char in text])


    def compress(self) -> dict:
        """
        Compresses the contents at `self.text` using Huffman coding and saves the compressed data to a binary.

        Returns:
            A dictionary with compress data
        """
        char_frequency: dict = self.count_each_character(self.text)
        
        tree: list = self.build_huffman_tree(char_frequency)
        self.compress_data['tree'] = tree

        code_words = self.encode(tree[0])
        code = self.get_code(code_words, self.text)
        self.compress_data['code'] = code

        return self.compress_data 
        

    def decompress(self) -> str:
        """
        Decompresses the contents of a binary variable that was previously compressed using
        the `compress` method of this class

        Returns:
            A string with decompressed data
        """
        return self.decode(self.compress_data['tree'], self.compress_data['code'])
