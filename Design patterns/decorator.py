"""

Any two objects of the Key class (and only them) change the way the result is displayed: instead of "The key was
pressed" it should read "The key was pressed!" (exclamation mark at the end of the text), and replace the second
method with "key was pressed?" (question mark at the end of the text).

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
    def __init__(self, key, index):
        self.key = key
        self.index = index
        
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            old = func(self)
            if self.index == 0:
                print(old + '!')
            elif self.index == 1:
                print(old + '?')
            else:
                print(old)
        return wrapper
            
    @decorator
    def update(self):
        if Keyboard.get_instance() == self.key:
            return 'Key pressed: {}'.format(self.key)
            


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
    keys = [Key('Q', i) for i in range(0, 5)]
    for key in keys:
        pub.register(key)

    p = Keyboard('Q')
    
    pub.dispatch()
    

