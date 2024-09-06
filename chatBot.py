import openai
import pyttsx3
import speech_recognition as sr
import time
import streamlit as st


engine = pyttsx3.init()

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        st.write("Speak Again")
    except sr.RequestError as e:
        print(f"Bot aint working; {e}")

def generate_response(prompt):
    template = """airo is conducted in sairam engineerning college on 17th october 2023
    """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=[prompt,template],
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        # st.write("Say 'Hello' to start recording your question...")
        # with sr.Microphone() as source:
        #     recognizer = sr.Recognizer()
        #     audio = recognizer.listen(source)

        try:
            # transcription = recognizer.recognize_google(audio)
            filename = "input.wav"
            st.write("ask question")
            with sr.Microphone() as source:
                recognizer = sr.Recognizer()
                source.pause_threshold = 1
                audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                with open(filename, "wb") as f:
                    f.write(audio.get_wav_data())

            text = transcribe_audio_to_text(filename)
            if text:
                st.write(f"You said: {text}")
                response = generate_response(text)
                st.write(f"AIRO Bot says: {response}")
                speak_text(response)
        except sr.WaitTimeoutError:
            print("Timeout: No speech detected")
        except sr.RequestError as e:
            print(f"Could not request results;")
        except sr.exceptions.UnknownValueError:
            print("repeat")

if __name__ == "__main__":
    main()
