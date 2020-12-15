#encoding:UTF-8

import  time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions   as ec
import time
import re
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.support.select import Select
import sys
# from selenium.common.exceptions import Timeouterror


class Log:
    def __init__(self):
        self.uid = '************'
        self.pwd = '************'
        self.i = 1
        self.fp = open(r" log posit", 'a+', encoding='utf8')



    def login(self):

            try:
                mobile = {"deviceName":"iPhone X"}
                option = webdriver.ChromeOptions()
                option.add_experimental_option('mobileEmulation', mobile)
                wd = webdriver.Chrome(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe',chrome_options=option)
                wd.set_window_size(600 , 800)
                wd.get("http://jksb.zzu.edu.cn/")
                wd.switch_to.frame(0)
                try:
                    wait(wd , 10 ,poll_frequency=0.5).until(ec.presence_of_element_located((By.NAME , 'uid'))).send_keys(self.uid)
                    time.sleep(0.5)
                    wait(wd , 10, poll_frequency=0.5).until(ec.visibility_of_element_located((By.NAME , "upw"))).send_keys(self.pwd)
                    time.sleep(0.5)
                    wait(wd , 10 , poll_frequency=0.5).until(ec.element_to_be_clickable((By.XPATH,".//div[@class='mt_3e']/input"))).submit()
                    time.sleep(0.5)

                except TimeoutException :
                    raise TimeoutError
                #切入frame
                wd.switch_to.frame('zzj_top_6s')
                time.sleep(0.5)
                init = wait(wd , 10 ,poll_frequency=0.5).until(ec.presence_of_element_located((By.XPATH , '//*[@id="bak_0"]/div[7]/span')))
                init_text  = init.text
                if '已经填报' in init_text:
                    self.fp.writelines(u"{} --> 打卡成功 -->已填报过了 无需重复填写  ^_^ \n ".format(time.strftime("%Y-%m-%d  %H : %M: %S", time.localtime())))
                    print(u"{}  已完成上报啦 ，无需重复啦 ^_^ ".format(time.strftime("%Y-%m-%d  %H : %M: %S", time.localtime())))
                    time.sleep(5)
                    sys.exit()
                else:
                    wait(wd ,10 ,poll_frequency=1).until(ec.element_to_be_clickable((By.XPATH , '//*[@id="bak_0"]/div[13]/div[5]/div[4]/span'))).click()  #第一页的 本人填报


                    wait(wd, 10, poll_frequency=0.5).until(ec.element_to_be_clickable((By.XPATH, '// *[ @ id = "bak_0"] / div[11] / div[4] / span'))).click() #第二页的提交表单

                    notis = wd.find_element_by_xpath('//*[@id="bak_0"]/div[2]').text

                    pattern = re.compile(r"感谢你今日上报健康状况！")
                    confirm = re.findall(pattern, notis)#
                    if confirm :
                        today = "{} --> 打卡成功 -->  ^_^\n".format(str(time.strftime(u"%Y-%m-%d  %H : %M: %S", time.localtime())))
                        print(today)
                        self.fp.writelines(today)
                        time.sleep(3)
                    else:
                        raise TimeoutError

            except (TimeoutError,SessionNotCreatedException):
                while 1:
                    if self.i <= 3:
                        error = u"{} --> 打卡失败 --> 已进行第{}次重试  (┬＿┬) \n".format(str(time.strftime(u"%Y-%m-%d  %H : %M: %S", time.localtime())) , str(self.i))
                        self.fp.writelines(error)
                        print(error)
                        self.i+=1
                        try:
                            wd.quit()

                        except:
                            pass
                        time.sleep(4)
                        self.login()
                    else:
                        error2 = u"{} --> 打卡失败 --> 已尝试{}次且未成功 ， 打卡失败请重试！！  (┬＿┬) \n".format(str(time.strftime(u"%Y-%m-%d  %H : %M: %S", time.localtime())) , str(self.i))
                        self.fp.writelines(error2)
                        print(error2)
                        break
            finally:
                try:
                    wd.quit()
                except:
                    pass
                self.fp.close()



if __name__ == "__main__":
    loging  = Log()
    loging.login()


