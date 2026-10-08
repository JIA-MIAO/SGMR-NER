import random


class Prompt:
    def __init__(self, dataset):
        self.dataset = dataset

        # Datasets used in the paper
        if self.dataset not in [
            'CoNLL03',
            'WNUT17',
            'ACE04',
            'ACE05',
            'JNLPBA',
            'BC5CDR'
        ]:
            raise NotImplementedError(
                f'This dataset {self.dataset} is not used!'
            )

        # =========================================================
        # CoNLL03
        # Entity types: PER, ORG, LOC, MISC
        # =========================================================
        if self.dataset == 'CoNLL03':
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

            self.icl_prompt2 = (
                'You should output your results in the format '
                '{"type": [entity]} as a json.'
            )

            self.picl_prompt1 = (
                'Please list all named entities of the following entity types in the input sentence:\n'
                '- PER: e.g. {PER}\n'
                '- ORG: e.g. {ORG}\n'
                '- LOC: e.g. {LOC}\n'
                '- MISC: e.g. {MISC}\n'
            )

            self.picl_prompt2 = self.icl_prompt2

            self.fusion_prompt = (
                self.picl_prompt1 + 'Here are some examples:\n'
            )

        # =========================================================
        # WNUT17
        # Entity types:
        # person, location, corporation, product,
        # creative-work, group
        # =========================================================
        elif self.dataset == 'WNUT17':
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

            self.icl_prompt1 = (
                'Please list all named entities of the following entity types in the input sentence:\n'
                '- person\n'
                '- location\n'
                '- corporation\n'
                '- product\n'
                '- creative-work\n'
                '- group\n'
                'Here are some examples:\n'
            )

            self.icl_prompt2 = (
                'You should output your results in the format '
                '{"type": [entity]} as a json.'
            )

            self.picl_prompt1 = (
                '- person: e.g. {person}\n'
                '- location: e.g. {location}\n'
                '- corporation: e.g. {corporation}\n'
                '- product: e.g. {product}\n'
                '- creative-work: e.g. {creative_work}\n'
                '- group: e.g. {group}\n'
            )

            self.picl_prompt2 = self.icl_prompt2

            self.fusion_prompt = (
                self.picl_prompt1 + 'Here are some examples:\n'
            )

        # =========================================================
        # ACE04 / ACE05
        # Entity types:
        # PER, ORG, GPE, LOC, FAC, VEH, WEA
        # =========================================================
        elif self.dataset in ['ACE04', 'ACE05']:
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

            self.icl_prompt2 = (
                'You should output your results in the format '
                '{"type": [entity]} as a json.'
            )

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

            self.fusion_prompt = (
                self.picl_prompt1 + 'Here are some examples:\n'
            )

        # =========================================================
        # JNLPBA
        # Entity types:
        # DNA, RNA, protein, cell_type, cell_line
        # =========================================================
        elif self.dataset == 'JNLPBA':
            self.baseline_prompt = (
                'Please list all named entities of the following entity types in the input sentence:\n'
                '- DNA\n'
                '- RNA\n'
                '- protein\n'
                '- cell_type\n'
                '- cell_line\n'
                'You should output your results in the format {"type": [entity]} as a json.'
            )

            self.icl_prompt1 = (
                'Please list all named entities of the following entity types in the input sentence:\n'
                '- DNA\n'
                '- RNA\n'
                '- protein\n'
                '- cell_type\n'
                '- cell_line\n'
                'Here are some examples:\n'
            )

            self.icl_prompt2 = (
                'You should output your results in the format '
                '{"type": [entity]} as a json.'
            )

            self.picl_prompt1 = (
                '- DNA: e.g. {DNA}\n'
                '- RNA: e.g. {RNA}\n'
                '- protein: e.g. {protein}\n'
                '- cell_type: e.g. {cell_type}\n'
                '- cell_line: e.g. {cell_line}\n'
            )

            self.picl_prompt2 = self.icl_prompt2

            self.fusion_prompt = (
                self.picl_prompt1 + 'Here are some examples:\n'
            )

        # =========================================================
        # BC5CDR
        # Entity types: Chemical, Disease
        # =========================================================
        elif self.dataset == 'BC5CDR':
            self.baseline_prompt = (
                'Please list all named entities of the following entity types in the input sentence:\n'
                '- Chemical\n'
                '- Disease\n'
                'You should output your results in the format {"type": [entity]} as a json.'
            )

            self.icl_prompt1 = (
                'Please list all named entities of the following entity types in the input sentence:\n'
                '- Chemical\n'
                '- Disease\n'
                'Here are some examples:\n'
            )

            self.icl_prompt2 = (
                'You should output your results in the format '
                '{"type": [entity]} as a json.'
            )

            self.picl_prompt1 = (
                '- Chemical: e.g. {Chemical}\n'
                '- Disease: e.g. {Disease}\n'
            )

            self.picl_prompt2 = self.icl_prompt2

            self.fusion_prompt = (
                self.picl_prompt1 + 'Here are some examples:\n'
            )


