from py2neo import Graph, RelationshipMatcher, NodeMatcher, STARTS_WITH, ENDS_WITH


class SearchDB(object):
    def __init__(self):
        self.graph = Graph('bolt://localhost:7687', user='neo4j', password='`')
        self.nmathcer = NodeMatcher(self.graph)
        self.rmatcher = RelationshipMatcher(self.graph)

    async def node_search(self, ntype, count=None, all=None, limit=None, **kwargs):
        if count:
            return self.nmathcer.match(ntype, **kwargs).count()
        if all:
            return self.nmathcer.match(ntype, **kwargs).all()
        if limit:
            return self.nmathcer.match(ntype, **kwargs).limit(limit)
        else:
            return self.nmathcer.match(ntype, **kwargs).first()

    async def node_get(self, id_):
        return self.nmathcer.get(id_)

    async def rel_get(self, id_):
        return self.rmatcher.get(id_)

    async def rel_search(self, nd, rtype, **kwargs):
        if 'count' in kwargs:
            return self.nmathcer.match(nd, rtype).count()
        if 'limit' in kwargs:
            return self.nmathcer.match(nd, rtype).limit(kwargs['limit'])
        else:
            return self.nmathcer.match(nd, rtype).first()

    async def shortestpath(self, city1, city2):
        s = """MATCH (c1:City {name:""" + f'"{city1}"' + """}), (c2:City{name:""" + f'"{city2}"' + """}),
        p = shortestPath((c1)-[r:cc_neighbor_city_of*..10]->(c2))
        RETURN p LIMIT 1
        """
        p = self.graph.run(s)
        p = p.data()
        nodes = p[0]['p'].nodes
        return nodes

    async def person(self, name):
        return self.nmathcer.match('Person', name=name).first()

    async def person_attr(self, name, attr):
        if attr in ['pp_person_like', 'pp_person_hate']:  # 所有 name 喜欢/厌恶 的武将
            rs = self.rmatcher.match(r_type=attr).all()
            return [r.end_node for r in rs if r.start_node.get('name') == name]
        elif attr == 'like_he':  # 所有喜欢 name 的武将
            rs = self.rmatcher.match(r_type='pp_person_like').all()
            return [r.start_node for r in rs if r.end_node.get('name') == name]
        elif attr == 'hate_he':  # 所有厌恶 name 的武将
            rs = self.rmatcher.match(r_type='pp_person_hate').all()
            return [r.start_node for r in rs if r.end_node.get('name') == name]
        elif attr in ['pp_blood_source_of', 'pf_member_of', 'pp_father_of', 'pc_birth_place',
                      'pc_city_now_in', 'pc_city_belongto']:
            rs = self.rmatcher.match(r_type=attr).all()
            for r in rs:
                if r.start_node.get('name') == name:
                    return r.end_node
        elif attr == 'descendants':  # name 所有儿子
            rs = self.rmatcher.match(r_type='pp_father_of').all()
            return [r.start_node for r in rs if r.end_node.get('name') == name]
        elif attr == 'descendants':  # name 所有后代
            rs = self.rmatcher.match(r_type='pp_blood_source_of').all()
            return [r.start_node for r in rs if r.end_node.get('name') == name]
        else:
            ps = self.nmathcer.match('Person', name=name).first()
            return ps.get(attr)

    async def city(self, name):
        return self.nmathcer.match('City', name=name).first()

    async def city_attr(self, name, attr):
        if attr in ['pc_city_belongto', 'pc_birth_place', 'pc_city_now_in']:
            rs = self.rmatcher.match(r_type=attr).all()
            return [r.start_node for r in rs if r.end_node.get('name') == name]
        elif attr in ['cp_mayor_of', 'cf_force_belongto']:
            rs = self.rmatcher.match(r_type=attr).all()
            for r in rs:
                if r.start_node.get('name') == name:
                    return r.end_node
        elif attr == 'cc_neighbor_city_of':
            rs = self.rmatcher.match(r_type=attr).all()
            return [r.end_node for r in rs if r.start_node.get('name') == name]

        else:
            nd = self.nmathcer.match('City', name=name).first()
            return nd.get(attr)

    async def states(self):
        cities = self.nmathcer.match('City').all()
        states = [nd.get('state') for nd in cities]
        return list(set(states))

    async def cities_in_state(self, state: str):
        cities = self.nmathcer.match('City').all()
        cities = [nd for nd in cities if nd.get('state') == state]
        return cities

    async def force(self, name):
        fc = self.nmathcer.match('Force', name=name).first()
        return fc

    async def force_attr(self, name, attr):
        fc = self.nmathcer.match('Force', name=name).first()

        # 君主
        if attr == 'boss' or attr == 'fp_boss_of':
            r = self.rmatcher.match([fc], r_type='fp_boss_of').first()
            return r.end_node
        # 军师
        elif attr == 'fp_counsellor_of' or attr == 'counsellor':
            r = self.rmatcher.match([fc], r_type='fp_counsellor_of').first()
            return r.end_node
        # 武将
        elif attr == 'people' or attr == 'member' or attr == 'pf_member_of':
            rs = self.rmatcher.match(r_type='pf_member_of').all()
            return [r.start_node for r in rs if r.end_node.get('name') == name]
        else:

            rs = self.rmatcher.match(r_type='cf_force_belongto').all()
            cities = [r.start_node for r in rs if r.end_node.get('name') == name]
            # 城市
            if attr == 'cities' or attr == 'city' or attr == 'cf_force_belongto':
                return cities
            # 基信息如钱粮等
            elif attr in ['jinum', 'swordnum', 'endurance', 'solidernum', 'food',
                          'qiangnum', 'horsenum', 'money', 'safety', 'id', 'nunum']:
                return sum([x.get('food', 0.) for x in cities])

    async def get_people_with_family_name(self, family_name):
        """
        找到所有姓‘family name’的人
        :param family_name:
        :return:
        """
        return self.nmathcer.match('Person', name=STARTS_WITH(family_name)).all()

    async def force_with_family_name(self, force, family_name):
        """
        势力中所有姓"family_name"的人
        :param force:
        :param family_name:
        :return:
        """
        persons = self.force_attr(force, 'pf_member_of')
        return [x for x in persons if x.get('name', 'x')[0] == family_name]

    async def city_with_family_name(self, city, family_name, attr='pc_city_now_in'):
        """
        城池中姓 'family name' 的人
        :param city:
        :param family_name:
        :param attr:  ['pc_city_belongto', 'pc_birth_place', 'pc_city_now_in']
        :return:
        """
        persons = self.city_attr(city, attr)
        return [x for x in persons if x.get('name', 'x')[0] == family_name]


if __name__ == '__main__':
    sdb = SearchDB()
