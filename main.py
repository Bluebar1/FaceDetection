import cv2
import sys
from modes.instant import runInstant
from modes.live import runLive 
from modes.offline import runOffline


if len(sys.argv) < 2:
    print('You did not specify a mode')
    quit()
    
args = sys.argv
mode = args[1]

if mode == 'instant':
    runInstant(args)
elif mode == 'live':
    runLive(args)
elif mode == 'offline':
    runOffline(args)
else:
     print(f'ERROR: "{mode}" is not a mode')





