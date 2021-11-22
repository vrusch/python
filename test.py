import datetime


ks_exp = '2021-11-23 13:42:25'
ks_exp = datetime.datetime.strptime(ks_exp, '%Y-%m-%d %H:%M:%S')
ks_exp_check = ks_exp - datetime.timedelta(minutes=15)
if datetime.datetime.now() <= ks_exp_check:
    print(ks_exp)
    print(ks_exp_check)