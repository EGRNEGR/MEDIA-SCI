"""Минимальная модель Zero Block: элементы, адаптив и анимация в формате редактора Tilda.

Формат проверен по редактору Zero Block (13.11.2026):
- элементы — словари с полями elem_id, elem_type, top, left, width, height, zindex …;
- адаптив — те же поля с суффиксом «-res-<ширина>» (top-res-480, hidden-res-640);
- базовая анимация — animstyle, animduration, animdelay, animdistance, animtriggeroffset,
  animprx/animprxs/animprxdx/animprxdy, animfix/animfixdist/animfixtrgofst, animmobile;
- пошаговая — sbsevent (intoview|blockintoview|scroll|hover|click), sbstrg (0|0.5|1),
  sbstrgofst, sbsloop, sbstrgels (id через запятую) и sbsopts — JSON-список шагов
  с одинарными кавычками. Шаг скролла: mx, my, sx, sy, op, ro, di (px), dd, fi;
  шаг по времени: mx, my, sx, sy, op, ro, ti (мс), ea, dt (мс). Нулевой шаг — стартовое состояние.
"""

import json
import math
import re

SANS = "TildaSans"
MONO = "TildaSans"  # моноширинных шрифтов в библиотеке Free нет: телеметрия — TildaSans с разрядкой

CARBON = "#0b0d10"
PANEL = "#12151b"
HOVER = "#161a22"
LINE = "#1e2023"
LINE_PANEL = "#25282d"
LINE_ACTIVE = "#3a3d42"
SILVER = "#f4f6f9"
MUTED = "#7a828e"
CYAN = "#38bdf8"
OK = "#22c55e"
WARN = "#f59e0b"

DESKTOP_SCALE_960 = 0.8
MOBILE_BASE = 480
MOBILE_SCREENS = {640: (1.0, 80), 480: (1.0, 0), 320: (2 / 3, 0)}

_id_seed = [1794600000000]


def new_id() -> str:
    _id_seed[0] += 7
    return str(_id_seed[0])


def muted(text: str) -> str:
    return f'<span style="color: {MUTED};">{text}</span>'


def cyan(text: str) -> str:
    return f'<span style="color: {CYAN};">{text}</span>'


def bold(text: str) -> str:
    return f"<strong>{text}</strong>"


def estimate_height(text: str, width: float, fontsize: float, lineheight: float, char_k: float = 0.6) -> int:
    """Грубая оценка высоты текста: важна только для раскладки соседних слоёв."""
    plain = re.sub(r"<br\s*/?>", "\n", text)
    plain = re.sub(r"<[^>]+>", "", plain)
    per_line = max(1, int(width / (fontsize * char_k)))
    lines = sum(max(1, math.ceil(len(chunk) / per_line)) for chunk in plain.split("\n"))
    return int(math.ceil(lines * fontsize * lineheight))


def steps_json(steps: list[dict]) -> str:
    return json.dumps(steps, ensure_ascii=False).replace('"', "'")


def scroll_step(di=0, mx=0, my=0, sc=1, op=1, ro=0, fi=0) -> dict:
    return {"mx": str(round(mx)), "my": str(round(my)), "sx": str(sc), "sy": str(sc), "op": str(op),
            "ro": str(ro), "di": str(round(di)), "dd": "0", "fi": str(fi)}


def time_step(ti=0, mx=0, my=0, sc=1, op=1, ro=0, ea="", dt=0) -> dict:
    return {"mx": str(round(mx)), "my": str(round(my)), "sx": str(sc), "sy": str(sc), "op": str(op),
            "ro": str(ro), "ti": str(round(ti)), "ea": ea or "0", "dt": str(round(dt))}


def scale_steps(steps: list[dict], k: float) -> list[dict]:
    out = []
    for s in steps:
        t = dict(s)
        for key in ("mx", "my", "di"):
            if key in t:
                t[key] = str(round(float(t[key]) * k))
        out.append(t)
    return out


