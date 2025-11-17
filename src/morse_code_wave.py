import base64
import math
import struct
import wave

# Morse code dictionary (uppercase, with common punctuation)
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
    ',': '--..--', '.': '.-.-.-', '?': '..--..', '/': '-..-.', '-': '-....-',
    '(': '-.--.', ')': '-.--.-', ' ': '/'  # Use '/' for word spaces
}

def text_to_morse(text):
    morse = []
    for char in text.upper():
        if char in MORSE_CODE_DICT:
            morse.append(MORSE_CODE_DICT[char])
    return ' '.join(morse)  # Spaces between letter codes, '/' becomes space separator

if __name__ == '__main__':
    data_base = 'hello world, this is a test of encoding text into audio using frequency shift keying. We will use two frequencies to represent binary 0 and 1, and generate a WAV file that encodes this message. The resulting audio can be played back and decoded to retrieve the original text message.'
    morse_code = text_to_morse(data_base)
    print("Morse code:", morse_code)

    sample_rate = 8000
    frequency = 800  # Tone frequency
    dot_duration = 0.1  # Seconds for dot
    dash_duration = 3 * dot_duration
    intra_symbol_duration = dot_duration  # Silence between dots/dashes in a letter
    inter_letter_duration = 3 * dot_duration  # Total silence between letters
    inter_word_duration = 7 * dot_duration  # Total silence between words

    audio_data = bytearray()

    # Split into letters/words
    letters = morse_code.split(' ')
    for i, letter in enumerate(letters):
        if letter == '/':  # Word space
            silence_duration = inter_word_duration
            num_samples = int(sample_rate * silence_duration)
            for _ in range(num_samples):
                audio_data += struct.pack('<B', 128)  # Silence
            continue

        # Symbols in letter
        symbols = list(letter)
        for j, symbol in enumerate(symbols):
            if symbol == '.':
                duration = dot_duration
            elif symbol == '-':
                duration = dash_duration
            else:
                continue

            # Generate tone
            num_samples = int(sample_rate * duration)
            for k in range(num_samples):
                t = k / sample_rate
                sample = 0.5 * math.sin(2 * math.pi * frequency * t)
                sample_int = int((sample + 1) / 2 * 255)
                audio_data += struct.pack('<B', sample_int)

            # Add intra-symbol silence (except after last symbol in letter)
            if j < len(symbols) - 1:
                num_samples_space = int(sample_rate * intra_symbol_duration)
                for _ in range(num_samples_space):
                    audio_data += struct.pack('<B', 128)

        # Add inter-letter silence (except after last letter)
        if i < len(letters) - 1 and letters[i+1] != '/':
            silence_duration = inter_letter_duration - intra_symbol_duration  # Adjust for last symbol's no space
            num_samples = int(sample_rate * silence_duration)
            for _ in range(num_samples):
                audio_data += struct.pack('<B', 128)

    # Write to WAV
    with wave.open('morse_audio.wav', 'wb') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(1)
        wav.setframerate(sample_rate)
        wav.writeframes(audio_data)

    print("WAV file created! Play 'morse_audio.wav'.")

    # Base64 of WAV
    with open('morse_audio.wav', 'rb') as f:
        wav_bytes = f.read()
    base64_wav = base64.b64encode(wav_bytes).decode('utf-8')
    print("Base64 of WAV:", base64_wav)