class PointICL:
    def __init__(
        self,
        dataset,
        type2entity,
        point_entity_cnt,
        use_bert=False
    ):
        self.dataset = dataset
        self.type2entity = type2entity
        self.cnt = point_entity_cnt
        self.use_bert = use_bert
        self.point_entity = {}

    def safe_sample(self, key):
        """
        Sample point entities while supporting automatic
        case adaptation of entity type keys.
        """

        # Prefer the original key
        if key in self.type2entity:
            lst = self.type2entity[key]

        # Try uppercase
        elif key.upper() in self.type2entity:
            lst = self.type2entity[key.upper()]

        # Try lowercase
        elif key.lower() in self.type2entity:
            lst = self.type2entity[key.lower()]

        # No matching entity type
        else:
            lst = []

        return (
            random.sample(lst, min(len(lst), self.cnt))
            if lst
            else []
        )

    def get_point_entity(self):

        # =========================================================
        # CoNLL03
        # =========================================================
        if self.dataset == 'CoNLL03':
            self.point_entity = {
                'per': self.safe_sample('PER'),
                'org': self.safe_sample('ORG'),
                'loc': self.safe_sample('LOC'),
                'misc': self.safe_sample('MISC')
            }

        # =========================================================
        # WNUT17
        # =========================================================
        elif self.dataset == 'WNUT17':
            self.point_entity = {
                'person': self.safe_sample('PERSON'),
                'location': self.safe_sample('LOCATION'),
                'corporation': self.safe_sample('CORPORATION'),
                'product': self.safe_sample('PRODUCT'),
                'creative-work': self.safe_sample('CREATIVE-WORK'),
                'group': self.safe_sample('GROUP')
            }

        # =========================================================
        # ACE04 / ACE05
        # =========================================================
        elif self.dataset in ['ACE04', 'ACE05']:
            self.point_entity = {
                'PER': self.safe_sample('PER'),
                'ORG': self.safe_sample('ORG'),
                'GPE': self.safe_sample('GPE'),
                'LOC': self.safe_sample('LOC'),
                'FAC': self.safe_sample('FAC'),
                'VEH': self.safe_sample('VEH'),
                'WEA': self.safe_sample('WEA')
            }

        # =========================================================
        # JNLPBA
        # =========================================================
        elif self.dataset == 'JNLPBA':
            self.point_entity = {
                'DNA': self.safe_sample('DNA'),
                'RNA': self.safe_sample('RNA'),
                'protein': self.safe_sample('protein'),
                'cell_type': self.safe_sample('cell_type'),
                'cell_line': self.safe_sample('cell_line')
            }

        # =========================================================
        # BC5CDR
        # =========================================================
        elif self.dataset == 'BC5CDR':
            self.point_entity = {
                'Chemical': self.safe_sample('Chemical'),
                'Disease': self.safe_sample('Disease')
            }

        return self.point_entity
