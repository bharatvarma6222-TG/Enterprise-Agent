import ast


def parse_plan(plan_text: str):

    try:
        return ast.literal_eval(plan_text)

    except Exception:
        return [plan_text]
