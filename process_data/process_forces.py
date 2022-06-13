from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher
import pandas as pd
import numpy as np
from tqdm import tqdm
from keymap import person_map, city_map, force_map, inv_force_map, inv_person_map, inv_city_map

graph = Graph('bolt://localhost:7687', user='neo4j', password='`')
matcher = NodeMatcher(graph)

psn = pd.read_csv('./raw_data/武将.csv')
ct = pd.read_csv('./raw_data/城市.csv')
fc = pd.read_csv('./raw_data/势力.csv')


##todo 下面有些的 pp, cc 开头的开关有多组，因此有些末尾关系进行了编号，如‘pp_person_like2’，‘pp_person_like3’， 使用过程中，两个关系是一样的，
## 为后续方便处理，其它 cc, pp 等关系都加了一个无意义的字符如空格，以便统一处理。


#
# person_properties = ['序号', '姓名', '官职', '身份', '忠诚', '统御', '武力', '智力', '政治', '魅力', '出生年', '死亡年', '特技', '枪兵适性', '戟兵适性',
#                      '弩兵适性', '骑兵适性', '兵器适性',
#                      '水军适性']
# city_properties = ['']
# relationships = ['势力', '所属', '所在', '亲近武将', '厌恶武将', '血缘', '父亲']

def get_property(x, mp):
    tmp = {mp[k]: v for k, v in x.items() if k in mp and '_' not in mp[k]}
    if tmp.get('pid'):
        _id = tmp.pop('pid')
    elif tmp.get('fid'):
        _id = tmp.pop('fid')
    elif tmp.get('cid'):
        _id = tmp.pop('cid')
    else:
        _id = x['序号']
    tmp['id'] = _id
    return tmp


def get_rel(dt, mp):
    rels = []
    df = dt.to_dict(orient='records')
    t = [str(x) for x in range(2000, 2050)]
    for x in tqdm(df):
        tmp = {mp[k]: v for k, v in x.items() if k in mp and '_' in mp[k]}
        for k, v in tmp.items():
            if v is None or v == '':
                continue
            if isinstance(v, float) and np.isnan(v):
                continue
            r = Relationship.type(k)
            if k[:2] == 'pp':
                r = Relationship.type(k[:-1])
                if k == 'pp_blood_source_of ':
                    if x['世代'] != 1:
                        tmpr = r(x['node'], psn[psn['序号'] == v].node.item())
                else:
                    if v not in t:
                        tmpr = r(x['node'], psn[psn['姓名'] == v].node.item())
            elif k[:2] == 'pc':
                if v not in ['虎牢关', '潼关']:
                    tmpr = r(x['node'], ct[ct['名称'] == v].node.item())
            elif k[:2] == 'pf':
                tmpr = r(x['node'], fc[fc['君主'] == v].node.item())
            elif k[:2] == 'cp':
                tmpr = r(x['node'], psn[psn['姓名'] == v].node.item())
            elif k[:2] == 'cc':
                r = Relationship.type(k[:-1])
                tmpr = r(x['node'], ct[ct['名称'] == v].node.item())
            elif k[:2] == 'cf':
                tmpr = r(x['node'], fc[fc['君主'] == v].node.item())
            elif k[:2] == 'fp':
                tmpr = r(x['node'], psn[psn['姓名'] == v].node.item())
            rels.append(tmpr)
    return rels


graph.delete_all()

psn['node'] = psn.apply(lambda x: Node('Person', **get_property(x, person_map)), axis=1)
ct['node'] = ct.apply(lambda x: Node('City', **get_property(x, city_map)), axis=1)
fc['node'] = fc.apply(lambda x: Node('Force', **get_property(x, force_map)), axis=1)
for x in tqdm(psn.node.tolist()):
    graph.create(x)

for x in tqdm(ct.node.tolist()):
    graph.create(x)

for x in tqdm(fc.node.tolist()):
    graph.create(x)

relsp = get_rel(psn, person_map)
relsc = get_rel(ct, city_map)
relsf = get_rel(fc, force_map)
for rl in [relsp, relsc, relsf]:
    for r in tqdm(rl):
        graph.create(r)
