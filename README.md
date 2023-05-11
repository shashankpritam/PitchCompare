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

```shell

ffmpeg -i input.mp3 -ac 1 -ar 16000 output.wav
```

Run the Python script, providing the paths to your two audio files:

```shell

python pitch.py audio1 audio2
```
The script will output the average pitch difference and average word duration difference between the two speakers.

When interpreting the results, it's important to understand what the two metrics represent:

Average Pitch Difference: This is the average difference in pitch between the two audio files. Pitch in audio can be thought of as how "high" or "low" the sound is. In this case, the value 505.163330078125 means that, on average, the pitch of one speaker is about 505 Hz different from the pitch of the other speaker. A large average pitch difference means that the speakers have very different pitch contours, which could indicate differences in their vocal characteristics or speaking style. However, the interpretation of this value also depends on the context and the specific speakers being compared.

Average Word Duration Difference: This is the average difference in the duration of words between the two audio files. It can be thought of as a measure of how quickly or slowly the speakers talk. The value nan stands for "not a number", which means that the average word duration difference couldn't be calculated for these audio files. This could be due to various reasons, such as one or both of the audio files not containing any recognizable words, or an issue with the transcription or word timing extraction.

Remember that these metrics are just tools to help compare the speech in two audio files. They can provide useful insights, but they may not capture all the nuances of human speech. Therefore, they should be interpreted in conjunction with other information about the speakers and the context of the speech.
