import re

# function_dictに登録した関数をreplace_functiondで使用できます。
# keyにreplace_functiondで使用する文字列を、valueに呼び出す関数を登録してください。
function_dict = {}

def replace_emphasis(s):
    result = ""
    is_applicable = False

    if re.search(r'\[ruby test="・"\]', s) != None:
        result = re.sub(r'<\[ruby test="・"\]', r'[ruby test="・"]', s)
        result = re.sub(r'\[ruby test="・"\]>', '', result)

        is_applicable = True
    else:
        result = s

    return result, is_applicable

function_dict["replace_emphasis"] = replace_emphasis