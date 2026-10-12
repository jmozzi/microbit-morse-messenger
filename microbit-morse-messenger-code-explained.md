This is the attempt for some kid-friendly explanations ... age group 12-13

## explanation
The code is designed for a **BBC micro:bit** to act as a wireless Morse code communicator. It allows you to input dots and dashes, decode them into letters, and send the full message to another micro:bit via radio. 

# Initialization and Setup

- **`from microbit import *`**: Imports the standard library called "microbit"  that is needed to control micro:bit hardware (display, buttons, accelerometer).
	- what does this mean? 
		- Think of the library "`microbit`" as opening a **special toolbox** for the micro:bit. Without it, the micro:bit doesn't know it has buttons or a screen. This line teaches the micro:bit what 'Button A' and 'The Display' are so you can just use a function from the library called `button_a.was_pressed()` and it actually knows it has a button A and it will tell its sensors to check whether button A was pressed. This helps our code very much as we don't have to write code ourselves to make the micro:bit aware that it has a button A, a display and other things. A library means, someone else has written this code for us and we can just use it by "importing" it. And the * means, we want to import everything in that toolbox. Awesome!
- **`import radio`**: Imports the wireless networking module.
	- this is another pre-made module that acts like a "Walkie-Talkie-upgrade"; it allows your micro:bit to "shout" messages through the air using invisible radio waves; it also enables your micro:bit to "listen" for messages from other micro:bits.
- **`radio.on()`**: Powers on the micro:bit’s radio antenna, which you need to use it as "walkie-talkie"; the radio is usually kept OFF to save battery, so you have to tell the micro:bit specifically to turn it on to listen for signals.
- **`radio.config(group=17)`**: Sets the radio to "group 17." Both the sender and receiver must be on the same group number to communicate.

# The Dictionary - the code book
- **`MORSE = {...}`**: A dictionary that maps Morse code strings (dots and dashes) to alphanumeric characters (eg "A"). It's basically a code book. The micro:bit doesn't know that a "dot-dash" (`.-`) means the letter "A." This section is where we give the micro:bit a list of rules to follow so it can translate (aka look-up or match) the dots and dashes into real letters.

# Variable Buffers - kind of like a storage for our letters and messages before we send them

- **`current_letter = ""`**: A temporary string (a bunch of characters) that stores the dots and dashes you are currently typing for a single character. Kind of like a "scrap piece of paper" where the micro:bit scribbles down the dots and dashes, so it can later assemble them to a letter.
- **`message_buffer = ""`**: Stores the actual translated letters (e.g., "HELLO") before they are sent. 

# Display Logic - displaying what you type

