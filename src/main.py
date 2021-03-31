# 主函数
# 新闻筛选 -> 情感标签 -> 建立语料库 -> 监督训练建立模型 -> 预测情绪分类 -> 统计分析

from src import focus, lable, trainAndPredict, stageClassify, visualize

initialize_flag = True

corpus_path = '../data/sentimentCorpus'

cctvnews_source_path = '../data/sourceData/cctvnews.json'
xinlangnews_source_path = '../data/sourceData/xinlangnews.json'
fenghuangnews_source_path = '../data/sourceData/fenghuangnews.json'
rmrb_source_path = '../data/sourceData/rmrb.json'


# 预处理与准备：筛选新闻、人工标注建立语料库、划分阶段
def initialize_prepare():
    # 新闻筛选：获取重点评论
    cctv_focus_comments_frame = focus.getFocusComments(cctvnews_source_path)
    xinlang_focus_comments_frame = focus.getFocusComments(xinlangnews_source_path)
    fenghuang_focus_comments_frame = focus.getFocusComments(fenghuangnews_source_path)
    rmrb_focus_comments_frame = focus.getFocusComments(rmrb_source_path)

    # 对重点评论进行文本情绪标注（情绪标注完后新建的json文件归类到'data/focus/'中）,建立语料库
    lable.textClassify(lable.putLable(cctv_focus_comments_frame), 'cctv_')
    lable.textClassify(lable.putLable(xinlang_focus_comments_frame), 'xinlang_')
    lable.textClassify(lable.putLable(fenghuang_focus_comments_frame), 'fenghuang_')
    lable.textClassify(lable.putLable(rmrb_focus_comments_frame), 'rmrb_')

    # 将新闻划分为四个阶段
    stageClassify.classify(cctvnews_source_path)
    stageClassify.classify(xinlangnews_source_path)
    stageClassify.classify(fenghuangnews_source_path)
    stageClassify.classify(rmrb_source_path)


# 对数据进行统计分析，解决研究问题
# 需要获取的数据：通过语料库训练出模型，用该模型预测每条评论的情绪类别，最后统计出每一个阶段各个情绪所占比例
# 研究问题：各阶段的主要情绪、以及随时间的情绪变化
def analyse():
    # 训练模型
    trainAndPredict.train(corpus_path)

    # 统计出每一个阶段各个情绪所占比例
    visualize.calculate_proportions()

    # 可视化各个阶段
    visualize.stage_1_sentiment_analyse()
    visualize.stage_2_sentiment_analyse()
    visualize.stage_3_sentiment_analyse()
    visualize.stage_4_sentiment_analyse()
    visualize.sentiment_change()


if __name__ == '__main__':
    if not initialize_flag:
        initialize_prepare()
    analyse()