# this now includes spaces in the alphabet

import string
import numpy as np

class Vigenere:
    
    def __init__(self):
        how_many_chars = 26
        self.alphabet = string.ascii_lowercase
        self.exclude = set(string.punctuation+string.digits+" ")
        self.matrix = np.zeros((how_many_chars,how_many_chars))
        for key_index in xrange(how_many_chars):
            self.matrix[key_index,:] = (np.arange(how_many_chars)+key_index)%how_many_chars
        self.matrix = self.matrix.astype(int)
        
    def decode(self,ciphertext,keyword):
        ciphertext = ''.join(ch for ch in ciphertext if ch not in self.exclude).lower()
        keyword = ''.join(ch for ch in keyword if ch not in self.exclude).lower()
        cipher_length = len(ciphertext)
        keyword_length = len(keyword)
        plain_string = ""
        for i in xrange(cipher_length):
            key_char = keyword[i%keyword_length]
            cipher_char = ciphertext[i]
            key_alphabet_index = self.alphabet.index(key_char)
            cipher_alphabet_index = self.alphabet.index(cipher_char)
            cipher_row = self.matrix[key_alphabet_index,:]
            plain_index = int(np.where(cipher_row==cipher_alphabet_index)[0])
            plain_string += self.alphabet[plain_index]
        return plain_string
        
    def encode(self,plaintext,keyword):
        plaintext = ''.join(ch for ch in plaintext if ch not in self.exclude).lower()
        keyword = keyword.lower()
        plaintext_length = len(plaintext)
        keyword_length = len(keyword)
        ciphertext_string = ""
        for i in xrange(plaintext_length):
            key_index = self.alphabet.index(keyword[i%keyword_length])
            plain_index = self.alphabet.index(plaintext[i])
            ciphertext_string += self.alphabet[self.matrix[key_index,plain_index]]
        return ciphertext_string
