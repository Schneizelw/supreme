service mongod start
# check 8052
nohup python3.6 ip_pool/ip_pool.py > /dev/null 2>&1 &
# check 8051
nohup python3.6 cookie_pool/cookie_pool.py > /dev/null 2>&1 &
# check 8050
docker run -d -p 8050:8050 scrapinghub/splash 
#check 6800
docker run -d -p 6800:6800 luvletterw/lianjia:RL_1.0.0
