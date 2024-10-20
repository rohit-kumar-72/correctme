### correctMe: Video Processing with Automatic Speech Transcription, Grammar Correction, and Audio Replacement

This Python script processes a video by splitting it into segments, transcribing the audio, correcting grammatical errors using the OpenAI API, generating new audio using Google Text-to-Speech (GTTS), and replacing the original audio in the video with the corrected audio. Finally, it reassembles the processed video segments into a single output video file.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Requirements](#requirements)
- [Folder Structure](#folder-structure)
- [Step-by-Step Process](#step-by-step-process)
- [Usage Instructions](#usage-instructions)
- [API Information](#api-information)
- [Known Limitations](#known-limitations)

---

## Project Overview

This script performs the following tasks:
1. Splits the input video into smaller segments.
2. Extracts audio from each segment.
3. Transcribes the audio using Google Speech Recognition.
4. Corrects grammatical errors in the transcription using Azure OpenAI API (GPT-4).
5. Generates a corrected audio file using Google Text-to-Speech (gTTS).
6. Replaces the original audio in the video segment with the corrected audio.
7. Combines all processed segments back into a single video.

---

## Requirements

The project requires the following Python packages:

- `moviepy` for video and audio manipulation.
- `speech_recognition` for audio transcription using Google Speech API.
- `gtts` for generating text-to-speech audio files.
- `requests` for making API calls to Azure OpenAI for grammar correction.
- `pydub` for audio file manipulation (optional).
- `os` and `time` for file and system handling.
- `streamlit` for creating the web application interface.

You can install all the dependencies using the following command:

```bash
pip install moviepy speechrecognition gtts pydub requests python-dotenv streamlit
```

You will also need:
- An **Azure OpenAI API Key** and **Endpoint** for grammar correction using GPT-4.
- A **Google Speech Recognition API** for transcribing the audio (no extra API key required for the Google Speech API, as `speech_recognition` uses a free version).

---

## Folder Structure

The script creates two directories to store intermediate and final files:
- `test_video/`: Stores the video segments that are split from the input video.
- `test_audio/`: Stores audio files extracted from video segments and the generated corrected audio files.

![folder structure](image.png)

---

## Step-by-Step Process

1. **Splitting the Video**:  
   The video is split into segments, each 5 seconds long (or another length as specified). These are saved as separate MP4 files.

2. **Processing Each Segment**:  
   - Extract the audio from the video segment and convert it to WAV format.
   - Transcribe the audio using Google Speech Recognition.
   - Correct the transcription by sending it to Azure OpenAI's GPT-4 API to remove grammatical errors.
   - Generate a new corrected audio file using Google Text-to-Speech.
   - Replace the original segment's audio with the corrected audio.

3. **Combining Segments**:  
   Once all segments are processed, they are concatenated back together to create a final output video.

---

## Usage Instructions

1. **Set Up API Keys**:
   You need to set your Azure OpenAI API key and endpoint in the script:
   
   ```python
   azure_openai_key = 'your-azure-openai-key'
   azure_openai_endpoint = 'your-azure-openai-endpoint'
   ```

2. **Run the Script with Streamlit**:
   To launch the Streamlit application, run the following command in your terminal:
   
   ```bash
   streamlit run main.py
   ```

   Ensure that the video file you want to process is uploaded through the web interface provided by Streamlit.

3. **Updating Libraries**:
   If you need to update your libraries to the latest versions, you can use the following command:

   ```bash
   pip install --upgrade moviepy speechrecognition gtts pydub requests python-dotenv streamlit
   ```

4. **Output**:
   The processed video will be saved as `final_video.mp4` in the current working directory.

---

## API Information

- **Azure OpenAI API**: Used for correcting grammatical errors in the transcription.
- **Google Speech Recognition**: Used for transcribing audio to text.
- **Google Text-to-Speech (gTTS)**: Used for converting corrected text back into audio.

You can increase your rate limit for Azure OpenAI by following the instructions here: [Azure OpenAI Quota Increase](https://aka.ms/oai/quotaincrease).

---

## Known Limitations

1. **API Rate Limits**:
   - You may run into rate limits if you process long videos with frequent API calls, especially if using a lower-tier plan for Azure OpenAI. A retry mechanism can be implemented to handle this.
   
2. **Audio Sync**:
   - Since the new audio is generated based on corrected text, there might be slight desynchronization with the video if the timing between the original and corrected audio changes significantly.

3. **Transcription Accuracy**:
   - Google Speech Recognition is not always 100% accurate, and its performance may degrade with noisy audio or unclear speech.

4. **Punctuation**:
   - The corrected text may have different punctuation, which could alter the timing slightly.

---

By following these instructions, you should be able to process videos automatically, correcting speech and re-integrating improved audio back into the original video!