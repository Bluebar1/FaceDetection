import cv2
import sys
from modes.instant import runInstant
from modes.live import runLive 
from modes.offline import runOffline


"""
Takes input from command line using the input() function
Stored as list args[]
Passes args to given mode 
"""
args = []


mode = input('What mode would you like to use? Options: instant|live|offline \n : ')

if mode == 'instant':
    args.append(input('Enter an algorithm. Options: mtcnn|haar|retina \n : '))
    args.append(input('Enter the filename located in your data/images/input/ folder. Ex: test1.jpg \n : '))
    runInstant(args)
elif mode == 'live':
    args.append(input('Enter an algorithm. Options: mtcnn|haar|retina \n : '))
    runLive(args)
elif mode == 'offline':
    args.append(input('Enter an algorithm. Options: mtcnn|haar|retina \n : '))
    args.append(input('Enter the name of the dataset folder in data/images/input/. Example: ffhq \n : '))
    args.append(input('Enter a limit. For no limit type 0 \n : '))
    runOffline(args)
else:
     print(f'ERROR: "{mode}" is not a mode')





