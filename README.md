# Micro:bit Morse Messenger
I built this fun little project with my miss 12 and friends. We used two micro:bits and let them talk to each other in Morse code over the built-in radio. You type dots and dashes with the buttons and they get decoded into letters and then sent to the other micro:bit. The other micro:bit board scrolls the text. This way messages can be sent back and forth.

## What you need

- Two BBC micro:bit V2 boards. Touching the logo is a V2 feature.
- [MicroPython for the micro:bit](https://python.microbit.org/), or another editor that can flash `MicroPython` (`flash` means you copy code onto the micro:bit so it runs there).
- A USB cable for each board you flash.

Flash the same script onto both boards. Each board can send and receive.

## The code explained

`microbit-radio-morse.md` walks through the script in plain language, written for ages 12 to 13.

## How to get the script onto the micro:bit

1. Open [the micro:bit Python editor](https://python.microbit.org/).
2. Paste in the script.
3. Connect a micro:bit and flash the script.
4. Flash the same script onto the second micro:bit.

Both scripts use radio group `17`. If you change that number, change it on both boards. Groups run from 0 to 255.

## How to use it

- Use the button **A** to type a dot `.` and button **B** to type a dash `-`. 
	- the display will show your current dots or dashes: 
		- A dot is a bright pixel on the middle row. 
		- A dash is a bright pixel on the top row. 
		- The screen is five LEDs wide, so only the last five symbols stay visible. 
		- If you type a pattern that is not in the Morse table it shows as **`?`**.
- Touch the **logo** to type a space.
- **Shake** the micro:bit to finish each letter or space, decode it and add it to a message buffer.
- Once you have typed out your entire message, press both button **A** and **B** together to send it
- The display scrolls `SENT` when sent.
- The receiving micro:bit will scroll the message on the screen.

| Action | What happens |
| --- | --- |
| Button A | Add a dot (`.`) |
| Button B | Add a dash (`-`) |
| Shake | Finish the letter, decode it, and add it to the message |
| Touch the logo | Add a space |
| Buttons A and B together | Send the message. The display scrolls `SENT` |
Have fun!





