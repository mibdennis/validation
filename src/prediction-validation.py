#!usr/bin/python

import sys
from math import floor
from decimal import Decimal

# analyze the arguments
if len(sys.argv) < 5:
    print("Arguments Error: windowFile actualFile predictedFile comparisonFile\n")
    sys.exit(1)
windowFile = sys.argv[1]
actualFile = sys.argv[2]
predictedFile = sys.argv[3]
comparisonFile = sys.argv[4]

# get the window size
fw = open(windowFile, 'r')
windowSize = int(fw.readline())
fw.close()
# get the first valid hour
fa = open(actualFile, 'r')
strTemp = fa.readline()
hourStart = int(strTemp.split('|')[0])
fa.close()


# calculate the absolute error for each hour
currentHour = 1
errorSum = 0
errorCount = 0
priceDict = {}
errorList = [(0, 0), ]
actualIndex = 0
predictedIndex = 0


# calculate the difference
with open(actualFile) as fa:
    with open(predictedFile) as fp:
        ActualStr2Read = True
        PredictedStr2Read = True
        while True:
            errorSum = Decimal(0)
            errorCount = 0
            # get the actual price for one hour
            if ActualStr2Read:
                ActualStr = fa.readline()
            while ActualStr:
                strList = ActualStr.split('|')
                # get the hour, stock name, price
                h = int(strList[0])
                stock = strList[1]
                # save the price using integer
                price = Decimal(strList[2])
                # write the price info into the dictionary
                if h == currentHour:
                    priceDict[stock] = price
                    actualIndex += 1
                    ActualStr = fa.readline()
                else:
                    ActualStr2Read = False
                    # end for current time
                    break
            # get the predicted price and directly calculate the absolute difference
            if PredictedStr2Read:
                PredictedStr = fp.readline()
            while PredictedStr:
                strList = PredictedStr.split('|')
                # get the hour, stock name, price
                h = int(strList[0])
                stock = strList[1]
                price = Decimal(strList[2])
                if h == currentHour:
                    # calculate the absolute difference info
                    errorCount += 1
                    errorSum += abs(price - priceDict[stock])
                    predictedIndex += 1
                    PredictedStr = fp.readline()
                else:
                    # end for current time
                    PredictedStr2Read = False
                    break
            # add the difference info of the current hour into the error list
            errorList.append((errorCount, errorSum))
            # get info for next hour
            currentHour += 1
            if (not ActualStr) and (not PredictedStr):
                break

# calculate the difference in special time window
# open the output file
fc = open(comparisonFile, 'w')
while hourStart <= len(errorList) - windowSize:
    errorCount = 0
    errorSum = Decimal(0)
    hourEnd = hourStart + windowSize - 1
    # collect all the diff info in current time window
    for i in range(hourStart, hourEnd + 1):
        errorCount += errorList[i][0]
        errorSum += errorList[i][1]
    # errorRes = floor((errorSum / errorCount + Decimal(0.005)) * 100)
    if errorCount > 0:
        # print the difference info
        resStr = '%d|%d|%0.2f\n' % (hourStart, hourEnd, (errorSum / errorCount))
    else:
        # if there is not any valid difference
        resStr = '%d|%d|NA\n' % (hourStart, hourEnd)
    fc.write(resStr)
    hourStart += 1
fc.close()




