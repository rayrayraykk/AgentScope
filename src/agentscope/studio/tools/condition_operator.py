# -*- coding: utf-8 -*-
"""Condition operator"""

from agentscope.message import Msg

def eval_condition_operator(actual_value: str, operator: str, target_value: str=None) -> bool:
    """Eval condition operator only for Msg content or string"""

    if isinstance(actual_value, Msg):
        actual_value = actual_value.get('content', '')
    if operator == "contains":
        return target_value in actual_value
    elif operator == "not contains":
        return target_value not in actual_value
    elif operator == "start with":
        return actual_value.startswith(target_value)
    elif operator == "end with":
        return actual_value.endswith(target_value)
    elif operator == "equals":
        return actual_value == target_value
    elif operator == "not equals":
        return actual_value != target_value
    elif operator == "is empty":
        return True if not actual_value else False
    elif operator == "is not empty":
        return True if actual_value else False
    elif operator == "is null":
        return True if actual_value is None else False
    elif operator == "is not null":
        return True if actual_value is not None else False
    else:
        raise ValueError(f"Invalid condition operator: {operator}")