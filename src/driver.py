import os

def external_fileI(buffer,matrix,sequence):
    file_nameI = input("Enter the name of file being tested : ")

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","test",file_nameI)

    try:
        with open(file_path,'r') as rfile:
            content = rfile.readline()
            buffer.buffer_size = int(content.strip())

            content = rfile.readline()
            matrix.row, matrix.col = map(int, content.split())

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
                new_score = int(content.strip())
                if len(content) > 0:
                    sequence.add_sequence(new_seq,new_score)

    except FileNotFoundError as fnfe:
        print("File not found or path is incorrect.", fnfe)

    except NotCorrectColumnCountError as nccce:
        print("Error in matrix formatting:", nccce)

    except Exception as e:
        print("An error occurred:", e)

class NotCorrectColumnCountError(Exception):
    def __init__(self, message="Found a line with incorrect column size"):
        self.message = message
        super().__init__(self.message)

class BreachMatrix:
    def __init__(self):
        self.matrix = []
        self.row = 0
        self.col = 0

    def renew_matrix(self):
        matrix = [["00" for _ in range(self.col)] for _ in range(self.row)]

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
        self.sequence_score = []
    
    def add_sequence(self,newseq,newscore):
        self.sequence_list.append(newseq)
        self.sequence_score.append(newscore)

    def score_sum(self):
        return sum(self.sequence_score)

class Buffer:
    def __init__(self) -> None:
        self.buffer_size = 0
        self.buffer_sequence = []
        self.buffer_score = 0

if __name__ == '__main__':
    buffer = Buffer()
    BPmatrix = BreachMatrix()
    sequence = Sequence()

    external_fileI(buffer,BPmatrix,sequence)

    tempbuffer = buffer

    BPmatrix.print_matrix()
    print(sequence.sequence_list)
    print(sequence.sequence_score)