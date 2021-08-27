import sys

class checkCondition:
    def __init__(self):
        pass

    def checkCleanliness(self):
        print("Cleaning")
        pass

    def checkDryness(self):
        print("Drying")
        pass


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if (sys.argv[1] == "clean"):
            detection = checkCondition()
            checkCondition.checkCleanliness(detection)
        elif (sys.argv[1] == "dry"):
            detection = checkCondition()
            checkCondition.checkDryness(detection)
        else:
            print("Invalid Choice!!!")

    else:
        print("No argument found, 'clean' or 'dry'")
