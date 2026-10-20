import json
import math

class Node:
    def __init__(self, data, probability, left=None, right=None):
        self.data = data
        self.probability = probability
        self.left = left
        self.right = right

class ModifiedHuffman:
    #convert file to string
    def read_file(self, input_path):
        with open(input_path, "r", encoding="utf-8") as file:
            return file.read()
    #return a dictionary of frequencies of each symbol in the data
    def calculate_frequencies(self, data):
        frequencies = {}
        for symbol in data:
            if symbol in frequencies:
                frequencies[symbol] += 1
            else:
                frequencies[symbol] = 1
        return frequencies

    def calculate_probabilities(self, frequencies, total):
        probabilities = {}
        for symbol in frequencies:
            probabilities[symbol] = frequencies[symbol] / total
        return probabilities

    def apply_min_probability(self, probabilities, min_probability):
        new_probabilities = {}
        self.others_symbols = []
        for symbol, probability in probabilities.items():
            if probability <= min_probability:
                self.others_symbols.append(symbol)
            else:
                new_probabilities[symbol] = probability

        if self.others_symbols:
            new_probabilities["Others"] = sum(
                probabilities[symbol]
                for symbol in self.others_symbols
            )
        return new_probabilities

    def build_huffman_tree(self, probabilities):
        nodes = []
        for symbol, probability in probabilities.items():
            nodes.append(Node(symbol, probability))

        while len(nodes) > 1:
            nodes.sort(key=lambda node: node.probability)
            
            #for the next operations we take the 2 smallest nodes and combine them into a new parent node and remove this 2 nodes from the list and add the new parent node to the list
            
            left = nodes.pop(0)
            right = nodes.pop(0)
            parent = Node(
                None,
                left.probability + right.probability,
                left,
                right
            )
            nodes.append(parent)

        if nodes:
            return nodes[0] #Root of the tree
        return None

    def generate_codes(self, root):
        codes = {}
        def traverse(node, code):
            if node is None:
                return
            if node.left is None and node.right is None:
                codes[node.data] = code if code else "0"
                return
            traverse(node.left, code + "0")
            traverse(node.right, code + "1")
        traverse(root, "")
        return codes

    def compress(self, input_path, output_path, min_probability):
        data = self.read_file(input_path)
        if not data:
            raise ValueError("Input file is empty.")
        frequencies = self.calculate_frequencies(data)
        probabilities = self.calculate_probabilities(
            frequencies, len(data)
        )
        modified_probabilities = self.apply_min_probability(
            probabilities, min_probability
        )
        root = self.build_huffman_tree(modified_probabilities)
        huffman_codes = self.generate_codes(root)

        # Assign fixed-length original codes to all symbols.
        symbols = sorted(frequencies.keys())
        self.original_code_length = max(
            1, math.ceil(math.log2(len(symbols)))
        )

        self.original_codes = {
            symbol: format(index, f"0{self.original_code_length}b")
            for index, symbol in enumerate(symbols)
        }

        # Encode each symbol.
        bitstream = ""
        for symbol in data:
            if symbol in self.others_symbols:
                bitstream += huffman_codes["Others"]
                bitstream += self.original_codes[symbol]
            else:
                bitstream += huffman_codes[symbol]

        compressed_data = {
            "bitstream": bitstream,
            "huffman_codes": huffman_codes,
            "original_codes": self.original_codes,
            "others_symbols": self.others_symbols,
            "original_code_length": self.original_code_length,
            "original_length": len(data)
        }

        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(compressed_data, file, ensure_ascii=False)

    def decompress(self, input_path, output_path):
        with open(input_path, "r", encoding="utf-8") as file:
            compressed_data = json.load(file)

        bitstream = compressed_data["bitstream"]
        huffman_codes = compressed_data["huffman_codes"]
        original_codes = compressed_data["original_codes"]
        others_symbols = compressed_data["others_symbols"]
        code_length = compressed_data["original_code_length"]
        original_length = compressed_data["original_length"]

        reverse_huffman = {
            code: symbol
            for symbol, code in huffman_codes.items()
        }
        reverse_original = {
            code: symbol
            for symbol, code in original_codes.items()
        }

        result = []
        current_code = ""
        i = 0
        while i < len(bitstream):
            current_code += bitstream[i]
            i += 1

            if current_code in reverse_huffman:
                symbol = reverse_huffman[current_code]

                if symbol == "Others":
                    original_code = bitstream[i:i + code_length]
                    i += code_length
                    result.append(reverse_original[original_code])
                else:
                    result.append(symbol)

                current_code = ""
        if len(result) != original_length:
            raise ValueError("Decompression failed.")
        with open(output_path, "w", encoding="utf-8") as file:
            file.write("".join(result))
            


def main():
    huffman = ModifiedHuffman()
    print("Modified Huffman Compression and Decompression")
    print("1. Compress a file")
    print("2. Decompress a file")
    choice = input("Enter your choice (1 or 2): ").strip()
    if choice =="1":
        input_path = input("Enter the path of the file to compress: ").strip()
        output_path = input("Enter the path to save the compressed file (e.g., compressed.json): ").strip()
        min_probability = float(input("Enter the minimum probability threshold (e.g., 0.05): ").strip())
        try:
            huffman.compress(input_path, output_path, min_probability)
            print(f"File compressed successfully and saved to {output_path}.")
        except Exception as e:
            print(f"Error during compression: {e}")
    elif choice == "2":
        input_path = input("Enter the path of the compressed file: ").strip()
        output_path = input("Enter the path to save the decompressed file: ").strip()
        try:
            huffman.decompress(input_path, output_path)
            print(f"File decompressed successfully and saved to {output_path}.")
        except Exception as e:
            print(f"Error during decompression: {e}")
    else:
        print("Invalid choice. Please enter 1 or 2.")
        main()
if __name__ == "__main__":
    main()                    
        


# huffman = ModifiedHuffman()
# huffman.compress(r"E:\compression Ass\Modefied\Modified-Huffman\input.txt", "compressed.json", 0.05)
# huffman.decompress("compressed.json", "output.txt")            