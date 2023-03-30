import unittest
import sys

class MyTestResult(unittest.TestResult):

    def startTest(self, test):
        print("startTest")

    def startTestRun(self):
        print("startTestRun")

    def stopTest(self, test):
        print("stopTest")

    def stopTestRun(self):
        print("stopTestRun")


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        print("setUp")

    def test01(self):
        print("test01")

    def tearDown(self) -> None:
        print("tearDown")


if __name__ == '__main__':

    result = MyTestResult()
    # testcase = MyTestCase("test01")
    # testcase.run(result)

    # suite = unittest.TestSuite()
    # suite.addTest(MyTestCase("test01"))
    # suite.run(result)

    suite = unittest.TestSuite()
    suite.addTest(MyTestCase("test01"))
    runner = unittest.TextTestRunner()
    runner.run(suite)