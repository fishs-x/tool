#!/bin/bash
c=50
n=1000
domain=http://localhost:8888

token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMDUsImxvZ2luVGltZSI6IjIwMTgtMDUtMTcgMTQ6MDE6MDQuMDc2MjI0In0.yk4Ttv1H0aBDh8w2e7W1QdEAogkl2uZs1YZiuS5r5yM"

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
    c=$3
fi

# 总请求数量
if [ -n "$4" ] ;then
    n=$4
fi
echo "$n$c"

if [ $1 == "post" ]; then
    ab -c ${c} -n ${n} -H 'Authentication:'${token} -p './post.txt' "$domain""$2"
elif [ $1 == "put" ]; then
    ab -c ${c} -n ${n} -H 'Authentication:'${token} -u './put.txt' "$domain""$2"
else
    ab -c ${c} -n ${n} -H 'Authentication:'${token} "$domain""$2"
fi
