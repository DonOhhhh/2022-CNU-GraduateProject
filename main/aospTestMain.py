class modifyManager():#modify
    def __init__(self):
        self.code = 'testtesttest\n'
        pass

    # os.walk() 함수를 사용하면 편합니다.
    def getFilePath(self,fname):
        return None

    # abcAfter.txt의 2번째 줄에 code를 삽입해주시면 됩니다.
    # 만약 수정이 잘못되었다면 abcBefore에서 복사해서 다시 수정하시면 됩니다.
    # ubuntu에서도 진행해보시고 실제 aosp 코드에 주석으로 코드를 삽입했을 때 권한문제가 없는지도 확인해주세요
    def modify(self,fpath):
        return None


class buildManager():
    def __init__(self):
        pass

    # 쉘 스크립트로 빌드하고 emulator 올리는 것까지 작성해주세요
    # 권한 문제가 없는지 확인해주세요
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
