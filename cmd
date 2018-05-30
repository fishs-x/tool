# grep 查找当前目录下所有文件包含 /api/v1/bind/pushToken 且 token
grep -r -n "/api/v1/bind/pushToken" . | grep "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxOTAsImxvZ2luVGltZSI6IjIwMTgtMDQtMjUgMDM6NTM6MzIuMjUyODY3In0.euZziUhV8LidjRaj3Y6tKV-Lp4C57srvhYbQkQjyEU8"

# grep 查找当前目录下所有文件包含 /api/v1/bind/pushToken 或 token
grep -r -n -E "/api/v1/bind/pushToken|eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxOTAsImxvZ2luVGltZSI6IjIwMTgtMDQtMjUgMDM6NTM6MzIuMjUyODY3In0.euZziUhV8LidjRaj3Y6tKV-Lp4C57srvhYbQkQjyEU8" .
