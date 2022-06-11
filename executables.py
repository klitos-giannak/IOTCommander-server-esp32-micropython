
def testString(myText):
    print("Command 'testString' successful. Received: " + myText)

def testInt(myInt):
    print("Command 'testInt' successful. Received: " + str(myInt))
    
def testFloat(myFloat):
    print("Command 'testFloat' successful. Received: " + str(myFloat))

def testBoolean(myBoolean):
    print("Command 'testBoolean' successful. Received: " + str(myBoolean))
    
def testAllTypes(myText, myFloat, myInt, myBoolean):
    print("Command 'testAllTypes' successful. Received: " + myText + ", " + str(myInt) + ", " + str(myFloat) + ", " + str(myBoolean))

def testNoParams():
    print("Command 'testNoParams' successful.")

