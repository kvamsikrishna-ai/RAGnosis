import time
import keyboard  # for interrupt control

from src.pipeline import rag_pipeline
from src.voice.stt import get_voice_input
from src.voice.tts import speak, stop_speaking

# 🔥 simple in-memory cache
cache = {}

DEBUG = True


def main():
    mode = input("Choose mode (text/voice): ").strip().lower()

    if mode not in ["text", "voice"]:
        print("❌ Invalid mode. Defaulting to text.")
        mode = "text"

    print("\n🚀 System Ready!\n")
    print("💡 Press 'S' anytime to stop voice output\n")

    while True:
        try:
            # -------------------------
            # INPUT
            # -------------------------
            if mode == "voice":
                query = get_voice_input()

                if query is None:
                    print("🔁 No valid speech. Try again.\n")
                    continue
            else:
                query = input("Ask something: ").strip()
                if not query:
                    continue

            # -------------------------
            # EXIT CONDITION
            # -------------------------
            if query.lower() in ["exit", "quit", "stop"]:
                print("👋 Exiting system...")
                break

            # -------------------------
            # STOP ANY ONGOING SPEECH
            # -------------------------
            stop_speaking()

            # -------------------------
            # CACHE CHECK
            # -------------------------
            if query in cache:
                print("⚡ Using cached response\n")
                response = cache[query]
            else:
                start_time = time.time()

                response = rag_pipeline(query)

                latency = time.time() - start_time
                cache[query] = response

                if DEBUG:
                    print(f"\n⏱️ Latency: {latency:.2f}s")

            # -------------------------
            # OUTPUT
            # -------------------------
            print("\n🧠 Answer:\n", response)

            # -------------------------
            # VOICE OUTPUT
            # -------------------------
            if mode == "voice":
                speak(response)

                print("\n🎤 Speaking... (press 'S' to stop)\n")

                # 🔥 allow interruption while speaking
                while True:
                    if keyboard.is_pressed("s"):
                        stop_speaking()
                        print("🛑 Speech stopped\n")
                        break

                    # exit loop when speaking finishes
                    time.sleep(0.1)
                    break

        except KeyboardInterrupt:
            print("\n👋 Interrupted. Exiting...")
            break

        except Exception as e:
            print("⚠️ Runtime Error:", e)


if __name__ == "__main__":
    main()