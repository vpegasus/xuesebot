## 训练 Rasa 模型

```bash
rasa train
```

```bash
sudo neo4j start
```

## 启动Rasa服务器和客户端

```bash
rasa run --enable-api --debug

```

```bash
rasa run actions
```

```bash

paddlespeech_server start --config_file ./conf/tts_online_application.yaml
paddlespeech_server start --config_file conf/ws_conformer_application.yaml
paddlespeech_server start --config_file conf/punc_application.yaml
```

尝试输入一些查询，例如“如何检查面试结果？” 并查看回复。

玩得开心！

## 功能

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


