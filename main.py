import os
import sys
import re
import definition

version = 0.10
preset = []
setting = {}
scinario = []
result = []

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
    result = str.split("=")
    return result

def modify_setting():
    # 構文が不正ならフォロー（あるべき値が無い、パラメータ指定が間違っている）
    pass

def modify_preset():
    # 構文が不正ならフォロー（あるべき値が無い、パラメータ指定が間違っている）
    pass

def convert_scinario():
    # 検索
    # 置換
    # 関数実行
    return ""


def make_default_preset():
    with open("preset.ini", "w") as f:
        setting = "[@SETTING]\nversion=0.10\nplaintext=:\nextension=ks\n"
        preset = "[]\nposition_search=none\nif_activated=none\ndefinition1=\ndefinition2=\ndefinition_function=\n"
        end ="[@END]"
        f.write(setting)
        f.write(preset)
        f.write(end)


if __name__ == "__main__":
    print("____scenario_converter_by_sato____")


    print("load preset...")
    
    # preset.iniがなければ新規作成
    if not os.path.isfile("preset.ini"):
        print("preset.ini is not found")
        print("create preset.ini")
        make_default_preset()

    with open("preset.ini", "r") as f:
        p = [s.strip() for s in f.readlines()]
    
    load_preset(p)
    modify_setting()
    modify_preset()


    print("please enter the file to convert")

    path = ""
    
    while os.path.exists(path) == False:
        path = input(">>> ").strip(r'"')
        if os.path.exists(path):
            print("**success**")
        else:
            print("**fail**")
            print("please try again")

    print("load scinario...")

    # シナリオファイル一行ずつリスト化
    with open(path, "r", encoding="utf-8") as f:
        scinario = [s.strip() for s in f.readlines()]


    print("convert scinario...")
    i = 0
    for s in scinario:
        result.append("")
        for p in preset:
            result[i] = convert_scinario()
            # if_activated

        result[i] = result[i] + "\n"
        print(result)
        i = i + 1


    print("output scinario...")
    output_path = "./result/" + os.path.splitext(os.path.basename(path))[0] + "." + setting["extension"]

    if not os.path.isdir("./result"):
        os.mkdir("./result")

    with open(output_path, "w") as f:
        f.writelines(result)

    print("**complete**")

    print("please press any key")