import matplotlib.pyplot as plt
import pandas as pd
from src import calculate

stage_1_zhong_proportion = 0
stage_1_positive_proportion = 0
stage_1_happy_proportion = 0
stage_1_taunt_proportion = 0
stage_1_worry_proportion = 0
stage_1_angry_proportion = 0

stage_2_zhong_proportion = 0
stage_2_positive_proportion = 0
stage_2_happy_proportion = 0
stage_2_taunt_proportion = 0
stage_2_worry_proportion = 0
stage_2_angry_proportion = 0

stage_3_zhong_proportion = 0
stage_3_positive_proportion = 0
stage_3_happy_proportion = 0
stage_3_taunt_proportion = 0
stage_3_worry_proportion = 0
stage_3_angry_proportion = 0

stage_4_zhong_proportion = 0
stage_4_positive_proportion = 0
stage_4_happy_proportion = 0
stage_4_taunt_proportion = 0
stage_4_worry_proportion = 0
stage_4_angry_proportion = 0


def calculate_proportions():
    global stage_1_zhong_proportion
    global stage_1_positive_proportion
    global stage_1_happy_proportion
    global stage_1_taunt_proportion
    global stage_1_worry_proportion
    global stage_1_angry_proportion

    global stage_2_zhong_proportion
    global stage_2_positive_proportion
    global stage_2_happy_proportion
    global stage_2_taunt_proportion
    global stage_2_worry_proportion
    global stage_2_angry_proportion

    global stage_3_zhong_proportion
    global stage_3_positive_proportion
    global stage_3_happy_proportion
    global stage_3_taunt_proportion
    global stage_3_worry_proportion
    global stage_3_angry_proportion

    global stage_4_zhong_proportion
    global stage_4_positive_proportion
    global stage_4_happy_proportion
    global stage_4_taunt_proportion
    global stage_4_worry_proportion
    global stage_4_angry_proportion

    stage_1_zhong_count, stage_1_positive_count, stage_1_happy_count, stage_1_taunt_count, stage_1_worry_count, stage_1_angry_count = calculate.stage_1_collect_sentiment()
    stage_1_count_all = stage_1_zhong_count + stage_1_positive_count + stage_1_happy_count + \
                        stage_1_taunt_count + stage_1_worry_count + stage_1_angry_count
    func_1 = lambda x: (x * 100) / stage_1_count_all
    stage_1_zhong_proportion = func_1(stage_1_zhong_count)
    stage_1_positive_proportion = func_1(stage_1_positive_count)
    stage_1_happy_proportion = func_1(stage_1_happy_count)
    stage_1_taunt_proportion = func_1(stage_1_taunt_count)
    stage_1_worry_proportion = func_1(stage_1_worry_count)
    stage_1_angry_proportion = func_1(stage_1_angry_count)

    stage_2_zhong_count, stage_2_positive_count, stage_2_happy_count, stage_2_taunt_count, stage_2_worry_count, stage_2_angry_count = calculate.stage_2_collect_sentiment()
    stage_2_count_all = stage_2_zhong_count + stage_2_positive_count + stage_2_happy_count + \
                        stage_2_taunt_count + stage_2_worry_count + stage_2_angry_count
    func_2 = lambda x: (x * 100) / stage_2_count_all
    stage_2_zhong_proportion = func_2(stage_2_zhong_count)
    stage_2_positive_proportion = func_2(stage_2_positive_count)
    stage_2_happy_proportion = func_2(stage_2_happy_count)
    stage_2_taunt_proportion = func_2(stage_2_taunt_count)
    stage_2_worry_proportion = func_2(stage_2_worry_count)
    stage_2_angry_proportion = func_2(stage_2_angry_count)

    stage_3_zhong_count, stage_3_positive_count, stage_3_happy_count, stage_3_taunt_count, stage_3_worry_count, stage_3_angry_count = calculate.stage_3_collect_sentiment()
    stage_3_count_all = stage_3_zhong_count + stage_3_positive_count + stage_3_happy_count + \
                        stage_3_taunt_count + stage_3_worry_count + stage_3_angry_count
    func_3 = lambda x: (x * 100) / stage_3_count_all
    stage_3_zhong_proportion = func_3(stage_3_zhong_count)
    stage_3_positive_proportion = func_3(stage_3_positive_count)
    stage_3_happy_proportion = func_3(stage_3_happy_count)
    stage_3_taunt_proportion = func_3(stage_3_taunt_count)
    stage_3_worry_proportion = func_3(stage_3_worry_count)
    stage_3_angry_proportion = func_3(stage_3_angry_count)

    stage_4_zhong_count, stage_4_positive_count, stage_4_happy_count, stage_4_taunt_count, stage_4_worry_count, stage_4_angry_count = calculate.stage_4_collect_sentiment()
    stage_4_count_all = stage_4_zhong_count + stage_4_positive_count + stage_4_happy_count + \
                        stage_4_taunt_count + stage_4_worry_count + stage_4_angry_count
    func_4 = lambda x: (x * 100) / stage_4_count_all
    stage_4_zhong_proportion = func_4(stage_4_zhong_count)
    stage_4_positive_proportion = func_4(stage_4_positive_count)
    stage_4_happy_proportion = func_4(stage_4_happy_count)
    stage_4_taunt_proportion = func_4(stage_4_taunt_count)
    stage_4_worry_proportion = func_4(stage_4_worry_count)
    stage_4_angry_proportion = func_4(stage_4_angry_count)


