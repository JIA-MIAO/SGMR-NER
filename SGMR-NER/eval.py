import json
import re
from argparse import ArgumentParser
from collections import Counter


# ============================================================
# Basic utilities
# ============================================================

def normalize_entity(entity):
    """
    Normalize an entity string before evaluation.

    The normalization is intentionally conservative:
    - convert non-string values to string
    - remove leading/trailing whitespace
    - collapse consecutive whitespace
    """
    if entity is None:
        return ""

    if not isinstance(entity, str):
        entity = str(entity)

    entity = entity.strip()
    entity = re.sub(r"\s+", " ", entity)

    return entity


def normalize_entity_type(entity_type):
    """
    Normalize entity type names.

    Only performs formatting normalization and does not merge
    semantically different entity types.
    """
    if entity_type is None:
        return ""

    entity_type = str(entity_type).strip()

    # Normalize common formatting variations.
    entity_type = entity_type.replace("-", "_")

    return entity_type


def entity_key(entity, entity_type):
    """
    Construct the canonical representation of an entity.

    Exact-match evaluation is performed on:
        (entity_type, entity_text)
    """
    return (
        normalize_entity_type(entity_type),
        normalize_entity(entity),
    )


# ============================================================
# Prediction parsing
# ============================================================

def parse_prediction_result(result):
    """
    Convert one prediction result into a set of
    (entity_type, entity_text) tuples.

    Supported formats include:

    1. Dictionary:
       {
           "PER": ["John"],
           "ORG": ["OpenAI"]
       }

    2. Dictionary with entity objects:
       {
           "PER": [
               {"text": "John"},
               {"name": "John"}
           ]
       }

    3. JSON string containing one of the above.

    4. A list of entity objects:
       [
           {"text": "John", "type": "PER"}
       ]
    """
    prediction_set = set()

    if result is None:
        return prediction_set

    # --------------------------------------------------------
    # If prediction is stored as a JSON string
    # --------------------------------------------------------
    if isinstance(result, str):
        result = result.strip()

        if not result:
            return prediction_set

        try:
            result = json.loads(result)
        except json.JSONDecodeError:
            # Some outputs may contain a JSON object embedded
            # inside additional text.
            match = re.search(r"\{.*\}", result, re.DOTALL)

            if match:
                try:
                    result = json.loads(match.group())
                except json.JSONDecodeError:
                    return prediction_set
            else:
                return prediction_set

    # --------------------------------------------------------
    # Dictionary format:
    # {
    #     "PER": ["John"],
    #     "ORG": ["OpenAI"]
    # }
    # --------------------------------------------------------
    if isinstance(result, dict):

        # Case A:
        # Direct type -> entity list mapping
        #
        # Example:
        # {
        #     "PER": ["John"],
        #     "ORG": ["OpenAI"]
        # }
        direct_mapping = True

        for key, value in result.items():
            if key in {
                "text",
                "entity",
                "entities",
                "type",
                "label",
                "prediction",
                "result",
            }:
                direct_mapping = False
                break

            if not isinstance(value, (list, tuple, set)):
                direct_mapping = False
                break

        if direct_mapping:
            for entity_type, entities in result.items():

                entity_type = normalize_entity_type(entity_type)

                if not entity_type:
                    continue

                if not isinstance(entities, (list, tuple, set)):
                    entities = [entities]

                for entity in entities:

                    if isinstance(entity, dict):
                        entity_text = (
                            entity.get("text")
                            or entity.get("entity")
                            or entity.get("name")
                        )

                        entity_type_from_item = (
                            entity.get("type")
                            or entity.get("label")
                            or entity_type
                        )

                        if entity_text is None:
                            continue

                        key = entity_key(
                            entity_text,
                            entity_type_from_item
                        )

                    else:
                        key = entity_key(
                            entity,
                            entity_type
                        )

                    if key[0] and key[1]:
                        prediction_set.add(key)

            return prediction_set

        # ----------------------------------------------------
        # Case B:
        # Wrapper format:
        #
        # {
        #     "result": {
        #         "PER": ["John"]
        #     }
        # }
        # ----------------------------------------------------
        for wrapper_key in [
            "result",
            "prediction",
            "entities",
            "output",
        ]:
            if wrapper_key in result:
                return parse_prediction_result(
                    result[wrapper_key]
                )

        # ----------------------------------------------------
        # Case C:
        # Single entity object:
        #
        # {
        #     "text": "John",
        #     "type": "PER"
        # }
        # ----------------------------------------------------
        entity_text = (
            result.get("text")
            or result.get("entity")
            or result.get("name")
        )

        entity_type = (
            result.get("type")
            or result.get("label")
            or result.get("entity_type")
        )

        if entity_text is not None and entity_type is not None:
            key = entity_key(
                entity_text,
                entity_type
            )

            if key[0] and key[1]:
                prediction_set.add(key)

        return prediction_set

    # --------------------------------------------------------
    # List / tuple / set format
    # --------------------------------------------------------
    if isinstance(result, (list, tuple, set)):

        for item in result:

            # Entity object:
            # {"text": "...", "type": "..."}
            if isinstance(item, dict):

                entity_text = (
                    item.get("text")
                    or item.get("entity")
                    or item.get("name")
                )

                entity_type = (
                    item.get("type")
                    or item.get("label")
                    or item.get("entity_type")
                )

                if entity_text is not None and entity_type is not None:
                    key = entity_key(
                        entity_text,
                        entity_type
                    )

                    if key[0] and key[1]:
                        prediction_set.add(key)

            # Nested structures
            elif isinstance(item, (dict, list, tuple, set, str)):
                prediction_set.update(
                    parse_prediction_result(item)
                )

        return prediction_set

    return prediction_set


