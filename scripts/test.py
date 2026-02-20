import time
import os
import itertools

# Frames van een draaiende "a"
frames = [
    "   a   \n"
    "       \n"
    "       ",

    "      \n"
    "     a \n"
    "      ",

    "       \n"
    "       \n"
    "   a   ",

    "      \n"
    " a     \n"
    "      ",
]

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

try:
    for frame in itertools.cycle(frames):
        clear()
        print(frame)
        time.sleep(0.2)
except KeyboardInterrupt:
    clear()
    print("Animatie gestopt.")