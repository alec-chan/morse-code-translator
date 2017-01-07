# morse-code-translator
Translates between alphanumeric text and morse code and generates audio for morse code.

##Setup
Requires python 2.7 and [Pyaudio](http://people.csail.mit.edu/hubert/pyaudio/)
Can be installed through pip:
```
pip install pyaudio
```

##Usage
```
#text -> morse (this also will play the morse code audio through your speakers)
python translator.py "<your text>"

#morse -> text
python translator.py "<your morse code>"

#or just
python translator.py
```
