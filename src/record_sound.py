import wave
import winsound
import os
import math
import struct


def generate_beep(filename: str, frequency: int, duration: float, sample_rate: int, amplitude: float):
    """Generate a beep sound and save it to a WAV file.
    
    Args:
        filename (str): The name of the output WAV file.
        frequency (int): Frequency of the beep in Hz.
        duration (float): Duration of the beep in seconds.
        sample_rate (int): Sample rate in Hz.
        amplitude (float): Amplitude of the beep (0.0 to 1.0).
    """
    # Calculate number of samples
    num_samples = int(sample_rate * duration)
    
    # Generate sine wave data
    audio_data = []
    for i in range(num_samples):
        # Calculate the sine wave value
        t = i / sample_rate
        sample = amplitude * math.sin(2 * math.pi * frequency * t)
        # Convert to 16-bit integer
        sample_int = int(sample * 32767)
        # Pack as 16-bit signed integer
        audio_data.append(struct.pack('<h', sample_int))
    
    # Write to WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(2)  # 2 bytes per sample (16-bit)
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(audio_data))
    
    print(f"Generated beep sound: {filename}")
    print(f"Frequency: {frequency} Hz, Duration: {duration} seconds")



def generate_multiple_beeps(filename, frequencies, duration=0.2, gap=0.1, sample_rate=44100, amplitude=0.5):
    """Generate multiple beep sounds in sequence and save to a WAV file.
    
    Args:
        filename (str): The name of the output WAV file.
        frequencies (list): List of frequencies in Hz.
        duration (float): Duration of each beep in seconds.
        gap (float): Gap between beeps in seconds.
        sample_rate (int): Sample rate in Hz.
        amplitude (float): Amplitude of the beeps (0.0 to 1.0).
    """
    all_audio_data = []
    
    for i, frequency in enumerate(frequencies):
        # Generate beep
        num_samples = int(sample_rate * duration)
        for j in range(num_samples):
            t = j / sample_rate
            sample = amplitude * math.sin(2 * math.pi * frequency * t)
            sample_int = int(sample * 32767)
            all_audio_data.append(struct.pack('<h', sample_int))
        
        # Add gap (silence) between beeps, except after the last beep
        if i < len(frequencies) - 1:
            gap_samples = int(sample_rate * gap)
            for _ in range(gap_samples):
                all_audio_data.append(struct.pack('<h', 0))
    
    # Write to WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(2)  # 2 bytes per sample (16-bit)
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(all_audio_data))
    
    print(f"Generated {len(frequencies)} beep sequence: {filename}")
    print(f"Frequencies: {frequencies} Hz, Duration: {duration} seconds each")

def generate_music_beeps(filename, frequencies, durations, gaps, sample_rate, amplitude):
    """Generate multiple beep sounds in sequence with different durations and gaps and save to a WAV file.
    
        Args:
        filename (str): The name of the output WAV file.
        frequencies (list): List of frequencies in Hz.
        durations (list): List of durations for each beep in seconds.
        gaps (list): List of gaps between beeps in seconds.
        sample_rate (int): Sample rate in Hz.
        amplitude (float): Amplitude of the beeps (0.0 to 1.0).
    """
    all_audio_data = []
    
    for i, frequency in enumerate(frequencies):
        duration = durations[i]
        gap = gaps[i] if i < len(gaps) else 0
        
        # Generate beep
        num_samples = int(sample_rate * duration)
        for j in range(num_samples):
            t = j / sample_rate
            sample = amplitude * math.sin(2 * math.pi * frequency * t)
            sample_int = int(sample * 32767)
            all_audio_data.append(struct.pack('<h', sample_int))
        
        # Add gap (silence) between beeps, except after the last beep
        if i < len(frequencies) - 1:
            gap_samples = int(sample_rate * gap)
            for _ in range(gap_samples):
                all_audio_data.append(struct.pack('<h', 0))
    
    # Write to WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(2)  # 2 bytes per sample (16-bit)
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(all_audio_data))
    
    print(f"Generated music beep sequence: {filename}")
    print(f"Frequencies: {frequencies} Hz, Durations: {durations} seconds each, Gaps: {gaps} seconds each")


if __name__ == "__main__":
    # Generate a beep sound instead of recording from microphone
    
    # Generate a 1000 Hz beep for 0.2 seconds
    # generate_beep(os.path.join(os.getcwd(), "output.wav"), frequency=1000, duration=0.2, sample_rate=44100, amplitude=0.5)
    # remove the 0 frequency parts to make continuous sound

    """generate_multiple_beeps(os.path.join(os.getcwd(), "mario_beeps.wav"), [2637, 2637, 2637, 2093, 2637, 3136, 1568, 2093, 1568, 1318, 1760, 1976, 1865, 
1760, 1568, 2637, 3136, 3520, 2794, 3136, 2637, 2093, 2349, 1976, 2093, 1568, 1318, 1760, 
1976, 1865, 1760, 1568, 2637, 3136, 3520, 2794, 3136, 2637, 2093, 2349, 1976], duration=0.5, gap=0.05, sample_rate=44100, amplitude=0.5)
    """
    frequencies = [2637, 2637, 0, 2637, 0, 2093, 2637, 0, 3136, 0, 0, 0, 1568, 0, 0, 0, 2093, 0, 0, 1568, 0, 0, 1318, 0, 0, 1760, 0, 1976, 0, 1865, 1760, 0, 1568, 2637, 3136, 3520, 0, 2794, 3136, 0, 2637, 0, 2093, 2349, 1976, 0, 0, 2093, 0, 0, 1568, 0, 0, 1318, 0, 0, 1760, 0, 1976, 0, 1865, 1760, 0, 1568, 2637, 3136, 3520, 0, 2794, 3136, 0, 2637, 0, 2093, 2349, 1976, 0, 0]

    durations = [0.085] * len(frequencies)

    gaps = [0.0] * (len(frequencies) - 1)

    sample_rate = 44100

    amplitude = 0.5

    generate_music_beeps('mario_theme.wav', frequencies, durations, gaps, sample_rate, amplitude)
    # generate_multiple_beeps(os.path.join(os.getcwd(), "descending_beeps.wav"), [1800, 1500, 1250, 1000, 750, 500], duration=0.5, gap=0.2, sample_rate=44100, amplitude=0.5)
    
    # You can also generate different types of beeps:
    # generate_beep(os.path.join(os.getcwd(), "beep_high.wav"), frequency=2000, duration=0.1, sample_rate=44100, amplitude=0.5)  # High pitch, short
    # generate_beep(os.path.join(os.getcwd(), "beep_low.wav"), frequency=500, duration=0.5, sample_rate=44100, amplitude=0.5)    # Low pitch, long

    # Or generate multiple beeps in sequence:
    # generate_multiple_beeps(os.path.join(os.getcwd(), "double_beep.wav"), [1000, 1000], duration=0.1, gap=0.05, sample_rate=44100, amplitude=0.5)
    # generate_multiple_beeps(os.path.join(os.getcwd(), "ascending_beeps.wav"), [500, 750, 1000, 1250], duration=0.2, gap=0.1, sample_rate=44100, amplitude=0.5)
'''
[2637, 2637, 2637, 2093, 2637, 3136, 1568, 2093, 1568, 1318, 1760, 1976, 1865, 
1760, 1568, 2637, 3136, 3520, 2794, 3136, 2637, 2093, 2349, 1976, 2093, 1568, 1318, 1760, 
1976, 1865, 1760, 1568, 2637, 3136, 3520, 2794, 3136, 2637, 2093, 2349, 1976, 0]
'''