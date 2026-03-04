import asyncio
import sounddevice as sd
import soundfile as sf
import numpy as np
import io
import os

from openai import OpenAI
from livekit import rtc
from livekit import api
from dotenv import load_dotenv
import os

load_dotenv()  # loads .env file

# ================= CONFIG =================
LIVEKIT_URL = "ws://127.0.0.1:7880"
API_KEY = "devkey"
API_SECRET = os.getenv("API_SECRET")    
ROOM_NAME = "local-room"
IDENTITY = "voice-agent"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# ============ TOKEN =======================
def create_token():
    token = api.AccessToken(API_KEY, API_SECRET)
    token = token.with_identity(IDENTITY)
    token = token.with_name("Voice Agent")
    token = token.with_grants(
        api.VideoGrants(
            room_join=True,
            room=ROOM_NAME
        )
    )
    return token.to_jwt()

# ============ STT =========================
import soundfile as sf
import tempfile

async def speech_to_text(wav_buffer):
    print("📝 Transcribing speech_to_text...")

    wav_buffer.seek(0)

    transcript = client.audio.transcriptions.create(
        model="gpt-4o-mini-transcribe",
        file=("speech.wav", wav_buffer, "audio/wav")
    )

    return transcript.text
# ============ LLM =========================
async def ask_llm(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful voice assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# ============ TTS =========================
async def text_to_speech(text):
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    )
    return response.read()

# ============ MAIN ========================
async def main():
    print("Connecting to LiveKit...")
    room = rtc.Room()
    await room.connect(LIVEKIT_URL, create_token())
    print("✅ Connected to LiveKit")

    while True:
        print("\n🎤 Speak for 4 seconds...")
        samplerate = 44100
        audio = sd.rec(int(4 * samplerate),
                       samplerate=samplerate,
                       channels=1,
                       dtype="float32")
        sd.wait()

        wav_buffer = io.BytesIO()
        sf.write(wav_buffer, audio, samplerate, format="WAV")
        wav_buffer.seek(0)

        print("📝 Transcribing...")
        user_text = await speech_to_text(wav_buffer)
        print("You:", user_text)

        print("🤖 Thinking...")
        reply = await ask_llm(user_text)
        print("AI:", reply)

        print("🔊 Speaking...")
        tts_audio = await text_to_speech(reply)

        data, sr = sf.read(io.BytesIO(tts_audio))
        sd.play(data, sr)
        sd.wait()

asyncio.run(main())