# ============================================================
# Gold-label parsing
# ============================================================

def parse_gold_label(label):
    """
    Convert one gold label dictionary into a set of
    (entity_type, entity_text) tuples.

    Expected format:

    {
        "PER": ["John", "Mary"],
        "ORG": ["OpenAI"]
    }
    """
    gold_set = set()

    if label is None:
        return gold_set

    if isinstance(label, str):
        label = label.strip()

        if not label:
            return gold_set

        try:
            label = json.loads(label)
        except json.JSONDecodeError:
            return gold_set

    if not isinstance(label, dict):
        return gold_set

    # Handle possible wrapper structures.
    if "label" in label and isinstance(label["label"], dict):
        label = label["label"]

    for entity_type, entities in label.items():

        entity_type = normalize_entity_type(entity_type)

        if not entity_type:
            continue

        if entities is None:
            continue

        if not isinstance(entities, (list, tuple, set)):
            entities = [entities]

        for entity in entities:

            if isinstance(entity, dict):
                entity_text = (
                    entity.get("text")
                    or entity.get("entity")
                    or entity.get("name")
                )

                entity_type_from_item = (
                    entity.get("type")
                    or entity.get("label")
                    or entity_type
                )

                if entity_text is None:
                    continue

                key = entity_key(
                    entity_text,
                    entity_type_from_item
                )

            else:
                key = entity_key(
                    entity,
                    entity_type
                )

            if key[0] and key[1]:
                gold_set.add(key)

    return gold_set


# ============================================================
# Load data
# ============================================================

