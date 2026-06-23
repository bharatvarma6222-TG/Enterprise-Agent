import ast


def parse_plan(plan):

    if isinstance(plan, list):
        return plan

    try:
        return ast.literal_eval(plan)

    except Exception:
        return [str(plan)]
