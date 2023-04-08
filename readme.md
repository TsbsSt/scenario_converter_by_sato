# はじめに

SCBS（正式名称：scenario_converter_by_sato）は、ノベルゲーム製作補助を目的としたテキスト変換ツールです。
定型書式で書かれたテキストファイルを、各種ゲームエンジンで実行可能なスクリプトファイルに変換することを想定したツールです。

例えば、テキスト文末に自動で[l]タグ（改行タグ）を挿入する、タグ名とパラメータのみ記入した行をタグの書式に変換する、日本語で入力したタグを正式なタグに変換する、等が行えます。

# ティラノスタジオとの差違

SCBSは元々ティラノスクリプト向け支援ツールとして制作されました。
ティラノスクリプトにはティラノスタジオという専用制作ツールがあり、シナリオコンバーターが付属しています（Pro版のみ）。
ティラノスタジオ付属シナリオコンバーターとの主な差違は以下の通りです。

- CUI
- 正規表現による置換
- pythonによる置換可
- プリセットはテキストファイル（preset.ini）で設定
- 文中向け平文化機能（特定文字以降の変換を行わない）

# 使い方

起動後、「1. please enter the file to convert」というメッセージが表示されます。
変換するシナリオファイルを指定してください。

次に「2. please enter preset.ini」というメッセージが表示されます。
変換に使用するプリセットファイルを指定してください。
未指定ならデフォルトプリセットが使用されます（main.pyと同じ階層にあるpreset.iniがデフォルトプリセットです）。

ファイル指定後、変換が行われます。
変換後のファイルはresultフォルダに出力されます。

実際の動作はdemoフォルダ内の「scinario.txt」「preset.ini」で試せます。

# プリセット仕様

プリセットのファイル名は必ず「preset.ini」にします。
preset.iniには以下の様なルールで記入します。

	[ヘッダー]
	属性=パラメーター
	属性=パラメーター

パラメータが未入力の場合、デフォルトのパラメータが使用されます。
ルートディレクトリにpreset.iniが存在しない場合、起動時にデフォルトのpreset.iniが自動で生成されます。


## [@SETTING]

プリセットの汎用的な設定を定義します。

### version

プリセットのバージョンです。
現在は使用していない属性です。
将来プリセット仕様を変更した際、互換性を保つために用意しています。

デフォルトは本体プログラムのバージョンです。

### plaintext

文中平文用の区切り文字です。
指定した文字列以降は変換対象になりません。
変換後、plaintextは削除されます。

主な使用用途は、「当該命令文で汎用的に使用するパラメータのみを省略した定型書式で記入し、例外的に使用するパラメータは本番環境の使用言語で記入する」等です。

デフォルトは「:」（半角コロン）です。

### extension

変換後のテキストの拡張子です。
変換後のテキストは「result」フォルダに出力されます。その際ファイル名は元ファイル名と同じになります。
（例：入力ファイルが「scenario.txt」、extensionが「ks」で、「\result\scenario.ks」が出力される）。
すでに同名ファイルが存在している場合、上書き保存されます。

デフォルトは「ks」です。

## [PRESET]

実際に使用されるプリセットを定義します。
「[～]」から「[～]」までの属性・パラメータが一つのプリセットとして使用されます。

[]の間にはプリセット名を記入します。
プリセット名はプリセットを視覚的に識別するためのものです。内部ではプリセットを番号で管理しているため、同じプリセット名が複数存在していても動作に支障はありません。
ただし内部で使用している名前（「@」から始まる名前）は避けてください。バグの原因になります。

複数のプリセットが定義可能です。
プリセットは文書先頭から順に処理されます。
つまり、先に実行したいプリセットは文書先頭に、後に実行したいプリセットは文書後方に記入します。

### position_search

変換を実行する行の種類です。
以下の四種類が指定可能です。

- none：未指定。全ての行が対象。
- begin：文頭。空行直後の行と同義。
- middle：文中。文と文に挟まれた行。
- end：文末。空行直前の行と同義。

デフォルトは「none」です。

### if_activated

行がプリセットの変換対象だった場合の変換実行後の処理です。
「none」で該当行の変換を終了し、次の行の変換に移ります。
「continue」で該当プリセット以後の変換を続けます。次の行の変換に移りません。

デフォルトは「none」です。

### find

正規表現を使用した検索文字列です。
デフォルトは未指定（＝何も検索しない）です。

### replace

正規表現を使用した変換後文字列です。
デフォルトは未指定（＝実質的な検索文字列削除）です。

### replace_function

変換に使用するpython関数を指定します。
「replace_function.py」内の関数を指定することを想定しています。
（exe版ではユーザーが関数を作ることはできません）

find・replaceによる変換を行った上で、replace_functionによる変換を行います。
つまりfindで検索されなかった行では関数が実行されません。

デフォルトは未指定（＝何も変換しない）です。

## [@END]

プリセットの終端を指定します。
これ以後に記入した設定は全て無視されます。


# ライセンス
MIT licenseに準拠します。


# リンク
## twitter
[Twitter](https://twitter.com/2basaSato)

## HP
[甘翼](https://sweetwings.feeling.jp/kanyoku/)

