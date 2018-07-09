import asyncio
import aiohttp
import time


# 通过async def定义的函数是原生的协程对象
async def download(url):
    print("get: %s" % url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            print(resp.text)


async def main():
    start = time.time()
    await asyncio.wait([
        download("http://www.163.com"),
        download("http://www.mi.com"),
        download("http://www.baidu.com")])
    end = time.time()
    print("Complete in {} seconds".format(end - start))

# 获取一个消息循环
loop = asyncio.get_event_loop()
# 把携程函数放入
loop.run_until_complete(main())
loop.close()
