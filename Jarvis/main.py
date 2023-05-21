import openai
import pyttsx3
import speech_recognition as sr
from googlesearch import search
import webbrowser
import pyautogui

#set our openia key
openai.api_key = "" #add your api_key
engine = pyttsx3.init()

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        speak_text("I dont understand")
    

def generate_response(prompt):
    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=4000, n=1, stop=None, temperature=0.5)
    return response["choices"][0]["text"]


def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def search_google(text, num_results=10):
    resault_list = []
    search_results = search(text, num_results=num_results, lang='en')
    for resault in search_results:
        resault_list.append(resault)
    webbrowser.open(resault_list[0])

def main():
    speak_text("Hello I am robot")
    while True:
        print("ask")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == "robot":
                    #Record audio
                    filename = "input.wav"
                    speak_text("Yes?")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_treshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())

                        #Transcribe audio to text
                        text = transcribe_audio_to_text(filename)
                        if text:
                            print("You said", text)
                            if text.lower() == "turn off":
                                speak_text("Turning off")
                                break

                            elif text.lower().startswith("open"):
                                u_input =  text.lower().lstrip("open")
                                speak_text(f"Opening {u_input}")
                                search_google(u_input)

                            elif text.lower() == "next song":
                                print("next")
                                pyautogui.press('nexttrack')

                            elif text.lower() == "last song":
                                print("last")
                                pyautogui.press('prevtrack')
                                pyautogui.press('prevtrack')

                            elif text.lower() == "play music":
                                print("play")
                                pyautogui.press('playpause')

                            elif text.lower() == "stop music":
                                print("stop")
                                pyautogui.press('playpause')

                            else:
                                print(f"You said: {text}")

                                #generating response using chatgpt
                                response = generate_response(text)
                                print(f"GPT said: {response}")

                                #read response using text_to_speach
                                speak_text(response)
            except Exception as e:
                print(f"An error accured: {e}")

if __name__ == "__main__":
    main()
