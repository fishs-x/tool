import unittest
from tests.testBase import *


class TestUser(TestBase):

    @staticmethod
    @http_post("/api/v1/login/imgCode")
    def test_imgCode(res):
        """获取图片验证码"""
        Test.assertEqual(0, res.get("state"))

    @staticmethod
    @http_get("/api/v2/earnings")
    def test_earnings(res):
        """昨日收益"""
        Test.assertEqual(0, res.get("state"))

    @staticmethod
    @http_get("/api/v2/minefield")
    def test_minefield(res):
        """我的矿场"""
        Test.assertEqual(0, res.get("state"))


if __name__ == '__main__':
    unittest.main()
