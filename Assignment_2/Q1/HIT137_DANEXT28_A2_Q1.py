'''

Group Name: DAN/EXT 28

Group Members:
FATEEN RAHMAN - s387983
HENDRICK DANG (VAN HOI DANG)- s395598
KEVIN ZHU (JIAWEI ZHU) - s387035
MEHRAAB FERDOUSE - s393148

'''

import os



# A dictionary to store keys in the format x# where x is the encrypted character and # is the nth time it appears, and the value which is the original character
encryption_map = {}  
# A dictionary that stores the encrypted character as the key, and the nth time it appears as the value (as multiple characters can have the same encrypted character)
encrypted_counts = {}  
# A dictionary that stores the character to be decrypted as the key, and the nth time it appears as the value
decrypted_counts = {}

# A global variable that stores the path to raw_text.txt
raw_path = None



def find_raw_text():
    """
    Finds the path of raw_text.txt
    """
    
    global raw_path
    
    base_dir = os.getcwd()
    for root, dirs, files in os.walk(base_dir):
        if 'raw_text.txt' in files:
            # Assigns the full path of raw_text.txt to the global variable
            raw_path = os.path.join(root, 'raw_text.txt')
            break
    if raw_path is None:
        # Raises an error if raw_text.txt is not found
        raise FileNotFoundError("raw_text.txt not found in the current directory tree.")



def shift_input():
    """
    Prompts the user for two shift values between 1 and 9
    This ensures that the encrypted characters are not out of the specified ASCII range
    """
    
    # While the user does not enter a valid integer between 1 and 9, the program will keep asking for shift1
    while True:
        try:
            shift1 = int(input("Enter the shift value (1-9): "))
            if 1 <= shift1 <= 9:
                break
            else:
                print("Shift value must be between 1 and 9")
        except ValueError:
            print("Please enter a valid integer.")

    # While the user does not enter a valid integer between 1 and 9, the program will keep asking for shift2
    while True:
        try:
            shift2 = int(input("Enter the second shift value (1-9): "))
            if 1 <= shift2 <= 9:
                break
            else:
                print("Second shift value must be between 1 and 9")
        except ValueError:
            print("Please enter a valid integer.")
            
    # Returns the two shift values
    return shift1, shift2



def encrypt_char(char, shift1, shift2):
    """
    Encrypts a single character using the specified shift values.
    Encrypted_counts keeps track of how many times each encrypted character has appeared.
    Encryption_map stores the encrypted characters along with a count suffix as the key and their corresponding original characters as the value.
    """
    
    # Calculates the encrypted character based on the ASCII value and the shift values
    o = ord(char)
    if 'a' <= char <= 'm':        
        encrypted_char = chr(o + (shift1*shift2))
    elif 'n' <= char <= 'z':      
        encrypted_char = chr(o - (shift1+shift2))
    elif 'A' <= char <= 'M':      
        encrypted_char = chr(o - shift1)
    elif 'N' <= char <= 'Z':      
        encrypted_char = chr(o + (shift2**2))
    else:
        encrypted_char = char

    # Assigns a value to count for the amount of times a character is encrypted to a specific encrypted character
    count = encrypted_counts.get(encrypted_char, 0) + 1
    # Adds the encrypted character into the encrypted_counts dictionary and the amount of times it has appeared as the value
    encrypted_counts[encrypted_char] = count

    # Creates a key for encryption_map in the format x# where x is the encrypted character and # is the nth time it appears
    key = f"{encrypted_char}{count}"
    # Adds the key created as the key in the dictionary and the original character as the value
    encryption_map[key] = char

    # Returns the encrypted character
    return encrypted_char



