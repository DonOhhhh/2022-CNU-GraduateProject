import frida, sys, os, json

class modifyManager():
    def __init__(self):
        self.imp = "import java.net.*;\n"
        #UDP 통신 코드
        self.UDPSock = 'try {\nbyte[] buffer = String.valueOf(System.currentTimeMillis()).getBytes();\nnew DatagramSocket(5000).send(new DatagramPacket(buffer, buffer.length, InetAddress.getByName("10.0.2.2"), 5001));\n} catch (IOException e) { }\n'
        pass

    def getJsonObjects(self, jfname):#{fname} json 파일을 읽어 객체를 반환
        #json은 파일명 및 각 파일별 소켓 객체 생성 위치, 소켓 통신 삽입 메시지 및 위치를 저장
        #{filename1 : {"socketObject" : [함수 이름, 위치], "insertCode" : {함수 이름1: [메시지1, 위치], 함수 이름2 : [메시지2, 위치], ...}},...}
        #함수 이름은 코드 내에서 해당 함수를 찾아 위치 값(0,1)에 따라 해당 문자열 전/후에 통신코드 삽입
        #socketObject는 소켓 객체 생성 위치를 저장하고, insertCode는 배열로 outstream을 삽입할 위치와 전송할 메시지를 저장
        #배열 내부에는 튜플로 위치와 메시지 저장
        with open(jfname) as f:
            data = json.load(f)
        return data

    # os.walk() 함수를 사용하면 편합니다.
    def getFilePath(self,fname):#fname 위치 찾아 문자열로 반환
        print("파일 경로 탐색을 시작합니다")
        root_dir = "/"
        for (root, dirs, files) in os.walk(root_dir):
            for walkin_fname in files:
                # print(root + fname)
                if walkin_fname == fname: #일치하는 파일 발견
                    print("파일 경로를 찾았습니다")
                    return root + "/" + fname #경로 + fname으로 파일 전체 상대 경로 반환
        print("파일 경로 탐색에 실패하였습니다")
        return None #None 반환시 파일 없는것으로 판단

    # abcAfter.txt의 2번째 줄에 code를 삽입해주시면 됩니다.
    # 만약 수정이 잘못되었다면 abcBefore에서 복사해서 다시 수정하시면 됩니다.
    # ubuntu에서도 진행해보시고 실제 aosp 코드에 주석으로 코드를 삽입했을 때 권한문제가 없는지도 확인해주세요
    def modify(self): #ZygoteInit.java 파일에 소켓 통신을 통한 성능측정 코드 추가

        data = modifyManager.getJsonObjects(self, "modify.json")
        fNames = list(data.keys())#json 내 각 파일별로 코드 수정 수행

        for fileName in fNames:
            fpath = self.getFilePath(fileName)
            if fpath == None:
                print(f"{fileName} 파일이 존재하지 않습니다.")
                continue
            else:
                print(f'{fileName} 경로: {fpath}')

            print(f"{fileName} 코드 수정을 시작합니다")

            with open(fpath, 'r') as fr: #파일 읽기모드로 열기
                codelines = fr.readlines() #파일 읽어와 배열 저장
            fr.close()

            with open(f"{fileName}.backup", 'w') as fb:#백업용 파일 생성
                for line in codelines:
                    fb.write(line)#백업

            print(f"{fileName} 파일이 현재 폴더에 백업되었습니다.")
            fb.close()

            import_inserted = False #import문 삽입 여부

            #현재 파일 json
            insertCode = data[fileName]["insertCode"]#소켓통신 코드, 메시지
            targetLines = list(insertCode.keys())#코드 삽입 위치(문자열)

            with open(fpath, 'w') as f:
                for i in range(len(codelines)):#읽은 파일 한줄씩 비교/ 쓰기
                    originalCodeInserted = False  # 원본 코드 삽입되었는지

                    if not import_inserted:
                        if "import" in codelines[i]:
                            ###소켓 통신 위한 파일 import 추가
                            print("import문 삽입")
                            f.write(self.imp)  # 서버로 전송만을 위한 ouput 스트림
                            f.write(codelines[i])  # 기존 파일 코드 작성
                            import_inserted = True
                            continue

                    for j in range(len(targetLines)):
                        if targetLines[j] in codelines[i]:
                            originalCodeInserted = True
                            print(f'{insertCode[targetLines[j]][0]} 메시지 삽입')
                            if int(insertCode[targetLines[j]][1]) == 0:
                                f.write(self.UDPSock)
                                f.write(codelines[i])  # 기존 파일 코드 작성
                            else:
                                f.write(codelines[i])  # 기존 파일 코드 작성
                                f.write(self.UDPSock)

                    if not originalCodeInserted:
                        f.write(codelines[i]) #기존 파일 코드 작성

            f.close()


        return None


