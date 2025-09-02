'''

Group Name: DAN/EXT 28

Group Members:
FATEEN RAHMAN - s387983
HENDRICK DANG - s395598
KEVIN ZHU - s387035
MEHRAAB FERDOUSE - s393148

'''

a = int(input("1st length: "))
b = int(input("2nd length: "))
c = int(input("3rd length: "))

if a + b > c and a + c > b and b + c > a:
    print("Yes, these three lengths can form a triangle.")
else:
    print("NO, these three lengths CANNOT form a triangle.")