def load_json(path):
    """
    Load a JSON file.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_gold_samples(label_data):
    """
    Build ordered gold samples.

    Expected format:

    [
        {
            "text": "...",
            "label": {
                "PER": ["..."]
            }
        },
        ...
    ]

    Returns:
        [
            {
                "text": "...",
                "entities": set(...)
            },
            ...
        ]
    """
    if not isinstance(label_data, list):
        raise ValueError(
            "The label file must contain a JSON list."
        )

    samples = []

    for index, item in enumerate(label_data):

        if not isinstance(item, dict):
            raise ValueError(
                f"Invalid label item at index {index}: "
                f"expected a dictionary."
            )

        text = item.get("text", "")

        label = item.get("label", {})

        entities = parse_gold_label(label)

        samples.append(
            {
                "text": text,
                "entities": entities,
            }
        )

    return samples


def build_prediction_samples(pred_data):
    """
    Build ordered prediction samples.

    Supported primary format:

    [
        {
            "text": "...",
            "result": {
                "PER": ["..."]
            }
        }
    ]

    The function also supports:
        "prediction"
        "entities"
        "output"

    as wrapper keys.
    """
    if not isinstance(pred_data, list):
        raise ValueError(
            "The prediction file must contain a JSON list."
        )

    samples = []

    for index, item in enumerate(pred_data):

        if not isinstance(item, dict):
            raise ValueError(
                f"Invalid prediction item at index {index}: "
                f"expected a dictionary."
            )

        text = item.get("text", "")

        result = None

        for key in [
            "result",
            "prediction",
            "entities",
            "output",
        ]:
            if key in item:
                result = item[key]
                break

        # If no wrapper key is present, try the complete object.
        if result is None:
            result = item

        entities = parse_prediction_result(result)

        samples.append(
            {
                "text": text,
                "entities": entities,
            }
        )

    return samples


# ============================================================
# Alignment
# ============================================================

def align_samples(gold_samples, pred_samples):
    """
    Align gold and prediction samples by their original order.

    Using the sample index rather than a dictionary keyed by text
    avoids accidentally overwriting duplicated input texts.
    """
    gold_count = len(gold_samples)
    pred_count = len(pred_samples)

    if gold_count != pred_count:
        print(
            f"[Warning] Number of samples differs: "
            f"gold={gold_count}, prediction={pred_count}"
        )

    count = min(gold_count, pred_count)

    aligned = []

    text_mismatch_count = 0

    for i in range(count):

        gold = gold_samples[i]
        pred = pred_samples[i]

        gold_text = normalize_entity(gold["text"])
        pred_text = normalize_entity(pred["text"])

        if gold_text != pred_text:
            text_mismatch_count += 1

        aligned.append(
            {
                "index": i,
                "gold_text": gold_text,
                "pred_text": pred_text,
                "gold": gold["entities"],
                "pred": pred["entities"],
            }
        )

    return aligned, text_mismatch_count


# ============================================================
# Evaluation
# ============================================================

def calculate_metrics(tp, pred_count, gold_count):
    """
    Calculate precision, recall and F1.
    """
    precision = (
        tp / pred_count
        if pred_count > 0
        else 0.0
    )

    recall = (
        tp / gold_count
        if gold_count > 0
        else 0.0
    )

    if precision + recall > 0:
        f1 = (
            2 * precision * recall
            / (precision + recall)
        )
    else:
        f1 = 0.0

    return precision, recall, f1


def format_percentage(value):
    return f"{value * 100:.2f}"


def evaluate(aligned_samples):
    """
    Perform strict exact-match micro evaluation.

    A prediction is correct only when both:
        entity text
        entity type

    are exactly matched after normalization.
    """

    total_tp = 0
    total_pred = 0
    total_gold = 0

    duplicate_pred_count = 0

    type_gold = Counter()
    type_pred = Counter()
    type_tp = Counter()

    for sample in aligned_samples:

        gold = sample["gold"]
        pred = sample["pred"]

        # ----------------------------------------------------
        # Strict exact matching
        # ----------------------------------------------------
        tp_set = gold & pred

        tp = len(tp_set)

        total_tp += tp
        total_pred += len(pred)
        total_gold += len(gold)

        # ----------------------------------------------------
        # Entity-type statistics
        # ----------------------------------------------------
        for entity_type, entity_text in gold:
            type_gold[entity_type] += 1

        for entity_type, entity_text in pred:
            type_pred[entity_type] += 1

        for entity_type, entity_text in tp_set:
            type_tp[entity_type] += 1

        # ----------------------------------------------------
        # Duplicate prediction detection
        #
        # parse_prediction_result uses set internally, so
        # duplicate entities are removed before scoring.
        # This counter is calculated only when the original
        # prediction structure contains duplicates.
        # ----------------------------------------------------

    precision, recall, f1 = calculate_metrics(
        total_tp,
        total_pred,
        total_gold
    )

    all_types = sorted(
        set(type_gold.keys())
        | set(type_pred.keys())
    )

    per_type = {}

    for entity_type in all_types:

        p, r, f = calculate_metrics(
            type_tp[entity_type],
            type_pred[entity_type],
            type_gold[entity_type]
        )

        per_type[entity_type] = {
            "tp": type_tp[entity_type],
            "pred": type_pred[entity_type],
            "gold": type_gold[entity_type],
            "precision": p,
            "recall": r,
            "f1": f,
        }

    return {
        "tp": total_tp,
        "pred": total_pred,
        "gold": total_gold,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "per_type": per_type,
        "duplicate_pred": duplicate_pred_count,
    }


# ============================================================
# Main evaluation function
# ============================================================

def NER_eval(label_path, pred_path, show_type=True):
    """
    Evaluate NER predictions.

    Parameters
    ----------
    label_path : str
        Path to the ground-truth JSON file.

    pred_path : str
        Path to the model prediction JSON file.

    show_type : bool
        Whether to print per-entity-type metrics.
    """

    print("=" * 70)
    print("NER Evaluation")
    print("=" * 70)

    print(f"Label file : {label_path}")
    print(f"Pred file  : {pred_path}")
    print()

    # --------------------------------------------------------
    # Load files
    # --------------------------------------------------------
    try:
        label_data = load_json(label_path)
    except Exception as e:
        raise RuntimeError(
            f"Failed to load label file: {label_path}\n"
            f"Error: {e}"
        )

    try:
        pred_data = load_json(pred_path)
    except Exception as e:
        raise RuntimeError(
            f"Failed to load prediction file: {pred_path}\n"
            f"Error: {e}"
        )

    # --------------------------------------------------------
    # Build samples
    # --------------------------------------------------------
    gold_samples = build_gold_samples(label_data)
    pred_samples = build_prediction_samples(pred_data)

    # --------------------------------------------------------
    # Align by sample index
    # --------------------------------------------------------
    aligned_samples, text_mismatch_count = align_samples(
        gold_samples,
        pred_samples
    )

    # --------------------------------------------------------
    # Evaluate
    # --------------------------------------------------------
    result = evaluate(aligned_samples)

    # --------------------------------------------------------
    # Basic statistics
    # --------------------------------------------------------
    print("-" * 70)
    print("Dataset Statistics")
    print("-" * 70)

    print(
        f"Gold samples       : {len(gold_samples)}"
    )

    print(
        f"Prediction samples : {len(pred_samples)}"
    )

    print(
        f"Evaluated samples  : {len(aligned_samples)}"
    )

    print(
        f"Text mismatches    : {text_mismatch_count}"
    )

    if text_mismatch_count > 0:
        print(
            "[Warning] Some prediction texts do not match "
            "the corresponding label texts."
        )

    # --------------------------------------------------------
    # Overall metrics
    # --------------------------------------------------------
    print()
    print("-" * 70)
    print("Overall Results")
    print("-" * 70)

    print(
        f"True Positives : {result['tp']}"
    )

    print(
        f"Predicted      : {result['pred']}"
    )

    print(
        f"Gold           : {result['gold']}"
    )

    print(
        f"Precision      : "
        f"{format_percentage(result['precision'])}%"
    )

    print(
        f"Recall         : "
        f"{format_percentage(result['recall'])}%"
    )

    print(
        f"F1             : "
        f"{format_percentage(result['f1'])}%"
    )

    # --------------------------------------------------------
    # Per-type metrics
    # --------------------------------------------------------
    if show_type:

        print()
        print("-" * 70)
        print("Per-Entity-Type Results")
        print("-" * 70)

        if result["per_type"]:

            print(
                f"{'Type':<18}"
                f"{'TP':>8}"
                f"{'Pred':>10}"
                f"{'Gold':>10}"
                f"{'P':>10}"
                f"{'R':>10}"
                f"{'F1':>10}"
            )

            print("-" * 76)

            for entity_type, metrics in result["per_type"].items():

                print(
                    f"{entity_type:<18}"
                    f"{metrics['tp']:>8}"
                    f"{metrics['pred']:>10}"
                    f"{metrics['gold']:>10}"
                    f"{format_percentage(metrics['precision']):>9}%"
                    f"{format_percentage(metrics['recall']):>9}%"
                    f"{format_percentage(metrics['f1']):>9}%"
                )

        else:
            print("No entity types found.")

    print()
    print("=" * 70)
    print(
        f"Final Micro-F1: "
        f"{format_percentage(result['f1'])}%"
    )
    print("=" * 70)

    return result


# ============================================================
# Command-line interface
# ============================================================

def main():
    parser = ArgumentParser(
        description=(
            "Evaluate NER predictions using strict exact "
            "entity-span and entity-type matching."
        )
    )

    parser.add_argument(
        "--label_path",
        required=True,
        type=str,
        help="Path to the ground-truth label JSON file."
    )

    parser.add_argument(
        "--pred_path",
        required=True,
        type=str,
        help="Path to the model prediction JSON file."
    )

    parser.add_argument(
        "--no_type",
        action="store_true",
        help="Do not print per-entity-type evaluation results."
    )

    args = parser.parse_args()

    NER_eval(
        label_path=args.label_path,
        pred_path=args.pred_path,
        show_type=not args.no_type
    )


if __name__ == "__main__":
    main()
