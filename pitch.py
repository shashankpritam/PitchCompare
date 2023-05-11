import os
import json
import librosa
import numpy as np
from vosk import Model, KaldiRecognizer, SetLogLevel
from datetime import datetime

# Paths to the input audio files
input_file1 = '360SP.wav'
input_file2 = '360SP.wav'

def transcribe_audio(file_path):
    """
    This function takes an audio file path, transcribes the audio using the Vosk library 
    (which uses Kaldi for speech recognition), and returns a list of results.
    """

    SetLogLevel(0)

    # Load the Vosk model, which is trained for English speech recognition
    model = Model("/Users/shashankpritam/Downloads/vosk/vosk-model-en-us-0.42-gigaspeech")
    rec = KaldiRecognizer(model, 16000)

    # Load the audio file using librosa, a library for audio and music analysis
    audio, sr = librosa.load(file_path, sr=16000)
    # Convert the audio to bytes, which can be used by the Vosk recognizer
    audio = np.int16(audio * 32768).tobytes()

    # Transcribe the audio in chunks
    results = []
    for i in range(0, len(audio), 2000):
        if rec.AcceptWaveform(audio[i:i+2000]):
            results.append(json.loads(rec.Result()))

    # Append the final result
    results.append(json.loads(rec.FinalResult()))

    return results

def compare_speakers(file_path1, file_path2):
    """
    This function takes two audio file paths, transcribes them, extracts the pitch contours, 
    and calculates the average pitch difference and average word duration difference.
    """

    # Transcribe both audio files
    transcription1 = transcribe_audio(file_path1)
    transcription2 = transcribe_audio(file_path2)

    # Extract pitch from both audio files
    pitch1 = extract_pitch(file_path1)
    pitch2 = extract_pitch(file_path2)

    # Calculate the average pitch difference
    avg_pitch_difference = np.mean([abs(p1 - p2) for p1, p2 in zip(pitch1, pitch2)])

    # Calculate the average word duration difference
    word_durations1 = [result['result'][0]['end'] - result['result'][0]['start'] for result in transcription1 if 'result' in result and result['result']]
    word_durations2 = [result['result'][0]['end'] - result['result'][0]['start'] for result in transcription2 if 'result' in result and result['result']]

    # We calculate the average word duration difference between the two speakers. 
    # This is done by subtracting the start time of each word from the end time to get the duration for each word. 
    # Then, for each pair of words (one from each speaker), we subtract the duration of the second word from the first, 
    # and calculate the average of these differences. This gives us an indication of the difference in speech rate between the speakers.
    if word_durations1 and word_durations2 and all(np.isfinite(word_durations1)) and all(np.isfinite(word_durations2)):
        avg_duration_difference = np.mean([abs(d1 - d2) for d1, d2 in zip(word_durations1, word_durations2)])
    else:
        # If either of the lists of word durations is empty, or contains any NaN values, 
        # we can't calculate the average duration difference, so we return NaN.
        avg_duration_difference = float('nan')  # Return NaN if average cannot be calculated

    return avg_pitch_difference, avg_duration_difference


def preprocess_audio(input_file, output_file):
    """
    This function takes an input audio file path and an output file path, 
    and uses ffmpeg to convert the audio to a consistent format (single channel, 16kHz sample rate).
    """

    # The command to run ffmpeg
    command = f"ffmpeg -i {input_file} -ac 1 -ar 16000 {output_file}"
    # Run the command
    os.system(command)


# Get the current time for use in the output file names
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

# Preprocess the first audio file
output_file1 = f'preprocessed_{os.path.basename(input_file1).split(".")[0]}_{timestamp}.wav'
preprocess_audio(input_file1, output_file1)

# Preprocess the second audio file
output_file2 = f'preprocessed_{os.path.basename(input_file2).split(".")[0]}_{timestamp}.wav'
preprocess_audio(input_file2, output_file2)

# Compare the speakers in the preprocessed audio files
avg_pitch_difference, avg_duration_difference = compare_speakers(output_file1, output_file2)

# Print the results
print(f'Average pitch difference: {avg_pitch_difference}')
print(f'Average word duration difference: {avg_duration_difference}')
"""
We print the average pitch difference and the average word duration difference. 
These are the main metrics that can be used to compare the prosody of the two speakers.
"""

