person_map = {'序号': 'pid', '姓名': 'name',
              '势力': 'pf_member_of',
              '所属': 'pc_city_belongto',
              '所在': 'pc_city_now_in',
              '官职': 'title', '性格': 'character',
              '身份': 'identiy', '忠诚': 'fidelity', '统御': 'lead', '武力': 'strength', '智力': 'iq', '政治': 'polity',
              '魅力': 'charm', '出生年': 'birthyear', '死亡年': 'deathyear', '相性': 'style', "性别": "gender",
              '血缘': 'pp_blood_source_of ', "世代": "generation",
              '父亲': 'pp_father_of ', "配偶": 'pp_mate_of ',
              '亲近武将': 'pp_person_like1', '亲近武将.1': 'pp_person_like2', '亲近武将.2': 'pp_person_like3',
              '亲近武将.3': 'pp_person_like4', '亲近武将.4': 'pp_person_like5',
              '厌恶武将': 'pp_person_hate1', '厌恶武将.1': 'pp_person_hate2', '厌恶武将.2': 'pp_person_hate3',
              '厌恶武将.3': 'pp_person_hate4', '厌恶武将.4': 'pp_person_hate5',
              '特技': 'skill',
              '出身地': 'pc_birth_place',
              '枪兵适性': 'qiangbing',
              '戟兵适性': 'jibing', '弩兵适性': 'nubing', '骑兵适性': 'qibing', '兵器适性': 'bingqi', '水军适性': 'shuijun'}

city_map = {'序号': "cid",
            '名称': "name",
            '太守': "cp_mayor_of",
            '势力': "cf_force_belongto",
            '士兵': "solidernum",
            '金钱': "money",
            '兵粮': "food",
            '剑': "swordnum",
            '枪': "qiangnum",
            '戟': "jinum",
            '弩': "nunum",
            '军马': "horsenum",
            '商人': "merchant",
            '最大耐久': "endurance",
            '治安': "safety",
            '州': "state",
            '邻接城市': "cc_neighbor_city_of1",
            '邻接城市.1': "cc_neighbor_city_of2",
            '邻接城市.2': "cc_neighbor_city_of3",
            '邻接城市.3': "cc_neighbor_city_of4",
            '邻接城市.4': "cc_neighbor_city_of5"}

force_map = {'序号': "fid",
             '君主': "fp_boss_of",
             '军师': "fp_counsellor_of",
             '国号': "name"}

inv_person_map = {v: k for k, v in person_map.items()}
inv_city_map = {v: k for k, v in city_map.items()}
inv_force_map = {v: k for k, v in force_map.items()}
