"""

The Keyboard class object has a key_pressed variable (variable) that stores the last key pressed on the keyboard.
You must specify the attribute type yourself. The Keyboard class can only have one instance.

The Key class objects have a key attribute (variable), initialized with a selected value that corresponds to an
existing key on the keyboard. Each individual object waits for the value of its key variable to be equal to the
key_presed variable of the Keyboard object. If this happens, the object prints a message to the screen (for example,
"The key was pressed") and ends its activity.

Write a program (in python, C ++, ...) that implements the above functionality. (Create an object of the Keyboard
class and five objects of the Key class (k1, ..., k5) with any values ​​of the variable key (but different for
different objects), performing the tasks as above. Make sure that it is impossible to create another instance of the
Keyboard class .)

"""

import random
import string
from typing import List


class Keyboard:
    __instance = None
        
    def __init__(self, key_pressed):
        if Keyboard.__instance:
            raise Exception("Singleton cannot be instatiated more then once")
        else:
            self.key_pressed = key_pressed
            Keyboard.__instance = self
    
    @staticmethod
    def get_instance():
        if Keyboard.__instance is None:
            print('Error')
        else:
            return Keyboard.__instance.key_pressed


class Key:
    def __init__(self, key):
        self.key = key
        
    def update(self):
        if Keyboard.get_instance() == self.key:
            print('Key pressed: {}'.format(self.key))


class Publisher:
    def __init__(self):
        self.subscribers: List[Key] = []
        
    def register(self, who):
        if isinstance(who, Key):
            self.subscribers.append(who)
        else:
            raise TypeError(f'Expected {Key.__class__}, got {who.__class__}')
        
    def dispatch(self):
        for subscriber in self.subscribers:
            subscriber.update()   
        

if __name__ == '__main__':

    pub = Publisher()
    for key in random.sample(string.ascii_letters, 5):
        pub.register(Key(key))

    p = Keyboard(random.choice([sub.key for sub in pub.subscribers]))
    
    pub.dispatch()

