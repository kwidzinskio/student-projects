'''
The program is designed to:

1. Loading data from a CSV file and initializing weights with random values.

2. Conducting the perceptron training on the application of the addition in the range [0,1]. Learning to superimpose
gradient. Plot a graph of RMSE versus epoch.
Perform a perceptron test (check its operation with new data).
Training and test files are provided
attached
combined in the summation-train.csv, summation-test.csv files.

3. Teach in addition in terms of (introduce data normalization).
   Repeat training and test for adding in application area.
   We have created our own scope for new program and test files.
'''

import numpy as np, csv
import matplotlib.pyplot as plt
import sys



def g(x):
    
    return x                                      # OPTIONAL
    # return np.tanh(x) 





def gprim(x):
  
    # return 1-np.tanh(x)*np.tanh(x)             # OPTIONAL
    return 1





def read_input_data(filename):

    X = []
    Y = []
    
    try:
        plik = open(filename, 'rt')
        dane = csv.reader(plik, delimiter=',')    
    except FileNotFoundError:
        print("Wrong file or file path")
        sys.exit(0)
        
    for rekord in dane:   
        try:
            a = [float(rekord[0]), float(rekord[1])]
            X.append(a)
            Y.append(float(rekord[2]))
            Nin = len(rekord) - 1
        except ValueError:
            print("Value error")
            sys.exit(0)   
            
    plik.close()
       
    return Nin, X, Y





def initialize_weights(Nin):

    weights = np.random.rand(Nin) 

    return weights
    




def train(epochs, X, Y, Nin, weights, eta):
    print()
    print('---------------')
    print('First training (float numbers)')
    Yout = []
    RMSEk = []
    epoch = []
    
    for k in range(epochs): # k - iterates over epoch
        epoch.append(k)
        RMSEi = 0
        
        for i in range(len(Xtrain)): # i - interates over vectors
            sumWeighted = 0
            
            for j in range(Nin): # j - iterates over inputs
                sumWeighted += weights[j] * Xtrain[i][j]
                
            Yout.append(g(sumWeighted))
            
            for j in range(Nin): # j - iterates over inputs
                weights[j] -= eta * gprim(sumWeighted) * (g(sumWeighted) - Ytrain[i]) * Xtrain[i][j]  
        
            
            
            RMSE = 0.5 * (g(sumWeighted) - (Ytrain[i]))**2  
            RMSEi += RMSE
            
        RMSEk.append(float(RMSEi))
            
            
    print()
    print('Yout:')
    print(Yout[-20:])
    print()
    print('Yexpected:')
    print(Ytrain[-20:])
    # print()                     OPTIONAL TO SHOW
    # print('RMSE')
    # print(RMSEk)
    print()
    print('Calculated weights:')
    print(weights)
    print()
        
        
    plt.plot(epoch, RMSEk)
    plt.savefig('RMSE.png', dpi=300, bbox_inches = "tight")
    plt.show()    
        
    return weights




def test(filename, weights):  
    print('---------------')
    print('First test (float numbers)')
    
    Nin, Xtest, Yexpected = read_input_data(filename)
    Yout = []


    for i in range(len(Xtest)): # i - interates over vectors
        sumWeighted = 0
        
        for j in range(Nin):
            sumWeighted += weights[j]*Xtest[i][j]
            
        Yout.append(g(sumWeighted)) # j - iterates over inputs
        
    print()    
    print("Yout:")
    print(Yout)
    print()
    print("Yexpected:")
    print(Yexpected)
        
    return Yout, Yexpected


def write_data_custom(Nin, filename):

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
    
        maxValueTrain = 0
        for i in range(10):
            a = np.random.randint(0, 20)
            b = np.random.randint(0, 20)
            output = a + b
            record = [a, b, output]
            if max(record) > maxValueTrain:
                maxValueTrain = max(record)
            writer.writerow(record) 

    return maxValueTrain


def train_custom(epochs, X, Y, Nin, weights, eta, maxValue):
    print()
    print('---------------')
    print('Second training (custom numbers)')
    
    Yout = []
    RMSEk = []
    epoch = []

    for i in range(len(X)):
        Y[i] = float(Y[i]/maxValue)
        for j in range(Nin):
            X[i][j] = float(X[i][j]/maxValue)

    
    for k in range(epochs): # k - iterate over epoch
        epoch.append(k)
        RMSEi = 0
        
        for i in range(len(Xtrain)): # i - interates over vectors
            sumWeighted = 0
            
            for j in range(Nin): # j - iterates over inputs
                sumWeighted += (weights[j] * Xtrain[i][j])
            
            for j in range(Nin): # j - iterates over inputs
                weights[j] -= eta * gprim(sumWeighted) * (g(sumWeighted) - Ytrain[i]) * Xtrain[i][j]  

            Yout.append(g(sumWeighted)*maxValue)
             
            RMSE = 0.5 * (g(sumWeighted) - (Ytrain[i]))**2  
            RMSEi += RMSE
            
        RMSEk.append(float(RMSEi))
    
    for i in range(len(X)):
        Ytrain[i] = float(Ytrain[i]*maxValue)
            
    print()
    print('Yout:')
    print(Yout[-10:])
    print()
    print('Yexpected:')
    print(Ytrain[-10:])
    # print()                                OPTIONAL TO SHOW
    # print('RMSE')
    # print(RMSEk)
    print()
    print('Calculated weights:')
    print(weights)
    
    return weights
        

def test_custom(filename, weights, maxValueTest):  
        print('---------------')
        print('Second test (custom numbers)')
        
        Nin, Xtest, Yexpected = read_input_data(filename)
        Yout = []
        
        for i in range(len(Xtest)):
            Yexpected[i] = float(Yexpected[i]/maxValueTest)
            for j in range(Nin):
                Xtest[i][j] = float(Xtest[i][j]/maxValueTest)
        
    
        for i in range(len(Xtest)): # i - interates over vectors
            sumWeighted = 0
            
            for j in range(Nin): # j - iterates over inputs
                sumWeighted += weights[j]*Xtest[i][j]
                
            Yout.append(g(sumWeighted)*maxValueTest) # j - iterates over inputs
        
        for i in range(len(Xtest)):
            Yexpected[i] = float(Yexpected[i]*maxValueTest)    
        
        print()    
        print("Yout:")
        print(Yout)
        print()
        print("Yexpected:")
        print(Yexpected)
            
        return Yout, Yexpected

    
if __name__ == '__main__':    


    # Read the training data
    Nin, Xtrain, Ytrain = read_input_data("summation-train.csv")

    # Initialize weights
    weights = initialize_weights(Nin)
    
    # Train of the perceptron
    epochs = 10000
    eta = 0.1
    weights = train(epochs, Xtrain, Ytrain, Nin, weights, eta)

    # Test of the perceptron with the trained weights
    Yout, Yexpected = test("summation-test.csv", weights)
    
    
    
    
    # Write the training data with custom numbers
    maxValueTrain = write_data_custom(Nin, "summation-train2.csv")

    # # Write the test data with custom numbers
    maxValueTest = write_data_custom(Nin, "summation-test2.csv")
    
    # Re-read the training data
    Nin, Xtrain, Ytrain = read_input_data("summation-train2.csv")
    
    # Initialize redifinied weights
    weights = initialize_weights(Nin)

    # Train of the perceptron on custom numbers 
    weights = train_custom(epochs, Xtrain, Ytrain, Nin, weights, eta, maxValueTrain)
    
    # Test of the perceptron with the trained weights
    Yout, Yexpected = test_custom("summation-test2.csv", weights, maxValueTest)
    
    
    












