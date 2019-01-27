import re
import wave
import pyaudio
import thread
import time

class TextToSpeech:
    CHUNK = 2048

    def __init__(self, words_pron_dict = 'cmudict-0.7b.txt'):
        self._l = {}
        self.load_words(words_pron_dict)

    def load_words(self, words_pron_dict):
        with open(words_pron_dict, 'r') as file:
            for line in file:
                if not line.startswith(';;;'):
                    key, val = line.split('  ',2)
                    self._l[key] = re.findall(r"[A-Z]+",val)

    def get_pronunciation(self, str_input):
        list_pron = []
        for word in re.findall(r"[\w']+",str_input.upper()):
            if word in self._l:
                list_pron += self._l[word]
        print(list_pron)
        delay=0
        for pron in list_pron:
            a = audio();
            a.play_audio(pron, 0)
            #thread.start_new_thread( a.play_audio, (pron, delay))
            delay += 0.145


class audio:
    def play_audio(self, sound, delay):
        try:
            time.sleep(delay)
            wf = wave.open("new_sounds/"+sound+".wav", 'rb')
            p = pyaudio.PyAudio()
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)
            data = wf.readframes(TextToSpeech.CHUNK)
            data = wf.readframes(TextToSpeech.CHUNK)
            data = wf.readframes(TextToSpeech.CHUNK)
            data = wf.readframes(TextToSpeech.CHUNK)
            while data:
                stream.write(data)
                data = wf.readframes(TextToSpeech.CHUNK)
            stream.stop_stream()
            stream.close()

            p.terminate()
            return
        except:
            pass


if __name__ == '__main__':
    tts = TextToSpeech()
    while True:
        tts.get_pronunciation(raw_input('Enter a word or phrase: '))
