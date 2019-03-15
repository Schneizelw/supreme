import json
import requests
from redis_client import RedisClient
from requests.exceptions import ConnectionError

class Check():
    
    def __init__(self, website):
        fd = open("conf/%s_website.json" % website, "r")
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


class WebCheck(Check):
    
    def __init__(self, website):
        Check.__init__(self, website)

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
            headers = {
                "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"
            }
            response = requests.get(self.check_url, cookies=cookies, timeout=5, allow_redirects=False, headers=headers)
            if response.status_code == 200:
                print("Cookies valid: %s" % username)
            else:
                print("response code %s" % response.status_code)
                print("response header %s" % response.headers)
                self.cookies_db.delete(username)
        except ConnectionError as e:
            print("error : %s" % str(e))
            
            
