from process_data.search_neo import SearchDB


class advanceCompare(SearchDB):
    def __init__(self):
        super(advanceCompare, self).__init__()

    def person_rank(self, namelist, attr, rank_type='equal'):
        """

        :param namelist:
        :param attr:
        :param rank_type: max, min, equal
        :return:
        """
        # 是否 属性
        # 两人之间相互喜欢/讨厌
        if attr in ['pp_person_like', 'pp_person_hate'] and len(namelist) == 2:
            pass
        # 三人及以上相互喜欢/讨厌
        # elif todo

        elif attr in ['pp_blood_source_of', 'pf_member_of', 'pp_father_of', 'pc_birth_place',
                      'pc_city_now_in', 'pc_city_belongto', 'pp_father_of', 'pp_blood_source_of']:
            pass
        else:
            res = [(name, self.person_attr(name, attr)) for name in namelist]
            if rank_type == 'equal':
                return len(set([x[1] for x in res])) == 1
            return sorted(res, key=lambda x: x[-1]) if rank_type == 'min' else sorted(res, key=lambda x: -x[-1])

    def city_rank(self, namelist, attr, rank_type='equal'):
        res = [(name, self.city_attr(name, attr)) for name in namelist]
        if rank_type == 'equal':
            return len(set([x[1] for x in res])) == 1
        return sorted(res, key=lambda x: x[-1]) if rank_type == 'min' else sorted(res, key=lambda x: -x[-1])

    def force_rank(self, namelist, attr, rank_type='equal'):
        res = [(name, self.force_attr(name, attr)) for name in namelist]
        if rank_type == 'equal':
            return len(set([x[1] for x in res])) == 1
        return sorted(res, key=lambda x: x[-1]) if rank_type == 'min' else sorted(res, key=lambda x: -x[-1])

if __name__ == '__main__':
    ac = advanceCompare()