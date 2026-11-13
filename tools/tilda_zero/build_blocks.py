"""Сборка JSON для Zero Block лонгрида «Несуществующий гардероб».

Запуск: python tools/tilda_zero/build_blocks.py → tools/tilda_zero/out/<record>.json
Тексты и раскладка — по docs/tilda/zero_block_longread_manual.md.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from zb import (CARBON, CYAN, LINE, LINE_ACTIVE, LINE_PANEL, MONO, MUTED, OK, PANEL, SILVER, WARN, Block,  # noqa: E402
                bold, cyan, estimate_height, muted, scroll_step, time_step)

OUT = Path(__file__).parent / "out"
CDN = json.loads((Path(__file__).parent / "cdn.json").read_text(encoding="utf-8"))
RECORDS = json.loads((Path(__file__).parent / "records.json").read_text(encoding="utf-8"))
VIEWER = "https://raw.githack.com/EGRNEGR/MEDIA-SCI/tilda-zero-longread/media/3d/iridescence-viewer/index.html"


def rec(key: str) -> str:
    return f"#rec{RECORDS[key]}"


def frame(i: int) -> str:
    return CDN[f"turntable/turntable_{i:02d}.jpg"]


def section_head(b: Block, y: int, index: str, h2: str, *, x=0, w=760, my=40, mw=460, fs=48, anim=True):
    """Индекс + двухцветный заголовок. Возвращает (низ на десктопе, низ на мобильном)."""
    a = Block.basic("fadeinup", 0.8, 0, 40) if anim else {}
    b.mono(x, y, w, cyan(index.split(" · ")[0]) + " · " + " · ".join(index.split(" · ")[1:]),
           mobile={"x": 10, "y": my, "w": mw, "fs": 11}, **a)
    h = estimate_height(h2, w, fs, 1.12)
    b.text(x, y + 30, w, h2, fs=fs, lh=1.12, fw=700, ls=-1, mobile={"x": 10, "y": my + 24, "w": mw, "fs": 28}, **a)
    mh = estimate_height(h2, mw, 28, 1.12)
    return y + 30 + h, my + 24 + mh


# --------------------------------------------------------------------------- ZB01
def zb01() -> Block:
    b = Block("ZB01", 860, 1240)
    for x in (0, 300, 600, 900, 1200):
        b.shape(x, 0, 1, 860, bg="#15181c", layer="hairline", mobile="hide")
    b.text(0, 28, 400, bold("НЕСУЩЕСТВУЮЩИЙ") + " ГАРДЕРОБ", fs=15, lh=1.3, ls=1.5, layer="brand",
           mobile={"x": 10, "y": 24, "w": 300, "fs": 13})
    nav = [("/01 ФОРМАТЫ", "ZB02", 420), ("/02 ХРОНОЛОГИЯ", "ZB04", 540), ("/03 РОССИЯ", "ZB06", 690),
           ("/04 ПРИМЕРКА", "ZB07", 800), ("/05 ЭКОЛОГИЯ", "ZB08", 925), ("/06 МИФ ИЛИ ФАКТ", "ZB10", 1045)]
    for label, target, x in nav:
        b.mono(x, 30, 150, f'<a href="{rec(target)}" style="color: {MUTED};">{label}</a>', fs=11, mobile="hide",
               layer="nav")
    b.mono(0, 150, 600, cyan("/00") + " · ЛОНГРИД ПО СТАТЬЕ РУВИКИ «ВИРТУАЛЬНАЯ ОДЕЖДА»",
           mobile={"x": 10, "y": 80, "w": 460, "fs": 11}, **Block.basic("fadein", 0.8))
    b.text(0, 190, 640, "Можно ли носить<br>одежду, которой<br>" + muted("не существует?"), fs=64, lh=1.06,
           fw=700, ls=-1.5, layer="h1", mobile={"x": 10, "y": 110, "w": 460, "fs": 36},
           **Block.basic("fadeinup", 0.9, 0, 40))
    b.text(0, 430, 540, "Виртуальная одежда — цифровые модели гардероба: от 3D-лекал в CLO 3D до образа, "
           "который нейросеть дорисовывает на ваше фото [1; 2; 3]. Разбираем 15 лет истории: от AR-примерочной "
           "2011 года до ИИ-примерки по селфи.", fs=18, lh=1.55, opacity=0.85, layer="lead",
           mobile={"x": 10, "y": 250, "w": 460, "fs": 16}, **Block.basic("fadeinup", 0.9, 0.2, 30))
    b.button(0, 580, 260, 52, "Покрутить 3D-платье ↗", VIEWER, layer="btn-3d",
             mobile={"x": 10, "y": 420, "w": 230, "h": 48}, **Block.basic("fadeinup", 0.8, 0.35, 20))
    b.button(276, 580, 160, 52, "Листать ↓", rec("ZB02"), primary=False, layer="btn-scroll",
             mobile={"x": 252, "y": 420, "w": 140, "h": 48}, **Block.basic("fadeinup", 0.8, 0.45, 20))
    b.image(740, 110, 400, 500, CDN["loop/iridescence_turntable.gif"], layer="dress",
            mobile={"x": 90, "y": 500, "w": 300, "h": 375}, **Block.parallax_mouse(20, 12))
    for (x, y, w, h) in ((724, 94, 18, 1), (724, 94, 1, 18), (1122, 94, 18, 1), (1139, 94, 1, 18),
                         (724, 626, 18, 1), (724, 609, 1, 18), (1122, 626, 18, 1), (1139, 609, 1, 18)):
        b.shape(x, y, w, h, bg="#3a3d42", layer="reticle", mobile="hide")
    callouts = [(610, 230, "3D CAD · CLO 3D · MARVELOUS DESIGNER [2; 3]", "fadeinleft", 0.6, 300),
                (1000, 400, "ДРАПИРОВКА = СИМУЛЯЦИЯ", "fadeinright", 0.8, 200),
                (610, 540, "IRIDESCENCE · 2019 · $9 500 [8; 9]", "fadeinleft", 1.0, 260)]
    for x, y, label, style, delay, w in callouts:
        a = Block.basic(style, 0.7, delay, 30, mobile=False)
        b.shape(x + w - 6 if style == "fadeinleft" else x - 74, y + 6, 8, 8, bg=CYAN, radius=4, layer="pin-dot",
                mobile="hide", **a)
        b.shape(x + w + 2 if style == "fadeinleft" else x - 66, y + 10, 64, 1, bg=CYAN, opacity=0.6,
                layer="pin-line", mobile="hide", **a)
        b.mono(x - 20 if style == "fadeinleft" else x, y, w, label, fs=11, color=SILVER, mobile="hide",
               layer="callout", **a)
    b.mono(740, 640, 400, "ROT 000° · FRAME 01/12 · STATUS: RENDER", fs=11, mobile="hide", layer="telemetry")
    b.mono(740, 662, 400, "УСЛОВНАЯ 3D-РЕКОНСТРУКЦИЯ · НЕ МОДЕЛЬ THE FABRICANT", fs=10, mobile={
        "x": 90, "y": 885, "w": 300, "fs": 9}, layer="caption")
    metrics = [("2011", "первая AR-примерочная Topshop в Москве на Kinect [32]"),
               ("$9 500", "цена цифрового платья Iridescence, 2019 [8; 9; 10]"),
               ("92 млн т", "текстильных отходов в мире за год, оценка UNEP [27]"),
               ("65 000+", "посетителей Московской недели моды 2026 года, где работала ИИ-примерочная GigaChat [37; 38]")]
    for i, (num, label) in enumerate(metrics):
        mx, myy = (10 + (i % 2) * 235, 930 + (i // 2) * 150)
        b.panel_text(i * 300, 712, 280, [(num, "metric"), (label, "small")], pad=20, gap=6,
                     mobile={"x": mx, "y": myy, "w": 225}, layer=f"metric{i + 1}", min_h=128,
                     anim_panel=Block.basic("fadeinup", 0.7, 0.2 + 0.1 * i, 40))
    return b


# --------------------------------------------------------------------------- ZB03
def zb03() -> Block:
    P = 1800
    D = 150
    b = Block("ZB03", 800 + P, 1700)

    def pin(y):
        return Block.fixing(y, P, "0")

    b.mono(0, 100, 330, cyan("/02") + " · 2019 · THE FABRICANT", mobile={"x": 10, "y": 40, "w": 460, "fs": 11},
           **pin(100))
    b.text(0, 130, 330, "Платье, которого нет,<br>" + muted("продали за $9 500."), fs=40, lh=1.12, fw=700, ls=-1,
           mobile={"x": 10, "y": 64, "w": 460, "fs": 28}, **pin(130))
    b.text(0, 380, 330, "В мае 2019 года нидерландский цифровой дом моды The Fabricant продал на аукционе "
           "Iridescence — первое в мире цифровое кутюрное платье на блокчейне [8; 9; 10]. Прокрутите страницу: "
           "платье сделает полный оборот.", fs=16, lh=1.5, opacity=0.85,
           mobile={"x": 10, "y": 150, "w": 460, "fs": 15}, **pin(380))
    b.image(40, 560, 120, 120, CDN["hud/dial_ring.png"], layer="dial_ring", mobile="hide", **pin(560))
    needle = [scroll_step(0), scroll_step(D * 11, my=D * 11, ro=330), scroll_step(P - D * 11, my=P, ro=330)]
    b.image(40, 560, 120, 120, CDN["hud/dial_needle.png"], layer="dial_needle", mobile="hide",
            **Block.sbs("scroll", needle, trg="0", offset=560))
    # кадры турникета: каждый следующий выше и включается позже
    for k in range(12):
        if k == 0:
            steps = [scroll_step(0), scroll_step(P, my=P)]
        else:
            steps = [scroll_step(0, op=0), scroll_step(D * k, my=D * k, op=0),
                     scroll_step(1, my=D * k + 1, op=1), scroll_step(P - D * k - 1, my=P, op=1)]
        b.image(360, 100, 480, 600, frame(k), layer=f"frame_{k:02d}", mobile="hide",
                **Block.sbs("scroll", steps, trg="0", offset=100))
    for (x, y, w, h) in ((344, 84, 18, 1), (344, 84, 1, 18), (838, 84, 18, 1), (855, 84, 1, 18),
                         (344, 716, 18, 1), (344, 699, 1, 18), (838, 716, 18, 1), (855, 699, 1, 18)):
        b.shape(x, y, w, h, bg="#3a3d42", layer="reticle", mobile="hide", **pin(y))
    b.mono(360, 726, 480, "УСЛОВНАЯ 3D-РЕКОНСТРУКЦИЯ КОМАНДЫ · НЕ МОДЕЛЬ THE FABRICANT", fs=10, mobile="hide",
           **pin(726))
    b.image(0, 0, 300, 375, CDN["loop/iridescence_turntable.gif"], layer="dress_m", desktop=False,
            mobile={"x": 90, "y": 290, "w": 300, "h": 375})
    b.mono(0, 0, 300, "УСЛОВНАЯ 3D-РЕКОНСТРУКЦИЯ · НЕ МОДЕЛЬ THE FABRICANT", fs=9, desktop=False,
           mobile={"x": 90, "y": 672, "w": 300, "fs": 9})
    facts = [("МАЙ 2019 · АУКЦИОН", "Покупатель — канадский предприниматель Ричард Ма. Основатель The Fabricant — "
              "Керри Мерфи [8; 9; 10]."),
             ("КТО СДЕЛАЛ", "Дизайн — креативный директор Эмбер Джей Слотен. Модель — Джоанна Джасковски, "
              "фотограф — Жюльен Буде [8; 9]."),
             ("БЛОКЧЕЙН", "Блокчейн-актив The Fabricant выпустил вместе с Dapper Labs — создателями игры "
              "CryptoKitties [8; 9]."),
             ("ОТКРЫТЫЙ ДОСТУП", "Часть разработок студия выложила бесплатно в форматах OBJ и CLO 3D. Были и проекты "
              "с Puma и Tommy Hilfiger [8; 9].")]
    my_ = 710
    ys = [100, 262, 424, 586]
    for i, (label, body) in enumerate(facts):
        y = ys[i]
        s = [0, 450, 900, 1350][i]
        if i == 0:
            anim = pin(y)
        else:
            steps = [scroll_step(0, my=24, op=0), scroll_step(s, my=s + 24, op=0),
                     scroll_step(120, my=s + 120, op=1), scroll_step(P - s - 120, my=P, op=1)]
            anim = Block.sbs("scroll", steps, trg="0", offset=y)
        _, _, h, mh = b.panel_text(880, y, 300, [(label, "mono"), (body, "small")], pad=18, gap=6,
                                   mobile={"x": 10, "y": my_, "w": 460}, layer=f"fact{i + 1}", anim_panel=anim)
        my_ += mh + 14
    b.mobile_height = my_ + 30
    return b


BLOCKS = {"ZB01": zb01, "ZB03": zb03}


def main(keys: list[str]) -> None:
    OUT.mkdir(exist_ok=True)
    for key in keys or BLOCKS:
        block = BLOCKS[key]()
        code = block.to_code()
        path = OUT / f"{key}.json"
        path.write_text(json.dumps({"recordid": RECORDS[key], "code": code}, ensure_ascii=False), encoding="utf-8")
        print(key, RECORDS[key], len(block.elements), "elements", path.stat().st_size, "bytes")


if __name__ == "__main__":
    main(sys.argv[1:])