class buildManager():
    def __init__(self):
        self.file = "Android.bp"
        self.path = ""
        self.buildAOSP()

    def pathFinder(self):
        root_dir = "/home/"
        for root, dirs, files in os.walk(root_dir):
            for fn in files:
                if fn == self.file:
                    return root+"/"
        return None

    # 쉘 스크립트로 빌드하고 emulator 올리는 것까지 작성해주세요
    # 권한 문제가 없는지 확인해주세요
    def buildAOSP(self):
        arg1 = self.pathFinder()
        while True:
            option = input("Select option <1: build  2: no build>: ")
            if option=="1":
                arg2 = int(1)
            elif option=="0":
                arg2 = int(0)
            else:
                print("try again, Not exist option.")
        sp.Popen(["./buildScript.sh %s %d" % (arg1, arg2)], shell=True)


class performanceManager():
    def __init__(self):
        self.message = ''
        self.className = ''
        self.methodName = ''
        self.Hook_package = ''
        self.data = []
        self.device = frida.get_usb_device(timeout=10)
        self.measureExecTime()

    def on_message(self, message, data):
        if message['type'] == 'send':
            self.message = message['payload']
            self.data.append(f'package : {self.Hook_package}, class : {self.className}, method : {self.methodName}, exec_time: {self.message}s')
            print(self.data[-1])

    def get_pid(self,Hook_package):
        pid = self.device.spawn([Hook_package])
        return pid

    def measureExecTime(self):
        try:
            # 작성된 후킹 스크립트 코드 로드 후 프로세스에 연결
            # Hooking 하는 대상 패키지 이름(앱의 본명)
            # "kr.ac.cnu.computer.homework10"
            self.Hook_package = input('Hooking 하는 대상 패키지 이름(앱의 본명): ')
            # self.Hook_package = 'kr.ac.cnu.computer.homework10'
            pid = self.get_pid(self.Hook_package)
            print("App is starting.. pid:{}".format(pid))
            process = self.device.attach(pid)
            self.device.resume(pid)

            # android.media.MediaPlayer
            self.className = input('Hooking 하고자 하는 Class Name: ')
            # self.className = 'android.media.MediaPlayer'
            # start
            self.methodName = input('Hooking 하고자 하는 Method Name: ')
            # self.methodName = 'start'

            # 후킹 JS 코드
            jscode = """
            Java.perform(function() {
                var classObj = Java.use("%s");
                classObj.%s.implementation = function() {
                    var nStart = new Date().getTime();
                    var retval = this.%s();
                    var nEnd =  new Date().getTime();
                    var nDiff = nEnd - nStart;
                    send(nDiff / 1000.0);
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
        except KeyboardInterrupt:
            print('\nWriting result on result.txt')
            with open('result.txt','a') as f:
                for d in self.data:
                    f.write(d+'\n')
        except Exception as e:
            print(e)



def main():
    print('1. modifyManager')
    print('2. buildManager')
    print('3. performanceManager')
    n = int(input('input number to test:'))

    if n == 1:
        obj = modifyManager()
        obj.modify()
    elif n == 2:
        obj = buildManager()
    elif n == 3:
        obj = performanceManager()


if __name__ == '__main__':
    main()