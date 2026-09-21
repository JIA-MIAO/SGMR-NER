
import json
from argparse import ArgumentParser


# =========================================================
# 统一实体格式
# =========================================================
def normalize_entity(ent):
    """
    Normalize entity string to avoid space / type mismatch
    """
    if not isinstance(ent, str):
        ent = str(ent)
    return ent.strip()


# =========================================================
# 统一解析预测结果（适配结构化 CoT + 多路径）
# =========================================================
def parse_prediction_result(result):
    """
    Support:
    - dict output from new generate.py
    - str output from old version or abnormal cases

    Return:
    parsed_entities: list of (TYPE, ENTITY)
    is_blocked: whether parsing failed
    """

    parsed = []

    # ========== Case 1: Standard dict ==========
    if isinstance(result, dict):

        for ent_type, ents in result.items():

            # 防止非列表异常
            if not isinstance(ents, list):
                continue

            for ent in ents:
                parsed.append(
                    (ent_type, normalize_entity(ent))
                )

        return list(set(parsed)), False


    # ========== Case 2: String (fallback) ==========
    if isinstance(result, str):
        try:
            if '{' in result and '}' in result:
                json_str = result[result.index('{'): result.rindex('}') + 1]
                obj = json.loads(json_str)

                if isinstance(obj, dict):
                    for ent_type, ents in obj.items():

                        if not isinstance(ents, list):
                            continue

                        for ent in ents:
                            parsed.append(
                                (ent_type, normalize_entity(ent))
                            )

                return list(set(parsed)), False

        except Exception:
            pass


    # ========== Parsing failed ==========
    return [], True


# =========================================================
# Main evaluation function
# =========================================================
def NER_eval(label_path, pred_path):

    # ---------- Load ----------
    with open(pred_path, 'r', encoding='utf-8') as f:
        raw_pred = json.load(f)

    with open(label_path, 'r', encoding='utf-8') as f:
        raw_label = json.load(f)

    preds = {}
    labels = {}
    blocked_count = 0


    # =====================================================
    # Process predictions
    # =====================================================
    for js in raw_pred:

        text = js.get('text', '')
        result = js.get('result', {})

        parsed_pred, is_blocked = parse_prediction_result(result)

        if is_blocked:
            blocked_count += 1

        preds[text] = parsed_pred


    # =====================================================
    # Process gold labels
    # =====================================================
    for js in raw_label:

        text = js.get('text', '')
        value = []

        label_dict = js.get('label', {})

        if isinstance(label_dict, dict):
            for ent_type, ents in label_dict.items():

                if not isinstance(ents, list):
                    continue

                for ent in ents:
                    value.append(
                        (ent_type, normalize_entity(ent))
                    )

        labels[text] = list(set(value))


    # =====================================================
    # Compute Precision / Recall / F1
    # =====================================================
    nb_true = 0
    nb_pred = 0
    nb_label = 0

    for text in preds:

        pred_set = set(preds.get(text, []))
        label_set = set(labels.get(text, []))

        nb_pred += len(pred_set)
        nb_label += len(label_set)
        nb_true += len(pred_set & label_set)

    precision = nb_true / nb_pred if nb_pred > 0 else 0.0
    recall = nb_true / nb_label if nb_label > 0 else 0.0

    if precision + recall == 0:
        f1 = 0.0
    else:
        f1 = 2 * precision * recall / (precision + recall)

    return f1, precision, recall, blocked_count


# =========================================================
# CLI
# =========================================================
if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument('--label_path', type=str, required=True)
    parser.add_argument('--pred_path', type=str, required=True)

    args = parser.parse_args()

    f1, precision, recall, blocked_count = NER_eval(
        args.label_path,
        args.pred_path
    )

    print("=" * 50)
    print(f"F1 score     : {f1:.4f}")
    print(f"Precision    : {precision:.4f}")
    print(f"Recall       : {recall:.4f}")
    print(f"Blocked cases: {blocked_count}")
    print("=" * 50)
