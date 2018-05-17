from collections import defaultdict
from datetime import datetime

import pymysql
from rediscluster import StrictRedisCluster

redis_host = [{'host': '127.0.0.1', 'port': 7000}]

redis = StrictRedisCluster(startup_nodes=redis_host, decode_responses=True)

saveFile = open("user_info.txt", "w")
today = datetime.now()

zombie = set()
account_dict = defaultdict(dict)
invite_dict = defaultdict(list)

config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'xxxxxx',
    'db': 'insur_wallet_db',
    'cursorclass': pymysql.cursors.DictCursor,
}
connection = pymysql.connect(**config)
cursor = connection.cursor()


def fetchone(sql, *args):
    cursor.execute(sql, args)
    return cursor.fetchone()


def fetchall(sql, *args):
    cursor.execute(sql, args)
    return cursor.fetchall()


def load_invite():
    """加载用户邀请关系"""
    with open("invite_info.txt") as f:
        f.readline()
        for line in f:
            # ['id', 'inviter_id', 'invitee_id', 'invite_ts']
            line = line.strip().split()
            invite_dict[line[1]].append(line[2])
        print("load_invite: ok")


def load_account():
    """加载用户"""
    with open("account.txt") as f:
        f.readline()
        for line in f:
            line = line.strip().split()
            if line[4] == "NULL":
                zombie.add(line[0])
                continue
            account_dict[line[0]].setdefault("user_id", line[0])
            account_dict[line[0]].setdefault("telephone", line[1])
            account_dict[line[0]].setdefault("insur_cnt", line[2])
            account_dict[line[0]].setdefault("status", line[3])
            account_dict[line[0]].setdefault("up_ts", line[4])
            account_dict[line[0]].setdefault(
                "invite_nums", len(invite_dict[line[0]]))  # 邀请好友人数
        print("load_account: ok")


def sumList(array):
    array = [int(i) for i in array if i]
    return sum(array)


def w2txt():
    for vals in account_dict.values():
        string = ""
        for key, val in vals.items():
            string += "%s %s " % (key, val)
        saveFile.write(string[:-1] + "\r\n")


def auth_level(status):
    """用户实名认证等级"""
    if status == "NULL":
        return 0
    level = 0
    status = int(status)
    if 0 <= status < 5:
        if status == 3:
            level = 2
        else:
            level = 1
    return level


def up_attr(uid):
        no_active = 0; no_auth = 0
        bp = sumList(redis.hvals("INSURCHAIN_basics_power_table_%s" % uid)) # 基础算力
        account_dict[uid].setdefault("basics_power", bp)

        ap = sumList(redis.hvals("INSURCHAIN_append_power_table_%s" % uid)) # 附加算力
        account_dict[uid].setdefault("append_power", ap)

        to = fetchone("select sum(amount) to_total from transfer where to_user_id = %s" % uid) # 转入总额
        if not to:
            to_total = 0
        else:
            to_total = to.get('to_total', 0)
        account_dict[uid].setdefault("to_total", to_total)

        fro = fetchone("select sum(amount) from_total from transfer where from_user_id = %s" % uid) # 转出总额
        if not fro:
            from_total = 0
        else:
            from_total = fro.get('from_total', 0)
        account_dict[uid].setdefault("from_total", from_total)

        zr = fetchone("select  to_user_id as uid, count(to_user_id) as to_num from transfer where to_user_id = %s" % uid) # 转入次数
        if not zr:
            to_num = 0
        else:
            to_num = zr.get('to_num', 0)
        account_dict[uid].setdefault("to_num", to_num)

        zc = fetchone("select  from_user_id as uid, count(from_user_id) as from_num from transfer where from_user_id = %s" % uid) # 转出次数
        if not zc:
            from_num = 0
        else:
            from_num = zc.get('from_num', 0)
        account_dict[uid].setdefault("from_num", from_num)

        # 获取邀请用户list
        for id in invite_dict.get(uid):
            if id in zombie:   # 是否僵尸
                no_active += 1
                no_auth += 1
                continue
            upts = datetime.strptime(account_dict[id].get("up_ts"), "%Y-%m-%d")
            if (today - upts).days > 20:
                no_active += 1
            if not auth_level(account_dict[id].get("status")):
                no_auth += 1
        account_dict[uid].setdefault("no_active", no_active)    # 没有激活
        account_dict[uid].setdefault("no_auth", no_auth)        # 没有认证

def run():
    load_invite()
    load_account()
    for i, uid in enumerate(account_dict):
        print("第{}位".format(i))
        up_attr(uid)
    w2txt()

if __name__ == '__main__':
    run()
