#! /bin/bash

mysql_host="127.0.0.1"
mysql_passwd="xxxxxx"

# account 用户信息
account="SELECT a.user_id,a.telephone,a.insur_cnt, u.status, a.up_ts FROM account a left join update_id_info u on u.user_id = a.user_id"
mysql -h"${mysql_host}" -uroot -p"${mysql_passwd}" -Dinsur_wallet -e "${account}" > "account.txt"

invite_info="select *  from invite_info"
mysql -h"${mysql_host}" -uroot -p"${mysql_passwd}" -Dinsur_wallet -e "${invite_info}" > "invite_info.txt";

