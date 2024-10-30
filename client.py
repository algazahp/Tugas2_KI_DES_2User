import socket

IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

FP = [40, 8, 48, 16, 56, 24, 64, 32,
      39, 7, 47, 15, 55, 23, 63, 31,
      38, 6, 46, 14, 54, 22, 62, 30,
      37, 5, 45, 13, 53, 21, 61, 29,
      36, 4, 44, 12, 52, 20, 60, 28,
      35, 3, 43, 11, 51, 19, 59, 27,
      34, 2, 42, 10, 50, 18, 58, 26,
      33, 1, 41, 9, 49, 17, 57, 25]

E = [32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1]

S_BOXES = [
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
 
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
 
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
 
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
 
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
 
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
 
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
 
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
]

PC1 = [57, 49, 41, 33, 25, 17, 9,
       1, 58, 50, 42, 34, 26, 18,
       10, 2, 59, 51, 43, 35, 27,
       19, 11, 3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15,
       7, 62, 54, 46, 38, 30, 22,
       14, 6, 61, 53, 45, 37, 29,
       21, 13, 5, 28, 20, 12, 4]

PC2 = [14, 17, 11, 24, 1, 5,
       3, 28, 15, 6, 21, 10,
       23, 19, 12, 4, 26, 8,
       16, 7, 27, 20, 13, 2,
       41, 52, 31, 37, 47, 55,
       30, 40, 51, 45, 33, 48,
       44, 49, 39, 56, 34, 53,
       46, 42, 50, 36, 29, 32]

P = [16, 7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25]

SHIFT_TABLE = [1, 1, 2, 2, 2, 2, 2, 2,
               1, 2, 2, 2, 2, 2, 2, 1]

def pad_message(text):
    padding_length = 8 - (len(text) % 8)
    padding = chr(padding_length) * padding_length
    return text + padding

def string_to_binary(text):
    binary = ''
    for char in text:
        binary += format(ord(char), '08b')
    return binary

def binary_to_hex(binary):
    decimal = int(binary, 2)
    hexadecimal = hex(decimal)[2:].upper()
    return hexadecimal.zfill(16)

def hex_to_binary(hex_str):
    binary = bin(int(hex_str, 16))[2:]
    return binary.zfill(64)

def binary_to_string(binary):
    text = ''
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        text += chr(int(byte, 2))
    return text

def permute(k, arr, n):
    permutation = ""
    for i in range(0, n):
        permutation += k[arr[i] - 1]
    return permutation

def shift_left(k, nth_shifts):
    return k[nth_shifts:] + k[:nth_shifts]

def encrypt(plain_text, rkb):
    plain_text = string_to_binary(plain_text)
    
    # Initial Permutation
    plain_text = permute(plain_text, IP, 64)
    
    # Splitting
    left = plain_text[0:32]
    right = plain_text[32:64]
    
    for i in range(0, 16):
        # Expansion D-box
        right_expanded = permute(right, E, 48)
        
        # XOR RoundKey[i] and right_expanded
        xor_x = bin(int(right_expanded, 2) ^ int(rkb[i], 2))[2:].zfill(48)
        
        # S-box
        sbox_str = ""
        for j in range(0, 8):
            row = int(xor_x[j * 6] + xor_x[j * 6 + 5], 2)
            col = int(xor_x[j * 6 + 1:j * 6 + 5], 2)
            val = S_BOXES[j][row][col]
            sbox_str += format(val, '04b')
            
        # Permutation
        sbox_str = permute(sbox_str, P, 32)
        
        # XOR left and sbox_str
        result = bin(int(left, 2) ^ int(sbox_str, 2))[2:].zfill(32)
        left = result
        
        if(i != 15):
            left, right = right, left
            
    # Combination
    combine = left + right
    
    # Final permutation
    cipher_text = permute(combine, FP, 64)
    return binary_to_hex(cipher_text)

def decrypt(cipher_text, rkb):
    # Reverse the round keys for decryption
    rkb_rev = rkb[::-1]
    
    # Convert hex to binary
    cipher_text = hex_to_binary(cipher_text)
    
    # Initial Permutation
    cipher_text = permute(cipher_text, IP, 64)
    
    # Splitting
    left = cipher_text[0:32]
    right = cipher_text[32:64]
    
    for i in range(16):
        # Expansion D-box
        right_expanded = permute(right, E, 48)
        
        # XOR RoundKey[i] and right_expanded
        xor_x = bin(int(right_expanded, 2) ^ int(rkb_rev[i], 2))[2:].zfill(48)
        
        # S-box
        sbox_str = ""
        for j in range(0, 8):
            row = int(xor_x[j * 6] + xor_x[j * 6 + 5], 2)
            col = int(xor_x[j * 6 + 1:j * 6 + 5], 2)
            val = S_BOXES[j][row][col]
            sbox_str += format(val, '04b')
            
        # Permutation
        sbox_str = permute(sbox_str, P, 32)
        
        # XOR left and sbox_str
        result = bin(int(left, 2) ^ int(sbox_str, 2))[2:].zfill(32)
        left = result
        
        if(i != 15):
            left, right = right, left
            
    # Combination
    combine = left + right
    
    # Final permutation
    plain_text = permute(combine, FP, 64)
    return binary_to_string(plain_text)

def generate_keys(key):
    # Key generation
    key = string_to_binary(key)
    
    # PC1 table
    key = permute(key, PC1, 56)
    
    # Splitting
    left = key[0:28]
    right = key[28:56]
    
    rkb = []  # rkb for RoundKeys in binary
    
    for i in range(0, 16):
        # Shifting
        left = shift_left(left, SHIFT_TABLE[i])
        right = shift_left(right, SHIFT_TABLE[i])
        
        # Combining
        combine_str = left + right
        
        # PC2 table
        round_key = permute(combine_str, PC2, 48)
        
        rkb.append(round_key)
        
    return rkb

def main():
    # Socket setup
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 5001))
    
    try:
        # Receive message from server 1
        encrypted_message = client.recv(1024).decode()
        print(f"Pesan Enkripsi dari server 1: {encrypted_message}")

        # Decrypt the received message
        key = "AABB09182736CCDD"  # 64-bit key
        round_keys = generate_keys(bytes.fromhex(key).decode('latin-1'))
        
        decrypted_message = ""
        for i in range(0, len(encrypted_message), 16):
            block = encrypted_message[i:i+16]
            decrypted_block = decrypt(block, round_keys)
            decrypted_message += decrypted_block
        
        # Correctly handling padding
        padding_length = ord(decrypted_message[-1])
        decrypted_message = decrypted_message[:-padding_length]
    
        print(f"Hasil Dekripsi: {decrypted_message}")

        # Prepare to send a response
        message_to_send = input("Masukkan pesan untuk dikirim: ")
        padded_message = pad_message(message_to_send)
        
        # Encrypt response message block by block
        encrypted_response = ""
        for i in range(0, len(padded_message), 8):
            block = padded_message[i:i+8]
            encrypted_block = encrypt(block, round_keys)
            encrypted_response += encrypted_block
        
        print(f"Hasil Enkripsi: {encrypted_response}")
        
        # Send encrypted response back to server 1
        client.send(encrypted_response.encode())
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        client.close()

if __name__ == "__main__":
    main()
