import os
import random

class NotCorrectColumnCountError(Exception):
    def __init__(self, message="Found a line with incorrect column size"):
        self.message = message
        super().__init__(self.message)

class NotEnoughTokens(Exception):
    def __init__(self, message="Doesn't have enough unique token input"):
        self.message = message
        super().__init__(self.message)

class BreachMatrix:
    def __init__(self):
        self.matrix = []
        self.row = 0
        self.col = 0

    def fill_empty_matrix(self,tokens):
        for i in range(self.row):
            self.matrix.append(random.choices(tokens, k = self.col))

    def append_to_matrix(self,Row):
        self.matrix.append(Row)

    def print_matrix(self):
        for i in range(self.row):
            for j in range(self.col - 1):
                print(self.matrix[i][j], end=" ")
            print(self.matrix[i][self.col - 1], end="\n")
            
class Sequence:
    def __init__(self):
        self.sequence_list = []
        self.sequence_points = []
        self.sequence_number = 0
    
    def add_sequence(self,newseq,newpoints):
        if not newseq in self.sequence_list:
            self.sequence_list.append(newseq)
            self.sequence_points.append(newpoints)
            self.sequence_number += 1

    def automatic_sequences(self,tokens,seq_n,max_length,max_points):
        while self.sequence_number < seq_n:
            token_numbers = random.randint(2,max_length)
            new_seq = random.choices(tokens, k = token_numbers)
            points = random.randint(0,max_points)
            self.add_sequence(new_seq,points)

    def optimal_points(self):
        optimal = 0
        for i in self.sequence_points:
            if i > 0:
                optimal += i
        return optimal

class Buffer:
    def __init__(self) -> None:
        self.buffer_size = 0
        self.buffer_coordinates = []
        self.buffer_sequence = []
        self.buffer_points = 0

def external_fileI(buffer,matrix,sequence):
    file_nameI = input("Enter the name of file being tested : ")

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","test",file_nameI)

    with open(file_path,'r') as rfile:
        content = rfile.readline()
        buffer.buffer_size = int(content.strip())

        content = rfile.readline()
        matrix.col, matrix.row = map(int, content.split())

        for _ in range(matrix.row):
            content = rfile.readline()
            if len(content.split()) != matrix.col:
                    raise NotCorrectColumnCountError
            matrix.append_to_matrix(content.split())

        content = rfile.readline()
        seq_n = int(content.strip())
        for _ in range (seq_n):
            content = rfile.readline()
            new_seq = content.split()
            content = rfile.readline()
            new_points = int(content.strip())
            if len(content) > 0:
                sequence.add_sequence(new_seq,new_points)

def CLI_Input(buffer,matrix,sequence):
    n_token = int(input("Masukkan jumlah token unik: "))
    tokens = list(set(input("Masukkan token unik: ").split()))
    if len(tokens) != n_token:
        raise NotEnoughTokens
    buffer.buffer_size = int(input("Masukkan panjang buffer: "))
    matrix.col, matrix.row = map(int,input("Masukkan ukuran matriks (Kolom Baris): ").split())
    seq_n = int(input("Masukkan jumlah sequence yang mungkin dihasilkan: "))
    max_seq_len = int(input("Masukkan panjang maksimum sequence (Sequence max point = 5 x Max Length): "))  # anggap poin tidak negatif untuk case ini
    max_seq_points = 5 * max_seq_len

    sequence.automatic_sequences(tokens,seq_n,max_seq_len,max_seq_points)

    matrix.fill_empty_matrix(tokens)

def main():
    try:
        buffer = Buffer()
        BPmatrix = BreachMatrix()
        sequence = Sequence()

        # external_fileI(buffer,BPmatrix,sequence)
        CLI_Input(buffer,BPmatrix,sequence)

        tempbuffer = buffer

        BPmatrix.print_matrix()
        print(sequence.sequence_list)
        print(sequence.sequence_points)
    
    except FileNotFoundError as fnfe:
        print("File not found or path is incorrect.", fnfe)

    except NotCorrectColumnCountError as nccce:
        print("Error in matrix formatting:", nccce)

    except NotEnoughTokens as net:
        print("Error in tokenization:", net)

    except Exception as e:
        print("An error occurred:", e)

if __name__ == '__main__':
    main()