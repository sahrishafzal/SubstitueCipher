# initialize useful variables
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
english_letter_frequencies = {
        'E': 0.127, 'T': 0.091, 'A': 0.082, 'O': 0.075, 'I': 0.070,
        'N': 0.067, 'S': 0.063, 'H': 0.061, 'R': 0.060, 'D': 0.043,
        'L': 0.040, 'C': 0.028, 'U': 0.028, 'M': 0.024, 'W': 0.024,
        'F': 0.022, 'G': 0.020, 'Y': 0.019, 'P': 0.019, 'B': 0.015,
        'V': 0.009, 'K': 0.008, 'J': 0.002, 'X': 0.001, 'Q': 0.001,
        'Z': 0.001
    }

def calculate_letter_frequencies(text):
    # initialize letter counts to all zeros
    letter_freqs = {}
    for char in alphabet:
        letter_freqs[char] = 0
    total_letters = 0

    # count the letters
    for char in text:
        if char in alphabet:
            letter_freqs[char] += 1
            total_letters += 1

    return letter_freqs

def frequency_analysis(ciphertext):
    # get the frequencies of letter in the cipher text
    cipher_freqs = calculate_letter_frequencies(ciphertext)
    cipher_to_plain = {}
    plain_to_cipher = {}

    plain_text = cipher_text # we will incrementally construct plain text from cipher text

    # get the most frequent remaining ciphertext and plain text letters and then swap
    # the most common cipher text letter with the most common plain text letter
    for i in range(26):
        max_english = -1
        max_english_char = ''
        max_cipher = -1
        max_cipher_char = ''
        for char in alphabet:
            if char not in plain_to_cipher and english_letter_frequencies[char] > max_english:
                max_english = english_letter_frequencies[char]
                max_english_char = char
            if char not in cipher_to_plain and cipher_freqs[char] > max_cipher:
                max_cipher = cipher_freqs[char]
                max_cipher_char = char
        cipher_to_plain[max_cipher_char] = max_english_char # map most common letters to each other
        plain_to_cipher[max_english_char] = max_cipher_char # map in reverse for convenience
        plain_text = plain_text.replace(max_cipher_char, max_english_char.lower()) # replace accordingly, use lowercase to prevent overwrite
    return [plain_text.upper(), cipher_to_plain, plain_to_cipher]

inFile = input("Supply path to cipher text: ")
cipher_text = ''
inF = open(inFile, 'r')
for line in inF:
    words = line.split()
    for word in words:
        cipher_text += word + ' '
cipher_text = cipher_text.upper()
[plain_text, cipher_to_plain, plain_to_cipher] = frequency_analysis(cipher_text)
skip = True
response = ''
print("Initial substitution using frequency analysis: ")
while response != '!':
    if not skip:
        cipher_letter = response[0].upper()
        replace_letter = response[1].upper()
        old_replace_letter = cipher_to_plain[cipher_letter] # find the letter previously being mapped to cipher letter
        old_cipher_letter = plain_to_cipher[replace_letter] # find the letter previously being mapped to replace_letter

        # update dictionaries and plain text
        cipher_to_plain[cipher_letter] = replace_letter
        plain_to_cipher[replace_letter] = cipher_letter
        cipher_to_plain[old_cipher_letter] = old_replace_letter
        plain_to_cipher[old_replace_letter] = old_cipher_letter
        plain_text = plain_text.replace(old_replace_letter.upper(), replace_letter.lower()) # use lowercase to prevent overwrite
        plain_text = plain_text.replace(replace_letter.upper(), old_replace_letter.lower()) # use lowercase to prevent overwrite
        plain_text = plain_text.upper()
        print('------------------------------------------------------------------------------------------------------------------')
    print("CT: " + cipher_text, end='\n\n')
    print("PT: " + plain_text)
    response = input("Enter the ciphertext letter followed by the letter you want to swap with (! to end decryption): ")
    skip = False
print("The final mapping from cipher to plain is...")
for cipher_letter in cipher_to_plain:
    print(cipher_letter + '-->' + cipher_to_plain[cipher_letter], end = " ")
print("\nThe final plain text is...")
print(plain_text)
