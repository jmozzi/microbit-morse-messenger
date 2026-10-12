# Little project with miss 12: trying to turn a micro:bit into a morse/letter radio
# Type letters in Morse (dots/dashes)
# Shake to finish a letter → it gets decoded locally
# Add letters to a message buffer
# Touch the logo to add a space
# Press both buttons together to send the whole message
# Receiver just scrolls the full message

from microbit import *
import radio

radio.on()
radio.config(group=17)  

# Morse dictionary for decoding
MORSE = {
    ".-": "A", "-...": "B", "-.-.": "C", "-..": "D", ".": "E",
    "..-.": "F", "--.": "G", "....": "H", "..": "I", ".---": "J",
    "-.-": "K", ".-..": "L", "--": "M", "-.": "N", "---": "O",
    ".--.": "P", "--.-": "Q", ".-.": "R", "...": "S", "-": "T",
    "..-": "U", "...-": "V", ".--": "W", "-..-": "X", "-.--": "Y",
    "--..": "Z",
    "-----": "0", ".----": "1", "..---": "2", "...--": "3",
    "....-": "4", ".....": "5", "-....": "6", "--...": "7",
    "---..": "8", "----.": "9"
}

current_letter = ""   # build dots/dashes for one letter
message_buffer = ""   # store full message

def show_current():
    """Show the current dots/dashes of the letter being typed."""
    display.clear()
    for i, c in enumerate(current_letter[-5:]):
        if c == ".":
            display.set_pixel(i, 2, 9)
        else:
            display.set_pixel(i, 0, 9)

while True:
    # BUTTONS: build dot or dash
    if button_a.was_pressed():
        current_letter += "."
        show_current()

    if button_b.was_pressed():
        current_letter += "-"
        show_current()

    # SHAKE: finish current letter
    if accelerometer.was_gesture("shake"):
        if current_letter != "":
            # decode Morse to letter
            letter = MORSE.get(current_letter, "?")
            message_buffer += letter
            current_letter = ""
            display.clear()
            display.show(letter)  # quick feedback
            sleep(500)

    # LOGO TOUCH: add space between words
    if pin_logo.is_touched():
        message_buffer += " "
        display.show("-")  # visual feedback for space
        sleep(300)

    # BOTH BUTTONS: send full message
    if button_a.is_pressed() and button_b.is_pressed():
        if message_buffer != "":
            radio.send(message_buffer)
            display.scroll("SENT")
            message_buffer = ""
            current_letter = ""
            display.clear()
            sleep(500)

    # RECEIVE
    incoming = radio.receive()
    if incoming:
        display.scroll(incoming)

    sleep(50)
