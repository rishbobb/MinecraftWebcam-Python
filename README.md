This is the official repo for my video "Playing MINECRAFT with a WEBCAM" on YouTube
Original video can be found here: https://youtu.be/701TPxL0Skg
Reddit Post: https://www.reddit.com/r/Minecraft/comments/o7vjh5/playing_with_a_webcam_is_really_fun/

A few things before attempting to use this program:

1. You must have a Python 3 interpreter installed. Found here https://www.python.org/downloads/
2. A few packages must be installed prior to launching the program
    `pip install opencv-python`
    `pip install numpy`
    `pip install pyautogui`
    `pip install mediapipe`
    `pip install serial`
3. If you are on a (non Windows) Unix based system like MacOS or Linux, you will need a Raspberry Pi Pico to control the mouse input. To set up the Pico:
    Install CircuitPython by pressing and holding the button on the pi, while plugging it into the computer. A disk will be shown connected to your computer. Drag the UF2 to the disk named something close to "RPI". The CircuitPython UF2 can be found here https://circuitpython.org/board/raspberry_pi_pico/
    
    Install the necessary libraries on the Raspberry Pi Pico. They can be found in the "pilibs" folder in the repo. Just drag them to the Pi's "lib" folder. 
    
    Every time you plug your pico into your computer, run these 3 lines of code after connecting to the Pi's python REPL (`screen /dev/tty.usbmodem*` on MacOS)
        `import usb_hid`
        `from adafruit_hid.mouse import Mouse`
        `mouse = Mouse(usb_hid.devices)`
 
4. If you are using a Windows computer, install the following package
    `pip install pydirectinput`
   Also turn on Direct Input in Minecraft controls menu
5. To run the program, run `python mcwebcam.py` from the program folder if you are on a Unix based computer, or `python mcwebcamWin10.py` if you are on a Windows computer. Then quickly tab to Minecraft. TO STOP THE PROGRAM, ALT TAB/COMMAND TAB INTO CMD OR TERMINAL AND PRESS CTRL+C AT THE SAME TIME. YOU MIGHT NEED TO SPAM IT.
ALTERNATIVELY, MOVE THE MOUSE TO A CORNER OF THE SCREEN (0,0). I AM NOT RESPONSIBLE FOR INABILITY TO STOP THE PROGRAM.  

The control might either be too sensitive or not sensitive at all, you can change this by editing the respective python file in a text editor or IDE. The scale factors can be found on line 181 for mcwebcam.py and line 186 for mcwebcamWin10.py.

The setup for the python version is overly long and requires lots of technical knowledge to get set up, so I plan on making a more polished version in C++ in the near future. 

I AM NOT RESPONSIBLE FOR ANY HARM DONE TO PERSONS OR PROPERTY AS A RESULT OF THIS CODE. 
