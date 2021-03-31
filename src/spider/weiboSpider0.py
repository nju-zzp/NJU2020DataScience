import json
import time as t
from selenium import webdriver
import re
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

all_data = []

wd = webdriver.Chrome(r"C:\Users\86159\Desktop\chromedriver.exe")
with open("rbrbURL040506.json", "r", encoding='utf-8')as file:
    url_list = json.loads(file.read())
    url_list = url_list[0:]

    for url in url_list:
        attempts = 0
        while 1:
            try:
                wd.get(url)
                t.sleep(1)
                time = wd.find_elements_by_xpath("//span[@class='time']")[0].text
                content = wd.find_elements_by_xpath("//div[@class='weibo-og']/div[@class='weibo-text']")[0].text
                forward_str = wd.find_elements_by_xpath("//div[contains(@ item,'[object Object]')]//i[2]")[0].text
                comment_str = wd.find_elements_by_xpath("//div[contains(@ item,'[object Object]')]//i[2]")[1].text
                like_str = wd.find_elements_by_xpath("//div[contains(@ item,'[object Object]')]//i[2]")[2].text

                forward_num = float(re.findall(r"[0-9]+\.*[0-9]*", forward_str)[0])
                comment_num = float(re.findall(r"[0-9]+\.*[0-9]*", comment_str)[0])
                like_num = float(re.findall(r"[0-9]+\.*[0-9]*", like_str)[0])
                if "万" in forward_str:
                    forward_num *= 10000
                if "万" in comment_str:
                    comment_num *= 10000
                if "万" in like_str:
                    like_num *= 10000
                comments = wd.find_elements_by_xpath("//div[@data-v-11d91d52]//h3")
                comments_list = []
                cnt = 0
                for comment in comments:
                    if cnt == 5:
                        break
                    comments_list.append(comment.text)
                    cnt += 1

                a_data = {"url": url,
                          "content": content,
                          "time": time,
                          "like_num": like_num,
                          "comment_num": comment_num,
                          "forward_num": forward_num,
                          "comments": comments_list
                          }
                all_data.append(a_data)
                break
            except:
                attempts += 1
                t.sleep(attempts * 2)
                with open("rbrb040506_comments.json", 'w', encoding='utf-8') as file_2:
                    file_2.write(json.dumps(all_data, ensure_ascii=False))
                if attempts > 10 or len(wd.find_elements_by_xpath("//p[@class='update-desc update-desc-r']")) != 0:
                    break

with open("rbrb040506_comments.json", 'w', encoding='utf-8') as file:
    file.write(json.dumps(all_data, ensure_ascii=False))
