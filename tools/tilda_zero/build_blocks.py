"""Сборка JSON для Zero Block лонгрида «Несуществующий гардероб».

Запуск: python tools/tilda_zero/build_blocks.py [ZB01 ZB03 …] → tools/tilda_zero/out/<ключ>.json
Тексты и раскладка — по docs/tilda/zero_block_longread_manual.md, факты — по финальной статье [1]–[39].
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from zb import (CARBON, CYAN, LINE_ACTIVE, LINE_PANEL, MUTED, OK, PANEL, SILVER, WARN, Block,  # noqa: E402
                bold, cyan, estimate_height, muted, scroll_step, time_step)

OUT = Path(__file__).parent / "out"
CDN = json.loads((Path(__file__).parent / "cdn.json").read_text(encoding="utf-8"))
RECORDS = json.loads((Path(__file__).parent / "records.json").read_text(encoding="utf-8"))
VIEWER = "https://raw.githack.com/EGRNEGR/MEDIA-SCI/tilda-zero-longread/media/3d/iridescence-viewer/index.html"
REPO = "https://github.com/EGRNEGR/MEDIA-SCI"
RETICLE = "#3a3d42"


def rec(key: str) -> str:
    return f"#rec{RECORDS[key]}"


def frame(i: int) -> str:
    return CDN[f"turntable/turntable_{i:02d}.jpg"]


def head(b: Block, y: int, index: str, h2: str, *, x=0, w=760, my=40, fs=48, anim=None, pin=None):
    """Индекс + двухцветный заголовок. Возвращает (низ на десктопе, низ на мобильном)."""
    num, _, rest = index.partition(" · ")
    a1 = dict(anim) if anim is not None else Block.basic("fadeinup", 0.8, 0, 40)
    a2 = dict(a1)
    if pin is not None:
        a1, a2 = Block.fixing(y, pin), Block.fixing(y + 30, pin)
    b.mono(x, y, w, cyan(num) + " · " + rest, fs=12, mobile={"x": 10, "y": my, "w": 460, "fs": 11}, **a1)
    b.text(x, y + 30, w, h2, fs=fs, lh=1.12, fw=700, ls=-1, layer="h2",
           mobile={"x": 10, "y": my + 24, "w": 460, "fs": 28}, **a2)
    return y + 30 + estimate_height(h2, w, fs, 1.12), my + 24 + estimate_height(h2, 460, 28, 1.12)


def reticle(b: Block, x0, y0, x1, y1, **anim):
    for (x, y, w, h) in ((x0, y0, 18, 1), (x0, y0, 1, 18), (x1 - 18, y0, 18, 1), (x1 - 1, y0, 1, 18),
                         (x0, y1 - 1, 18, 1), (x0, y1 - 18, 1, 18), (x1 - 18, y1 - 1, 18, 1), (x1 - 1, y1 - 18, 1, 18)):
        a = dict(anim)
        if "animfixtrgofst" in a:
            a["animfixtrgofst"] = str(y)
        b.shape(x, y, w, h, bg=RETICLE, layer="reticle", mobile="hide", **a)


def fan(i: int, n: int = 3, delay_step=0.12) -> dict:
    """R1: появление карточки с «перекрутом» — разворот, уменьшение и сдвиг к центру."""
    side = i - (n - 1) / 2
    start = time_step(0, mx=-140 * side, my=120 if side else 160, sc=0.86, op=0, ro=12 * side)
    end = time_step(900, ea="easeOut", dt=i * delay_step * 1000)
    return Block.sbs("intoview", [start, end], trg="1", offset=120)


# --------------------------------------------------------------------------- ZB01 герой
def zb01() -> Block:
    b = Block("ZB01", 900, 1300)
    for x in (0, 300, 600, 900, 1200):
        b.shape(x, 0, 1, 900, bg="#15181c", layer="hairline", mobile="hide")
    b.text(0, 28, 400, bold("НЕСУЩЕСТВУЮЩИЙ") + " ГАРДЕРОБ", fs=15, lh=1.3, ls=1.5, layer="brand",
           mobile={"x": 10, "y": 24, "w": 300, "fs": 13})
    nav = [("/01 ФОРМАТЫ", "ZB02", 430), ("/02 ХРОНОЛОГИЯ", "ZB04", 545), ("/03 РОССИЯ", "ZB06", 690),
           ("/04 ПРИМЕРКА", "ZB07", 800), ("/05 ЭКОЛОГИЯ", "ZB08", 920), ("/06 МИФ ИЛИ ФАКТ", "ZB10", 1040)]
    for label, target, x in nav:
        b.mono(x, 30, 150, f'<a href="{rec(target)}" style="color: {MUTED};">{label}</a>', fs=11, mobile="hide",
               layer="nav")
    b.mono(0, 150, 640, cyan("/00") + " · ЛОНГРИД ПО СТАТЬЕ РУВИКИ «ВИРТУАЛЬНАЯ ОДЕЖДА»", fs=12,
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
    reticle(b, 724, 94, 1156, 627)
    callouts = [(610, 230, "3D CAD · CLO 3D · MARVELOUS DESIGNER [2; 3]", "fadeinleft", 0.6, 300),
                (1000, 400, "ДРАПИРОВКА = СИМУЛЯЦИЯ", "fadeinright", 0.8, 200),
                (610, 540, "IRIDESCENCE · 2019 · $9 500 [8; 9]", "fadeinleft", 1.0, 260)]
    for x, y, label, style, delay, w in callouts:
        a = Block.basic(style, 0.7, delay, 30, mobile=False)
        left = style == "fadeinleft"
        b.shape(x + w - 6 if left else x - 74, y + 6, 8, 8, bg=CYAN, radius=4, layer="pin-dot", mobile="hide", **a)
        b.shape(x + w + 2 if left else x - 66, y + 10, 64, 1, bg=CYAN, opacity=0.6, layer="pin-line",
                mobile="hide", **a)
        b.mono(x - 20 if left else x, y, w, label, fs=11, color=SILVER, mobile="hide", layer="callout", **a)
    b.mono(740, 640, 400, "ROT 000° · FRAME 01/12 · STATUS: RENDER", fs=11, mobile="hide", layer="telemetry")
    b.mono(740, 662, 420, "УСЛОВНАЯ 3D-РЕКОНСТРУКЦИЯ · НЕ МОДЕЛЬ THE FABRICANT", fs=10,
           mobile={"x": 90, "y": 885, "w": 300, "fs": 9}, layer="caption")
    metrics = [("2011", "первая AR-примерочная Topshop в Москве на Kinect [32]"),
               ("$9 500", "цена цифрового платья Iridescence, 2019 [8; 9; 10]"),
               ("92 млн т", "текстильных отходов в мире за год, оценка UNEP [27]"),
               ("65 000+", "посетителей Московской недели моды 2026 года, где работала ИИ-примерочная GigaChat "
                           "[37; 38]")]
    for i, (num, label) in enumerate(metrics):
        b.panel_text(i * 300, 712, 280, [(num, "metric"), (label, "small")], pad=20, gap=6, min_h=160,
                     mobile={"x": 10 + (i % 2) * 235, "y": 930 + (i // 2) * 160, "w": 225}, layer=f"metric{i + 1}",
                     anim_panel=Block.basic("fadeinup", 0.7, 0.2 + 0.1 * i, 40))
    return b


# --------------------------------------------------------------------------- ZB02 форматы
def zb02() -> Block:
    b = Block("ZB02", 900, 1600)
    for i, word in enumerate(("3D", "AR", "2D")):
        b.text(i * 400, 250, 380, word, fs=240, lh=1, fw=700, color="#141820", layer="bg-word", mobile="hide",
               **Block.parallax_scroll(70))
    _, my = head(b, 100, "/01 · ФОРМАТЫ", "Одна вещь —<br>" + muted("три разных цифровых объекта."))
    cards = [("/01", "3D CAD-модель", "Модель строят по лекалам и задают свойства ткани. Складки, натяжение и "
              "драпировку считает программа: это математическая симуляция, а не поведение настоящей вещи. "
              "Инструменты — CLO 3D, Marvelous Designer, VStitcher, DC Suite [2; 3].", "ДЛЯ: ПРОТОТИПЫ КОЛЛЕКЦИЙ"),
             ("/02", "Вещь для аватара и AR", "Интерактивный предмет для персонажа в игре, метавселенной или "
              "дополненной реальности. Перенести его на другую платформу удаётся не всегда: всё решают форматы "
              "файлов, технические стандарты и правила конкретной среды [1; 2; 4].", "ДЛЯ: АВАТАРЫ, AR-ФИЛЬТРЫ"),
             ("/03", "2D-образ на фото", "Картинка, которую дизайнер накладывает на снимок покупателя или которую "
              "синтезирует нейросеть. Диффузионная модель Google строит фото человека в выбранной вещи по двум "
              "снимкам — человека и изделия [1].", "ДЛЯ: СОЦСЕТИ, ОНЛАЙН-ПРИМЕРКА")]
    my += 30
    for i, (idx, title, body, tag) in enumerate(cards):
        _, _, h, mh = b.panel_text(i * 400, 300, 380, [(cyan(idx), "mono"), (title, "h3"), (body, "body"),
                                                         (tag, "mono")], pad=28, gap=14, min_h=430,
                                   mobile={"x": 10, "y": my, "w": 460}, layer=f"card{i + 1}", anim_panel=fan(i))
        my += mh + 16
    note = ("Для ручной подгонки 3D-вещи под фото заказчик обычно присылает снимок в облегающей одежде при хорошем "
            "свете. Цена складывается из дизайна, адаптации под фото и сложности работы [2; 3].")
    b.text(0, 780, 1160, note, fs=15, lh=1.5, color=MUTED, mobile={"x": 10, "y": my + 10, "w": 460, "fs": 14},
           **Block.basic("fadein", 0.8, 0.3))
    b.mobile_height = my + 10 + estimate_height(note, 460, 14, 1.5) + 50
    return b


# --------------------------------------------------------------------------- ZB03 турникет
def zb03() -> Block:
    P, D = 1800, 150
    b = Block("ZB03", 800 + P, 1700)

    def pin(y):
        return Block.fixing(y, P, "0")

    b.mono(0, 100, 330, cyan("/02") + " · 2019 · THE FABRICANT", fs=12, mobile={"x": 10, "y": 40, "w": 460, "fs": 11},
           **pin(100))
    b.text(0, 130, 330, "Платье,<br>которого нет,<br>" + muted("продали за $9 500."), fs=36, lh=1.12, fw=700, ls=-1,
           layer="h2", mobile={"x": 10, "y": 64, "w": 460, "fs": 28}, **pin(130))
    b.text(0, 290, 330, "В мае 2019 года нидерландский цифровой дом моды The Fabricant продал на аукционе "
           "Iridescence — первое в мире цифровое кутюрное платье на блокчейне [8; 9; 10]. Прокрутите страницу: "
           "платье сделает полный оборот.", fs=16, lh=1.5, opacity=0.85,
           mobile={"x": 10, "y": 170, "w": 460, "fs": 15}, **pin(290))
    b.mono(40, 530, 200, "ROT · УГОЛ ПОВОРОТА", fs=10, mobile="hide", **pin(530))
    b.image(40, 560, 120, 120, CDN["hud/dial_ring.png"], layer="dial_ring", mobile="hide", **pin(560))
    needle = [scroll_step(0), scroll_step(D * 11, my=D * 11, ro=330), scroll_step(P - D * 11, my=P, ro=330)]
    b.image(40, 560, 120, 120, CDN["hud/dial_needle.png"], layer="dial_needle", mobile="hide",
            **Block.sbs("scroll", needle, trg="0", offset=560))
    for k in range(12):
        if k == 0:
            steps = [scroll_step(0), scroll_step(P, my=P)]
        else:
            steps = [scroll_step(0, op=0), scroll_step(D * k, my=D * k, op=0),
                     scroll_step(1, my=D * k + 1, op=1), scroll_step(P - D * k - 1, my=P, op=1)]
        b.image(360, 100, 480, 600, frame(k), layer=f"frame_{k:02d}", mobile="hide",
                **Block.sbs("scroll", steps, trg="0", offset=100))
    reticle(b, 344, 84, 856, 717, **pin(0))
    b.mono(360, 726, 480, "УСЛОВНАЯ 3D-РЕКОНСТРУКЦИЯ КОМАНДЫ · НЕ МОДЕЛЬ THE FABRICANT", fs=10, mobile="hide",
           **pin(726))
    b.image(0, 0, 300, 375, CDN["loop/iridescence_turntable.gif"], layer="dress_m", desktop=False,
            mobile={"x": 90, "y": 300, "w": 300, "h": 375})
    b.mono(0, 0, 300, "УСЛОВНАЯ 3D-РЕКОНСТРУКЦИЯ · НЕ МОДЕЛЬ THE FABRICANT", fs=9, desktop=False,
           mobile={"x": 90, "y": 682, "w": 300, "fs": 9})
    facts = [("МАЙ 2019 · АУКЦИОН", "Покупатель — канадский предприниматель Ричард Ма. Основатель The Fabricant — "
              "Керри Мерфи [8; 9; 10]."),
             ("КТО СДЕЛАЛ", "Дизайн — креативный директор Эмбер Джей Слотен. Модель — Джоанна Джасковски, "
              "фотограф — Жюльен Буде [8; 9]."),
             ("БЛОКЧЕЙН", "Блокчейн-актив The Fabricant выпустил вместе с Dapper Labs — создателями игры "
              "CryptoKitties [8; 9]."),
             ("ОТКРЫТЫЙ ДОСТУП", "Часть разработок студия выложила бесплатно в форматах OBJ и CLO 3D. Были и проекты "
              "с Puma и Tommy Hilfiger [8; 9].")]
    y, my = 100, 720
    for i, (label, body) in enumerate(facts):
        s = (0, 450, 900, 1350)[i]
        if i == 0:
            steps = [scroll_step(0), scroll_step(P, my=P)]
        else:
            steps = [scroll_step(0, my=24, op=0), scroll_step(s, my=s + 24, op=0),
                     scroll_step(120, my=s + 120, op=1), scroll_step(P - s - 120, my=P, op=1)]
        anim = Block.sbs("scroll", steps, trg="0", offset=y)
        _, _, h, mh = b.panel_text(880, y, 300, [(label, "mono"), (body, "small")], pad=18, gap=6,
                                   mobile={"x": 10, "y": my, "w": 460}, layer=f"fact{i + 1}", anim_panel=anim)
        y += h + 22
        my += mh + 14
    b.mobile_height = my + 30
    return b


# --------------------------------------------------------------------------- ZB04 хронология
TIMELINE = [
    ("2011.05", "Topshop, Москва", "Студия AR Door собрала AR-примерочную на Microsoft Kinect: камера следила за "
     "телом, а на экране поверх изображения появлялось 3D-платье [32]."),
    ("2015", "Cattytay", "Британская художница Кэт Тейлор переводит в цифру вещи Vetements, Gucci, Off-White, "
     "Balenciaga, Alexander Wang и Chloé. В 2019 году она основала коллектив Digi-Gxl: более 300 женщин, "
     "трансгендерных, интерсекс- и небинарных специалистов [2; 5]."),
    ("2016", "Bitmoji × Bergdorf Goodman", "Аватары получили образы Zac Posen, Alexander McQueen и Calvin Klein [4]."),
    ("2018.11", "Carlings × Virtue", "19 вещей без размерной и гендерной маркировки, от 10 до 30 евро, по 12 "
     "экземпляров. По данным Vogue Business, коллекцию распродали за неделю [6; 7]."),
    ("2019.05", "Iridescence", "Первое цифровое кутюрное платье на блокчейне ушло с аукциона за 9 500 долларов "
     "[8; 9; 10]."),
    ("2020.08", "DRESSX", "Дарья Шаповалова и Наталья Моденова запустили платформу цифровой одежды со "
     "штаб-квартирой в Лос-Анджелесе [11; 12]."),
    ("2022.06", "Meta Avatars Store", "Пользователи Facebook, Instagram и Messenger получили для аватаров комплекты "
     "Balenciaga, Prada и Thom Browne [13]."),
    ("2023.06", "Google TryOnDiffusion", "Генеративная примерка в Google Shopping. На запуске показали 40 реальных "
     "моделей с размерами от XXS до 4XL [1; 33]."),
    ("2024.06", "Хайп остывает", "Vogue Business отмечает заметное ослабление ажиотажа вокруг криптовалют, NFT и "
     "метавселенных [24]."),
    ("2025.04", "Metaverse Fashion Week", "Неделя моды в Decentraland с 9 по 12 апреля: 105 виртуальных участков, "
     "16 шоурумов, тема Infinite Identities [15]."),
    ("2025.12", "Nano Banana", "Google строит студийный полноростовой образ покупателя по одному селфи и указанному "
     "размеру [36]."),
    ("2026.03", "GigaChat на МНМ", "На VI Московской неделе моды в «Манеже» гости примеряли цифровые версии "
     "коллекций молодых дизайнеров. Всего за шесть дней — более 65 000 посетителей [37; 38]."),
]


def zb04() -> Block:
    P, SHIFT = 2400, 3360
    b = Block("ZB04", 800 + P, 4000)
    _, my = head(b, 90, "/03 · ХРОНОЛОГИЯ", "15 лет за один скролл.<br>" + muted("От Kinect до селфи."), pin=P)
    lane = [scroll_step(0), scroll_step(P, mx=-SHIFT, my=P)]
    b.shape(0, 300, 4520, 1, bg=LINE_ACTIVE, layer="rail", mobile="hide",
            **Block.sbs("scroll", lane, trg="0", offset=300))
    b.shape(10, my + 20, 1, 10, bg=CYAN, opacity=0.3, layer="rail_m", desktop=False, mobile={"x": 10, "y": my + 20,
                                                                                             "w": 1, "h": 10})
    my += 30
    m_start = my
    for i, (date, title, body) in enumerate(TIMELINE):
        x = i * 380
        b.shape(x, 296, 1, 9, bg=CYAN, layer="tick", mobile="hide", **Block.sbs("scroll", lane, trg="0", offset=296))
        items = [(cyan(date) + f" · /{i + 1:02d}", "mono"), (title, "h3"), (body, "small")]
        b.panel_text(x, 330, 340, items, pad=24, gap=10, min_h=360, mobile="hide", layer=f"card{i + 1:02d}",
                     anim_panel=Block.sbs("scroll", lane, trg="0", offset=330))
        _, _, _, mh = b.panel_text(0, 0, 340, items, pad=24, gap=10, desktop=False,
                                   mobile={"x": 30, "y": my, "w": 440}, layer=f"card{i + 1:02d}_m",
                                   anim_panel=Block.basic("fadeinup", 0.6, 0, 30))
        my += mh + 14
    # вертикальный рельс для мобильной версии: высота по факту
    b.elements[-1 - 0]  # noqa: B018 — карточки уже добавлены
    for el in b.elements:
        if el["layer"] == "rail_m":
            el["_mobile"] = {"x": 14, "y": m_start, "w": 1, "h": my - m_start}
    b.mono(0, 740, 600, "SCROLL → 2011 … 2026", fs=11, mobile="hide", **Block.fixing(740, P))
    b.mobile_height = my + 30
    return b


# --------------------------------------------------------------------------- ZB05 эпохи
def zb05() -> Block:
    b = Block("ZB05", 1000, 2200)
    for i, num in enumerate(("01", "02", "03")):
        b.text(i * 400 + 160, 60, 240, num, fs=200, lh=1, fw=700, color="#141820", layer="era-num", mobile="hide",
               **Block.parallax_scroll(75))
    _, my = head(b, 90, "/03.1 · ТРИ ЭПОХИ", "Игры, блокчейн,<br>" + muted("генеративный ИИ."))
    eras = [
        ("ДО 2018 · ИГРЫ И АВАТАРЫ", "Сначала одежда жила в играх и аватарах",
         "Ещё до маркетплейсов цифровые вещи продавались в играх и сервисах кастомизации аватаров [4; 6]. "
         "В 2016 году Bitmoji и Bergdorf Goodman одели аватары в образы известных брендов [4].",
         [("$53,4 млн", "выручка Covet Fashion за 2018 год"), ("ОГОВОРКА", "часть суммы — реклама, а не продажи одной "
           "цифровой одежды [7]")]),
        ("2019–2024 · NFT И МЕТАВСЕЛЕННЫЕ", "Потом — NFT и метавселенные",
         "В 2021–2022 годах внимание подогрели NFT и метавселенные [13; 24]. Рост не был линейным: в июне 2024 года "
         "Vogue Business писал об ослаблении ажиотажа [24].",
         [("50 копий", "лимит редкости Exotic в Decentraland, II квартал 2024 года. Инструмент для авторов, "
           "а не показатель продаж [14]"), ("7 500 MANA", "призовой фонд разового конкурса Wearables, апрель 2025 [16]")]),
        ("2023–2026 · ГЕНЕРАТИВНЫЙ ИИ", "Теперь вещь дорисовывает нейросеть",
         "С 2023 года в примерке распространился генеративный ИИ [1]. Нейросеть рисует картинку, но не заменяет "
         "3D-модель: по-прежнему нужны лекала, свойства материалов и проверка геометрии.",
         [("24.07.2025", "ИИ-примерка Google доступна по всей территории США [34; 35]"),
          ("1 селфи", "нужно Nano Banana для полноростового образа, декабрь 2025 [36]")]),
    ]
    my += 30
    for i, (label, title, body, stats) in enumerate(eras):
        items = [(cyan(label), "mono"), (title, "h3"), (body, "small")]
        for num, cap in stats:
            if num == "ОГОВОРКА":
                items.append(("ОГОВОРКА: " + cap, "warn"))
                continue
            items.append((num, "metric"))
            items.append((cap, "small"))
        _, _, h, mh = b.panel_text(i * 400, 300, 380, items, pad=26, gap=10, min_h=620,
                                   mobile={"x": 10, "y": my, "w": 460}, layer=f"era{i + 1}", anim_panel=fan(i))
        my += mh + 16
    b.mobile_height = my + 40
    return b


# --------------------------------------------------------------------------- ZB06 Россия
def zb06() -> Block:
    b = Block("ZB06", 1180, 2000)
    _, my = head(b, 80, "/04 · РОССИЯ", "Первая продажа — за 5 000 рублей.<br>" + muted("Дальше — маркетплейс и музей."),
                 w=1000)
    big = [("5 000 ₽", "первый цифровой наряд, проданный в России, 2020 [17]"),
           ("48 ч", "за столько Replicant присылал фото покупателя в цифровом образе [18]")]
    my += 24
    for i, (num, cap) in enumerate(big):
        y = 290 + i * 190
        b.text(0, y, 400, num, fs=72, lh=1, fw=700, color=SILVER, layer="big",
               mobile={"x": 10 + i * 235, "y": my, "w": 225, "fs": 40}, **Block.basic("zoomin", 0.9, 0.1 * i))
        b.text(0, y + 86, 360, cap, fs=15, lh=1.45, color=MUTED, layer="big-cap",
               mobile={"x": 10 + i * 235, "y": my + 52, "w": 220, "fs": 13}, **Block.basic("fadein", 0.9, 0.2))
    my += 52 + 80
    events = [("2020.03.04", "Регина Турбина, дизайнер из Уфы и основательница марки Ophelica, продала цифровой "
               "свитшот и брюки за 5 000 рублей Даниилу Трабуну, тогдашнему медиадиректору «Яндекса». The Blueprint "
               "назвал сделку первой зафиксированной продажей виртуального наряда в России [17]."),
              ("2020.05.20", "Турбина открыла Replicant. По описанию самой платформы, это первый в стране "
               "мультибрендовый маркетплейс цифровой моды с работами независимых 3D-дизайнеров [18]."),
              ("2021.08", "Replicant запустил браузерную примерочную: цифровую одежду примеряли через обычную "
               "веб-камеру, без приложения [20]."),
              ("2022.11", "Сбер выпустил «Калейдоскоп культур»: десять 3D-костюмов с оцифрованными народными "
               "орнаментами. Компьютерное зрение распознавало позу на фото и подгоняло под неё «скелет» костюма [21]."),
              ("2026.03", "ИИ-примерочная на базе GigaChat на VI Московской неделе моды [37; 38]."),
              ("2026.11.12", "Сайт Replicant сообщает: продажи прекращены, архив сохранён как онлайн-музей цифровой "
               "моды [18].")]
    y = 290
    rail_top, mrail_top = y, my
    nodes = []
    for date, text in events:
        html = cyan(date) + "<br>" + text
        h = estimate_height(html, 660, 16, 1.5)
        mh = estimate_height(html, 430, 14, 1.5)
        node_steps = [scroll_step(0, op=0.2), scroll_step(80, op=1, sc=1.6), scroll_step(80, op=1, sc=1)]
        nodes.append(b.shape(456, y + 6, 9, 9, bg=CYAN, radius=5, layer="node",
                             mobile={"x": 10, "y": my + 6, "w": 9, "h": 9},
                             **Block.sbs("scroll", node_steps, trg="0.5", offset=0)))
        b.text(500, y, 660, html, fs=16, lh=1.5, layer="event", mobile={"x": 34, "y": my, "w": 436, "fs": 14},
               **Block.basic("fadeinleft", 0.7, 0, 40))
        y += h + 36
        my += mh + 26
    b.shape(460, rail_top, 1, y - rail_top - 30, bg=LINE_ACTIVE, layer="rail",
            mobile={"x": 14, "y": mrail_top, "w": 1, "h": my - mrail_top - 20})
    # рельс должен лежать под узлами: переносим его в начало списка слоёв
    rail = b.elements.pop()
    b.elements.insert(0, rail)
    for z, el in enumerate(b.elements, 1):
        el["zindex"] = z
    b.height = max(1180, y + 40)
    b.mobile_height = my + 40
    return b


# --------------------------------------------------------------------------- ZB07 примерочные
def zb07() -> Block:
    b = Block("ZB07", 1080, 2300)
    _, my = head(b, 80, "/05 · ВИРТУАЛЬНАЯ ПРИМЕРОЧНАЯ", "Три технологии<br>" + muted("с одним названием."))
    b.button(900, 100, 260, 52, "3D-сцена ↗", VIEWER, layer="cta-3d", mobile={"x": 10, "y": my + 14, "w": 200, "h": 48},
             **Block.basic("fadein", 0.8, 0.3))
    my += 80
    techs = [("/01 · AR-НАЛОЖЕНИЕ", "Камера и цифровая модель", "Модель накладывается поверх изображения с камеры. "
              "Пример — примерка обуви у Gucci и Lamoda; Rebecca Minkoff показывала через AR, как сумка смотрится "
              "в интерьере [4; 32]."),
             ("/02 · 3D-ПАРАМЕТРИЧЕСКАЯ", "Тело и одежда в 3D", "Результат строится сопоставлением 3D-моделей тела и "
              "одежды [1; 4]."),
             ("/03 · ГЕНЕРАТИВНАЯ", "Новое фото от нейросети", "Нейросеть синтезирует новое двухмерное изображение "
              "человека в выбранной вещи [1; 33].")]
    for i, (label, title, body) in enumerate(techs):
        _, _, h, mh = b.panel_text(i * 400, 250, 380, [(cyan(label), "mono"), (title, "h3"), (body, "small")],
                                   pad=24, gap=10, min_h=230, mobile={"x": 10, "y": my, "w": 460}, layer=f"tech{i + 1}",
                                   anim_panel=fan(i))
        my += mh + 14
    cap = ("Google TryOnDiffusion, 2023: модель учится на миллионах пар изображений из Shopping Graph и рисует картинку "
           "с нуля, а не растягивает контур вещи [1; 33].")
    b.text(0, 530, 1160, cap, fs=16, lh=1.5, color=MUTED, mobile={"x": 10, "y": my + 16, "w": 460, "fs": 14},
           **Block.basic("fadein", 0.8))
    my += 16 + estimate_height(cap, 460, 14, 1.5) + 16
    nodes = [("ФОТО ЧЕЛОВЕКА", 0, 600), ("ФОТО ВЕЩИ", 0, 720), ("PERSON-UNET", 300, 600), ("GARMENT-UNET", 300, 720),
             ("CROSS-ATTENTION", 620, 660), ("НОВОЕ ФОТО", 940, 660)]
    for k, (label, x, y) in enumerate(nodes):
        accent = label == "CROSS-ATTENTION"
        b.shape(x, y, 220, 72, bg=PANEL, border=CYAN if accent else LINE_PANEL, radius=12, layer="pipe-node",
                mobile={"x": 10 + (k % 2) * 235, "y": my + (k // 2) * 86, "w": 225, "h": 72},
                **Block.basic("fadein", 0.6, 0.15 * k))
        b.mono(x + 20, y + 27, 180, label, fs=12, color=CYAN if accent else SILVER,
               mobile={"x": 30 + (k % 2) * 235, "y": my + (k // 2) * 86 + 27, "w": 185, "fs": 11},
               **Block.basic("fadein", 0.6, 0.15 * k))
    for (x, y, w) in ((220, 636, 80), (220, 756, 80), (520, 636, 100), (520, 756, 100), (840, 696, 100)):
        b.shape(x, y, w, 1, bg=LINE_ACTIVE, layer="pipe-line", mobile="hide")
    packet = [time_step(0, op=0), time_step(200, op=1), time_step(1600, mx=400, my=60), time_step(200, mx=400, my=60,
                                                                                                    op=0)]
    b.shape(216, 632, 8, 8, bg=CYAN, radius=4, layer="packet", mobile="hide",
            **Block.sbs("intoview", packet, trg="1", offset=0, loop="loop"))
    packet2 = [time_step(0, op=0), time_step(200, op=1), time_step(1600, mx=400, my=-60), time_step(200, mx=400, my=-60,
                                                                                                      op=0)]
    b.shape(216, 752, 8, 8, bg=CYAN, radius=4, layer="packet", mobile="hide",
            **Block.sbs("intoview", packet2, trg="1", offset=0, loop="loop"))
    my += 3 * 86 + 20
    caveat = [("ОГОВОРКА", "warn"), ("Примерка показывает образ, а не размер. Генеративная картинка — ориентир, а не "
              "антропометрически точная копия тела, и размер для покупки она не определяет [36]. Примерка товара в "
              "магазине тоже не делает его виртуальной одеждой.", "body")]
    _, _, _, mh = b.panel_text(0, 860, 1160, caveat, pad=24, gap=8, border=WARN, mobile={"x": 10, "y": my, "w": 460},
                               layer="caveat", anim_panel=Block.basic("fadeinup", 0.7, 0, 30))
    b.mobile_height = my + mh + 40
    return b


# --------------------------------------------------------------------------- ZB08 экология
def zb08() -> Block:
    b = Block("ZB08", 1260, 2100)
    for n in range(6):
        rot = (-18, 12, -9, 9, -12, 18)[n]
        mx = (-120, 80, -40, 40, -80, 120)[n]
        steps = [scroll_step(0, mx=mx, ro=rot, op=0.4), scroll_step(500, op=1)]
        msteps = [scroll_step(0, mx=mx / 2, ro=rot, op=0.4), scroll_step(400, op=1)]
        b.image(60, 160 + 100 * n, 480, 100, CDN[f"twist/twist_strip_{n + 1}.jpg"], layer=f"strip{n + 1}",
                mobile={"x": 90, "y": 40 + 62 * n, "w": 300, "h": 62, "steps": msteps},
                **Block.sbs("scroll", steps, trg="1", offset=0))
    b.mono(60, 770, 480, "ЦИФРОВАЯ ВЕЩЬ СОБИРАЕТСЯ ИЗ ДАННЫХ · УСЛОВНАЯ 3D-РЕКОНСТРУКЦИЯ", fs=10,
           mobile={"x": 90, "y": 420, "w": 300, "fs": 9})
    _, my = head(b, 120, "/06 · ЭКОЛОГИЯ", "Цифровая вещь не шьётся.<br>" + muted("Но и не бесплатна для планеты."),
                 x=620, w=560, fs=40, my=470)
    big_steps = [scroll_step(0, sc=0.6, op=0), scroll_step(400, op=1)]
    b.text(620, 330, 560, "92 млн т", fs=88, lh=1, fw=700, layer="big-number",
           mobile={"x": 10, "y": my + 20, "w": 460, "fs": 56}, **Block.sbs("scroll", big_steps, trg="1", offset=0))
    cap = "текстильных отходов в мире за год — оценка UNEP, март 2025 года [27]"
    b.text(620, 430, 560, cap, fs=15, lh=1.45, color=MUTED, mobile={"x": 10, "y": my + 86, "w": 460, "fs": 13})
    my += 86 + 40
    stats = [("×2", "производство одежды в 2000–2015 годах [27]"),
             ("−36 %", "срок службы вещей за тот же период [27]"),
             ("8 %", "доля волокон из вторсырья в 2023 году [27]"),
             ("< 1 %", "старой одежды перерабатывается в новую [27]"),
             ("2–8 %", "доля текстильной отрасли в мировых выбросах парниковых газов [28]"),
             ("9 %", "британских покупателей брали вещь ради фото и возвращали. Barclaycard, 2018, только "
                     "Великобритания [25]")]
    for i, (num, label) in enumerate(stats):
        x = 620 + (i % 2) * 290
        y = 500 + (i // 2) * 150
        b.panel_text(x, y, 270, [(num, "metric"), (label, "small")], pad=18, gap=4, min_h=136,
                     mobile={"x": 10 + (i % 2) * 235, "y": my + (i // 2) * 150, "w": 225}, layer=f"stat{i + 1}",
                     anim_panel=Block.basic("fadeinup", 0.6, 0.08 * i, 30))
    my += 3 * 150 + 10
    caveat = [("ОГОВОРКА", "warn"), ("Виртуальная одежда не экологична автоматически. Эффект есть, если она заменяет "
              "пошив и покупку реальной вещи. Против неё работают энергия серверов, обучение и работа нейросетей, "
              "хранение данных и наши устройства. Цифровые прототипы способны заменить часть физических образцов: "
              "шведский бренд Atacac визуализирует модели в CLO 3D и принимает предзаказы до пошива [29].", "body")]
    _, _, _, mh = b.panel_text(0, 1000, 1160, caveat, pad=24, gap=8, border=WARN, mobile={"x": 10, "y": my, "w": 460},
                               layer="caveat", anim_panel=Block.basic("fadeinup", 0.7, 0, 30))
    b.mobile_height = my + mh + 40
    return b


# --------------------------------------------------------------------------- ZB09 право
def zb09() -> Block:
    b = Block("ZB09", 720, 1200)
    _, my = head(b, 80, "/07 · ПРАВО", "Сумка, которой нет,<br>" + muted("всё равно нарушила товарный знак."), w=1000)
    my += 30
    cards = [[("$133 000", "metric"), ("В 2023 году присяжные суда Южного округа Нью-Йорка признали художника "
              "Мэйсона Ротшильда ответственным за нарушение прав Hermès: его NFT-коллекция MetaBirkins изображала "
              "цифровые сумки в стиле Birkin. 23 июня 2023 года суд вынес постоянный запрет [31].", "body")],
             [(cyan("ЧТО ЭТО ЗНАЧИТ"), "mono"), ("Дело показало, как законы США о товарных знаках применяются к NFT. "
              "Универсальных международных правил для цифровой моды оно не создало [31]. Открытыми остаются вопросы о "
              "защите пользовательских фото в облачных примерочных и о стандартах переноса 3D-вещей между мирами "
              "[14; 36].", "body")]]
    for i, items in enumerate(cards):
        _, _, h, mh = b.panel_text(i * 600, 290, 560, items, pad=28, gap=12, min_h=320,
                                   mobile={"x": 10, "y": my, "w": 460}, layer=f"law{i + 1}", anim_panel=fan(i, 2))
        my += mh + 16
    b.mobile_height = my + 40
    return b


# --------------------------------------------------------------------------- ZB10 квиз
QUIZ = [
    ("«Цифровая одежда автоматически экологичнее обычной.»", "myth",
     "Всё зависит от того, заменяет ли она пошив и покупку настоящей вещи и сколько энергии съедают серверы, "
     "нейросети и устройства. Это вывод статьи (раздел «Влияние на модную индустрию»)."),
    ("«Первое цифровое платье на блокчейне продали дороже 9 000 долларов.»", "fact",
     "Iridescence ушло с аукциона в мае 2019 года за 9 500 долларов [8; 9; 10]."),
    ("«9 % покупателей в мире покупают вещи ради фото и потом возвращают.»", "myth",
     "9 % — результат опроса Barclaycard 2018 года, и только в Великобритании [25]."),
    ("«Первый цифровой наряд в России продали за 5 000 рублей.»", "fact",
     "Регина Турбина, 4 марта 2020 года, по данным The Blueprint [17]."),
    ("«ИИ-примерка по селфи подбирает точный размер.»", "myth",
     "Нейросеть показывает ориентировочный образ вещи на фигуре, точный размер она не определяет [36]."),
]


def zb10() -> Block:
    b = Block("ZB10", 260 + 230 * 5 + 60, 2600)
    _, my = head(b, 80, "/08 · ПРОВЕРЬ СЕБЯ", "Миф или факт?<br>" + muted("Пять утверждений из статьи."))
    sub = "Без регистрации. Ответы нигде не сохраняются — это проверка для себя."
    b.text(0, 220, 760, sub, fs=15, lh=1.45, color=MUTED, mobile={"x": 10, "y": my + 12, "w": 460, "fs": 14})
    my += 12 + estimate_height(sub, 460, 14, 1.45) + 24
    off = 2000  # артборд обрезает всё за краем: до клика вердикт не виден
    reveal = [time_step(0, mx=-off, my=12, op=0), time_step(350, mx=-off, ea="easeOut")]
    for i, (q, answer, why) in enumerate(QUIZ):
        y = 260 + 230 * i
        b.shape(0, y, 1160, 210, bg=PANEL, border=LINE_PANEL, radius=16, layer=f"row{i + 1}",
                mobile={"x": 10, "y": my, "w": 460, "h": 360}, **Block.basic("fadeinup", 0.6, 0, 30))
        b.mono(32, y + 28, 100, cyan(f"/0{i + 1}"), fs=12, mobile={"x": 28, "y": my + 20, "w": 100, "fs": 11})
        b.text(32, y + 54, 620, q, fs=22, lh=1.3, fw=600, layer="q", mobile={"x": 28, "y": my + 44, "w": 424, "fs": 18})
        myth = b.button(700, y + 32, 140, 48, "Миф", primary=False, layer="btn-myth",
                        mobile={"x": 28, "y": my + 140, "w": 130, "h": 46})
        fact = b.button(860, y + 32, 140, 48, "Факт", primary=False, layer="btn-fact",
                        mobile={"x": 172, "y": my + 140, "w": 130, "h": 46})
        right_btn, wrong_btn = (myth, fact) if answer == "myth" else (fact, myth)
        verdict = "ЭТО МИФ" if answer == "myth" else "ЭТО ФАКТ"
        for ok, btn in ((False, wrong_btn), (True, right_btn)):
            anim = Block.sbs("click", reveal, loop="once", triggers=[btn["elem_id"]])
            b.shape(700 + off, y + 96, 440, 100, bg=PANEL, border=OK if ok else WARN, radius=12,
                    layer="v-right" if ok else "v-wrong",
                    mobile={"x": 28 + off, "y": my + 200, "w": 424, "h": 140, "steps": reveal}, **anim)
            head_txt = ("ВЕРНО · " if ok else "НЕ СОВСЕМ · ") + verdict
            b.text(718 + off, y + 108, 404, f'<span style="color: {OK if ok else WARN};">{head_txt}</span><br>{why}',
                   fs=13, lh=1.4, layer="verdict",
                   mobile={"x": 44 + off, "y": my + 212, "w": 392, "fs": 13, "steps": reveal}, **anim)
        my += 360 + 16
    b.mobile_height = my + 40
    return b


# --------------------------------------------------------------------------- ZB11 методология
NOTES = [
    "Google. Virtual try-on in Google Shopping, 14.06.2023", "i-D Magazine. What is digital clothing? (архив)",
    "РБК Стиль. Что такое виртуальная одежда… (архив)", "Железникова П. // vc.ru, 08.07.2020",
    "Williams M. Catty Taylor // Creative Review, 26.10.2020", "NowFashion. Virtual Fashion (архив)",
    "McDowell M. // Vogue Business, 04.04.2019", "The Fabricant. Iridescence", "Roberts-Islam B. // Forbes, 14.05.2019",
    "BBC News. The £7,500 dress that does not exist (архив)", "Roberts-Islam B. // Forbes, 21.08.2020",
    "DRESSX. О компании", "Meta. Meta Avatars Store, 20.06.2022", "Decentraland Q2 2024 Update",
    "Decentraland. MVFW 2025 Guide", "Decentraland. Wearables Contest, 28.04.2025",
    "Нисневич Л. // The Blueprint, 05.03.2020", "Replicant. Официальный сайт",
    "Russia Beyond. Digital clothes… (архив)", "Афиша Daily, 11.08.2021", "Sostav. «Калейдоскоп культур», 04.11.2022",
    "Feldmann A. et al. The Lockdown Effect // IMC’20", "DataReportal. Digital 2020: July",
    "Kotsoni E. // Vogue Business, 04.06.2024", "Skeldon P. // InternetRetailing, 10.08.2018",
    "Šajn N. // EPRS, 17.01.2019", "UNEP. Zero Waste Day 2025, 27.03.2025", "UNEP Annual Report 2025",
    "Atacac. How we design garments with CLO 3D", "Unspun. History", "Hermès v. Rothschild, S.D.N.Y., 23.06.2023",
    "WIRED. Kinect fitting-room for Topshop, май 2011", "Google Research. TryOnDiffusion, 2023",
    "Google. Virtual try-on tool, 20.05.2025", "Google try-on (SEJ), 24.07.2025", "Rincon L. // Google, 11.12.2025",
    "СберБизнес. ГигаЧат на МНМ, 16.03.2026", "Moscow Fashion Week, 30.03.2026", "Донских Н. // Business FM, 12.01.2021",
]


def zb11() -> Block:
    b = Block("ZB11", 1500, 3000)
    _, my = head(b, 80, "/09 · МЕТОДОЛОГИЯ", "Каждая цифра —<br>" + muted("с источником и датой."))
    my += 30
    steps = [("Источник", "Цитата и ссылка для проверки. Если страница исчезла — архивная копия. Ссылки сверены "
              "12.11.2026."),
             ("Утверждение", "Где, когда и на какой выборке получена цифра. Пример: 9 % — британская выборка, а не "
              "весь мир [25]."),
             ("Решение человека", "Оставить, сузить или исключить. «Подешевеет в 10 раз» мы оставили только как "
              "прогноз участников рынка 2021 года [39].")]
    for i, (title, body) in enumerate(steps):
        _, _, h, mh = b.panel_text(i * 400, 270, 380, [(cyan(f"/0{i + 1}"), "mono"), (title, "h3"), (body, "small")],
                                   pad=24, gap=10, min_h=210, mobile={"x": 10, "y": my, "w": 460}, layer=f"step{i + 1}",
                                   anim_panel=Block.basic("fadeinup", 0.7, 0.1 * i, 30))
        my += mh + 14
    ai = [(cyan("ИИ И ВИЗУАЛ"), "mono"), ("3D-платье и кадры турникета — условная реконструкция, сделанная кодом на "
          "Three.js по описанию Iridescence; это не модель The Fabricant. Тексты сверены с 39 источниками статьи, "
          "вывод нейросетей фактом не считается.", "body")]
    _, _, h, mh = b.panel_text(0, 510, 1160, ai, pad=24, gap=8, mobile={"x": 10, "y": my, "w": 460}, layer="ai",
                               anim_panel=Block.basic("fadeinup", 0.7, 0, 30))
    my += mh + 20
    b.button(0, 660, 260, 52, "3D-сцена ↗", VIEWER, layer="btn-3d", mobile={"x": 10, "y": my, "w": 220, "h": 48})
    b.button(276, 660, 300, 52, "Материалы проекта на GitHub ↗", REPO, primary=False, layer="btn-repo",
             mobile={"x": 10, "y": my + 60, "w": 300, "h": 48})
    my += 130
    b.mono(0, 760, 600, cyan("ИСТОЧНИКИ") + " · НУМЕРАЦИЯ ПРИМЕЧАНИЙ СТАТЬИ", fs=12,
           mobile={"x": 10, "y": my, "w": 460, "fs": 11})
    my += 30
    half = (len(NOTES) + 1) // 2
    cols = [NOTES[:half], NOTES[half:]]
    for c, col in enumerate(cols):
        start = 1 + c * half
        html = "<br>".join(f"{start + k}. {t}" for k, t in enumerate(col))
        b.text(c * 600, 795, 560, html, fs=13, lh=1.6, color=MUTED, layer=f"notes{c + 1}",
               mobile={"x": 10, "y": my, "w": 460, "fs": 12})
        my += estimate_height(html, 460, 12, 1.6) + 6
    b.mono(0, 1440, 1160, "НЕСУЩЕСТВУЮЩИЙ ГАРДЕРОБ · 2026 · ТЕКСТ ПО СТАТЬЕ РУВИКИ «ВИРТУАЛЬНАЯ ОДЕЖДА»", fs=11,
           mobile={"x": 10, "y": my + 20, "w": 460, "fs": 10})
    b.mobile_height = my + 70
    return b


BLOCKS = {"ZB01": zb01, "ZB02": zb02, "ZB03": zb03, "ZB04": zb04, "ZB05": zb05, "ZB06": zb06, "ZB07": zb07,
          "ZB08": zb08, "ZB09": zb09, "ZB10": zb10, "ZB11": zb11}


def main(keys: list[str]) -> None:
    OUT.mkdir(exist_ok=True)
    for key in keys or BLOCKS:
        block = BLOCKS[key]()
        code = block.to_code()
        path = OUT / f"{key}.json"
        path.write_text(json.dumps({"recordid": RECORDS[key], "code": code}, ensure_ascii=False), encoding="utf-8")
        print(key, RECORDS[key], len(block.elements), "elements", block.height, "/", block.mobile_height, "px")


if __name__ == "__main__":
    main(sys.argv[1:])
