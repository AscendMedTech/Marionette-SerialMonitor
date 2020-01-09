import serial


class Comm:
    def __init__(self, comm_port, baud_rate):
        self.comm = serial.Serial(comm_port, baud_rate, timeout=1)
        return

    def close_serial(self):
        self.comm.close()
        return

    def open_serial(self, path):
        self.comm.close()
        self.comm = serial.Serial(path)
        return

    # write any message to serial
    def write_anything(self, message):
        msg = '\r\n' + message
        self.comm.write(msg.encode())
        return

    #read the most recent line sent over serial
    def read(self):
        msg = ''
        msg = self.comm.readline().decode().strip()
        print(msg)

    def send_length(self, x, y):
        msg = str(x) + ',' + str(y) + '\n'
        print(msg)
        self.comm.write(msg.encode())
        return

    # returns true if the bluepill is ready to recieve serial
    def recieve_send_command_bool(self):
        msg = ''
        #while msg == '':
        msg = self.comm.readline().decode().strip()
        print(msg)
        if msg == "send":
            return True
        return False

    ''' Gets the number of steps the stepper motors has turned and 
    converts that into inches of string pulled'''

    def recieve_steps(self):
        msg = ''
        # 0.9738929 inches reeled in/out per revolution
        step_ratio = 0.9738929

        # continually poll the serial bus until a message is recieved
        while msg == '' or msg == '\n':
            msg = self.comm.readline().decode().strip()
        msg = msg.split(',')
        if msg[0] != 'xy':
            return None
        xSteps, ySteps = msg[1:3]  # get index 1 and 2 of the list
        # 1600 steps in a revolution
        xInch, yInch = round((int(xSteps) * step_ratio) / 1600, 3), round(
            (int(ySteps) * step_ratio) / 1600, 3)
        return [int(xSteps), int(ySteps), xInch, yInch]
