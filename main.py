import os
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import speech_recognition as sr
from gtts import gTTS
import requests
from pydub import AudioSegment
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Set your Azure OpenAI API key and endpoint
azure_openai_key = os.getenv('AZURE_OPENAI_KEY')
azure_openai_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')

# Function to split video into 10-second segments
def split_video(video_path, segment_length=10):
    video = VideoFileClip(video_path)
    segments = []
    duration = int(video.duration)

    for start in range(0, duration, segment_length):
        end = min(start + segment_length, duration)
        segment = video.subclip(start, end)
        segment_filename = f"test_video/segment_{start // segment_length}.mp4"
        segment.write_videofile(segment_filename, codec="libx264")
        segments.append(segment_filename)

    return segments

# Function to process each video segment
# Function to process each video segment
def process_segment(segment_filename):
    # Extract audio from segment
    segment = VideoFileClip(segment_filename)
    audio_filename = f"test_audio/{segment_filename.split('/')[-1]}_audio.mp3"
    segment.audio.write_audiofile(audio_filename)

    # Convert MP3 audio to WAV format directly using moviepy
    wav_audio_filename = f"test_audio/{segment_filename.split('/')[-1]}_audio.wav"
    audio_clip = AudioFileClip(audio_filename)
    audio_clip.write_audiofile(wav_audio_filename, codec='pcm_s16le')

    # Transcribe audio
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(wav_audio_filename) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
    except Exception as e:
        print(f"Error transcribing {wav_audio_filename}: {e}")
        st.error('Error in transcribing audio.. ⚠️')
        st.stop()
        return segment_filename  # Skip processing if transcription fails

    # Correct grammar using OpenAI
    headers = {
        "Content-Type": "application/json",
        "api-key": azure_openai_key
    }
    
    content = f'i am going to give you a text in double quotes remove all grammatical error from the text and return only revised text nothing else "{text}"'
    data = {
        "messages": [{"role": "user", "content": content}]
    }

    try:
        response = requests.post(azure_openai_endpoint, headers=headers, json=data)
        corrected_text = response.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error calling OpenAI API: {response.json()}")
        st.error('Error in calling openai api .. ⚠️')
        st.stop()
        return segment_filename  # Skip processing if API call fails

    # Generate TTS audio
    tts = gTTS(corrected_text)
    corrected_audio_filename = f"test_audio/{(segment_filename.split('/')[-1]).split('.')[0]}_corrected_audio.mp3"
    tts.save(corrected_audio_filename)

    # Replace the original audio with corrected audio
    corrected_audio = AudioFileClip(corrected_audio_filename)
    final_segment = segment.set_audio(corrected_audio)
    final_segment_filename = f"test_video/processed_{segment_filename.split('/')[-1]}"
    final_segment.write_videofile(final_segment_filename)

    # Clean up temporary files
    os.remove(audio_filename)
    os.remove(wav_audio_filename)
    os.remove(corrected_audio_filename)

    return final_segment_filename

# Main function to process the video
def main(video_path):
    # Create necessary directories
    os.makedirs("test_video", exist_ok=True)
    os.makedirs("test_audio", exist_ok=True)

    # Step 1: Split video into segments
    segments = split_video(video_path)

    # Step 2: Process each segment
    processed_segments = [process_segment(seg) for seg in segments]

    # Step 3: Combine processed segments back into a final video
    final_segments = [VideoFileClip(seg) for seg in processed_segments if seg is not None]
    final_video = concatenate_videoclips(final_segments)
    final_video.write_videofile("final_video.mp4")

    # Clean up temporary segment files
    for seg in segments + processed_segments:
        if os.path.exists(seg):
            os.remove(seg)

# Run the main function
st.markdown('### Important instructions to use.')
import streamlit as st

st.markdown("""
#### Upload Your Video

- **Duration Limit**: Your video must be less than **2 minutes** to ensure faster processing. 
  - *Note*: Videos longer than this may take more than **5 minutes** to process.

#### Refresh Before Reupload

- Before re-uploading any video, please **refresh the window** to ensure the application works correctly.

#### Error Handling

- If you encounter any errors, please **re-run the program** from the terminal to restart the process.
""")

st.markdown('### Upload your video 📽️ here...')
st.info("upload video which is less than 2min for big video can take more than 5 min to convert.")
sample_video = st.file_uploader("", ['mp4', 'mov', 'webm'], accept_multiple_files=False)

if sample_video is None:
    st.warning("No video file uploaded.")
    st.stop()

video_path='input_video.mp4'

with open(video_path, 'wb') as f:
    f.write(sample_video.read())

with st.spinner("removing all grammaticla error from video please wait it may take time..."):
    main(video_path)
    
st.markdown('### video processed successfully 🎊')
st.video('final_video.mp4')
