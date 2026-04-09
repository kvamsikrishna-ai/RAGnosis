import speech_recognition as sr
import keyboard


def get_voice_input():
    recognizer = sr.Recognizer()

    print("\n🎤 Hold SPACE to speak...")
    keyboard.wait("space")

    with sr.Microphone() as source:
        print("🎙️ Recording... (release SPACE to stop)")

        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        audio_chunks = []

        while keyboard.is_pressed("space"):
            try:
                audio = recognizer.listen(
                    source,
                    timeout=1,
                    phrase_time_limit=2
                )
                audio_chunks.append(audio)
            except sr.WaitTimeoutError:
                continue

    print("🛑 Processing...")

    # 🔴 FIX: handle empty audio
    if not audio_chunks:
        print("❌ No speech detected")
        return None

    try:
        full_audio = sr.AudioData(
            b"".join([a.get_raw_data() for a in audio_chunks]),
            audio_chunks[0].sample_rate,
            audio_chunks[0].sample_width
        )

        text = recognizer.recognize_google(full_audio)
        print("🗣️ You said:", text)
        return text

    except sr.UnknownValueError:
        print("❌ Could not understand audio")
        return None

    except Exception as e:
        print("⚠️ STT Error:", e)
        return None