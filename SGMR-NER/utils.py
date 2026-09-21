import random


class Prompt:
    def __init__(self, dataset):
        self.dataset = dataset

        if self.dataset not in ['CoNLL2003', 'ACE2004', 'ACE2005', 'WNUT2017']:
            raise NotImplementedError(f'This dataset {self.dataset} is not used!')

        if self.dataset == 'CoNLL2003':
            self.baseline_prompt = (
                'Please list all named entities of the following entity types in the input sentence:\n'
                '- PER\n'
                '- ORG\n'
                '- LOC\n'
                '- MISC\n'
                'You should output your results in the format {"type": [entity]} as a json.'
            )

            self.icl_prompt1 = (
                'Please list all named entities of the following entity types in the input sentence:\n'
                '- PER\n'
                '- ORG\n'
                '- LOC\n'
                '- MISC\n'
                'Here are some examples:\n'
            )

            self.icl_prompt2 = 'You should output your results in the format {"type": [entity]} as a json.'

            self.picl_prompt1 = (
                'Please list all named entities of the following entity types in the input sentence:\n'
                '- PER: e.g. {PER}\n'
                '- ORG: e.g. {ORG}\n'
                '- LOC: e.g. {LOC}\n'
                '- MISC: e.g. {MISC}\n'
            )

            self.picl_prompt2 = self.icl_prompt2

            self.fusion_prompt = self.picl_prompt1 + 'Here are some examples:\n'

        elif self.dataset == 'WNUT2017':
            self.baseline_prompt = (
                'Please list all named entities of the following entity types in the input sentence:\n'
                '- person\n'
                '- location\n'
                '- corporation\n'
                '- product\n'
                '- creative-work\n'
                '- group\n'
                'You should output your results in the format {"type": [entity]} as a json.'
            )

            self.icl_prompt1 = self.baseline_prompt.replace(
                'You should output your results in the format {"type": [entity]} as a json.',
                'Here are some examples:\n'
            )

            self.icl_prompt2 = 'You should output your results in the format {"type": [entity]} as a json.'

            self.picl_prompt1 = (
                '- person: e.g. {person}\n'
                '- location: e.g. {location}\n'
                '- corporation: e.g. {corporation}\n'
                '- product: e.g. {product}\n'
                '- creative-work: e.g. {creative_work}\n'
                '- group: e.g. {group}\n'
            )

            self.picl_prompt2 = self.icl_prompt2

            self.fusion_prompt = self.picl_prompt1 + 'Here are some examples:\n'

        elif self.dataset == 'ACE2004' or self.dataset == 'ACE2005':

            # ✅ 全部改为ACE标准标签
            self.baseline_prompt = (
                'Please list all named entities of the following entity types in the input sentence:\n'
                '- PER (person)\n'
                '- ORG (organization)\n'
                '- GPE (countries, cities, regions)\n'
                '- LOC (location)\n'
                '- FAC (facility)\n'
                '- VEH (vehicle)\n'
                '- WEA (weapon)\n'
                'You should output your results in the format {"type": [entity]} as a json.'
            )

            self.icl_prompt1 = (
                'Please list all named entities of the following entity types in the input sentence:\n'
                '- PER (person)\n'
                '- ORG (organization)\n'
                '- GPE (countries, cities, regions)\n'
                '- LOC (location)\n'
                '- FAC (facility)\n'
                '- VEH (vehicle)\n'
                '- WEA (weapon)\n'
                'Here are some examples:\n'
            )

            self.icl_prompt2 = 'You should output your results in the format {"type": [entity]} as a json.'

            self.picl_prompt1 = (
                '- PER: e.g. {PER}\n'
                '- ORG: e.g. {ORG}\n'
                '- GPE: e.g. {GPE}\n'
                '- LOC: e.g. {LOC}\n'
                '- FAC: e.g. {FAC}\n'
                '- VEH: e.g. {VEH}\n'
                '- WEA: e.g. {WEA}\n'
            )

            self.picl_prompt2 = self.icl_prompt2

            self.fusion_prompt = self.picl_prompt1 + 'Here are some examples:\n'


class PointICL:
    def __init__(self, dataset, type2entity, point_entity_cnt, use_bert=False):
        self.dataset = dataset
        self.type2entity = type2entity
        self.cnt = point_entity_cnt
        self.use_bert = use_bert
        self.point_entity = {}

    def safe_sample(self, key):
        """
        支持大小写自动适配
        """
        # 优先原始 key
        if key in self.type2entity:
            lst = self.type2entity[key]
        # 尝试大写
        elif key.upper() in self.type2entity:
            lst = self.type2entity[key.upper()]
        # 尝试小写
        elif key.lower() in self.type2entity:
            lst = self.type2entity[key.lower()]
        else:
            lst = []

        return random.sample(lst, min(len(lst), self.cnt)) if lst else []

    def get_point_entity(self):

        # =========================================================
        # CoNLL2003
        # =========================================================
        if self.dataset == 'CoNLL2003':
            self.point_entity = {
                'per': self.safe_sample('PER'),
                'org': self.safe_sample('ORG'),
                'loc': self.safe_sample('LOC'),
                'misc': self.safe_sample('MISC')
            }

        # =========================================================
        # WNUT2017 ⭐（关键修复）
        # =========================================================
        elif self.dataset == 'WNUT2017':
            self.point_entity = {
                'person': self.safe_sample('PERSON'),
                'location': self.safe_sample('LOCATION'),
                'corporation': self.safe_sample('CORPORATION'),
                'product': self.safe_sample('PRODUCT'),
                'creative-work': self.safe_sample('CREATIVE-WORK'),
                'group': self.safe_sample('GROUP')
            }

        # =========================================================
        # ACE2004 / ACE2005
        # =========================================================
        elif self.dataset in ['ACE2004', 'ACE2005']:
            self.point_entity = {
                'PER': self.safe_sample('PER'),
                'ORG': self.safe_sample('ORG'),
                'GPE': self.safe_sample('GPE'),
                'LOC': self.safe_sample('LOC'),
                'FAC': self.safe_sample('FAC'),
                'VEH': self.safe_sample('VEH'),
                'WEA': self.safe_sample('WEA')
            }

        return self.point_entity