def testCasePassed(userCode, definedCode, funcName, testCases):
    userFunction = getattr( __import__(userCode), funcName)
    definedFunction = getattr(__import__(definedCode), funcName)

    passCounter = 0
    failCounter = 0
    for eachCases in testCases:
        definedOutput = userFunction(eachCases)
        userOutput = definedFunction(eachCases)
        print(1)
        if definedOutput == userOutput:
            passCounter +=1
        else :
            failCounter +=1
    
    if passCounter > failCounter:
        return [1,passCounter,failCounter]
    else:
        return [0,passCounter,failCounter]

def singleTestCasePassed(userCode, definedCode, funcName, testCase):

    userFunction = getattr( __import__(userCode), funcName)
    definedFunction = getattr(__import__(definedCode), funcName)

    passCounter = 0
    failCounter = 0
    definedOutput = userFunction(testCase)
    userOutput = definedFunction(testCase)
    if definedOutput == userOutput:
        passCounter +=1
    else :
        failCounter +=1
    
    if passCounter > failCounter:
        return 1
    else:
        return 0
