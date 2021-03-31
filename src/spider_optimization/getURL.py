import json
import time as t
from selenium import webdriver
import re

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

class InterceptedException(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self, *args, **kwargs):
        return self.error


class ClientRequiredException(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self, *args, **kwargs):
        return self.error


class NoCommentsException(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self, *args, **kwargs):
        return self.error


def scroll_down(wd):
    attemps = 0
    while len(wd.find_elements_by_xpath("//div[contains(@node-type,'feed_list_page')]")) == 0:
        wd.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        attemps += 1
        if attemps == 6:
            wd.refresh()
            attemps = 0
        t.sleep(1)


def add_cookies(wd):
    with open("cookies.json", 'r', encoding='utf-8') as file:
        cookie_list = json.loads(file.read())

    wd.delete_all_cookies()
    for cookie in cookie_list:
        wd.add_cookie(cookie)


def get_data_from_a_page(wd, url):
    all_url = []
    wd.get(url)
    add_cookies(wd)
    # wd.add_cookie(cookies)
    wd.get(url)
    scroll_down(wd)
    hitwords = ['病毒', '吹哨人', '李文亮', '钟南山', '抗疫', '疫情', '新冠', '肺炎', '隔离', '口罩']
    try:
        wd.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        elements = WebDriverWait(wd, timeout=5, poll_frequency=0.5).until(
            lambda x: wd.find_elements_by_xpath("//div[contains(@action-data,'cur_visible=0')]"))
    except TimeoutException:
        raise TimeoutException("读取微博超时！")
    except Exception:
        raise Exception

    for index in range(0, len(elements)):
        forward_button = []
        content = wd.find_elements_by_xpath(
            "//div[contains(@action-data,'cur_visible=0')][" + str(index + 1) + "]//div[@class='WB_text W_f14']")[
            0].text
        for i in hitwords:  # 这条微博无有效信息
            if i in content:
                break
        else:
            continue

        try:
            button = WebDriverWait(wd, timeout=5, poll_frequency=0.5).until(
                lambda x: wd.find_elements_by_xpath("//div[contains(@action-data,'cur_visible=0')][" + str(
                    index + 1) + "]//ul[@class='WB_row_line WB_row_r4 clearfix S_line2']/li[2]/a"))
            wd.execute_script('arguments[0].click();', button[0])
        except TimeoutException:
            raise TimeoutException("转发按钮获取失败")
        except Exception:
            raise Exception

        try:
            forward_button = WebDriverWait(wd, timeout=5, poll_frequency=0.5).until(
                lambda x: wd.find_elements_by_xpath('//div[@class="W_layer "]//li[3]'))
            forward_button[0].click()
        except TimeoutException:
            raise TimeoutException("转发框中转发按钮获取失败")
        except Exception:
            print("点击失败")
            wd.execute_script('arguments[0].click();', forward_button[0])

        try:
            mobile_url = WebDriverWait(wd, timeout=5, poll_frequency=0.5).until(
                lambda x: wd.find_elements_by_xpath(
                    '//div[@node-type="toMessage_client"]//div[@class="WB_feed_publish clearfix"]//div[@class="sendbox_area S_bg2"]'))
            mobile_url = mobile_url[0].text
        except TimeoutException:
            print("获取移动链接超时")
            try:
                forward_button[0].click()
            except Exception:
                raise Exception
            t.sleep(1)
            mobile_url = wd.find_elements_by_xpath(
                '//div[@node-type="toMessage_client"]//div[@class="WB_feed_publish clearfix"]//div[@class="sendbox_area S_bg2"]')[
                0].text

        mobile_url = re.findall(r"给你推荐一条微博\n(.*)", mobile_url)[0]
        all_url.append(mobile_url)
        ActionChains(wd).send_keys(Keys.ESCAPE).perform()

    return all_url


def save(path, url_list):
    with open(path, 'w', encoding='utf-8') as file:
        file.write(json.dumps(url_list, ensure_ascii=False))


def get_pages_num(wd, url):
    wd.get(url)
    add_cookies(wd)
    wd.get(url)

    # wd.add_cookie(cookies)
    # wd.get(url)
    scroll_down(wd)
    pages = WebDriverWait(wd, timeout=5, poll_frequency=0.5).until(
        lambda x: wd.find_elements_by_xpath('//span[@class="list"]//ul/li'))
    return len(pages)


def papa(dest, path):
    base = r"https://weibo.com/{0}?is_all=1&stat_date={1}{2}&page={3}#feedtop"
    base = base.format(dest, '{0}', '{1}', "{2}")
    url_list = []

    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    wd = webdriver.Chrome(r"D:\project\chromedriver.exe", options=chrome_options)
    wbcookies = dict()
    for year in range(2019, 2021):
        for month in range(1, 13):
            if year == 2019 and month < 12:
                continue
            if year == 2020 and month >= 7:
                break

            attemps = 0
            try:
                pages = get_pages_num(wd, base.format(str(year), str(month).zfill(2), 1))

            except TimeoutException as e:
                attemps += 1
                t.sleep(1)
                pages = get_pages_num(wd, base.format(str(year), str(month).zfill(2), 1))
                if attemps == 6:
                    wd.refresh()

            for i in range(0, pages):
                url = base.format(str(year), str(month).zfill(2), i + 1)
                while 1:
                    print("正在爬取", dest, year, "-", month, "第", i + 1, "页")
                    try:
                        page_url_list = get_data_from_a_page(wd, url)
                        url_list = url_list + page_url_list
                        print("成功！")
                        break
                    except TimeoutException as e:
                        print(e)
                        wd.refresh()
                        save(path, url_list)
                    except NoCommentsException as e:
                        print(e)
                        save(path, url_list)

                        break
                    except ClientRequiredException as e:
                        save(path, url_list)

                        print(e)
                        break
                    except InterceptedException as e:
                        save(path, url_list)
                        print(e, "被拦截！")
                        input("输入任意内容继续")
                        wd.refresh()
        save(path, url_list)


def main():
    dest = 'xjb'  # 博主名字
    path = r'D:\project\test2\allulrs.json'  # 存储路径
    papa(dest, path)


if __name__ == '__main__':
    main()

