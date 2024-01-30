import os
import re
import replace_function as rf

version = 0.83

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

    files = None

    while True:
        # パスには"が含まれるため取り除く
        input_path = input(">>> ")

        files = input_path.split(",")

        for i in range(0, len(files)):
            files[i] = files[i].strip(r'"')

        print("check file existence")
        
        i = 0

        for f in files:

            if os.path.exists(f):
                print(f"{i}-----**OK**")
            else:
                print(f"{i}-----**NG**")
                del files[i]

            i = i + 1

        if len(files) > 0:
            print("**success**")
            break
        else:
            print("**fail**")
            print("please try again")

    print("2. please enter preset.ini")
    print("(if blank, the default preset is loaded.)")

    path_preset = ""

    while True:
        path_preset = input(">>> ").strip(r'"')
        path_exists = os.path.exists(path_preset)
        path_bassname = os.path.basename(path_preset)

        if path_preset == "":
            print("**load the default preset**")
            path_preset = "./preset.ini"
            break
        elif path_exists and path_bassname == "preset.ini":
            print("**success**")
            break
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

    load_preset(p)
    modify_setting()
    modify_preset()

    print("load scinario...")

    # シナリオファイル一行ずつリスト化

    scinario = []
    result = []

    for path in files:

        with open(path, "r", encoding="utf-8") as f:
            scinario.append([
                path,
                [s.strip() for s in f.readlines()]
                ])

    for s in scinario:

        basename = os.path.splitext(os.path.basename(s[0]))[0]

        print(f"convert scinario --- {basename}")
        result.append([
            s[0],
            convert_scinario(s[1])
            ])

    for r in result:

        basename = os.path.splitext(os.path.basename(r[0]))[0]

        print(f"output scinario --- {basename}")
        output_scinario(r[0], r[1])

    print("**complete**")

    input("please press any key")


def load_preset(preset_list=[]):
    global preset
    global setting

    preset_number = -1

    # ヘッダーの正規表現定義
    rehead = re.compile(r"\[.*\]")

    # preset_setting
    mode = "preset"

    for p in preset_list:
        header = re.fullmatch(rehead, p)

        # ヘッダー[@END]ならプリセットのロードを終了
        if p == "[@END]":
            break

        # ヘッダーの種類でモードを変更
        if header is None:
            # そもそもヘッダーじゃない
            pass
        elif p == "[@SETTING]":
            mode = "setting"
        else:
            mode = "preset"
            preset.append({})
            preset_number = preset_number + 1

        if mode == "setting" and header is None:
            attribute, parameter = set_parameter(p)
            setting[attribute] = parameter

        if mode == "preset" and header is None:
            attribute, parameter = set_parameter(p)
            preset[preset_number][attribute] = parameter


def set_parameter(str):
    result = str.split("=", 1)
    return result


def modify_setting():
    # キーが存在しなければデフォルト値を代入
    if "version" not in setting:
        setting["version"] = default_setting["version"]

    if "plaintext" not in setting:
        setting["plaintext"] = default_setting["plaintext"]

    if "extension" not in setting:
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
        if "position_search" not in p:
            preset[i]["position_search"] = default_preset["position_search"]

        if "if_activated" not in p:
            preset[i]["if_activated"] = default_preset["if_activated"]

        if "find" not in p:
            preset[i]["find"] = default_preset["find"]

        if "replace" not in p:
            preset[i]["replace"] = default_preset["replace"]

        if "replace_function" not in p:
            preset[i]["replace_function"] = default_preset["replace_function"]

        # 値が不正ならデフォルト値を代入
        if not re.fullmatch(r"none|begin|middle|end", p["position_search"]):
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

    for s in scinario:
        j = 0
        result.append("")
        result[i] = s
        is_applicable = False
        plaintext = ""

        # plaintext
        if re.search(setting["plaintext"], result[i]) is not None:
            result[i], plaintext = result[i].split(setting["plaintext"], 1)

        for p in preset:
            # position_search
            is_search = get_is_serch(scinario, p, i)

            # convert
            if is_search:
                result[i], is_applicable = convert_line(result[i], j)

            j = j + 1

            # if_activated
            if p["if_activated"] == "none" and is_applicable:
                break

        result[i] = result[i] + plaintext + "\n"
        i = i + 1

    return result


def get_is_serch(scinario, p, i):

    if i == 0:
        before_line = ""
    else:
        before_line = scinario[i-1]

    if i == len(scinario) - 1:
        after_line = ""
    else:
        after_line = scinario[i+1]

    if p["position_search"] == "begin":
        if before_line == "":
            is_search = True
        else:
            is_search = False

    elif p["position_search"] == "middle":

        if before_line != "" and after_line != "":
            is_search = True
        else:
            is_search = False

    elif p["position_search"] == "end":
        if after_line == "":
            is_search = True
        else:
            is_search = False

    else:
        is_search = True

    return is_search


def convert_line(s, number):
    global preset
    result = ""
    is_applicable = False

    # 検索文字列が指定されていれば置換する
    if preset[number]["find"] is not None:
        result = re.sub(preset[number]["find"], preset[number]["replace"], s)
    else:
        result = s

    # 変換が行われていれば記録
    if preset[number]["find"] is not None:
        if re.search(preset[number]["find"], s) is not None:
            is_applicable = True

    # 関数実行
    if preset[number]["replace_function"] != "" and is_applicable:
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


def output_scinario(path, result):
    basename = os.path.splitext(os.path.basename(path))[0]
    extension = setting["extension"]
    output_path = "./result/" + basename + "." + extension

    if not os.path.isdir("./result"):
        os.mkdir("./result")

    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(result)


if __name__ == "__main__":
    main()
