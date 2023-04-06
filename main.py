import os
import re
import replace_function as rf

version = 0.81

preset = []
setting = {}
default_preset = {
"position_search": "none",
"if_activated": "none",
"find": "",
"replace": "",
"replace_function": ""
}
default_setting = {
"version": version,
"plaintext": ":",
"extension": "ks"
}

def main():

    print("____scenario_converter_by_sato____")

    print("1. please enter the file to convert")

    path = ""
    
    while os.path.exists(path) == False:
        path = input(">>> ").strip(r'"')
        if os.path.exists(path):
            print("**success**")
        else:
            print("**fail**")
            print("please try again")

    print("2. please enter preset.ini")
    print("(if blank, the default preset is loaded.)")

    path_preset = ""

    while os.path.exists(path_preset) == False or os.path.basename(path_preset) != "preset.ini":
        path_preset = input(">>> ").strip(r'"')
        if path_preset == "":
            print("**load the default preset**")
            path_preset = "./preset.ini"
        elif os.path.exists(path_preset) and os.path.basename(path_preset) == "preset.ini":
            print("**success**")
        else:
            print("**fail**")
            print("please try again")

    print("load preset...")
    
    # preset.iniがなければ新規作成
    if not os.path.isfile("preset.ini"):
        print("preset.ini is not found")
        print("create preset.ini")
        make_default_preset()

    with open(path_preset, "r", encoding="utf-8") as f:
        p = [s.strip() for s in f.readlines()]
    
    # print(preset)

    load_preset(p)
    modify_setting()
    modify_preset()

    print("load scinario...")

    # シナリオファイル一行ずつリスト化
    with open(path, "r", encoding="utf-8") as f:
        scinario = [s.strip() for s in f.readlines()]

    print("convert scinario...")
    result = convert_scinario(scinario)

    print("output scinario...")
    output_path = "./result/" + os.path.splitext(os.path.basename(path))[0] + "." + setting["extension"]

    if not os.path.isdir("./result"):
        os.mkdir("./result")

    with open(output_path, "w") as f:
        f.writelines(result)

    print("**complete**")

    # input("please press any key")


def load_preset(preset_list=[]):
    # ヘッダーの正規表現定義
    rehead = re.compile(r"\[.*\]")

    preset_number = -1
    mode = "preset" # preset setting
    global preset
    global setting

    for p in preset_list:
        header = re.fullmatch(rehead, p)

        # ヘッダー[@END]ならプリセットのロードを終了
        if p == "[@END]":
            break

        # ヘッダーの種類でモードを変更
        if header == None:
            # そもそもヘッダーじゃない
            pass
        elif p == "[@SETTING]":
            mode = "setting"
        else:
            mode = "preset"
            preset.append({})
            preset_number = preset_number + 1

        if mode == "setting" and header == None:
            attribute, parameter =set_parameter(p)
            setting[attribute] = parameter

        if mode == "preset" and header == None:
            attribute, parameter =set_parameter(p)
            preset[preset_number][attribute] = parameter


def set_parameter(str):
    result = str.split("=", 1)
    return result

def modify_setting():
    # キーが存在しなければデフォルト値を代入
    if not "version" in setting:
        setting["version"] = default_setting["version"]

    if not "plaintext" in setting:
        setting["plaintext"] = default_setting["plaintext"]

    if not "extension" in setting:
        setting["extension"] = default_setting["extension"]


    # 値が不正ならデフォルト値を代入
    if type(setting["version"]) is not float:
        if type(setting["version"]) is not int:
            # 整数であれば許容
            setting["version"] = float(setting["version"])
        else:
            setting["version"] = default_setting["version"]

    if type(setting["plaintext"]) is not str:
        setting["plaintext"] = default_setting["plaintext"]

    if type(setting["extension"]) is not str:
        setting["extension"] = default_setting["extension"]

    # ファイル名に使えない文字列は除外
    reserch = re.compile(r'[\\|/|:|?|.|*|"|<|>|\|]')
    setting["extension"] = re.sub(reserch, "", setting["extension"])


