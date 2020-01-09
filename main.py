from Comm import Comm
from inputs import get_gamepad
from inputs import get_key
import serial
import time
#test = serial.Serial('COM11', 9600, timeout = 1)

ser = Comm('/dev/ttyUSB0', 9600)


def main():
    controller = True
    try: # detects if a game controller is connected
        events = get_gamepad()
    except:
        print("No game controller found. Using keyboard.")
        controller = False
    x, y = 0, 0
    while True:
        if controller == True:
            x, y = getController(x, y)
            #time.sleep(5)
            break
        else:
            if ser.recieve_send_command_bool():
                while x == 0 and y == 0:
                    x, y = getKeyboard(x, y)
                print(x, y)
                ser.send_length(x, y)
        '''if x2 != x or y2 != y:
            if ser.recieve_send_command_bool():
            ser.send_length(x, y)'''

    return


def getControllerX():
    events = get_gamepad()
    for event in events:
        if event.code == 'ABS_X':
            return event.state


def getControllerY():
    events = get_gamepad()
    for event in events:
        if event.code == 'ABS_Y':
            return event.state


def getKeyboard(x, y):
    x, y = 0, 0
    keyboardEvents = get_key()

    for event in keyboardEvents:
        #print(event.ev_type, event.code, event.state)
        if event.state == 1 or event.state == 2:
            if event.code == 'KEY_W':
                x = 0.1
            elif event.code == 'KEY_S':
                x = -0.1
            elif event.code == 'KEY_D':
                y = 0.1
            elif event.code == 'KEY_A':
                y = -0.1
    return x, y


if __name__ == '__main__':
    main()
