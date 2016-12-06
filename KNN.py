import csv
import random
import math

#Read in training set
importedTrain = []
importedTrain = csv.reader(open('SchoolkidsTrain.csv'))
importedTrain.__next__()

#Read in testing set
importedTest = []
importedTest = csv.reader(open('SchoolkidsTest.csv'))
importedTest.__next__()

#Hard coded value for k any value 1-458 works.
k = 3

#Map for normalization of data set
myMap = {'boy': 0, 'girl': 1,
        '1' : 0.0, '2' : 0.3333333, '3' : 0.6666666,
        '4' : 1.0,
        '5' : 0.5,'6' : 0.0,
        '7' : 0.0,'9' : 0.2, '10' : 0.4, '11' : 0.6, '12' : 0.8, '13' : 1.0,
        'Rural' : 0.0, 'Suburban': 0.5, 'Urban' : 1.0,
        'Sports' : 0.0, 'Grades' : 0.5, 'Popular' : 1.0}
        # 4 is set to 1 because it is used in Importance ranking and grades.
        # thus I inverted grades.

#Calculate Hamming Distance
def HamDistance(trainVal, testVal):
    if (trainVal == testVal):
        return 0
    else:
        return 1
#Calculate Eucilidian Distance, Also calls Hamming within
def EucDistance(trainVal, testVal):
    dist = math.sqrt((math.pow((trainVal[1]-trainVal[1]),2)) +
    (math.pow((testVal[2]-trainVal[2]),2)) +
    (math.pow((testVal[4]-trainVal[4]),2)) +
    (math.pow((testVal[5]-trainVal[5]),2)) +
    (math.pow((testVal[6]-trainVal[6]),2)) +
    (math.pow((testVal[7]-trainVal[7]),2)) +
    (HamDistance(training[0], testing[0])) +
    (HamDistance(training[3], testing[3])))

    return dist

training = []
#Read the training set, and place into arrays while normalizing
for row in importedTrain:
    tmpTrain = []
    for item in range(len(row)):
        if row[item] in myMap:
            tmpTrain.append(myMap[row[item]])
        else:
            tmpTrain.append(float(row[item]))
    training.append(tmpTrain) # add the row to the training data

testing = []
#Read the testing set, and place into arrays while normalizing
for row in importedTest:
    tmpTest = []
    for item in range(len(row)):
        if row[item] in myMap:
            tmpTest.append(myMap[row[item]])
        else:
            tmpTest.append(float(row[item]))
    testing.append(tmpTest) # add the row to the training data

goalCorrect = []
#Collect all correct Goals.
for i in testing:
    goalCorrect.append(i[8])

print("Correct : " + str(goalCorrect))

distance = []
#Determines the distances for all values in training set, also adds location in set
for i in range(len(testing)):
    tmpDist = []
    for j in range(len(training)):
        tdist = []
        tdist.append(j)
        tdist.append(EucDistance(training[j], testing[i]))
        tmpDist.append(tdist)
    distance.append(tmpDist)
sortedDist = []
for i in distance:
    sortedDist.append(sorted(i, key=lambda x: x[1]))

num = 0
topk = []
#Select the best k values from sorted list of distances
for i in sortedDist:
    num = 0
    tmpk = []
    for j in i:
        tmpk.append(j)
        num = num + 1
        if (num == k):
            break
    topk.append(tmpk)

topkValue = []
for i in topk:
    tmpVal = []
    for j in i:
        tmpVal.append(j[0])
    topkValue.append(tmpVal)

goalK = []
#Put all of the best k values into one array
for i in topkValue:
    goalTmp = []
    for j in i:
        arr = training[j]
        goalTmp.append(arr[8])
    goalK.append(goalTmp)


num = 0
goalGuess = []
#Determine best candidates for the set amount of k vlaues.
for i in goalK:
    sumTot = 0.0
    for j in i:
        sumTot = sumTot + j
    guess = sumTot/k

    if (guess == 0.0 or guess == 0.5 or guess == 1.0):
        goalGuess.append(guess)
    elif(guess < .249999):
        goalGuess.append(0.0)
    elif(guess > 0.750001):
        goalGuess.append(1.0)
    else:
        arr1 = topkValue[0]
        arr2 = topkValue[1]
        if ((arr1) == 0.0 and (arr2 == 0.0)):
            goalGuess.append(0.0)
        elif ((arr1) == 0.5 and (arr2 == 0.5)):
            goalGuess.append(0.5)
        elif ((arr1) == 1.0 and (arr2 == 1.0)):
            goalGuess.append(1.0)
        else:
            goalGuess.append(0.5)
    num = num + 1
print("Guess   : " + str(goalGuess))

correct = 0
wrong = 0
#Determine is answer is correct or not
for i in range(len(goalCorrect)):
    if (goalCorrect[i] == goalGuess[i]):
        correct = correct + 1
    else:
        wrong = wrong + 1

#General output
print("\n\nConfusion Matrix for k = "  + str(k) + "\n--------------------------")
print("Correct: " + str(correct))
print("Incorrect: " + str(wrong))
print("Percentage: " + str(correct/len(testing)*100) + "%")
