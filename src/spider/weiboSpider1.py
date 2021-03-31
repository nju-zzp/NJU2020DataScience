import json
from selenium import webdriver
import re
from atexit import register
from selenium.common.exceptions import TimeoutException
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


class NoCommetsException(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self, *args, **kwargs):
        return self.error


def test_client_required(wd):
    if len(wd.find_elements_by_xpath("//p[@class='update-desc update-desc-r']")) != 0:
        raise ClientRequiredException("客户端打开，跳过")


def test_intercepted(wd):
    if len(wd.find_elements_by_xpath("//*[contains(text(), '请求过于频繁')]")) != 0:
        raise InterceptedException("请求过于频繁")


# 得到一条微博的数据
def get_data(wd, url):
    wd.get(url)
    try:
        test_client_required(wd)
        test_intercepted(wd)
    except Exception as e:
        raise
    try:
        time = WebDriverWait(wd, timeout=5, poll_frequency=0.5).until(
            lambda x: wd.find_elements_by_xpath("//span[@class='time']"))
        content = WebDriverWait(wd, timeout=5, poll_frequency=0.5).until(
            lambda x: wd.find_elements_by_xpath("//div[@class='weibo-og']/div[@class='weibo-text']"))
        forward_str = WebDriverWait(wd, timeout=5, poll_frequency=0.5).until(
            lambda x: wd.find_elements_by_xpath("//div[contains(@ item,'[object Object]')]//i[2]"))
        comment_str = WebDriverWait(wd, timeout=5, poll_frequency=0.5).until(
            lambda x: wd.find_elements_by_xpath("//div[contains(@ item,'[object Object]')]//i[2]"))
        like_str = WebDriverWait(wd, timeout=5, poll_frequency=0.5).until(
            lambda x: wd.find_elements_by_xpath("//div[contains(@ item,'[object Object]')]//i[2]"))

    except TimeoutException:
        raise TimeoutException("超时，请检查网络或者是否被拦截")
    time = time[0].text
    content = content[0].text
    forward_str = forward_str[0].text
    comment_str = comment_str[1].text
    like_str = like_str[2].text

    forward_num = float(re.findall(r"[0-9]+\.*[0-9]*", forward_str)[0])
    comment_num = float(re.findall(r"[0-9]+\.*[0-9]*", comment_str)[0])
    like_num = float(re.findall(r"[0-9]+\.*[0-9]*", like_str)[0])

    try:
        comments = WebDriverWait(wd, timeout=5, poll_frequency=0.5).until(
            lambda x: wd.find_elements_by_xpath("//div[@data-v-11d91d52]//h3"))
    except TimeoutException:
        if comment_num != 0:
            raise NoCommetsException("无评论！")
        else:
            comments = []

    if "万" in forward_str:
        forward_num *= 10000
    if "万" in comment_str:
        comment_num *= 10000
    if "万" in like_str:
        like_num *= 10000

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
              "like_num": int(like_num),
              "comment_num": int(comment_num),
              "forward_num": int(forward_num),
              "comments": comments_list
              }

    return a_data


# 返回尚未被爬取过的链接列表
def get_urls(url_list, data_list):
    url_list = [url for url in url_list if url not in [x["url"] for x in data_list]]
    return url_list


def save(data_path, data_list, url_path, url_list, used):
    url_list = [url for url in url_list if url not in used]
    with open(url_path, 'w', encoding='utf-8') as file:
        file.write(json.dumps(url_list, ensure_ascii=False))
    with open(data_path, 'w', encoding='utf-8') as file:
        file.write(json.dumps(data_list, ensure_ascii=False))


def papapa(name, url_path, data_path):
    mobile_emulation = {
        "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},  # 定义设备高宽，像素比
        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) "  # 通过UA来模拟
                     "AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"}
    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument('--headless')
    chrome_options.add_argument(
        'User-Agent=Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 ('
        'KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36')
    wd = webdriver.Chrome(r"C:\Users\86159\Desktop\chromedriver.exe", options=chrome_options)

    with open(url_path, "r", encoding='utf-8') as f:
        url_list = json.loads(f.read())
    with open(data_path, "r", encoding='utf-8') as f:
        data_list = json.loads(f.read())
    url_list = get_urls(url_list, data_list)

    used = []

    for i in range(0, len(url_list)):
        print(name, "正在爬取第", i + 1, "条微博", ",剩余", len(url_list) - i)
        while 1:
            try:
                data_list.append(get_data(wd, url_list[i]))
                print("成功！")
                used.append(url_list[i])
                break
            except TimeoutException as e:
                print(e)
                wd.refresh()
                save(data_path, data_list, url_path, url_list, used)
            except NoCommetsException as e:
                print(e)
                break
            except ClientRequiredException as e:
                used.append(url_list[i])
                save(data_path, data_list, url_path, url_list, used)
                print(e)
                break
            except InterceptedException as e:
                save(data_path, data_list, url_path, url_list, used)
                print(e, "被拦截！")
                input("输入任意内容继续")
                wd.refresh()

    save(data_path, data_list, url_path, url_list, used)
    register(save, data_list, url_path, url_list, used)


def main():
    url_path = r"C:\Users\86159\Desktop\WeiboSpider\rbrbURL03.json"  # 存放所有链接
    data_path = r"C:\Users\86159\Desktop\WeiboSpider\rbrb_comments_03.json"  # 已经爬下来的数据
    papapa("人民日报", url_path, data_path)


if __name__ == '__main__':
    main()