class Block:
    def __init__(self, key: str, height: int, mobile_height: int, bg: str = CARBON):
        self.key = key
        self.height = height
        self.mobile_height = mobile_height
        self.bg = bg
        self.elements: list[dict] = []

    # --- базовые конструкторы -------------------------------------------------
    def _base(self, etype: str, x, y, w, h, layer: str, mobile=None, desktop=True, **fields) -> dict:
        el = {
            "elem_id": new_id(), "elem_type": etype, "layer": layer,
            "top": str(round(y)), "left": str(round(x)), "width": str(round(w)), "height": str(round(h)),
            "topunits": "px", "leftunits": "px", "widthunits": "px", "heightunits": "px",
            "container": "grid", "axisx": "left", "axisy": "top",
            "zindex": len(self.elements) + 1, "hidden": "n" if desktop else "y",
        }
        el.update({k: v for k, v in fields.items() if v is not None})
        el["_mobile"] = mobile  # dict(x, y, w, h, fs?) или "hide"
        self.elements.append(el)
        return el

    def text(self, x, y, w, html, fs=18, lh=1.55, fw=400, color=SILVER, font=SANS, ls=0, align=None,
             layer="text", mobile=None, desktop=True, opacity=None, **anim) -> dict:
        html = re.sub(r"(\d) (\d{3})", r"\1&nbsp;\2", html)
        h = estimate_height(html, w, fs, lh)
        return self._base("text", x, y, w, h, layer, mobile, desktop, text=html, fontsize=str(fs),
                          lineheight=str(lh), fontweight=str(fw), color=color, fontfamily=font,
                          letterspacing=str(ls), textfit="autoheight", align=align,
                          opacity=None if opacity is None else str(opacity), **anim)

    def mono(self, x, y, w, html, fs=13, color=MUTED, layer="mono", mobile=None, desktop=True, **anim) -> dict:
        return self.text(x, y, w, html, fs=fs, lh=1.45, fw=500, color=color, font=MONO, ls=1.2,
                         layer=layer, mobile=mobile, desktop=desktop, **anim)

    def shape(self, x, y, w, h, bg=PANEL, border=None, radius=0, layer="shape", mobile=None, desktop=True,
              opacity=None, **anim) -> dict:
        extra = {}
        if border:
            extra.update(borderwidth="1", bordercolor=border, borderstyle="solid")
        return self._base("shape", x, y, w, h, layer, mobile, desktop, figure="rectangle", bgcolor=bg,
                          borderradius=f"{radius}px {radius}px {radius}px {radius}px",
                          opacity=None if opacity is None else str(opacity), **extra, **anim)

    def image(self, x, y, w, h, src, layer="image", mobile=None, desktop=True, **anim) -> dict:
        return self._base("image", x, y, w, h, layer, mobile, desktop, img=src, imagefit="cover",
                          imageposition="center center", filewidth=str(round(w * 2)), fileheight=str(round(h * 2)),
                          lazyoff="y", **anim)

    def button(self, x, y, w, h, caption, link="", primary=True, layer="button", mobile=None, desktop=True,
               target="_blank", **anim) -> dict:
        style = dict(bgcolor=CYAN, color=CARBON) if primary else dict(bgcolor="", color=SILVER, borderwidth="1",
                                                                         bordercolor=LINE_ACTIVE, borderstyle="solid")
        return self._base("button", x, y, w, h, layer, mobile, desktop, caption=caption, link=link or None,
                          linktarget=target if link and link.startswith("http") else None,
                          fontsize="15", fontweight="600", fontfamily=SANS, lineheight="1.55", letterspacing="0",
                          borderradius=f"{h // 2} {h // 2} {h // 2} {h // 2}", speedhover="0.2", **style, **anim)

    def panel_text(self, x, y, w, html_list, pad=24, gap=10, mobile=None, border=LINE_PANEL, layer="card",
                   anim_panel=None, anim_text=None, desktop=True, min_h=0):
        """Карточка: подложка + стопка текстов. html_list: [(html, kind)], kind in h3|body|small|mono|metric."""
        kinds = {"h3": (24, 1.25, 600, SILVER, SANS), "body": (17, 1.5, 400, SILVER, SANS),
                 "small": (15, 1.45, 400, MUTED, SANS), "mono": (12, 1.45, 500, MUTED, MONO),
                 "metric": (40, 1.1, 600, SILVER, MONO), "warn": (12, 1.45, 600, WARN, MONO),
                 "ok": (12, 1.45, 600, OK, MONO)}
        mkinds = {"h3": 19, "body": 15, "small": 14, "mono": 11, "metric": 30, "warn": 11, "ok": 11}
        inner_w = w - 2 * pad
        cy = y + pad
        items = []
        for html, kind in html_list:
            fs, lh, fw, color, font = kinds[kind]
            items.append((html, kind, fs, lh, fw, color, font, cy))
            cy += estimate_height(html, inner_w, fs, lh) + gap
        h = max(min_h, cy - gap + pad - y)
        mob_panel = mob_items = None
        if isinstance(mobile, dict):
            mw = mobile["w"]
            mi_w = mw - 2 * 18
            my_ = mobile["y"] + 18
            mob_items = []
            for html, kind, *_ in items:
                mfs = mkinds[kind]
                lh = kinds[kind][1]
                mob_items.append({"x": mobile["x"] + 18, "y": my_, "w": mi_w, "fs": mfs})
                my_ += estimate_height(html, mi_w, mfs, lh) + 8
            mob_panel = {"x": mobile["x"], "y": mobile["y"], "w": mw, "h": my_ - 8 + 18 - mobile["y"]}
        elif mobile == "hide":
            mob_panel = "hide"
        panel = self.shape(x, y, w, h, bg=PANEL, border=border, radius=16, layer=f"{layer}_panel",
                           mobile=mob_panel, desktop=desktop, **(anim_panel or {}))
        texts = []
        for i, (html, kind, fs, lh, fw, color, font, ty) in enumerate(items):
            m = mob_items[i] if mob_items else ("hide" if mobile == "hide" else None)
            anim = dict(anim_text or anim_panel or {})
            # смещение триггера считается от собственного Y слоя: текст ниже подложки на (ty - y)
            for key in ("animfixtrgofst", "sbstrgofst"):
                if key in anim:
                    anim[key] = str(round(float(anim[key]) + ty - y))
            t = self.text(x + pad, ty, inner_w, html, fs=fs, lh=lh, fw=fw, color=color, font=font,
                          ls=1.2 if font == MONO and kind != "metric" else 0, layer=f"{layer}_{kind}", mobile=m,
                          desktop=desktop, **anim)
            texts.append(t)
        return panel, texts, h, (mob_panel["h"] if isinstance(mob_panel, dict) else 0)

    # --- анимация ------------------------------------------------------------
    @staticmethod
    def basic(style="fadeinup", duration=0.8, delay=0, distance=40, offset=0, mobile=True) -> dict:
        return {"animstyle": style, "animduration": str(duration), "animdelay": str(delay),
                "animdistance": str(distance), "animtriggeroffset": str(offset), "animmobile": "y" if mobile else ""}

    @staticmethod
    def parallax_scroll(speed=70) -> dict:
        return {"animprx": "scroll", "animprxs": str(speed)}

    @staticmethod
    def parallax_mouse(dx=20, dy=12) -> dict:
        return {"animprx": "mouse", "animprxdx": str(dx), "animprxdy": str(dy)}

    @staticmethod
    def fixing(offset, distance, area="0") -> dict:
        return {"animfix": area, "animfixtrgofst": str(round(offset)), "animfixdist": str(round(distance))}

    @staticmethod
    def sbs(event, steps, trg="0", offset=0, loop="", triggers=None) -> dict:
        d = {"sbsevent": event, "sbsopts": steps_json(steps), "sbsloop": loop}
        if event in ("scroll", "intoview", "blockintoview"):
            d.update(sbstrg=trg, sbstrgofst=str(round(offset)))
        if triggers:
            d["sbstrgels"] = ",".join(triggers)
        d["_steps"] = steps
        return d

    # --- сборка JSON ---------------------------------------------------------
    def to_code(self) -> dict:
        code = {}
        for i, el in enumerate(self.elements):
            e = {k: v for k, v in el.items() if not k.startswith("_")}
            steps = el.get("_steps")
            mobile = el.get("_mobile")
            # 960: пропорциональное уменьшение десктопа
            k = DESKTOP_SCALE_960
            for f in ("top", "left", "width", "height"):
                e[f"{f}-res-960"] = str(round(float(el[f]) * k))
            if "fontsize" in el:
                e["fontsize-res-960"] = str(max(10, round(float(el["fontsize"]) * k)))
            if steps:
                e["sbsopts-res-960"] = steps_json(scale_steps(steps, k))
            if "sbstrgofst" in el:
                e["sbstrgofst-res-960"] = str(round(float(el["sbstrgofst"]) * k))
            if "animfixdist" in el:
                e["animfixdist-res-960"] = str(round(float(el["animfixdist"]) * k))
                e["animfixtrgofst-res-960"] = str(round(float(el["animfixtrgofst"]) * k))
            # мобильные экраны
            if mobile == "hide":
                e["hidden-res-640"] = "y"
            elif isinstance(mobile, dict):
                for bp, (s, dx) in MOBILE_SCREENS.items():
                    e[f"top-res-{bp}"] = str(round(mobile["y"] * s))
                    e[f"left-res-{bp}"] = str(round(mobile["x"] * s + dx))
                    e[f"width-res-{bp}"] = str(round(mobile["w"] * s))
                    if "h" in mobile:
                        e[f"height-res-{bp}"] = str(round(mobile["h"] * s))
                    if "fs" in mobile:
                        e[f"fontsize-res-{bp}"] = str(max(10, round(mobile["fs"] * s)))
                    if mobile.get("steps") is not None:
                        e[f"sbsopts-res-{bp}"] = steps_json(scale_steps(mobile["steps"], s))
                if el["hidden"] == "y":
                    e["hidden-res-640"] = "n"
            code[str(i)] = e
        code.update({
            "groups": [],
            "ab_height": str(self.height),
            "ab_height-res-960": str(round(self.height * DESKTOP_SCALE_960)),
            "ab_height-res-640": str(self.mobile_height),
            "ab_height-res-480": str(self.mobile_height),
            "ab_height-res-320": str(round(self.mobile_height * 2 / 3)),
            "ab_bgcolor": self.bg,
            "ab_filteropacity": "0.5", "ab_filteropacity2": "0.5",
            "ab_bgattachment": "scroll", "ab_bgposition": "center center",
            "ab_valign": "center", "ab_upscale": "grid", "ab_ovrflw": "hidden",
            "ab_screens": "320,480,640,960,1200",
            "meta": {"feeds": {"version": "1", "render": {}},
                     "migrations": {"elements": {"form": 3, "feeds-tile": 1}, "artboard": {"screens": 1}}},
        })
        return code
