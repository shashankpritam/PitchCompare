# PitchCompare

# Audio Analysis with FFMPEG, Vosk, and Librosa

This script allows you to compare the average pitch and the speech rate between two speakers in different audio files. 

## Dependencies

- Python 3.7 or higher
- [Librosa](https://librosa.org/doc/main/install.html)
- [Vosk](https://alphacephei.com/vosk/)
- [FFMPEG](https://www.ffmpeg.org/)

You can install the Python dependencies by running:

```shell
pip install librosa vosk
```
Ensure your audio files are in WAV format. If not, you can convert them using FFMPEG:

'''shell
ffmpeg -i input.mp3 -ac 1 -ar 16000 output.wav
'''

Run the Python script, providing the paths to your two audio files:

'''shell
python pitch.py
'''
The script will output the average pitch difference and average word duration difference between the two speakers.
