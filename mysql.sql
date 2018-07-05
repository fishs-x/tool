-- MySql 从withdraw表中指定id, user_id, create_ts 导入到user_balance中 其中 1, '充值' 是固定导入到flag, remark中
insert into user_balance (flag, remark, from_id, user_id, create_time) select 1, '充值', id, user_id, create_ts  from withdraw where type = 1
