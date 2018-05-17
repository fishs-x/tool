#!/bin/bash
c=50
n=1000
domain=http://localhost:8888

token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMDUsImxvZ2luVGltZSI6IjIwMTgtMDMtMjQgMjI6MjE6NDguMjg5NjQ3In0.IP55U94gKZ3T-zUJcA8pfYPHOZHWWIkDk2elq7qH4gg"

# method 类型
if [ ! -n "$1" ] ;then
    echo "请输入API请求类型: get, post, put"
    exit
fi

# API path 地址
if [ ! -n "$2" ] ;then
    echo "请输入API path地址: /api/v1/user/login"
    exit
fi

# 并发数量
if [ -n "$3" ] ;then
    c=50
fi

# 总请求数量
if [ -n "$4" ] ;then
    n=1000
fi
echo "$n$c"

if [ $1 == "post" ]; then
    ab -c ${c} -n ${n} -H 'Authentication:'${token} -p './post.txt' "$token""$2"
elif [ $1 == "put" ]; then
    ab -c ${c} -n ${n} -H 'Authentication:'${token} -u './put.txt' "$token""$2"
else
    ab -c ${c} -n ${n} -H 'Authentication:'${token} "$token""$2"
fi
