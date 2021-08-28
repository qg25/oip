import sys
import detect

class checkCondition:
    def __init__(self):
        pass

    def checkCleanliness(self):
        count = detect.main()
        print("check count: ", count)
        result = True
        if count >= 1:
            return True
        else:
            return False

    def checkDryness(self):
        print("Drying")
        return False


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
