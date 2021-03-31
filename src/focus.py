# 获取点赞评论转发数量较高的重点新闻的评论，以作为情感分类的训练集
# 依据权值power = 点赞数 + 转发数 + 评论数，找到power的中位数
# 将高于平均数的新闻的评论作为训练集

import pandas as pd

focus_path = '../data/focus/'


def getFocusComments(json_path):
    data_frame = pd.read_json(json_path)
    data_frame['power'] = data_frame['like_num'] + data_frame['comment_num'] + data_frame['forward_num']
    power_median = data_frame['power'].median()  # 依据权值power = 点赞数 + 转发数 + 评论数，找到power的中位数
    focus_news = data_frame[data_frame['power'] > power_median].copy()  # 将高于中位数的作为训练集
    frame = focus_news.loc[:, ['time', 'content', 'comments']]
    comment_list = []
    for index in frame.index:
        time = frame.loc[index, 'time']
        content = frame.loc[index, 'content']
        comments = frame.loc[index, 'comments']
        for comment in comments:
            comment_list.append({'time': time, 'content':content, 'comment': comment, 'sentiment': 'Z'})
    return pd.DataFrame(comment_list)

