# xuesebot
这是一个可以回答游戏《三国志11》著名mod《血色衣冠》中人物、城池、势力等情况的对话机器人。其基于Rasa，并辅以paddlespeech。实现可语音与机器人沟通。
目前，这个机器人刚刚出生，其很多功能不全，且有些问题回答不了，一步步完善。

# 简述：

这是一个暂未充分训练，但却相对完整的对话机器人： 
1. 其主本基于Rasa 3.0，Rasa可实现任务型(Task Oriented)对话。 

2. 此对话机器人可以实现基KG的KBQA形式的对话系系统。即血色衣冠中的人物、城池、势力等属性与关系信息，经处理存储于图数据库neo4j中。

3. 闲聊实现基于CDial-GPT。

4. 对话机器人，需要听、说，即机器人可与人交流， 此处主要基于paddlespeech 实现, paddlespeecq负责语音识别(Automatic Speech Recognition, ASR)
与语音生成(Text To Speech,TTS)，另外也基于pyaudio与auditok实现语音端点检测(Voice Activity Detection, VAD)。

# 必备
1. rasa 3.0
2. transformers
3. paddlespeech （最好源码安装或hard模式）
4. 其他requirements.txt要求模块

# 使用
## 训练 Rasa 模型
尝试与此机器人交流，首先需要训练rasa模型，数据已经做处理， 可以直接训练。

```bash
rasa train
```
## 启动知识库
模型训练结束后，需要将数据放进neo4j当中(此步不依赖于上步训练，故可以提前执行)。


```bash
sudo neo4j start #如果启动不了，加sudo试下
python process_raw_data/process_forces.py # 将处理好的数插入neo4j中
```
## 启动Rasa服务器和客户端

```bash
rasa run --enable-api --debug #--debug 表调试模型

```
## 启动rasa 动作服务
用于处理定制的机器人动作。
```bash
rasa run actions
```

## 启动paddlespeech 的ASR， TTS 与文本断句服务。
```bash

paddlespeech_server start --config_file ./conf/tts_online_application.yaml
paddlespeech_server start --config_file conf/ws_conformer_application.yaml
paddlespeech_server start --config_file conf/punc_application.yaml
```

## 开始交流

```bash
python interact.py
```

注： 以上最好者分别在当前目录下启动新的terminal 窗口。

## 功能
以下功能基本上实现了图谱查询功能，bot可回答一些简单的问题，但暂不能回答关系性问题如“比较”，“双条件查询”等。

+ 查询武将、城池与势力等单体的属性，总体情况
    + 武将各属性： 如诸葛亮的出生地在哪，张飞的武力是多少， 陈宫的智力有80吗， 关于的枪兵能力怎么样， 刘备的特技是什么等
    + 城池各属性： 洛阳的武将都有谁， 开封有多少钱， 与长安相邻的城市有哪些等
    + 势力各属性： 李渊势力有多少武将， 刘邦的军师是谁，赵匡胤有多少个城池
+ 查询总体情况：
    + 姓刘的都有谁
    + 成吉思汗哪个属性最弱
    + 司马懿的哪个兵种最强
    + 金钱超过8000的都有哪些城市、势力
    + 武力超过80的都有谁
    + 当前还有几个势力
    + 哪个势力钱最多
    + 哪个城市最富有
    + 哪里马最多
    + 长安是谁的势力范围
+ 双条件查询：
    + 曹操手下姓张的有谁
    + 朱元璋手下政治最高的是谁
    + 谁的统帅与武力都超过80？
    + 出生在洛阳的人中，谁的智力最高
    + 秦的城池中，哪个最穷？
+ 比较：
    + 关羽与赵云谁的武力高；
    + 徐达的枪兵有李世民的厉害吗
    + 洛阳与寿春比，谁的马匹更多
    + 刘备与刘邦比谁的城多？
    + 梓潼相邻城的数量有没有江夏的多
+ 最短路径:
    + 从襄阳到柴桑需要经过几个城市