def encrypt(shift1, shift2, output_folder):
    """
    Reads raw_text.txt, uses the encrypt_char function to encrypt each character
    and writes the encrypted text to encrypted_text.txt in the same folder as raw_text.txt
    """
    
    # Path for the encrypted file is set in the same folder as raw_text.txt
    encrypted_file_path = os.path.join(output_folder, 'encrypted_text.txt')
    
    # raw_text.txt is opened for reading, and encrypted_text.txt is created for writing
    with open(raw_path, 'r', encoding='utf-8') as file:
        with open(encrypted_file_path, 'w', encoding='utf-8') as encrypted_file:
            raw_text = file.read()
            # For each character in the raw text, encrypt it using the encrypt_char function
            # and write the encrypted characters to the encrypted file to form the encrypted text
            for char in raw_text:
                encrypted_file.write(encrypt_char(char, shift1, shift2))
    
    # Returns the path to the encrypted file
    return encrypted_file_path



def decrypt(encryption_map, output_folder):
    """
    Reads encrypted_text.txt, uses the encryption_map to decrypt each character
    and writes the decrypted text to decrypted_text.txt in the same folder as raw_text.txt
    """
    
    # Paths for the encrypted and decrypted files are located
    encrypted_file_path = os.path.join(output_folder, 'encrypted_text.txt')
    decrypted_file_path = os.path.join(output_folder, 'decrypted_text.txt')
    
    # encrypted_text.txt is opened for reading, and decrypted_text.txt is created for writing
    with open(encrypted_file_path, 'r', encoding='utf-8') as encrypted_file:
        with open(decrypted_file_path, 'w', encoding='utf-8') as decrypted_file:
            # For each character in the encrypted text, check if it exists in the encryption_map
            for char in encrypted_file.read():
                # Assigns a value to count for the amount of times a character is to be decrypted to a specific encrypted character
                count = decrypted_counts.get(char, 0) + 1
                # Adds the character to be decrypted into the decrypted_counts dictionary and the amount of times it has appeared as the value
                # ***IF ENCRYPTION AND DECRYPTION ARE PERFORMED CORRECTLY, decrypted_counts AND encrypted_counts SHOULD BE IDENTICAL***
                decrypted_counts[char] = count
                
                # Creates a key in the format x# where x is the character to be decrypted and # is the nth time it appears
                key = f"{char}{count}"
                # Searches for the key inside encryption_map, and if found, writes the corresponding value to the decrypted file
                decrypted_file.write(encryption_map.get(key, char))
    
    # Returns the path to the decrypted file
    return decrypted_file_path



def verify_decryption(output_folder):
    """
    Verifies that the decryption was successful by comparing the decrypted text with the original raw text
    """
    
    # Path for the decrypted file
    decrypted_file_path = os.path.join(output_folder, 'decrypted_text.txt')
    
    # Opens both the raw text and decrypted text files for comparison
    with open(raw_path, 'r', encoding='utf-8') as raw_file:
        with open(decrypted_file_path, 'r', encoding='utf-8') as decrypted_file:
            raw_lines = raw_file.readlines()
            decrypted_lines = decrypted_file.readlines()            
            # Compares each line using an index
            for x in range(len(raw_lines)):
                if x >= len(decrypted_lines) or raw_lines[x] != decrypted_lines[x]:
                    # Returns False if any line does not match
                    return False
    # Returns True if all lines match
    return True



def main():
    """
    The main function that handles the encryption and decryption process
    """
    
    # Finds raw_text.txt dynamically
    find_raw_text()
    
    # Determines the folder containing raw_text.txt so all output files are saved there
    output_folder = os.path.dirname(raw_path)

    # Prompts the user for two shift values
    shift1, shift2 = shift_input()
    
    # Calls the encrypt function with the shift values to encrypt the text and save it to a file
    encrypt(shift1, shift2, output_folder)
    
    # Calls the decrypt function with the encryption_map to decrypt the text and save it to a file
    decrypt(encryption_map, output_folder)

    # Verifies that the decrypted file and the raw text file are similar
    if verify_decryption(output_folder):
        print("Decryption successful! The decrypted text matches the original raw text.")
    else:
        print("Decryption failed! The decrypted text does not match the original raw text.")


if __name__ == "__main__":
    main()
