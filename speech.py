import os
import time
import datetime
import azure.cognitiveservices.speech as speechsdk


def recognize_from_microphone():
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get(
        'SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    speech_config.speech_recognition_language = "en-US"
    speech_config.request_word_level_timestamps()

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config)

    done = False
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    def stop_cb(evt):
        print('CLOSING on {}'.format(evt))
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True

    def save_recognized_text(evt):
        result_text = evt.result.text
        time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        formatted_text = f"{time}: {result_text}"
        print('RECOGNIZED: {}'.format(formatted_text))
        file_name = f"record-{timestamp.replace(':', '-')}.md"
        with open(file_name, "a") as file:
            file.write(formatted_text + '\n')

    print("Speak into your microphone.")
    speech_recognizer.recognizing.connect(
        lambda evt: {})
    speech_recognizer.recognized.connect(save_recognized_text)
    speech_recognizer.session_started.connect(
        lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(
        lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(
        lambda evt: print('CANCELED {}'.format(evt)))

    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)


recognize_from_microphone()
