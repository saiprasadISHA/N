def prepare_key(key):
    """Creates a 5x5 matrix using the provided key."""
    key = key.upper().replace('J', 'I')
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    matrix = []
    seen = set()
    
    # Add unique characters from key, then rest of alphabet
    for char in key + alphabet:
        if char not in seen and char.isalpha():
            seen.add(char)
            matrix.append(char)
            
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def find_position(matrix, char):
    """Returns (row, col) of a character in the matrix."""
    for r, row in enumerate(matrix):
        if char in row:
            return r, row.index(char)
    return None

def prepare_text(text, fill='X'):
    """Cleans text and creates digraphs (pairs)."""
    text = text.upper().replace('J', 'I')
    text = "".join(filter(str.isalpha, text))
    prepared = ""
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if (i + 1) < len(text) else fill
        
        if a == b:
            prepared += a + fill
            i += 1
        else:
            prepared += a + b
            i += 2
            
    if len(prepared) % 2 != 0:
        prepared += fill
    return prepared

def playfair_cipher(text, key, decrypt=False):
    """Encrypts or decrypts text using the Playfair algorithm."""
    matrix = prepare_key(key)
    # Only prepare text for encryption; decryption assumes even pairs
    processed_text = prepare_text(text) if not decrypt else text.upper()
    result = ""
    shift = -1 if decrypt else 1
    
    for i in range(0, len(processed_text), 2):
        r1, c1 = find_position(matrix, processed_text[i])
        r2, c2 = find_position(matrix, processed_text[i+1])
        
        if r1 == r2:  # Same row
            result += matrix[r1][(c1 + shift) % 5] + matrix[r2][(c2 + shift) % 5]
        elif c1 == c2:  # Same column
            result += matrix[(r1 + shift) % 5][c1] + matrix[(r2 + shift) % 5][c2]
        else:  # Rectangle rule
            result += matrix[r1][c2] + matrix[r2][c1]
            
    return result

# --- Example Usage ---
user_key = "MONARCHY"
message = "instruments"

cipher_text = playfair_cipher(message, user_key)
plain_text = playfair_cipher(cipher_text, user_key, decrypt=True)

print(f"Key: {user_key}")
print(f"Encrypted: {cipher_text}") # Output: GATLMZCLRQXA
print(f"Decrypted: {plain_text}")  # Output: INSTRUMENTSX
