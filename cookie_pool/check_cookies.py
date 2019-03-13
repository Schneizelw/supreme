import json
import requests
from redis_client import RedisClient
from requests.exceptions import ConnectionError

class Check():
    
    def __init__(self):
        fd = open("conf/website_config.json", "r")
        tmp = fd.read()
        data = json.loads(tmp)
        self.website = data["website_name"]
        self.check_url = data["check_url"]
        self.cookies_db = RedisClient('cookies', self.website)
        self.users_db = RedisClient('users', self.website)

    def single_check(self, username, cookie):
        pass

    def check(self):
        cookies = self.cookies_db.all_pairs()
        for user, cookie in cookies.items():
            self.single_check(user, cookie)


class QfangCheck(Check):
    
    def __init__(self):
        Check.__init__(self)

    def single_check(self, username, cookie):
        print("checking user:%s" % username)
        try:
            cookies = json.loads(cookie)
        except Exception as e:
            print("cookie type is error. user:%s" % username)
            self.cookies_db.delete(username)
            print("delete username %s cookie" % username)
            return
        try:
            response = requests.get(self.check_url, cookies=cookies, timeout=5, allow_redirects=False)
            if response.status_code == 200:
                print("Cookies valid: %s" % username)
            else:
                print("response code %s" % response.status_code)
                print("response header %s" % response.headers)
                self.cookie_db.delete(username)
        except ConnectionError as e:
            print("error : %s" % str(e))
            
            