- **`def show_current():`**: A helper function that visualizes your typing.
	- it basically says: Whenever I call this name `show_current()`, look at my scrap paper `current_letter` and draw the dots and dashes on the screen so I can see what I'm typing. 
	- And because the micro:bit screen can only show you a max of 5 symbols (cause that's how wide it is), this code block also clears the screen with `display.clear()` and then loops through the last 5 symbols in `current_letter` and it does this with a so called "for" loop like this: 
```python
# this loops through the last 5 symbols in `current_letter`
for i, c in enumerate(current_letter[-5:]): 
    # if it finds a `dot` 
    if c == ".":  
        # it will highlight a certain pixel on the screen, namely a pixel in the middle row (y=2), `9` is full brightness.         
	    display.set_pixel(i, 2, 9)  
    # if it doesn't find a `dot`, we know it will find a `dash`
    else:                                                   
	    # and it will highlight a pixel in the top row (y=0) of the display and `9` is full brightness.
	    display.set_pixel(i, 0, 9)           
```

- so this way you can see whether you've typed a dash or a dot.
- This will make more sense once you read about the code in the `while loop` further down - because in each loop (see further down), we call on this `show_current()` function and every time we do this, the micro:bit will show us the dots and dashes as we create them by pressing buttons.

# The Main Loop (while True) - this runs continuously, it's like a spinning mouse wheel

This section runs continuously to check for user input: that means it checks whether you press button A, or button B, or whether you shake or whether you touch the logo or whether you have an incoming message. And then it does things according to what you coded should happen.

**`while True:`**: This tells the micro:bit to **wake up and stay alert**. It runs the following instructions over and over again, many times a second, so it doesn't miss a button press. A button press is remembered until the loop comes back to check, so a quick tap still counts. This works because in Python, `True` means _true forever_, so **“while True”** means: “As long as this is true (which it always is), keep looping through whatever code comes next" ... and that is how we create a never-ending-loop (well, at least until you turn off the micro:bit).

## 1. **Inputting Morse:**
```python
if button_a.was_pressed():   #if I press button A
    current_letter += "."        # add a dot (.) to the `current_letter`, which is your scrap paper, remember?
    show_current()               # and now we call `show_current` which shows the dot on the screen as we press the button
```
 - and we do the same for button b:
    - **`button_b.was_pressed()`**: Adds a dash (`-`) to the `current_letter`, which is your scrap paper and then shows on our display that we pressed a dash
    - the symbol ``+=`` is a short version of saying `current_letter = current_letter + "."` , so take `current_letter` and add a dot and then stick the result back into `current_letter`. So if `current_letter` already had a dot in it, we now add another dot and now `current_letter` contains two dots. That's how we can stitch together a whole Morse code letter.
## 2. **Decoding your dots and dashes into a letter and finishing a letter (The "Shake"):**
```python
if accelerometer.was_gesture("shake"):
	if current_letter != "":  # check that `current_letter` is not empty
		letter = MORSE.get(current_letter, "?")  # decode Morse to letter, if it doesn't match anything in the dict show ? 
		message_buffer += letter  #add the letter into the `message_buffer`
		current_letter = ""       #clear `current_letter`
		display.clear()           #clear display
		display.show(letter)      # quick feedback on your decoded letter
		sleep(500)                # 500 milliseconds are half a second
```
- **`if accelerometer.was_gesture("shake"):`**: When you shake the device, it signals the end of a letter. It's like saying: "I've finished creating my letter"
- `if current_letter != "":` this is a quick check to ensure that the code only runs if the current_letter is NOT empty (`!=` means is NOT), because it doesn't make sense to send an "empty" letter, right?
- **`letter = MORSE.get(current_letter, "?")`**: The micro:bit looks at its **Code Book** (remember this bit: `MORSE = {...}`). If it sees the dots and dashes you typed, it finds and matches the letter and sticks it into a variable called "letter". A variable is like a little container where we put the letter for the time being, so we can grab it later to add it to the message we collect in `message_buffer`. If you typed something weird that isn't in the book, it just says **"?"** - if we don't tell the program what to do in case it doesn't find a match, it will crash, so the "?" is a polite way to say "no match and no need to crash cause we will display a "?" instead). 
	- Here again with a bit more details if you're curious:
	- in Python, `.get()` method is a safer way to look up values in a dictionary. This line acts as translator with backup plan.
	- **`MORSE`**: This is the dictionary you created that lists all valid Morse code sequences (keys) and their corresponding letters (values).
	- **`.get(current_letter, ...)`**: This part tells Python to search the `MORSE` dictionary for whatever dots and dashes are currently stored in the `current_letter` variable.
	- **The "Found" Case**: If the sequence is valid (e.g., if `current_letter` is `.-`), the method returns the matching letter (e.g., `"A"`).
	- **The "Not Found" Case (The Backup)**: This is the most important part. If you enter a sequence that doesn't exist in your dictionary (e.g., `.......`), a standard dictionary lookup like `MORSE[current_letter]` would crash your program with a **KeyError**.
		- By using `.get()`, the second argument (`"?"`) is returned as a **default value** instead of crashing.
- **`message_buffer += letter`**: Adds the decoded letter to the final message, see how handy it is that we put our letter previously into the variable "letter", so now we can move the letter somewhere else, in this case into the final message placeholder `message_buffer` (where we collect all letters until they make up a message that we can send)
- `current_letter = ""` this means we clear `current_letter` ready for the next one.
- `display.clear()` we also clear our display and then
- `display.show(letter)` and then we show our letter for us to quickly check that this is the letter we wanted (here it's handy again that we previously put our letter into the variable "letter", so now we can quickly "call" it )
- `sleep(500)`: here we just make the micro:bit wait or "sleep" for a little bit, so things don't' move too fast, you can certainly play around with this value  and pick one you like
## 3. **adding a space** in between words:
```python
    if pin_logo.is_touched():
        message_buffer += " "
        display.show("-")  # visual feedback for space (hyphen) 
        sleep(300)
```
- **`pin_logo.is_touched()`**: If you touch the gold logo briefly (on micro:bit V2), 
- `message_buffer += " "`   adds a space to the message buffer (where you collect all letters to make your message).
	- remember `+=` is like saying add a space to whatever is already in `message_buffer` and then stick all of that back into the container (variable) `message_buffer`
- so you can press the logo after each word:
	- press A or B to create letters, shake to move each letter to the message buffer and don't forget to touch the logo to create a space after each word (note: make sure you only press the logo briefly, a long press I think will add a few spaces)
## 4. **send  your message**:
- **`button_a.is_pressed() and button_b.is_pressed()`**: If both buttons are held at once, it triggers the **`radio.send(message_buffer)`** command, transmitting your text (which you collected in the `message_buffer`) to any other micro:bit nearby (that is on the same group).
- Note: did you spot the difference? 
	- `was_pressed()` means "did it get clicked since last time?" and `is_pressed()` means "is it held down right now?" 
	- That difference is why a single button types one symbol, and both buttons together can mean send.
```python
if button_a.is_pressed() and button_b.is_pressed():
	if message_buffer != "":        #quick check to make sure message is NOT empty
		radio.send(message_buffer)  #send the message
		display.scroll("SENT")      #display that it is sent
		message_buffer = ""         #clear the message_buffer ready for the next message
		current_letter = ""         #clear the current_letter ready for the next
		display.clear()             #clear the display
		sleep(500)                  # create a little break
```
## 5. **Receiving:**
- to receive a message we have this code:
```python
# RECEIVE
incoming = radio.receive()   # Constantly checks if another micro:bit has sent a message.
if incoming:                 # If a message arrives, 
    display.scroll(incoming) # it scrolls the text across the display.

sleep(50)                     # A tiny pause so it's not too fast.
```







