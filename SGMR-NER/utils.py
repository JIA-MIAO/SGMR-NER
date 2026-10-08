import random


class Prompt:
    """
    Dataset-specific prompt configuration.

    The prompt definitions are kept compatible with the original
    P-ICL / ICL implementation while providing unified interfaces
    for the six datasets used in SGMR-NER.
    """

    DATASETS = [
        'CoNLL03',
        'WNUT17',
        'ACE04',
        'ACE05',
        'JNLPBA',
        'BC5CDR'
    ]

    ENTITY_TYPES = {
        'CoNLL03': [
            'PER',
            'ORG',
            'LOC',
            'MISC'
        ],

        'WNUT17': [
            'person',
            'location',
            'corporation',
            'product',
            'creative-work',
            'group'
        ],

        'ACE04': [
            'PER',
            'ORG',
            'GPE',
            'LOC',
            'FAC',
            'VEH',
            'WEA'
        ],

        'ACE05': [
            'PER',
            'ORG',
            'GPE',
            'LOC',
            'FAC',
            'VEH',
            'WEA'
        ],

        'JNLPBA': [
            'DNA',
            'RNA',
            'protein',
            'cell_type',
            'cell_line'
        ],

        'BC5CDR': [
            'Chemical',
            'Disease'
        ]
    }

    def __init__(self, dataset):

        if dataset not in self.DATASETS:
            raise NotImplementedError(
                f'This dataset {dataset} is not used!'
            )

        self.dataset = dataset

        # Keep the exact label order used by the dataset.
        self.entity_types = list(
            self.ENTITY_TYPES[dataset]
        )

        self._build_prompts()

    # =====================================================
    # Prompt construction
    # =====================================================
    def _build_prompts(self):

        if self.dataset == 'CoNLL03':

            self.baseline_prompt = (
                'Please list all named entities of the following '
                'entity types in the input sentence:\n'
                '- PER\n'
                '- ORG\n'
                '- LOC\n'
                '- MISC\n'
                '\n'
                'Entities should be continuous spans from the input '
                'sentence. Prefer complete entity names and do not '
                'invent entities.\n'
                '\n'
                'You should output your results in the format '
                '{"type": [entity]} as a JSON.'
            )

            self.icl_prompt1 = (
                'Please list all named entities of the following '
                'entity types in the input sentence:\n'
                '- PER\n'
                '- ORG\n'
                '- LOC\n'
                '- MISC\n'
                '\n'
                'Here are some examples:\n'
            )

            self.picl_prompt1 = (
                'Please list all named entities of the following '
                'entity types in the input sentence:\n'
                '- PER: e.g. {PER}\n'
                '- ORG: e.g. {ORG}\n'
                '- LOC: e.g. {LOC}\n'
                '- MISC: e.g. {MISC}\n'
            )

        elif self.dataset == 'WNUT17':

            self.baseline_prompt = (
                'Please list all named entities of the following '
                'entity types in the input sentence:\n'
                '- person\n'
                '- location\n'
                '- corporation\n'
                '- product\n'
                '- creative-work\n'
                '- group\n'
                '\n'
                'Entities should be continuous spans from the input '
                'sentence. Prefer complete entity names and do not '
                'invent entities.\n'
                '\n'
                'You should output your results in the format '
                '{"type": [entity]} as a JSON.'
            )

            self.icl_prompt1 = (
                'Please list all named entities of the following '
                'entity types in the input sentence:\n'
                '- person\n'
                '- location\n'
                '- corporation\n'
                '- product\n'
                '- creative-work\n'
                '- group\n'
                '\n'
                'Here are some examples:\n'
            )

            self.picl_prompt1 = (
                '- person: e.g. {person}\n'
                '- location: e.g. {location}\n'
                '- corporation: e.g. {corporation}\n'
                '- product: e.g. {product}\n'
                '- creative-work: e.g. {creative-work}\n'
                '- group: e.g. {group}\n'
            )

        elif self.dataset in [
            'ACE04',
            'ACE05'
        ]:

            self.baseline_prompt = (
                'Please list all named entities of the following '
                'entity types in the input sentence:\n'
                '- PER (person)\n'
                '- ORG (organization)\n'
                '- GPE (countries, cities, regions)\n'
                '- LOC (location)\n'
                '- FAC (facility)\n'
                '- VEH (vehicle)\n'
                '- WEA (weapon)\n'
                '\n'
                'Entities should be continuous spans from the input '
                'sentence. Prefer complete entity names and do not '
                'invent entities.\n'
                '\n'
                'You should output your results in the format '
                '{"type": [entity]} as a JSON.'
            )

            self.icl_prompt1 = (
                'Please list all named entities of the following '
                'entity types in the input sentence:\n'
                '- PER (person)\n'
                '- ORG (organization)\n'
                '- GPE (countries, cities, regions)\n'
                '- LOC (location)\n'
                '- FAC (facility)\n'
                '- VEH (vehicle)\n'
                '- WEA (weapon)\n'
                '\n'
                'Here are some examples:\n'
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

        elif self.dataset == 'JNLPBA':

            self.baseline_prompt = (
                'Please list all named entities of the following '
                'entity types in the input sentence:\n'
                '- DNA\n'
                '- RNA\n'
                '- protein\n'
                '- cell_type\n'
                '- cell_line\n'
                '\n'
                'Entities should be continuous spans from the input '
                'sentence. Prefer complete entity names and do not '
                'invent entities.\n'
                '\n'
                'You should output your results in the format '
                '{"type": [entity]} as a JSON.'
            )

            self.icl_prompt1 = (
                'Please list all named entities of the following '
                'entity types in the input sentence:\n'
                '- DNA\n'
                '- RNA\n'
                '- protein\n'
                '- cell_type\n'
                '- cell_line\n'
                '\n'
                'Here are some examples:\n'
            )

            self.picl_prompt1 = (
                '- DNA: e.g. {DNA}\n'
                '- RNA: e.g. {RNA}\n'
                '- protein: e.g. {protein}\n'
                '- cell_type: e.g. {cell_type}\n'
                '- cell_line: e.g. {cell_line}\n'
            )

        elif self.dataset == 'BC5CDR':

            self.baseline_prompt = (
                'Please list all named entities of the following '
                'entity types in the input sentence:\n'
                '- Chemical\n'
                '- Disease\n'
                '\n'
                'Entities should be continuous spans from the input '
                'sentence. Prefer complete entity names and do not '
                'invent entities.\n'
                '\n'
                'You should output your results in the format '
                '{"type": [entity]} as a JSON.'
            )

            self.icl_prompt1 = (
                'Please list all named entities of the following '
                'entity types in the input sentence:\n'
                '- Chemical\n'
                '- Disease\n'
                '\n'
                'Here are some examples:\n'
            )

            self.picl_prompt1 = (
                '- Chemical: e.g. {Chemical}\n'
                '- Disease: e.g. {Disease}\n'
            )

        # -------------------------------------------------
        # Common prompt endings
        # -------------------------------------------------
        self.icl_prompt2 = (
            'You should output your results in the format '
            '{"type": [entity]} as a JSON.'
        )

        self.picl_prompt2 = self.icl_prompt2

        self.fusion_prompt = (
            self.picl_prompt1
            + 'Here are some examples:\n'
        )

    # =====================================================
    # Unified interfaces
    # =====================================================
    def get_entity_types(self):
        return list(self.entity_types)

    def get_baseline_prompt(self):
        return self.baseline_prompt

    def get_icl_prompt(
        self,
        demonstrations=''
    ):
        return (
            self.icl_prompt1
            + demonstrations
            + '\n'
            + self.icl_prompt2
        )

    def get_picl_prompt(
        self,
        point_entities=''
    ):
        return (
            self.picl_prompt1
            .format(**self._safe_format_dict(point_entities))
            + '\n'
            + self.picl_prompt2
        )

    def get_fusion_prompt(
        self,
        point_entities='',
        demonstrations=''
    ):
        point_prompt = self.picl_prompt1

        if point_entities:
            point_prompt = point_prompt.format(
                **self._safe_format_dict(
                    point_entities
                )
            )

        return (
            point_prompt
            + 'Here are some examples:\n'
            + demonstrations
            + '\n'
            + self.picl_prompt2
        )

    @staticmethod
    def _safe_format_dict(point_entities):

        if isinstance(point_entities, dict):
            return point_entities

        return {}


class PointICL:
    """
    Point-based In-Context Learning entity sampler.

    The class preserves the original P-ICL interface while making
    entity-type handling consistent across all six datasets.
    """

    DATASETS = Prompt.DATASETS

    ENTITY_TYPES = Prompt.ENTITY_TYPES

    def __init__(
        self,
        dataset,
        type2entity,
        point_entity_cnt,
        use_bert=False
    ):

        if dataset not in self.DATASETS:
            raise NotImplementedError(
                f'This dataset {dataset} is not used!'
            )

        self.dataset = dataset
        self.type2entity = type2entity or {}
        self.cnt = max(
            0,
            int(point_entity_cnt)
        )
        self.use_bert = use_bert

        self.entity_types = list(
            self.ENTITY_TYPES[dataset]
        )

        self.point_entity = {
            entity_type: []
            for entity_type in self.entity_types
        }

    # =====================================================
    # Type matching
    # =====================================================
    def _resolve_key(self, key):

        if key in self.type2entity:
            return key

        key_lower = str(key).lower()

        # Exact case-insensitive match
        for existing_key in self.type2entity:

            if str(existing_key).lower() == key_lower:
                return existing_key


        normalized_key = (
            key_lower
            .replace('_', '-')
        )

        for existing_key in self.type2entity:

            normalized_existing = (
                str(existing_key)
                .lower()
                .replace('_', '-')
            )

            if normalized_existing == normalized_key:
                return existing_key

        return None

    # =====================================================
    # Safe sampling
    # =====================================================
    def safe_sample(self, key):

        resolved_key = self._resolve_key(
            key
        )

        if resolved_key is None:
            return []

        entities = self.type2entity.get(
            resolved_key,
            []
        )

        if not entities:
            return []

        clean_entities = []

        for entity in entities:

            if not isinstance(entity, str):
                continue

            entity = entity.strip()

            if entity:
                clean_entities.append(
                    entity
                )

        if not clean_entities:
            return []

        sample_count = min(
            len(clean_entities),
            self.cnt
        )

        if sample_count <= 0:
            return []

        return random.sample(
            clean_entities,
            sample_count
        )

    # =====================================================
    # Point entity generation
    # =====================================================
    def get_point_entity(self):

        point_entity = {}

        for entity_type in self.entity_types:

            point_entity[entity_type] = (
                self.safe_sample(
                    entity_type
                )
            )

        self.point_entity = point_entity

        return self.point_entity


    def get_point_entity_prompt(self):

        point_entity = (
            self.get_point_entity()
        )

        blocks = []

        for entity_type in self.entity_types:

            entities = point_entity.get(
                entity_type,
                []
            )

            if not entities:
                continue

            entity_text = ', '.join(
                f'"{entity}"'
                for entity in entities
            )

            blocks.append(
                f'- {entity_type}: '
                f'{entity_text}'
            )

        return '\n'.join(blocks)


    def reset(self):

        self.point_entity = {
            entity_type: []
            for entity_type in self.entity_types
        }


    def update_type2entity(
        self,
        type2entity
    ):

        self.type2entity = (
            type2entity or {}
        )

        self.reset()
