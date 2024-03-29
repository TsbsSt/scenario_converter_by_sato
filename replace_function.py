import re

# function_dictに登録した関数をreplace_functiondで使用できます。
# keyにreplace_functiondで使用する文字列を、valueに呼び出す関数を登録してください。
function_dict = {}


def replace_emphasis(s):
    result = ""

    if re.search(r'\[oct_mc_em\]', s) is not None:
        result = s
        result = re.sub(r'<\[oct_mc_em]', r'[oct_mc_em]', result)
        result = re.sub(r'\[oct_mc_em]>', '', result)
    else:
        result = s

    return result


function_dict["replace_emphasis"] = replace_emphasis


def replace_emphasis_rp(s):
    result = ""

    if re.search(r'\{rt\}・\{/rt\}', s) is not None:
        result = s
        result = re.sub(r'<\{rt\}・\{/rt\}', '', result)
        result = re.sub(r'\{rt\}・\{/rt\}>', '{rt}・{/rt}', result)
    else:
        result = s

    return result


function_dict["replace_emphasis_rp"] = replace_emphasis_rp
