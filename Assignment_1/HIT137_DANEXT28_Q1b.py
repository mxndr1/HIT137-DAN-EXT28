'''

Group Name: DAN/EXT 28

Group Members:
FATEEN RAHMAN - s387983
HENDRICK DANG - s395598
KEVIN ZHU - s387035
MEHRAAB FERDOUSE - s393148

'''

square = int(input("Enter the number: "))
print("* " * square)
for i in range(square - 2):
    print("* " + "  " * (square - 2) + "*")
if square > 1:
    print("* " * square)
