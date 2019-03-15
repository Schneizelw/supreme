import json
import time
from selenium import webdriver
from redis_client import RedisClient
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Generator():
    
    def __init__(self, hostname):
        """
            connect redis get cookies map and username map
            and init browser(use selenium)
        """
        fd = open("conf/%s_website.json" % hostname, "r")
        tmp = fd.read()
        data = json.loads(tmp)
        self.website = data["website_name"]
        self.login_url = data["login_url"]
        self.cookies_db = RedisClient('cookies', self.website)
        self.users_db = RedisClient('users', self.website)
        self.users_db.set("15320347357","123456wyq")
        #self.users_db.set("15320343017","123456wyq")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1980,1980')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.wait = WebDriverWait(self.browser, 20)

    def get_cookie_dict(self, cookie):
        """
            return a cookie type is dict
        """
        res = {}
        for item in cookie:
            res[item["name"]] = item["value"]
        return res
    
    def open_lianjia(self, username, password):
        """
            open website,input username and password finally click it
        """
        self.browser.get(self.login_url)
        time.sleep(2)
        #点击登录
        button = self.browser.find_element_by_css_selector("a.btn-login.bounceIn.actLoginBtn")
        button.click()
        time.sleep(2)
        #使用密码账号登录
        button = self.browser.find_element_by_css_selector("#con_login_user_tel a.tologin")
        button.click()
        username_input = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input.the_input.topSpecial.users")
        ))
        password_input = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input.the_input.password")
        ))
        loginSubmit = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".li_btn a.login-user-btn")
        ))
        #输入账号密码login
        username_input.send_keys(username)
        password_input.send_keys(password)
        loginSubmit.click()
        time.sleep(3)

    def open_qfang(self, username, password):
        """
            open linajia,input username and password finally click it
        """
        self.browser.get(self.login_url)
        time.sleep(2)
        #点击登录
        button = self.browser.find_element_by_css_selector("#noLoginUser .nav-link a")
        button.click()
        time.sleep(2)
        #使用密码账号登录
        button = self.browser.find_element_by_css_selector("#loginTbs a:nth-child(2)")
        button.click()
        username_input = self.wait.until(EC.presence_of_element_located(
            (By.ID, "phone")
        ))
        password_input = self.wait.until(EC.presence_of_element_located(
            (By.ID, "password")
        ))
        loginSubmit = self.wait.until(EC.presence_of_element_located(
            (By.ID, "loginSubmit")
        ))
        #输入账号密码login
        username_input.send_keys(username)
        password_input.send_keys(password)
        loginSubmit.click()
        time.sleep(3)

    def new_cookie_qfang(self, username, password):
        """
            request website,login and get cookie
        """
        self.open_qfang(username, password)
        #确认是否登录成功
        check = self.browser.find_element_by_css_selector("#loginOrUserName a.frontUserName")
        text = check.text
        res = {}
        if text == "我的Q房":
            res["code"] = 1
            res["data"] = self.browser.get_cookies()
        else:
            res["code"] = -1
            res["data"] = "login failed"
        return res
 
            
    def new_cookie_lianjia(self, username, password):
        """
            request lianjia,login and get cookie
        """
        self.open_lianjia(username, password)
        check = self.browser.find_element_by_css_selector(".ti-hover .typeShowUser a:link")
        res = {}
        if "1" in check.text:
            res["code"] = 1
            res["data"] = self.browser.get_cookies()
        else:
            res["code"] = -1
            res["data"] = "login failed"
        return res
        
    def save_cookies(self):
        """
            get all cookies and save
        """
        all_users = self.users_db.all_users()
        done_users = self.cookies_db.all_users()
        if len(all_users) == len(done_users):
            print("No users can get cookie")
        for user in all_users:
            if user not in done_users:
                pw = self.users_db.get(user)
                print("get cookie user:%s,website:%s..." % (user, self.website) )
                if self.website == "qfang":
                    result = self.new_cookie_qfang(user, pw)
                elif self.website == "lianjia":
                    result =self.new_cookie_lianjia(user, pw)
                else:
                    print("not support this website")
                if result["code"] == 1:
                    cookie = self.get_cookie_dict(result["data"])
                    self.cookies_db.set(user, json.dumps(cookie))
                    print("save cookie %s succ" % cookie)
                elif result["code"] == -1:
                    print(result["data"])
                    self.users_db.delete(user)
                    print("delete account :%s" % user)
                else:
                    print(result["data"])             
                    
    def get_cookie(self):
        """
            get_cookie from redis
        """
        cookie = cookies_db.get_cookie()
        return cookie

    def close(self):
        self.browser.close()

if __name__ == "__main__":
    g = Generator("lianjia") 
    g.save_cookies()
    g.close()
