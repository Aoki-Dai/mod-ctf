
MORSE_CODE_DICT = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z', '-----': '0', '.----': '1', '..---': '2',
    '...--': '3', '....-': '4', '.....': '5', '-....': '6',
    '--...': '7', '---..': '8', '----.': '9',
    '.-.-.-': '.', '--..--': ',', '..--..': '?', '.----.': "'",
    '-.-.--': '!', '-..-.': '/', '-.--.': '(', '-.--.-': ')',
    '.-...': '&', '---...': ':', '-.-.-.': ';', '-...-': '=',
    '.-.-.': '+', '-....-': '-', '..--.-': '_', '.-..-.': '"',
    '...-..-': '$', '.--.-.': '@'
}

def parse_history(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    on_intervals = []
    
    current_on_start = None
    
    for line in lines:
        parts = line.strip().split(',')
        if len(parts) != 2:
            continue
        state = parts[0]
        timestamp = float(parts[1])
        
        if state == 'ON':
            current_on_start = timestamp
        elif state == 'OFF' and current_on_start is not None:
            duration = timestamp - current_on_start
            on_intervals.append({
                'start': current_on_start,
                'end': timestamp,
                'duration': duration
            })
            current_on_start = None
            
    return on_intervals

def decode_morse(intervals):
    morse_chars = []
    current_char = ""
    
    last_end = 0
    
    for interval in intervals:
        gap = interval['start'] - last_end
        
        # Intra-char gap is ~0.3, Inter-char is ~0.9, Word is > 1.5 (maybe)
        # Check gap
        if gap > 1.5:
             # Word separator
             if current_char:
                 morse_chars.append(current_char)
                 current_char = ""
             morse_chars.append(" ") # Space
        elif gap > 0.6:
            # New character
            if current_char:
                morse_chars.append(current_char)
                current_char = ""
        
        # Dot or Dash
        if interval['duration'] < 0.6:
            current_char += "."
        else:
            current_char += "-"
            
        last_end = interval['end']
        
    if current_char:
        morse_chars.append(current_char)
        
    print("Extracted Morse:", morse_chars)
    
    decoded_message = ""
    for code in morse_chars:
        if code == " ":
            decoded_message += " "
        elif code in MORSE_CODE_DICT:
            decoded_message += MORSE_CODE_DICT[code]
        else:
            decoded_message += "?"
            
    return decoded_message

if __name__ == "__main__":
    intervals = parse_history('history.txt')
    msg = decode_morse(intervals)
    print("Decoded Message:", msg)
