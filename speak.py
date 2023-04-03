import pyttsx3
import speech_recognition as sr


SPEECH_RATE = 210
VOLUME = .7

MAX_AUDIO_LEN = 10
AUDIO_TIMEOUT = 5

engine = pyttsx3.init()
engine.setProperty('rate', SPEECH_RATE)
engine.setProperty('volume', VOLUME)

r = sr.Recognizer()


def speak(text):
    if isinstance(text, list):
        for line in text:
            print(line)
            engine.say(line)
        engine.runAndWait()
    else:
        print(text)
        engine.say(text)
        engine.runAndWait()


def get_audio():
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, AUDIO_TIMEOUT, MAX_AUDIO_LEN)
                print("Finished listening.")

            phrase = r.recognize_google(audio).lower()
            print("You said:", phrase)
            return phrase
        except sr.exceptions.WaitTimeoutError:
            print("try again")
            continue
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            continue
        except sr.RequestError as e:
            print(
                "Could not request results from Google Speech Recognition service; {0}".format(e))
            continue


if __name__ == "__main__":
    speak(["hello", "there"])
    speak("what's up fucker")
