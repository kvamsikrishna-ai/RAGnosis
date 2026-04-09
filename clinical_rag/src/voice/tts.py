import pyttsx3
import threading

engine = pyttsx3.init()

engine.setProperty('rate', 170)
engine.setProperty('volume', 1.0)

lock = threading.Lock()
stop_signal = False
is_speaking = False


def _speak_worker(text):
    global stop_signal, is_speaking

    with lock:  # 🔥 CRITICAL FIX
        is_speaking = True

        sentences = text.replace("\n", ". ").split(".")

        for sentence in sentences:
            if stop_signal:
                break

            sentence = sentence.strip()
            if not sentence:
                continue

            try:
                engine.say(sentence)
                engine.runAndWait()
            except RuntimeError:
                # 🔥 FIX: reset loop safely
                try:
                    engine.stop()
                except:
                    pass

        is_speaking = False


def speak(text):
    global stop_signal

    stop_speaking()

    stop_signal = False

    thread = threading.Thread(target=_speak_worker, args=(text,))
    thread.daemon = True
    thread.start()


def stop_speaking():
    global stop_signal

    stop_signal = True
    try:
        engine.stop()
    except:
        pass


def speaking_status():
    return is_speaking