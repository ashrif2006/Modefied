

class Node:
    def __init__(self, data, probability, left=None, right=None):
        self.data = data
        self.probability = probability
        self.left = left
        self.right = right

class ModifiedHuffman:
    def read_file(self,input_path):
        pass
    
    def calculate_frequencies(self, data):
        pass
    
    def calculate_probabilities(self, frequencies , total):
        pass
    
    def apply_min_probability(self, probabilities , min_probability):
        pass
    
    def build_huffman_tree(self, probabilities):
        pass
    
    def generate_codes(self,root):
        pass
    
    def compress(self,input_path, output_path, min_probability):
        pass
    
    def decompress(self,input_path, output_path):
        pass