#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
import time
import sys
import win32pipe, win32file, pywintypes
import threading

numBuf = 3
stop = False
class Bufor:
    
    _buf = [0] * numBuf
    posWrite= -1
    posRead = -1



    def get(self):
        
        while self.posWrite == -1 or \
              self.posRead == self.posWrite:
            time.sleep(0.001)

        self.posRead += 1
        self.posRead %= numBuf

        return self._buf[self.posRead]

    def set(self, val):
        
        self.posWrite += 1
        self.posWrite %= numBuf
        self._buf[self.posWrite] = val
        
def pipeServer():
    
    print("pipe server")
    count = 0
    pipe = win32pipe.CreateNamedPipe(
        r'\\.\pipe\Foo',
        win32pipe.PIPE_ACCESS_DUPLEX,
        win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
        1, 65536, 65536,
        0,
        None)
    try:
        print("waiting for client")
        win32pipe.ConnectNamedPipe(pipe, None)
        print("got client")

        while count < 100:
            print("writing message", count)
            some_data = str.encode(f"{count}")
            win32file.WriteFile(pipe, some_data)
            time.sleep(1)
            count += 1
        print("finished now")
    finally:
        win32file.CloseHandle(pipe)


def pipeClient():
    
    print("pipe client")
    quit = False

    while not quit:
        try:
            handle = win32file.CreateFile(
                r'\\.\pipe\Foo',
                win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                0,
                None,
                win32file.OPEN_EXISTING,
                0,
                None
            )
            res = win32pipe.SetNamedPipeHandleState(handle, win32pipe.PIPE_READMODE_MESSAGE, None, None)
            if res == 0:
                print("SetNamedPipeHandleState return code:", res)
            while True:
                bufor = Bufor()
                thread = threading.Thread(target=reader, args=(bufor, handle))
                thread.start()
                try:
                    printer(bufor)
                except KeyboardInterrupt:
                    stop = True
                    thread.join()
        except pywintypes.error as e:
            if e.args[0] == 2:
                print("no pipe, trying again in a sec")
                time.sleep(1)
            elif e.args[0] == 109:
                print("broken pipe, bye bye")
                quit = True

def printer(buf):
    
    while not stop:
        val = buf.get()
        print(val)
        time.sleep(1.5)
        
def reader(buf, handle):
    
    while not stop:
        resp = win32file.ReadFile(handle, 64*1024)
        if resp != "":
            for i in range(len(resp)):
                val = int(resp[1])
        buf.set(val)
        time.sleep(1)    

def main():

    print("Choose s or c as argument")
    user_choice = str(input())
    if user_choice == "s":
        pipeServer()
    elif user_choice == "c":
        pipeClient()
    else:
        print("Try again:")
        
if __name__ == '__main__':
    main()