def stage_1_sentiment_analyse():
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = 'Neutral', 'Positive', 'Happy', 'Taunt', 'Worry', 'Angry'
    sizes = [stage_1_zhong_proportion, stage_1_positive_proportion, stage_1_happy_proportion,
             stage_1_taunt_proportion, stage_1_worry_proportion, stage_1_angry_proportion]
    explode = (0, 0, 0, 0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.savefig('stage_1_comment.jpg')
    plt.show()


def stage_2_sentiment_analyse():
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = 'Neutral', 'Positive', 'Happy', 'Taunt', 'Worry', 'Angry'
    sizes = [stage_2_zhong_proportion, stage_2_positive_proportion, stage_2_happy_proportion,
             stage_2_taunt_proportion, stage_2_worry_proportion, stage_2_angry_proportion]
    explode = (0, 0, 0, 0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.savefig('stage_2_comment.jpg')
    plt.show()


def stage_3_sentiment_analyse():
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = 'Neutral', 'Positive', 'Happy', 'Taunt', 'Worry', 'Angry'
    sizes = [stage_3_zhong_proportion, stage_3_positive_proportion, stage_3_happy_proportion,
             stage_3_taunt_proportion, stage_3_worry_proportion, stage_3_angry_proportion]
    explode = (0, 0, 0, 0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.savefig('stage_3_comment.jpg')
    plt.show()


def stage_4_sentiment_analyse():
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = 'Neutral', 'Positive', 'Happy', 'Taunt', 'Worry', 'Angry'
    sizes = [stage_4_zhong_proportion, stage_4_positive_proportion, stage_4_happy_proportion,
             stage_4_taunt_proportion, stage_4_worry_proportion, stage_4_angry_proportion]
    explode = (0, 0, 0, 0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.savefig('stage_4_comment.jpg')
    plt.show()


def sentiment_change():
    value_frame = [[stage_1_zhong_proportion, stage_1_positive_proportion, stage_1_happy_proportion,
                    stage_1_taunt_proportion, stage_1_worry_proportion, stage_1_angry_proportion],
                   [stage_2_zhong_proportion, stage_2_positive_proportion, stage_2_happy_proportion,
                    stage_2_taunt_proportion, stage_2_worry_proportion, stage_2_angry_proportion],
                   [stage_3_zhong_proportion, stage_3_positive_proportion, stage_3_happy_proportion,
                    stage_3_taunt_proportion, stage_3_worry_proportion, stage_3_angry_proportion],
                   [stage_4_zhong_proportion, stage_4_positive_proportion, stage_4_happy_proportion,
                    stage_4_taunt_proportion, stage_4_worry_proportion, stage_4_angry_proportion]]

    sentiment_list = ['Neutral', 'Positive', 'Happy', 'Taunt', 'Worry', 'Angry']

    stage_list = ['stage_1', 'stage_2', 'stage_3', 'stage_4']

    data_frame = pd.DataFrame(value_frame, columns=sentiment_list, index=stage_list)

    data_frame.plot()

    plt.show()
    plt.savefig('stage_change.jpg')