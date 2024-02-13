import os
import random
from time import time

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

    def most_points(self):
        optimal = 0
        for i in self.sequence_points:
            if i > 0:
                optimal += i
        return optimal
    
    def print_sequence(self):
        for i in range(self.sequence_number):
            for cseq in self.sequence_list[i]:
                print(cseq, end=" ")
            print(":",self.sequence_points[i],"points")

class Buffer:
    def __init__(self) -> None:
        self.buffer_size = 0
        self.buffer_coordinates = []
        self.buffer_sequence = []
        self.buffer_points = 0
        self.buffer_used = 0

    def append_el(self,el,iRow,iCol):
        self.buffer_coordinates.append((iRow,iCol))
        self.buffer_sequence.append(el)
        self.buffer_used += 1

    def pop_last(self):
        self.buffer_coordinates.pop()
        self.buffer_sequence.pop()
        if self.buffer_used > 0:
            self.buffer_used -= 1

    def print_buffer(self):
        for token in self.buffer_sequence:
            print(token, end=" ")
        print(":",self.buffer_points,"points")
        print("Coordinates")
        for coord in self.buffer_coordinates:
            print(f"({coord[1] + 1}, {coord[0] + 1})")

def external_fileI(buffer,matrix,sequence):
    file_name = input("Enter the name of file being tested : ")

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","test",file_name)

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

def savingfile(buffer,searchtime):
    file_name = input("Tolong beri nama file output (Akan disimpan dalam ekstensi .txt) : ") + ".txt"
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","test",file_name)

    if os.path.exists(file_path):
        print("Sudah ada file dengan nama tersebut, apakah ingin ditimpa? (y/n)")
        selection = input("> ")
        while selection != "y" and selection != "Y" and selection != "n" and selection != "N":
            selection = input("> ")
        if selection == "n" or selection == "N":
            savingfile(buffer,searchtime)
        else:
            print("Menimpa file . . .")
            writeoutput(buffer,searchtime,file_path)
    else:
        print("Menyimpan file . . .")
        writeoutput(buffer,searchtime,file_path)

def writeoutput(buffer,searchtime,filepath):
    with open(filepath,'w') as wfile:
        line = str(buffer.buffer_points) + "\n"
        wfile.write(line)

        line = ""
        for i in range(buffer.buffer_used):
            line = line + buffer.buffer_sequence[i]
            if i < buffer.buffer_used - 1:
                line = line + " "
            else:
                line = line + "\n"
        wfile.write(line)

        for i in range(buffer.buffer_used):
            line = str(buffer.buffer_coordinates[i][1] + 1) + ", " + str(buffer.buffer_coordinates[i][0] + 1) + "\n"
            wfile.write(line)

        line = "\n" + str(searchtime) + " ms"
        wfile.write(line)

def breachprotocol(buffer, matrix, sequence, iRow, iCol, optimalBuffer):
    breachMatrix = matrix.matrix
    if not (iRow,iCol) in buffer.buffer_coordinates:
        buffer.append_el(breachMatrix[iRow][iCol],iRow,iCol)

    loop = 0

    newRow = (iRow + buffer.buffer_used % 2) % matrix.row
    newCol = (iCol + (buffer.buffer_used + 1) % 2) % matrix.col

    while buffer.buffer_used < buffer.buffer_size and (newRow != iRow or newCol != iCol):
        if not (newRow,newCol) in buffer.buffer_coordinates:
            breachprotocol(buffer, matrix, sequence, newRow, newCol, optimalBuffer)
            loop += 1

        newRow = (newRow + buffer.buffer_used % 2) % matrix.row
        newCol = (newCol + (buffer.buffer_used + 1) % 2) % matrix.col

    if loop == 0:
        sequence_search(buffer, sequence, optimalBuffer)
    
    buffer.pop_last()

def sequence_search(buffer, sequence, optimalBuffer):
    checked_sequence = buffer.buffer_sequence
    compared_sequences = sequence.sequence_list
    point_distribution = sequence.sequence_points

    total_points = 0
    used_size = 0

    buf_len = len(checked_sequence)
    seq_n = sequence.sequence_number

    for i in range(seq_n):
        seqt_len = len(compared_sequences[i])

        j = 0
        while j + seqt_len <= buf_len and checked_sequence[j : j + seqt_len] != compared_sequences[i]:
             j += 1
        if j + seqt_len <= buf_len:
            total_points += point_distribution[i]
            if used_size < j + seqt_len:
                used_size = j + seqt_len
    
    if total_points > optimalBuffer.buffer_points or (total_points == optimalBuffer.buffer_points and used_size < optimalBuffer.buffer_used):
        optimalBuffer.buffer_sequence = checked_sequence[:used_size]
        optimalBuffer.buffer_coordinates = buffer.buffer_coordinates[:used_size]
        optimalBuffer.buffer_points = total_points
        optimalBuffer.buffer_used = used_size

def main():
    try:
        buffer = Buffer()
        optimal_buffer = Buffer()
        BPmatrix = BreachMatrix()
        sequence = Sequence()

        print("===================== Input Methods =====================")
        print("| 1. Input from command line                            |")
        print("| 2. Input from file in test folder                     |")
        print("=========================================================\n")

        selection = int(input("> Choose the Input method : "))

        while selection != 1 and selection != 2:
            selection = int(input("> Select a valid number! : "))

        print()
        if selection == 1:
            CLI_Input(buffer,BPmatrix,sequence)
        else:
            external_fileI(buffer,BPmatrix,sequence)

        optimal_buffer.buffer_size = buffer.buffer_size

        starttime = time()

        for i in range(BPmatrix.col):
            breachprotocol(buffer, BPmatrix, sequence, 0, i, optimal_buffer)


        endtime = time()

        time_used = round((endtime - starttime) * 1000)

        print("Below is the matrix!")
        BPmatrix.print_matrix()

        print("\nBelow are the sequences!")
        sequence.print_sequence()

        print("\nBelow is the most optimal buffer found!")
        optimal_buffer.print_buffer()

        print()
        print(time_used, "ms")
        print()

        print("Apakah ingin menyimpan solusi? (y/n)")
        selection = input("> ")

        while selection != "y" and selection != "Y" and selection != "n" and selection != "N":
            selection = input("> ")

        if selection == "Y" or selection == "y":
            savingfile(optimal_buffer,time_used)

    
    except FileNotFoundError as fnfe:
        print("File not found or path is incorrect.", fnfe)

    except NotCorrectColumnCountError as nccce:
        print("Error in matrix formatting:", nccce)

    except NotEnoughTokens as net:
        print("Error in tokenization:", net)

    except Exception as e:
        print("An error occurred:", e)

    print("\nExitting program . . .")

if __name__ == '__main__':
    main()