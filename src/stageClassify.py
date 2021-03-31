# 将新闻进行四个阶段的划分

import pandas as pd
from datetime import datetime

stage_1_path = '../data/stageData/stage_1/'
stage_2_path = '../data/stageData/stage_2/'
stage_3_path = '../data/stageData/stage_3/'
stage_4_path = '../data/stageData/stage_4/'


first_start = datetime(2019, 12, 8)
second_start = datetime(2020, 1, 22)
third_start = datetime(2020, 2, 10)
fourth_start = datetime(2020, 3, 10)
end = datetime(2020, 6, 30)


def classify(source_path):
    file_name = source_path.split('/')[-1][:-5]  # 获取文件名
    data_frame = pd.read_json(source_path)

    data_frame['time'] = pd.to_datetime(data_frame['time'])
    first_stage_news = data_frame[((data_frame['time'] >= first_start) & (data_frame['time'] < second_start))]
    second_stage_news = data_frame[((data_frame['time'] >= second_start) & (data_frame['time'] < third_start))]
    third_stage_news = data_frame[((data_frame['time'] >= third_start) & (data_frame['time'] < fourth_start))]
    fourth_stage_news = data_frame[((data_frame['time'] >= fourth_start) & (data_frame['time'] < end))]

    first_stage_news['time'] = first_stage_news['time'].apply(lambda x: x.strftime('%Y-%m-%d'))
    second_stage_news['time'] = second_stage_news['time'].apply(lambda x: x.strftime('%Y-%m-%d'))
    third_stage_news['time'] = third_stage_news['time'].apply(lambda x: x.strftime('%Y-%m-%d'))
    fourth_stage_news['time'] = fourth_stage_news['time'].apply(lambda x: x.strftime('%Y-%m-%d'))

    with open(stage_1_path + file_name + '1.json', 'w', encoding='utf-8') as f:
        first_stage_news.to_json(f, orient='records', force_ascii=False)
    with open(stage_2_path + file_name + '2.json', 'w', encoding='utf-8') as f:
        second_stage_news.to_json(f, orient='records', force_ascii=False)
    with open(stage_3_path + file_name + '3.json', 'w', encoding='utf-8') as f:
        third_stage_news.to_json(f, orient='records', force_ascii=False)
    with open(stage_4_path + file_name + '4.json', 'w', encoding='utf-8') as f:
        fourth_stage_news.to_json(f, orient='records', force_ascii=False)