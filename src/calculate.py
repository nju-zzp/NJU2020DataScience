# 对各个阶段所有数据进行情绪预测
# 计算每一条评论的情绪
# 再统计每个情绪对应的数量和比例

from src import trainAndPredict
import pandas as pd
import os

corpus_path = '../data/sentimentCorpus'


stage_1_data = '../data/stageData/stage_1/'
stage_2_data = '../data/stageData/stage_2/'
stage_3_data = '../data/stageData/stage_3/'
stage_4_data = '../data/stageData/stage_4/'


def stage_collect_sentiment(stage_data_path):
    zhong_count = 0
    positive_count = 0
    happy_count = 0
    taunt_count = 0
    worry_count = 0
    angry_count = 0

    files = os.listdir(stage_data_path)
    print(files)
    classifier = trainAndPredict.train(corpus_path)
    for file_name in files:
        file_path = stage_data_path + file_name
        news_frame = pd.read_json(file_path, encoding='utf-8')
        for index in news_frame.index:
            comments = news_frame.loc[index, 'comments']
            for comment in comments:
                sentiment_str = classifier.classify(comment)
                if sentiment_str == '中性':
                    zhong_count += 1
                elif sentiment_str == '乐观':
                    positive_count += 1
                elif sentiment_str == '喜悦':
                    happy_count += 1
                elif sentiment_str == '嘲讽':
                    taunt_count += 1
                elif sentiment_str == '忧虑':
                    worry_count += 1
                elif sentiment_str == '愤怒':
                    angry_count += 1
                else:
                    print("ERROR")

    print('zhong_count = ' + str(zhong_count))
    print('positive_count = ' + str(positive_count))
    print('happy_count = ' + str(happy_count))
    print('taunt_count = ' + str(taunt_count))
    print('worry_count = ' + str(worry_count))
    print('angry_count = ' + str(angry_count))

    return zhong_count, positive_count, happy_count, taunt_count, worry_count, angry_count


def stage_1_collect_sentiment():
    t = stage_collect_sentiment(stage_1_data)
    with open('../data/stageSentiment/stage_1/stage_1_sentiment_count.txt', 'w') as f:
        f.write(str(t))
    return t


def stage_2_collect_sentiment():
    t = stage_collect_sentiment(stage_2_data)
    with open('../data/stageSentiment/stage_2/stage_2_sentiment_count.txt', 'w') as f:
        f.write(str(t))
    return t


def stage_3_collect_sentiment():
    t = stage_collect_sentiment(stage_3_data)
    with open('../data/stageSentiment/stage_3/stage_3_sentiment_count.txt', 'w') as f:
        f.write(str(t))
    return t


def stage_4_collect_sentiment():
    t = stage_collect_sentiment(stage_4_data)
    with open('../data/stageSentiment/stage_4/stage_4_sentiment_count.txt', 'w') as f:
        f.write(str(t))
    return t

