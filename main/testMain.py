import unittest
import main.aospTestMain as atm


class MyTest(unittest.TestCase):
    def setUp(self):
        self.modify = atm.modifyManager()
        self.performance = atm.performanceManager()

    def test_modify(self):
        filePath = self.modify.getFilePath(fname="")
        self.assertEqual(filePath, "")
        with open(filePath, 'r') as f:
            data1 = f.read()
        # data1에 코드 삽입 추가
        #
        self.modify.modify(fpath=filePath)
        with open(filePath, 'r') as f:
            data2 = f.read()
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
