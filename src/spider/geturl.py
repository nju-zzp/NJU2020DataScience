import json
import time as t
from selenium import webdriver
import re
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys


wd = webdriver.Chrome(r"C:\Users\86159\Desktop\chromedriver.exe")

base = r"https://weibo.com/globaltimes?is_all=1&stat_date={0}{1}&page={2}#feedtop"


def nextpage():
    attemps=0
    succsess= 0
    while not succsess and attemps < 3:
        try:
            next_page = wd.find_elements_by_xpath(
                "//div[contains(@node-type,'feed_list_page')]//a[contains(text(),'下一页')]")
            front_page = wd.find_elements_by_xpath(
                "//div[contains(@node-type,'feed_list_page')]//a[contains(text(),'上一页')]")
            if len(next_page) == 0 and len(front_page) != 0:
                return False
            wd.execute_script('arguments[0].click();', next_page[0])
            t.sleep(2)
            succsess = 1
        except:
            attemps += 1
    return True

all_url = []
url = ''
for year in range(2019,2021):
    for month in range(1,13):
        if year == 2019 and month <12:
            continue
        if year == 2020 and month>=7:
            break

        url = base.format(str(year), str(month).zfill(2), 1)
        wd.get(url)
        while 1:
            eachpage = dict()

            # current = wd.current_window_handle
            t.sleep(1)
            attemps = 0
            while len(wd.find_elements_by_xpath("//div[contains(@node-type,'feed_list_page')]")) == 0:
                wd.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                attemps+=1
                if attemps == 6:
                    wd.refresh()
                    attemps=0
                t.sleep(1)


            succsess = 0
            attemps=0

            while not succsess and attemps<5:
                try:
                    wd.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                    t.sleep(1)
                    elements = wd.find_elements_by_xpath("//div[contains(@action-data,'cur_visible=0')]")
                    attemps=0
                    succsess=1
                except:
                    attemps+=1
            index = 0
            for eachwb in elements:
                index+=1
                content = ''

                button=[]
                forward_button = []
                content = wd.find_elements_by_xpath(
                    "//div[contains(@action-data,'cur_visible=0')][" + str(index) + "]//div[@class='WB_text W_f14']")[
                    0].text
                if "病毒" in content or "吹哨人" in content or "李文亮" in content  or "钟南山" in content or "抗疫" in content or "疫情" in content or "新冠" in content or "肺炎"  in content or "隔离" in content or "口罩" in content:
                    pass
                else:
                    continue

                attemps = 0
                while len(forward_button)==0:
                    attemps+=1
                    if attemps==4:
                        break
                    button = wd.find_elements_by_xpath("//div[contains(@action-data,'cur_visible=0')][" + str(
                        index) + "]//ul[@class='WB_row_line WB_row_r4 clearfix S_line2']/li[2]/a")
                    for i in range(0, 2):
                        try:
                            wd.execute_script('arguments[0].click();', button[0])
                            break
                        except:
                            t.sleep(1)
                            pass
                    t.sleep(1)
                    forward_button = wd.find_elements_by_xpath('//div[@class="W_layer "]//li[3]')
                if attemps==4:
                    continue
                t.sleep(0.5)
                try:
                    forward_button[0].click()
                except:
                    t.sleep(1)
                    wd.execute_script('arguments[0].click();', forward_button[0])
                t.sleep(0.5)
                mobile_url = ''
                while mobile_url =='':
                    try:
                        mobile_url = wd.find_elements_by_xpath('//div[@node-type="toMessage_client"]//div[@class="WB_feed_publish clearfix"]//div[@class="sendbox_area S_bg2"]')[0].text
                    except:
                        forward_button[0].click()
                        t.sleep(1)
                        mobile_url = wd.find_elements_by_xpath('//div[@node-type="toMessage_client"]//div[@class="WB_feed_publish clearfix"]//div[@class="sendbox_area S_bg2"]')[0].text
                mobile_url = re.findall(r"给你推荐一条微博\n(.*)",mobile_url)[0]
                all_url.append(mobile_url)
                ActionChains(wd).send_keys(Keys.ESCAPE).perform()



            if not nextpage():
                break

with open("globaltimes_url.json", 'w', encoding='utf-8') as file:
    file.write(json.dumps(all_url, ensure_ascii=False))
