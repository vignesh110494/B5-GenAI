# import streamlit as st
# st.title("My First Streamlit App")
# st.audio()
import streamlit as st

st.title("🎵 Simple Audio Player")
st.write("This is a basic Streamlit app that plays an audio file.")

# Correct Windows path (RAW STRING)
audio_path = r"C:\Users\vigne\Codebase\B5-GenAI\06_streamlit\practiseaudio.mp3"

# Read audio file safely
with open(audio_path, "rb") as audio_file:
    audio_bytes = audio_file.read()

# Display audio player in UI
st.audio(audio_bytes, format="audio/mp3")
