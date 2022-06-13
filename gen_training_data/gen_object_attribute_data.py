import re
import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from process_data.keymap import person_map, city_map, force_map, inv_force_map, inv_person_map, inv_city_map


class MetaPattern(object):
    def __init__(self, msg, type='general'):
        """

        :param msg: pattern prompt: "[name]的[attr]是什么"
        """
        # self.msg = re.split('\[.*?\]',"[name]的[attr]是什么[xx]")
        self.raw_msg = msg
        self.keys = re.findall('\[(.*?)\]', msg)
        self.type = type

    def __str__(self):
        return self.raw_msg

    def __call__(self, **kwargs):
        """
        kwargs: '{entity_object: [entity]\{\"entity\":\"entity_object\",\"role\":\"role\"\}'
        :param kwargs:
        :return:
        """
        tmp = self.raw_msg
        for k, v in kwargs.items():
            tmp = re.sub(f"\[{k}]", v, tmp)
        return tmp


class GenAttriData(object):
    def __init__(self):
        self.intro_patterns = [
            MetaPattern("介绍下[name]"),
            MetaPattern("聊聊[name]"),
            MetaPattern("说说[name]"),
            MetaPattern("我想了解下[name]"),
            MetaPattern("[name]能介绍下嘛"),
            MetaPattern("你知道[name]吗"),
            MetaPattern("[name]的基本情况是怎样的")
        ]
        self.person_attri_patterns = [
            MetaPattern("[person]的[attri]是多少", 'num'),
            MetaPattern("[person]的[attri]能力怎样", 'rank'),
            MetaPattern("[person]的[attri]厉害吗", 'rank'),
            MetaPattern("[person]的[attri]是什么", 'skill'),  # 特技
            MetaPattern("[person]的[attri]都有谁", 'who'),  # 人
            MetaPattern("[person]的[attri]都哪些", 'who'),
            MetaPattern("[person]的[attri]在哪", 'place'),  # 出生地
            MetaPattern("[person]现在在哪", 'place')  # 现居地
        ]
        self.city_attri_pattens = [
            MetaPattern("[city]的[attri]是多少", 'num'),
            MetaPattern("[city]有多少[attri]", 'num'),  # 包括武将
            MetaPattern("[city]的[attri]是谁", 'who'),
            MetaPattern("[city]属于哪个[attri]", 'belong'),  # 势力,州
            MetaPattern("[city]现在有[attri]吗", 'merchant'),  # 商人
            MetaPattern("[city]的邻接[attri]有哪些", 'place'),  # 商人
        ]

        self.force_attri_patterns = [
            MetaPattern("[force]的[attri]是谁", 'who'),  #
            MetaPattern("谁是[force]的[attri]", 'who'),  #
        ]

    def gen_intro(self, entity, entity_type):
        name_entity = f'[{entity}]({entity_type})'
        return self._gen_intro(name_entity)

    def _gen_intro(self, name_entity):
        """

        :param name_entity: [entity](entity_type)
        :return:
        """
        data = {"name": name_entity}
        return [pt(**data) for pt in self.intro_patterns]

    def gen_person_attr(self, person_dict):
        person_dict.pop('序号')
        name = person_dict.pop(inv_person_map['name'])
        res = list()
        for k, v in person_dict.items():
            ck = person_map.get(k)  # column name
            if not ck:
                continue
            if ck == 'gender':
                continue
            if isinstance(v, float) and np.isnan(v):
                continue
            for pt in self.person_attri_patterns:
                if isinstance(v, int) and pt.type == 'num':
                    tmp = pt(**{"person": f'[{name}](person)', "attri": f"[{k}](person_attr)"})
                elif ck in ['skill', 'character'] and pt.type == 'skill':
                    tmp = pt(**{"name": f'[{name}](city)', "attri": f"[{k}](city_attr)"})
                elif 'city' in ck and pt.type == 'place':
                    tmp = pt(**{"person": f'[{name}](person)', "attri": f"[{k}](person_attr)"})
                elif ('person' in ck) and pt.type == 'who':
                    tmp = pt(**{"person": f'[{name}](person)', "attri": f"[{k}](person_attr)"})
                elif '适性' in k and pt.type == 'rank':
                    tmp = pt(**{"person": f'[{name}](person)', "attri": f"[{k.replace('适性','')}](person_attr)"})
                else:
                    continue
                res.append(tmp)
        return res

    def gen_city_attr(self, city_dict):
        city_dict.pop('序号')
        name = city_dict.pop(inv_city_map['name'])

        res = list()
        for k, v in city_dict.items():
            ck = city_map.get(k)  # column name
            if not ck:
                continue
            if '.' in k:
                continue
            for pt in self.city_attri_pattens:
                if isinstance(v, int) and pt.type == 'num':
                    tmp = pt(**{"city": f'[{name}](city)', "attri": f"[{k}](city_attr)"})
                elif ck == 'merchant' and pt.type == 'merchant':
                    tmp = pt(**{"city": f'[{name}](city)', "attri": f"[{k}](city_attr)"})
                elif 'city' in ck and pt.type == 'place':
                    tmp = pt(**{"city": f'[{name}](city)', "attri": f"[{k}](city_attr)"})
                elif ('mayor' in ck) and pt.type == 'who':
                    tmp = pt(**{"city": f'[{name}](city)', "attri": f"[{k}](city_attr)"})
                else:
                    continue
                res.append(tmp)
        return res

    def gen_force_attr(self, force_dict):
        force_dict.pop('序号')
        name = force_dict.pop(inv_force_map['name'])
        res = list()
        for k, v in force_dict.items():
            ck = force_map.get(k)
            if not ck:
                continue
            for pt in self.force_attri_patterns:
                tmp = pt(**{"force": f'[{name}](force)', "attri": f"[{k}](force_attr)"})
                res.append(tmp)

        return res

    @staticmethod
    def batch_gen(lst_lst):
        res = list()
        for lst in lst_lst:
            res += lst
        return res


