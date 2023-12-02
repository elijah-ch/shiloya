import json
import time

import requests
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By  # 元素定位
from selenium.webdriver.support.ui import WebDriverWait  # 元素等待
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains


def requestgetcode():
    url = 'https://api.aaaaa-kj.com//open/getCode'
    data = {
        "phone": "15357955223"
    }
    return requests.post(url, json=data)


class OptModify():
    xydm = '91340100MA8PNXMBXM'
    phonenumber = '15357955223'
    pwd = 'ys123456'

    def __init__(self):
        opt = ChromeOptions()
        # opt.headless = True   # 程序测试稳定后，可采用无头模式提高工作效率
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def homepage(self):
        # 打开登陆页面
        self.driver.get(
            "https://tpass.anhui.chinatax.gov.cn:8443/#/login?redirect_uri=https%3A%2F%2Fetax.anhui.chinatax.gov.cn%2Fcas%2Fkxlogin&client_id=gcZa37Z93gjc424j95e2bcgccZ57d752&response_type=code")

    def loggin(self):
        try:
            # 输入企业信用代码
            tyshxydm = self.driver.find_element(By.XPATH,
                                                '//*[@id="app"]/div/div[1]/div[2]/div/div[2]/div[3]/div[2]/div/div[1]/div[1]/div/form/div[1]/div/div/div/div[1]/input')
            tyshxydm.send_keys(self.xydm)
            # 输入手机号
            phonenumber = self.driver.find_element(By.CSS_SELECTOR,
                                                   '#app > div > div.loginCls > div.mainCls > div > div.login_box > div.password_ddd > div.formContentE > div > div:nth-child(1) > div:nth-child(1) > div > form > div:nth-child(2) > div > div.el-row > div > input')
            phonenumber.send_keys(self.phonenumber)
            # 输入密码
            pwd = self.driver.find_element(By.XPATH,
                                           '//*[@id="app"]/div/div[1]/div[2]/div/div[2]/div[3]/div[2]/div/div[1]/div[1]/div/form/div[3]/div[1]/div/div[2]/div/input')
            pwd.send_keys(self.pwd)
            # 拖拽验证滑块
            slpblk = self.driver.find_element(By.CSS_SELECTOR,
                                              '#app > div > div.loginCls > div.mainCls > div > div.login_box > div.password_ddd > div.formContentE > div > div:nth-child(1) > div:nth-child(1) > div > form > div:nth-child(4) > div > div > div > div > div.handler.animate')
            ActionChains(self.driver).drag_and_drop_by_offset(slpblk, 400, 0).perform()
            #  点击登录按钮
            self.driver.find_element(By.CSS_SELECTOR,
                                     '#app > div > div.loginCls > div.mainCls > div > div.login_box > div.password_ddd > div.formContentE > div > div:nth-child(1) > div:nth-child(1) > div > form > div.el-row > div > button').click()
        except Exception as E:
            print(E)

    def smscheck(self):
        # 两次获取手机短信数量，如果短信数量增加，尝试获取验证码并检查，正确就填入验证码框登陆。
        try:
            countprim = json.loads(requestgetcode().content).get("data").get("count")
            self.driver.find_element(By.XPATH,
                                     '//*[@id="app"]/div/div[1]/div[2]/div/div[2]/div/div[3]/div/div[1]/div/div[3]/span').click()
            sendbtn = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH,
                 '//*[@id="app"]/div/div[1]/div[2]/div/div[2]/div/div[3]/div/div[2]/div/form/div[1]/div[2]/div/div/button/span')))
            sendbtn.click()

            chcode = None
            # 五分钟内每5秒轮询访问一次接口数据
            for i in range(60):
                time.sleep(5)
                rst = json.loads(requestgetcode().content).get("data")
                countnow = rst.get("count")
                if int(countnow) > int(countprim):
                    if rst.get("code"):
                        chcode = rst.get("code")
                        break

            if chcode:
                codelocator = '//*[@id="app"]/div/div[1]/div[2]/div/div[2]/div/div[3]/div/div[2]/div/form/div[1]/div[2]/div/div/div/input'
                self.driver.find_element(By.XPATH, codelocator).send_keys(chcode)
                logginbtnlct = '//*[@id="app"]/div/div[1]/div[2]/div/div[2]/div/div[3]/div/div[2]/div/form/div[2]/div/button'
                self.driver.find_element(By.XPATH, logginbtnlct).click()
            else:
                pass
        except Exception as E:
            print(E)

    def getCookies(self):
        try:
            cks = self.driver.get_cookies()
            with open("cookies.txt", "w", encoding="utf-8") as f:
                f.write(json.dumps(cks))
            self.driver.quit()
        except Exception as E:
            print(E)

    def relog(self):
        try:
            with open("cookies.txt", "r", encoding="utf-8") as f:
                cookie_list = json.loads(f.read())
            _url = 'https://etax.anhui.chinatax.gov.cn/home/portal'
            self.driver.get(_url)
            for cookie in cookie_list:
                cookie["domain"] = ".chinatax.gov.cn"
                self.driver.add_cookie(cookie)
            self.driver.get(_url)
        except Exception as E:
            print(E)
        # self.driver.refresh()
        # self.driver.get(_url)


if __name__ == "__main__":
    operator = OptModify()
    operator.homepage()
    time.sleep(2)
    operator.loggin()
    time.sleep(2)
    operator.smscheck()
    time.sleep(3)
    operator.getCookies()

    time.sleep(3)
    operator2 = OptModify()
    operator2.relog()
    # res = requestgetcode()
    # print(json.loads(res.content).get("data").get("count"))