def modify_preset():
    i = 0
    for p in preset:
        # キーが存在しなければデフォルト値を代入
        if not "position_search" in p:
            preset[i]["position_search"] = default_preset["position_search"]

        if not "if_activated" in p:
            preset[i]["if_activated"] = default_preset["if_activated"]

        if not "find" in p:
            preset[i]["find"] = default_preset["find"]

        if not "replace" in p:
            preset[i]["replace"] = default_preset["replace"]

        if not "replace_function" in p:
            preset[i]["replace_function"] = default_preset["replace_function"]

        # 値が不正ならデフォルト値を代入
        if not re.fullmatch(r"none|bigin|middle|end", p["position_search"]):
            preset[i]["position_search"] = default_preset["position_search"]

        if not re.fullmatch(r"none|continue", p["if_activated"]):
            preset[i]["if_activated"] = default_preset["if_activated"]

        # 存在しない関数を指定していたらデフォルト値
        is_function = False
        for key in rf.function_dict:
            if preset[i]["replace_function"] == key:
                is_function = True

        if not is_function:
            preset[i]["replace_function"] = default_preset["replace_function"]

        if preset[i]["find"] == "":
            # 検索文字未指定の場合はNoneを代入
            preset[i]["find"] = None
        else:
            # 正規表現を事前にコンパイル
            preset[i]["find"] = re.compile(p["find"])

        i = i + 1

def convert_scinario(scinario):
    global setting
    global preset
    result = []
    i = 0

    re_str = re.compile(r".+")

    for s in scinario:
        j = 0
        result.append("")
        is_applicable = False
        is_search = False
        plaintext = ""

        # plaintext
        if re.search(setting["plaintext"], s) != None:
            s, plaintext = s.split(setting["plaintext"], 1)

        for p in preset:
            
            # position_search
            if p["position_search"] == "begin":
                if i == 0:
                    is_search = True
                elif "" == scinario[i-1]:
                    is_search = True
                else:
                    is_search = False

            elif p["position_search"] == "middle":
                if i == 0:
                    is_search = False
                elif i == len(scinario) - 1:
                    is_search = False
                elif re.match(re_str, scinario[i-1]) != None and re.match(re_str, scinario[i+1]) != None:
                    is_search = True
                else:
                    is_search = False

            elif p["position_search"] == "end":
                if i == len(scinario) - 1:
                    is_search = True
                elif "" == scinario[i+1]:
                    is_search = True
                else:
                    is_search = False

            else:
                is_search = True

            # convert
            if is_search:
                result[i],is_applicable = convert_line(s, j)

            s = result[i]
            j = j + 1
            
            # if_activated
            if p["if_activated"] == "none" and is_applicable:
                break

        result[i] = result[i] + plaintext + "\n"
        i = i + 1

    return result

def convert_line(s, number):
    global preset
    result = ""
    is_applicable = False

    # 検索文字列が指定されていれば置換する
    if preset[number]["find"] != None:
        result = re.sub(preset[number]["find"], preset[number]["replace"], s)
    else:
        result = s

    # 変換が行われていれば記録
    if preset[number]["find"] != None:
        if re.search(preset[number]["find"], s) != None:
            is_applicable = True

    # 関数実行
    if preset[number]["replace_function"] != "" and is_applicable == True:
        func = preset[number]["replace_function"]
        result = rf.function_dict[func](result)

    return result, is_applicable


def make_default_preset():
    global setting
    global preset
    result = ""

    # setting
    result = result + "[@SETTING]\n"
    for key in default_setting:
        result = result + key + "=" + str(default_setting[key]) + "\n"

    # preset
    result = result + "[]\n"
    for key in default_preset:
        result = result + key + "=" + str(default_preset[key]) + "\n"

    # end
    result = result + "[@END]"

    with open("preset.ini", "w") as f:

        f.write(result)


if __name__ == "__main__":
    main()