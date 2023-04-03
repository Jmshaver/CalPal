import pyttsx3

# print("fdkl")
# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set the speed of the speech
engine.setProperty('rate', 250)

# Set the volume of the speech
engine.setProperty('volume', 0.7)

# Convert text to speech
text = "Hello, how are you today?"
engine.say(text)

# Speak the text
engine.runAndWait()
