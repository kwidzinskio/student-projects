"""

Write a program using the abstract factory pattern to solve the following problem.

There are 2 integers: m, n, m <= n, m, n> = 0 and the logical variable sort. Optimally generate a random m-element
substring of 1,2,3, ... n, such that no number repeats itself in this substring. If sort is true, the result string
should be sorted. Return the result string in an array.

Example: m = 2, n = 5, example result: 3.5

The problem can be solved with 3 algorithms, but their number may change in the future. Each of the algorithms is better
suited to a specific set of m and n numbers and the logical variable sort (determine by yourself which algorithm is
best suited to solve the problem for given values ​​of m, n, sort).

"""



from __future__ import annotations
from abc import ABC, abstractmethod
import numpy as np
import random


class AbstractFactory(ABC):
    @abstractmethod
    def create_substring(self) -> AbstractSubstring:
        pass


class ConcreteFactoryClassic(AbstractFactory):
    def create_substring(self) -> AbstractSubstring:
        return ConcreteSubstringClassic()


class ConcreteFactoryTest(AbstractFactory):
    def create_substring(self) -> AbstractSubstring:
        return ConcreteSubstringTest()
    
    
class ConcreteFactoryIntermix(AbstractFactory):
    def create_substring(self) -> AbstractSubstring:
        return ConcreteSubstringIntermix()
    

class AbstractSubstring(ABC):
    @abstractmethod
    def define(self):
        pass


class ConcreteSubstringClassic(AbstractSubstring):
    def define(self, sort):
        self.n = n
        self.m = m
        self.sort = sort
        self.substring = []
        
        i = 0
        while i < m:
            if i == 0:
                x = np.random.randint(1, n+1)
                self.substring.append(x)
                i += 1
            else:
                x = np.random.randint(1, n+1)
                if x in self.substring:
                    pass
                else:
                    self.substring.append(x)
                    i += 1
        if sort:
           self.substring.sort()
        return self.substring
        
        
class ConcreteSubstringTest(AbstractSubstring):
    def define(self, sort):
        self.n = n
        self.m = m
        self.substring = []
        choice = m
        left = n
        
        i = 0
        for i in range(1, n+1):
            p = choice / left
            los = random.uniform(0, 1)
            if p > los:
                self.substring.append(i)
                choice = choice - 1
            left = left - 1
        return self.substring
    
    
class ConcreteSubstringIntermix(AbstractSubstring):
    def define(self, sort):
        self.n = n
        self.m = m
        self.substring = []
        T = [i for i in range(1, n+1)]
        
        i = 0
        for i in range(m):
            x = np.random.randint(0, n)
            a = T[i]
            b = T[x]
            T[i] = b
            T[x] = a
           
        self.substring = T[:m]  
        if sort:
            self.substring.sort()
        return self.substring


def client_code(factory: AbstractFactory, sort):
    product = factory.create_substring()
    return product.define(sort)
    


if __name__ == "__main__":
    
    i = 0
    n = 10
    m = 3
    sort = True
    available_methods = [ConcreteFactoryClassic(), ConcreteFactoryTest(), ConcreteFactoryIntermix()]
    
    choice = input("Optimize method? (y/n) ")
    if choice == 'n':
        for i in range(3):
            print("Output from factory {}:".format(i+1))
            SUBSTRING = client_code(available_methods[i], sort)
            print(SUBSTRING)
    if choice == 'y':
        if not sort:
            if m > 0.05*n:
                i = 2
            else:
                i = 0
        if sort:
            if m > 0.05*n:
                if n > 100000:
                    i = 2
                else:
                    i = 1
            else: 
               i = 0
        SUBSTRING = client_code(available_methods[i], sort)
        print("Output from factory {}:".format(i+1))
        print(SUBSTRING[:10])
                
            
    

    

