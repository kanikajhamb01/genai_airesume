import speech_recognition as sr

def transcribe_voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Speak now...")
        audio = r.listen(source, timeout=5, phrase_time_limit=10)

    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Sorry, I could not understand your voice."
    except sr.RequestError:
        return "Error with the speech recognition service."
