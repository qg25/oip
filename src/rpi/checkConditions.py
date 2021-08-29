from detectStain import stainDetection
from detectDryness import dryDetection
import sys


DRY = 'Dry'

class checkCondition:
    def __init__(self):
        pass

    def checkCleanliness(self, fname):
        count = stainDetection(fname)
        print("check count: ", count)
        if count >= 1:
            return False
        return True

    def checkDryness(self, fname):
        result = dryDetection(fname)
        print("results: ", result)
        if result == DRY:
            return True
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
