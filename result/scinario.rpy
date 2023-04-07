label start:

$ bg("hoge")
$ pbgm("hoge")

line narrator "
ナレーション。"

set_chara "skm" l2
hyojo "skm" nor

line skm "
「セリフ」"

set_chara "igt" r3
hyojo "igt" nor

line igt "
「セリフ」"

hyojo_mode "igt" pupil2 True
hyojo_item "skm" sweat 1
hyojo_part "skm" blow nor

line skm "
『セリフ』"

hide_chara igt
$ se("hoge")
$ hode = hoge

line skm "
（モノローグ）"

set_chara "igt" r3

line igt "
「セリフ。
セリフ」"

line igt "
「{rb}セリフ{/rb}{rt}台詞{/rt}。
セ{rt}・{/rt}リ{rt}・{/rt}フ{rt}・{/rt}」"

hide_chara_all
$ sbgm()