if __name__ == '__main__':
    from tqdm import tqdm
    from random import choices, random, choice
    from gen_training_data.save2yml import intentdata2str, add_head, save2yml

    psn = pd.read_csv('./raw_data/武将.csv')
    ct = pd.read_csv('./raw_data/城市.csv')
    fc = pd.read_csv('./raw_data/势力.csv')

    gad = GenAttriData()

    # 介绍人物意图
    intro_person = gad.batch_gen([gad.gen_intro(x, 'person') for x in tqdm(psn['姓名']) if isinstance(x, str)])
    pts = intentdata2str('intro_person', intro_person)
    pts = add_head('nlu', pts)
    save2yml(pts, './data/nlu/intro_person.yml')

    # 介绍城池意图
    intro_city = gad.batch_gen([gad.gen_intro(x, 'city') for x in tqdm(ct['名称']) if isinstance(x, str)])
    cts = intentdata2str('intro_city', intro_city)
    cts = add_head('nlu', cts)
    save2yml(cts, './data/nlu/intro_city.yml')

    # 介绍势力意图
    intro_force = gad.batch_gen(
        [gad.gen_intro(x + choice(['国', '朝']) if random() > 0.5 and isinstance(x, str) and len(x) < 2 else x, 'force')
         for x in tqdm(fc['国号']) if isinstance(x, str)])
    fts = intentdata2str('intro_force', intro_force)
    fts = add_head('nlu', fts)
    save2yml(fts, './data/nlu/intro_force.yml')

    person_attr = gad.batch_gen([gad.gen_person_attr(x) for x in tqdm(psn.to_dict(orient='records'))])
    pts = intentdata2str('person_attr', person_attr)
    pts = add_head('nlu', pts)
    save2yml(pts, './data/nlu/person_attr.yml')


    city_attr = gad.batch_gen([gad.gen_city_attr(x) for x in tqdm(ct.to_dict(orient='records'))])
    pts = intentdata2str('city_attr', city_attr)
    pts = add_head('nlu', pts)
    save2yml(pts, './data/nlu/city_attr.yml')


    force_attr = gad.batch_gen([gad.gen_force_attr(x) for x in tqdm(fc.to_dict(orient='records'))])
    pts = intentdata2str('force_attr', force_attr)
    pts = add_head('nlu', pts)
    save2yml(pts, './data/nlu/force_attr.yml')