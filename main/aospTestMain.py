class modifyManager():
    def __init__(self):
        pass

    def getFilePath(self,fname):
        return None

    def modify(self,fpath):
        return None


class buildManager():
    def __init__(self):
        pass

    def buildAOSP(self):
        return None


class performanceManager():
    def __init__(self):
        pass

    def getPID(self,packageName):
        return None

    def measureExecTime(self,pid,func):
        return None


def main():
    print('1. modifyManager')
    print('2. buildManager')
    print('3. performanceManager')
    n = input('input number to test:')

    if n == 1:
        obj = modifyManager()
    elif n == 2:
        obj = buildManager()
    elif n == 3:
        obj = performanceManager()


if __name__ == '__main__':
    main()
