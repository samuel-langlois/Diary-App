import base64
import math
import struct
import wave
if __name__ == '__main__':
    data_base = 'hello world, this is a test of encoding text into audio using frequency shift keying. We will use two frequencies to represent binary 0 and 1, and generate a WAV file that encodes this message. The resulting audio can be played back and decoded to retrieve the original text message.'
    data_64 = base64.b64encode(data_base.encode('utf-8'))
    print(data_64)
    sample_rate = 8000  # Low sample rate for a retro, buzzy feel; adjust as needed
    audio_data = bytearray()
    for l in data_base:
        byte = ord(l)
        bits = [(byte >> i) & 1 for i in range(8)][::-1]  # Get bits from MSB to LSB
        for bit in bits:
            frequency = 1200 if bit == 1 else 600  # FSK: 1200 Hz for '1', 600 Hz for '0'
            duration = 0.1  # Duration of each bit in seconds
            num_samples = int(sample_rate * duration)
            for j in range(num_samples):
                t = j / sample_rate
                sample = 0.5 * math.sin(2 * math.pi * frequency * t)  # Amplitude scaled to 0.5
                sample_int = int((sample + 1) / 2 * 255)  # Convert to unsigned 8-bit
                audio_data += struct.pack('<B', sample_int)
    # Write to a real file on disk
    with wave.open('text_as_audio.wav', 'wb') as wav:
        wav.setnchannels(1)  # Mono
        wav.setsampwidth(1)  # 8-bit samples
        wav.setframerate(sample_rate)
        wav.writeframes(audio_data)

    print("WAV file created! Play 'text_as_audio.wav' in any audio player.")

    # Optional: If you want the Base64-encoded version of the full WAV (e.g., to share/embed)
    with open('text_as_audio.wav', 'rb') as f:
        wav_bytes = f.read()
    base64_wav = base64.b64encode(wav_bytes).decode('utf-8')
    print("Base64 of WAV:", base64_wav)