# 将获取的重点评论 focus comments 作为训练集，进行情绪分类（打标签）
# 并创建文本文件归类到各个类目下，从而建立语料库

import src.focus
import pandas as pd

zhong_path = "../data/sentimentCorpus/中性/"
positive_path = "../data/sentimentCorpus/乐观/"
happy_path = "../data/sentimentCorpus/喜悦/"
taunt_path = "../data/sentimentCorpus/嘲讽/"
worry_path = "../data/sentimentCorpus/忧虑/"
angry_path = "../data/sentimentCorpus/愤怒/"
quit_path = "../data/quit_rubbish/"

path_map = {'Z': zhong_path, 'P': positive_path, 'H': happy_path, 'T': taunt_path, 'W': worry_path, 'A': angry_path, 'Q': quit_path}
count_map = {'Z': 0, 'P': 0, 'H': 0, 'T': 0, 'W': 0, 'A': 0, 'Q': 0}


def putLable(data_frame):
    for index in data_frame.index:
        content = data_frame.loc[index, 'content']
        comment = data_frame.loc[index, 'comment']
        print('【news text】: ' + content)
        print('【comment】: ' + comment)
        sentiment = input('请输入该文本的情感分类： 【中性 Z】【乐观 P】【喜悦 H】【嘲讽 T】【忧虑 W】【愤怒 A】【无效文本：Q】:  ')
        while sentiment not in ['Z', 'P', 'H', 'T', 'W', 'A', 'Q']:
            sentiment = input('请输入该文本的情感分类： 【中性 Z】【乐观 P】【喜悦 H】【嘲讽 T】【忧虑 W】【愤怒 A】【无效文本：Q】:  ')
        print()
        data_frame.loc[index, 'sentiment'] = sentiment
    return data_frame


def textClassify(data_frame, file_name):
    with open(src.focus.focus_path + file_name + '_focus.json', 'w', encoding='utf-8') as f:
        data_frame.drop('content', axis='columns').to_json(f, orient='records', force_ascii=False)

    for index in data_frame.index:
        comment = data_frame.loc[index, 'comment']
        sentiment = data_frame.loc[index, 'sentiment']
        path = path_map.get(sentiment)
        count = count_map.get(sentiment)
        count_map[sentiment] += 1
        with open(path + file_name + str(count) + '.txt', 'w', encoding='utf-8') as f:
            f.write(comment)


def focus_classification(focus_path, file_name):
    data_frame = pd.read_json(focus_path)
    for index in data_frame.index:
        comment = data_frame.loc[index, 'comment']
        sentiment = data_frame.loc[index, 'sentiment']
        while sentiment not in ['Z', 'P', 'H', 'T', 'W', 'A', 'Q']:
            print('【comment】: ' + comment)
            sentiment = input('请输入该文本的情感分类： 【中性 Z】【乐观 P】【喜悦 H】【嘲讽 T】【忧虑 W】【愤怒 A】【无效文本：Q】:  ')
        path = path_map.get(sentiment)
        count = count_map.get(sentiment)
        count_map[sentiment] += 1
        with open(path + file_name + str(count) + '.txt', 'w', encoding='utf-8') as f:
            f.write(comment)
