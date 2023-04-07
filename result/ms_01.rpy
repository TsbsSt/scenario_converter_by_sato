label ms_01:

line narrator "
――十二月二十四日、マンション廊下――"

$ bg("igatakemae")

line tnk "
「ひどい、ひどい、ひどい！」"

set_chara "igt" l2
hyojo "igt" sed

line narrator "
田中まほがじゃがいもを投げる。
手に提げたエコバッグからまたじゃがいもをひっつかみ投げる。"

set_chara "tnk" r3
hyojo "tnk" pod

$ se("attack")

line narrator "
投げたじゃがいもが{rb}いがたしゅう{/rb}{rt}伊方終{/rt}の腹に当たる。
伊方に避ける素振りは無い。"

line igt "
「だからさあ、謝ったじゃん？
他の子と会う約束しちゃったーって」"

hyojo "tnk" sei

line tnk "
「謝って許されることじゃないです！」"

hyojo "tnk" sem

line tnk "
「そもそもクリスマスイブですよ、
なんで他の女と約束するんですか」"

line igt "
「しょうがないじゃん、
会ってって言われちゃったんだし」"

hyojo "tnk" sed

line tnk "
「じゃあ断ればいいじゃないですか！」"

$ se("attack")

line narrator "
そう叫んで今度はにんじんを投げる。"

line narrator "
腹に当たって床に落ちたにんじんを、
伊方は仕方なさげに拾う。"

hyojo "igt" sem
hyojo_item "igt" sweat 1

line igt "
「なんでそんな怒ってんの？
オレと一日会えなかったぐらいで」"

hyojo "tnk" ses

line tnk "
「……！」"

hyojo "tnk" sea
hyojo_part "tnk" mouth_close sek

line tnk "
「……、そうですよね」"

line tnk "
「終くんにとってわたしって、
大勢いる女の子の一人ですもんね」"

hyojo "igt" ses

line igt "
「は？そんな話してねぇ――」"

hyojo "tnk" sed

line narrator "
田中がたまねぎを持った手を振り上げ、
勢いよく伊方に叩きつける"

$ se("explosion")

line narrator "
叩きつけたたまねぎが爆発する。
爆発したたまねぎから濃い紫色の煙が広がる。"

hyojo "igt" poi

line igt "
「うげっ、なんだこれ、魔{rt}・{/rt}法{rt}・{/rt}……？！」"

line narrator "
咽せながらうずくまる伊方を田中が見下ろす。"

$ show_still("ms_01")

line tnk "
「これは呪いです」"

line tnk "
「終くんが真{rt}・{/rt}実{rt}・{/rt}の{rt}・{/rt}愛{rt}・{/rt}を知ったとき、
死ぬ呪いをかけました」"

line tnk "
「終くんはわたしを苦しめた、
そしてきっと他の女の子も苦しめてる」"

line tnk "
「だから同じ苦しみを味わってください――」"

jump ms_02
