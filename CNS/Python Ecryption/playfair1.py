def get_matrix(key):
    # Create a 25-character string: key (unique letters) + remaining alphabet
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    s = ""
    for char in (key.upper() + alphabet):
        if char not in s and char != 'J':
            s += char
    return s

def playfair(text, key, mode=1):
    matrix = get_matrix(key)
    text = text.upper().replace('J', 'I').replace(" ", "")
    
    # Simple digraph (pair) creator
    pairs = []
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if (i+1) < len(text) else 'X'
        if a == b:
            pairs.append(a + 'X')
            i += 1
        else:
            pairs.append(a + b)
            i += 2

    result = ""
    for pair in pairs:
        # Find index in the 1D string and convert to (row, col)
        idx1, idx2 = matrix.find(pair[0]), matrix.find(pair[1])
        r1, c1 = idx1 // 5, idx1 % 5
        r2, c2 = idx2 // 5, idx2 % 5

        if r1 == r2:    # Same Row: Shift Right (or Left if mode is -1)
            result += matrix[r1*5 + (c1 + mode) % 5] + matrix[r2*5 + (c2 + mode) % 5]
        elif c1 == c2:  # Same Column: Shift Down (or Up if mode is -1)
            result += matrix[((r1 + mode) % 5)*5 + c1] + matrix[((r2 + mode) % 5)*5 + c2]
        else:           # Rectangle: Swap Columns
            result += matrix[r1*5 + c2] + matrix[r2*5 + c1]
            
    return result

# --- Test ---
my_key = "SECRET"
msg = "HELLO"

enc = playfair(msg, my_key, mode=1)  # Mode 1 to Encrypt
dec = playfair(enc, my_key, mode=-1) # Mode -1 to Decrypt

print(f"Encrypted: {enc}")
print(f"Decrypted: {dec}")