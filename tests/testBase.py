import unittest
import requests

# 本地域名
host = "http://localhost:8888"
private_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMDUsImxvZ2luVGltZSI6IjIwMTgtMDUtMTcgMTQ6MDE6MD" \
                "QuMDc2MjI0In0.yk4Ttv1H0aBDh8w2e7W1QdEAogkl2uZs1YZiuS5r5yM"
public_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjowLCJsb2dpblRpbWUiOiIyMDE4LTA0LTAyIDEzOjIxOjU0LjI" \
               "yNTM1MSJ9.jqxh_hqSujSClRg8-eTk6ghmVgANkBnGhAePk6AAEbk"


# GET 请求
def http_get(url, data=None, public=False):
    def wrapper(func):
        try:
            if public:
                token = public_token
            else:
                token = private_token
            response = requests.get(host + url, params=data, headers={"Authentication": token})
            print(host + url + ": ok")
            return func(response.json())
        except Exception as e:

            print("请求地址：" + host + url)
            print("错误信息: %s" % e)

    return wrapper


# POST 请求
def http_post(url, data=None, json=None, public=False):
    def wrapper(func):
        try:
            if public:
                token = public_token
            else:
                token = private_token
            response = requests.post(host + url, data=data, json=json, headers={"Authentication": token})
            print(host + url + ": ok")
            return func(response.json())
        except Exception as e:

            print("请求地址：" + host + url)
            print("错误信息: %s" % e)

    return wrapper


# PUT 请求
def http_put(url, data=None, public=False):
    def wrapper(func):
        try:
            if public:
                token = public_token
            else:
                token = private_token
            response = requests.put(host + url, data=data, headers={"Authentication": token})
            return func(response.json())
        except Exception as e:

            print("请求地址：" + host + url)
            print("错误信息: %s" % e)

    return wrapper


class TestBase(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        super(TestBase, self).__init__(methodName)

    def requets(self, methond, url, data=None, json=None, public=False, **kwargs):
        if public:
            token = public_token
        else:
            token = private_token
        methond = methond.lower()
        if methond == "get":
            kwargs.setdefault('allow_redirects', True)
            return requests.request(methond, host + url, params=data, headers={"Authentication": token}, **kwargs)
        else:
            return requests.request(methond, host + url, data=data, json=json, headers={"Authentication": token}, **kwargs)


Test = TestBase()
