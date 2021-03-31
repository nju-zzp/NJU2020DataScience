# 目录结构

├─data		数据  

│  ├─focus		重点新闻的评论  

│    ├─quit_rubbish		人工标注时的无效文本  

│    ├─sentimentCorpus		语料库  

│    │    ├─中性  

│    │    ├─乐观  

│    │    ├─喜悦  

│    │    ├─嘲讽  

│    │    ├─忧虑  

│    │    └─愤怒  

│    ├─sourceData		爬取的源数据  

│    ├─stageData		划分阶段后的新闻数据  

│    │    ├─stage_1  

│    │    ├─stage_2  

│    │    ├─stage_3  

│    │    └─stage_4  

│    └─stageSentiment		各个阶段评论的各类情绪的计数  

│          ├─stage_1  

│          ├─stage_2  

│          ├─stage_3  

│          └─stage_4  

└─src	源码  

	│  calculate.py		使用训练出的模型-计算各个阶段的各类情绪评论数  
	
	│  focus.py		筛选出重点新闻  
	
	│  lable.py		人工标注，建立训练集  
	
	│  main.py		主程序入口  
	
	│  stageClassify.py		疫情时间阶段划分  
	
	│  stage_1_comment.jpg	第一阶段情绪饼状图  
	
	│  stage_2_comment.jpg	第二阶段情绪饼状图  
	
	│  stage_3_comment.jpg	第三阶段情绪饼状图  
	
	│  stage_4_comment.jpg	第四阶段情绪饼状图  
	
	│  stage_change.jpg		情绪阶段折线图  
	
	│  trainAndPredict.py		机器学习-训练模型  
	
	│  visualize.py		数据的可视化  
	
	│  spider				数据爬虫  
	
