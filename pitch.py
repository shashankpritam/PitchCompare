import os
import json
import librosa
import numpy as np
from vosk import Model, KaldiRecognizer, SetLogLevel
from datetime import datetime
import sys

def transcribe_audio(file_path):
    """
    Transcribe speech in an audio file using automatic speech recognition.

    This function uses the Vosk library, which is built on Kaldi, a popular open-source speech recognition toolkit. 

    Args:
        file_path: Path to the audio file.

    Returns:
        List of transcriptions with associated timestamps.
    """
    # Set the verbosity level of Vosk (0 = silent)
    SetLogLevel(0)

    # Load the pre-trained Vosk model for English
    model = Model("/Users/shashankpritam/Downloads/vosk/vosk-model-en-us-0.42-gigaspeech")

    # Create a recognizer with the model and the expected sample rate (16kHz)
    rec = KaldiRecognizer(model, 16000)

    # Load the audio file with librosa, a Python library for audio analysis
    # The audio is resampled to 16kHz to match the recognizer's expected sample rate
    audio, sr = librosa.load(file_path, sr=16000)

    # Convert the audio data to bytes, as expected by the recognizer
    audio = np.int16(audio * 32768).tobytes()

    # Perform the transcription, processing the audio in chunks
    results = []
    for i in range(0, len(audio), 2000):
        if rec.AcceptWaveform(audio[i:i+2000]):
            results.append(json.loads(rec.Result()))

    # Append the final result
    results.append(json.loads(rec.FinalResult()))

    return results


def extract_pitch(file_path):
    """
    Extracts the pitch contour from an audio file.

    This function uses librosa to load the audio file and extract the pitch contour.

    Args:
        file_path: Path to the audio file.

    Returns:
        pitches: A list or array of pitch values.
    """
    # Load the audio file
    audio, sr = librosa.load(file_path, sr=16000)

    # Extract the pitch contour
    pitches, magnitudes = librosa.piptrack(y=audio, sr=sr)

    # Convert the 2D pitch matrix to a 1D pitch array
    pitches = pitches[magnitudes > np.median(magnitudes)]
    
    return pitches



def compare_speakers(file_path1, file_path2):
    """
    Compare the prosody of two speakers based on their pitch contours and speaking rate.

    This function transcribes the speech in two audio files, extracts the pitch contours, and then calculates the average 
    pitch difference and the average word duration difference between the two speakers.

    Args:
        file_path1: Path to the first audio file.
        file_path2: Path to the second audio file.

    Returns:
        The average pitch difference and average word duration difference between the two speakers.
    """
    # Transcribe both audio files
    transcription1 = transcribe_audio(file_path1)
    transcription2 = transcribe_audio(file_path2)

    # Extract pitch from both audio files (NOTE: the `extract_pitch` function is not defined in this script)
    pitch1 = extract_pitch(file_path1)
    pitch2 = extract_pitch(file_path2)

    # Calculate the average difference in pitch between the two speakers
    avg_pitch_difference = np.mean([abs(p1 - p2) for p1, p2 in zip(pitch1, pitch2)])

    # Calculate the average difference in word duration between the two speakers
    word_durations1 = [result['result'][0]['end'] - result['result'][0]['start'] for result in transcription1 if 'result' in result and result['result']]
    word_durations2 = [result['result'][0]['end'] - result['result'][0]['start'] for result in transcription2 if 'result' in result and result['result']]

    if word_durations1 and word_durations2 and all(np.isfinite(word_durations1)) and all(np.isfinite(word_durations2)):
                avg_duration_difference = np.mean([abs(d1 - d2) for d1, d2 in zip(word_durations1, word_durations2)])
    else:
        # If we can't calculate the average duration difference (e.g., if one of the speakers doesn't say anything), 
        # we return NaN (not a number).
        avg_duration_difference = float('nan')

    return avg_pitch_difference, avg_duration_difference


def preprocess_audio(input_file, output_file):
    """
    Preprocess an audio file to ensure consistent format.

    This function uses ffmpeg, a command-line tool for handling multimedia data, 
    to convert the audio to a consistent format (single channel, 16kHz sample rate).

    Args:
        input_file: Path to the input audio file.
        output_file: Path to the output audio file.

    Returns:
        None. The preprocessed audio is saved to the output file.
    """
    # The command to run ffmpeg
    command = f"ffmpeg -i {input_file} -ac 1 -ar 16000 {output_file}"

    # Run the command
    os.system(command)


if __name__ == "__main__":
    # Get the input file paths from the command line
    input_file1 = sys.argv[1]
    input_file2 = sys.argv[2]

    # Create unique output filenames based on the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_file1 = f'preprocessed_{os.path.basename(input_file1).split(".")[0]}_{timestamp}.wav'
    output_file2 = f'preprocessed_{os.path.basename(input_file2).split(".")[0]}_{timestamp}.wav'

    # Preprocess the audio files
    preprocess_audio(input_file1, output_file1)
    preprocess_audio(input_file2, output_file2)

    # Compare the speakers in the preprocessed audio files
    avg_pitch_difference, avg_duration_difference = compare_speakers(output_file1, output_file2)

    # Print the results
    print(f'Average pitch difference: {avg_pitch_difference}')
    print(f'Average word duration difference: {avg_duration_difference}')

