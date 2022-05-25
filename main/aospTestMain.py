import frida, sys

class modifyManager():
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
        self.message = ''
        self.className = ''
        self.methodName = ''
        self.Hook_package = ''
        self.device = frida.get_usb_device(timeout=10)
        self.measureExecTime()
        print(self.message)

    def on_message(self, message, data):
        if message['type'] == 'send':
            self.message = message['payload']
            print(f'package : {self.Hook_package}, class : {self.className}, method : {self.methodName}, exec_time: {self.message}s')

    def get_pid(self,Hook_package):
        pid = self.device.spawn([Hook_package])
        return pid

    def measureExecTime(self):
        try:
            # 작성된 후킹 스크립트 코드 로드 후 프로세스에 연결
            # Hooking 하는 대상 패키지 이름(앱의 본명)
            # "kr.ac.cnu.computer.homework10"
            # self.Hook_package = input('Hooking 하는 대상 패키지 이름(앱의 본명): ')
            self.Hook_package = 'kr.ac.cnu.computer.homework10'
            pid = self.get_pid(self.Hook_package)
            print("App is starting.. pid:{}".format(pid))
            process = self.device.attach(pid)
            self.device.resume(pid)

            # android.media.MediaPlayer
            # self.className = input('Hooking 하고자 하는 Class Name: ')
            self.className = 'android.media.MediaPlayer'
            # start
            # self.methodName = input('Hooking 하고자 하는 Method Name: ')
            self.methodName = 'start'

            # 후킹 JS 코드
            jscode = """
            Java.perform(function() {
                var classObj = Java.use("%s");
                classObj.%s.implementation = function() {
                    var nStart = new Date().getTime();
                    var retval = this.%s();
                    var nEnd =  new Date().getTime();
                    var nDiff = nEnd - nStart;
                    send(nDiff);
                    // console.log("Execute time: " + nDiff / 1000.0 + "(s)");
                    return retval;
                }
            });
            """ % (self.className, self.methodName, self.methodName)
            # print(jscode)
            script = process.create_script(jscode)
            script.on('message', self.on_message)
            print("[-] Running FR1DA!")
            script.load()
            sys.stdin.read()

        except Exception as e:
            print(e)


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
