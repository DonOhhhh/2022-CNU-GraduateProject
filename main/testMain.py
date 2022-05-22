import unittest
import main.aospTestMain as atm


class MyTest(unittest.TestCase):
    def setUp(self):
        self.modify = atm.modifyManager()
        self.performance = atm.performanceManager()

    def test_modify(self):
        filePath = self.modify.getFilePath(fname="abcBefore.txt")
        self.assertEqual(filePath, "")
        # abcBefore의 데이터의 2번째 줄에 code 삽입
        data1 = b''
        with open('abcBefore.txt', 'r') as f:
            for i,line in enumerate(f.readlines()):
                if i==2:
                    data1 += self.modify.code
                data1 += line
        # abcAfter 파일의 2번째 줄에 code 삽입
        self.modify.modify(fpath=filePath)
        with open(filePath, 'r') as f:
            data2 = f.read()
        # 미리 수정된 abcBefore와 modifyManager()가 수정한 abcAfter의 데이터를 비교
        self.assertEqual(data1, data2)

    def test_performance(self):
        pid = self.performance.getPID(packageName="")
        self.assertEqual(0, pid)
        time = self.performance.measureExecTime(pid, func="")
        self.assertIsNotNone(time)

    def test_runs(self):
        atm.modifyManager()
        atm.buildManager()
        atm.performanceManager()
