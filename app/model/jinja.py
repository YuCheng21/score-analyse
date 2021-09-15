"""
Jinja 模板用的自訂 function, filter...
"""


def col_len(course_list):
    reshape = []
    for key, value in enumerate(course_list):
        reshape += value
    count_type = [reshape.count('核心課程'), reshape.count('應用課程')]
    return count_type


def is_pass(course_type, course_target, pass_dict):
    pass_list = []
    for i in ['核心課程', '應用課程']:
        pass_list += pass_dict[course_type][i]

    if course_target in pass_list:
        return True
    else:
        return False
