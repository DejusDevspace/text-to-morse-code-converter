import pygame
from pygame import mixer
import time
from gtts import gTTS
from io import BytesIO
import winsound


class Converter:
    def __init__(self):
        self.TEXT_T0_MORSE_DICT = {
            'A': '.-',
            'B': '-...',
            'C': '-.-.',
            'D': '-..',
            'E': '.',
            'F': '..-.',
            'G': '--.',
            'H': '....',
            'I': '..',
            'J': '.---',
            'K': '-.-',
            'L': '.-..',
            'M': '--',
            'N': '-.',
            'O': '---',
            'P': '.--.',
            'Q': '--.-',
            'R': '.-.',
            'S': '...',
            'T': '-',
            'U': '..-',
            'V': '...-',
            'W': '.--',
            'X': '-..-',
            'Y': '-.--',
            'Z': '--..',
            '0': '-----',
            '1': '.----',
            '2': '..---',
            '3': '...--',
            '4': '....-',
            '5': '.....',
            '6': '-....',
            '7': '--...',
            '8': '---..',
            '9': '----.',
            ' ': ' ',  # Space
        }  # Dictionary of characters and their morse code equivalent
        self.PUNCTUATION_TO_MORSE_DICT = {
            '.': '.-.-.-',  # Period
            ',': '--..--',  # Comma
            '?': '..--..',  # Question mark
            "'": '.----.',  # Apostrophe
            '!': '-.-.--',  # Exclamation mark
            '/': '-..-.',  # Slash
            '(': '-.--.',  # Left parenthesis
            ')': '-.--.-',  # Right parenthesis
            '&': '.-...',  # Ampersand
            ':': '---...',  # Colon
            ';': '-.-.-.',  # Semicolon
            '=': '-...-',  # Equals sign
            '+': '.-.-.',  # Plus sign
            '-': '-....-',  # Hyphen
            '_': '..--.-',  # Underscore
            '"': '.-..-.',  # Quotation mark
            '$': '...-..-',  # Dollar sign
            '@': '.--.-.',  # At sign
        }  # Dictionary of punctuation marks and morse code equivalent
        self.MORSE_TO_TEXT_DICT = {
            '.-': 'A',
            '-...': 'B',
            '-.-.': 'C',
            '-..': 'D',
            '.': 'E',
            '..-.': 'F',
            '--.': 'G',
            '....': 'H',
            '..': 'I',
            '.---': 'J',
            '-.-': 'K',
            '.-..': 'L',
            '--': 'M',
            '-.': 'N',
            '---': 'O',
            '.--.': 'P',
            '--.-': 'Q',
            '.-.': 'R',
            '...': 'S',
            '-': 'T',
            '..-': 'U',
            '...-': 'V',
            '.--': 'W',
            '-..-': 'X',
            '-.--': 'Y',
            '--..': 'Z',
            '-----': '0',
            '.----': '1',
            '..---': '2',
            '...--': '3',
            '....-': '4',
            '.....': '5',
            '-....': '6',
            '--...': '7',
            '---..': '8',
            '----.': '9',
            '.-.-.-': '.',
            '--..--': ',',
            '..--..': '?',
            '.----.': "'",
            '-.-.--': '!',
            '-..-.': '/',
            '-.--.': '(',
            '-.--.-': ')',
            '.-...': '&',
            '---...': ':',
            '-.-.-.': ';',
            '-...-': '=',
            '.-.-.': '+',
            '-....-': '-',
            '..--.-': '_',
            '.-..-.': '"',
            '...-..-': '$',
            '.--.-.': '@',
            '': ' '
        }  # Dictionary of morse codes and their character equivalent
        mixer.init()  # Initializes the pygame mixer
        self.SILENCE_DURATION = 0.2  # Duration of silence between sounds (in seconds)

    def text_to_morse(self, text) -> str:
        """Takes text input and returns it in morse code"""
        # Create an empty string for the morse code
        morse_code = ''
        for char in text.upper():  # Converts input to uppercase like dictionary characters for consistency
            if char in self.TEXT_T0_MORSE_DICT:
                # Adds the morse code sequence and a space for each character in the user's input
                morse_code += f'{self.TEXT_T0_MORSE_DICT[char]} '
            elif char in self.PUNCTUATION_TO_MORSE_DICT:
                # Adds the morse code sequence and a space for punctuations in the input
                morse_code += f'{self.PUNCTUATION_TO_MORSE_DICT[char]} '
            else:
                morse_code += ''  # Adds space for unknown characters
        return morse_code.strip()  # Removes trailing space(s) in morse code sequence

    def play_morse_audio(self, morse_code):
        """Plays the sound for a morse code sequence"""
        mixer.init()  # Initializes the Pygame mixer
        for char in morse_code:
            if char == '-':
                winsound.Beep(frequency=800, duration=400)  # Plays the dash (-) sound
            elif char == '.':
                winsound.Beep(frequency=800, duration=200)  # Plays the dot (.) sound
            elif char == '':
                time.sleep(self.SILENCE_DURATION)  # Plays no sounds for specified silence duration

    def morse_to_text(self, morse_code) -> str:
        """Takes morse code input and changes it to text"""
        morse_words = morse_code.split('  ')  # Splits morse code into words (words are separated by double spaces)
        # Create an empty string for the text
        text = ''
        for morse_word in morse_words:
            morse_chars = morse_word.split()  # Splits morse words into characters
            word = ''  # Becomes empty during each iteration to house the next word
            for char in morse_chars:
                if char in self.MORSE_TO_TEXT_DICT:
                    word += f'{self.MORSE_TO_TEXT_DICT[char]}'  # Add the equivalent characters of each morse sequence
            text += f'{word.lower()} '  # Adds each word to the text with a space between words
        return text.strip()  # Removes trailing space(s)

    def play_text_audio(self, text):
        """Converts text to speech and plays the audio of the text"""
        speech_stream = BytesIO()  # Creates a BytesIO stream (gets speech as a binary stream)
        # Generate speech from text using gTTS
        tts = gTTS(text=text, lang='en')
        speech_stream.truncate(0)  # Discards all previous data written to the BytesIO stream (if any)
        tts.write_to_fp(speech_stream)  # Write the speech data from the gTTS to the BytesIO stream
        speech_stream.seek(0)  # Return stream cursor to the beginning of the text
        mixer.music.load(speech_stream)  # Loads speech stream (BytesIO) into the Pygame mixer
        mixer.music.play()  # Plays the loaded speech
        time.sleep(self.SILENCE_DURATION)  # Wait for specified number of seconds (optional) !irrelevant!

        # Wait until speech finishes playing
        while mixer.music.get_busy():  # Returns true while playing audio
            pygame.time.Clock().tick(60)

    def is_morse_code(self, morse_code) -> bool:
        """Checks if input is in form of morse code"""
        for char in morse_code:
            if char.upper() in self.TEXT_T0_MORSE_DICT and char != ' ':
                # Check if there are numbers of letters in the input
                return False
            # Check if there are symbols apart from dot and dash in the input
            elif char in self.PUNCTUATION_TO_MORSE_DICT and char not in self.MORSE_TO_TEXT_DICT:
                return False
            else:
                continue
        return True  # If all characters are in form of morse code
