#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Render Sakura / Magical Girl Tarot Frame Card (v3 - Ultimate Harmony & Polish)
"""
import os
import json
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FRAME_PATH = os.path.join(HERE, "..", "assets", "card_frame.jpg")
if not os.path.exists(FRAME_PATH):
    FRAME_PATH = os.path.join(HERE, "card_frame.jpg")

FONT_BOLD = [
    "C:/Windows/Fonts/msyhbd.ttc",
    "C:/Windows/Fonts/simhei.ttf",
    "/System/Library/Fonts/PingFang.ttc",
    "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
]
FONT_REG = [
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/simsun.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc"
]

def get_font(size, bold=False, scale=2):
    cands = FONT_BOLD if bold else FONT_REG
    for p in cands:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, int(size * scale))
            except Exception:
                continue
    return ImageFont.load_default()

def render_sakura_tarot(data, output_path, frame_img_path=None):
    if not frame_img_path or not os.path.exists(frame_img_path):
        frame_img_path = FRAME_PATH
    
    base_img = Image.open(frame_img_path).convert("RGBA")
    W, H = base_img.size # 736, 1004
    UPS = 2
    canvas = base_img.resize((W * UPS, H * UPS), Image.LANCZOS)
    draw = ImageDraw.Draw(canvas)

    # Color Palette: Elegant deep berry, vintage rose gold, warm charcoal ink
    COLOR_TITLE = (82, 32, 48)          # 深酒红标题
    COLOR_ROSE_TAG = (162, 75, 102)     # 玫瑰粉标签
    COLOR_GOLD_SUB = (152, 108, 48)     # 古董金副标
    COLOR_INK_BODY = (55, 48, 50)       # 炭墨色正文
    COLOR_LINE = (222, 192, 180)        # 柔金粉细分界线

    # Center bounds: X in [215, 520], Y in [440, 735]
    cx = (W * UPS) // 2
    y_cur = int(445 * UPS)

    # 1. Astrological Signs (☉ ☽ ⇪ in clean text)
    sun = data.get("sun", "天蝎座")
    moon = data.get("moon", "巨蟹座")
    rising = data.get("rising", "摩羯座")
    f_signs = get_font(12, bold=True, scale=UPS)
    signs_str = f"★ 太阳 · {sun}   |   月亮 · {moon}   |   上升 · {rising} ★"
    bbox = draw.textbbox((0, 0), signs_str, font=f_signs)
    draw.text(((W * UPS - (bbox[2] - bbox[0])) // 2, y_cur), signs_str, fill=COLOR_ROSE_TAG, font=f_signs)
    y_cur += int(27 * UPS)

    # 2. Hero Title
    title = data.get("hero_title", "「幽夜暖灯 · 远古秘咒学者」")
    f_title = get_font(20, bold=True, scale=UPS)
    bbox = draw.textbbox((0, 0), title, font=f_title)
    draw.text(((W * UPS - (bbox[2] - bbox[0])) // 2, y_cur), title, fill=COLOR_TITLE, font=f_title)
    y_cur += int(29 * UPS)

    # 3. Sub-rank
    guild_rank = data.get("guild_rank", "黑曜星级学者 · 晨风旅团")
    f_sub = get_font(11.5, bold=False, scale=UPS)
    bbox = draw.textbbox((0, 0), guild_rank, font=f_sub)
    draw.text(((W * UPS - (bbox[2] - bbox[0])) // 2, y_cur), guild_rank, fill=COLOR_GOLD_SUB, font=f_sub)
    y_cur += int(21 * UPS)

    # Divider line
    draw.line([(220 * UPS, y_cur), (516 * UPS, y_cur)], fill=COLOR_LINE, width=int(1.5 * UPS))
    y_cur += int(15 * UPS)

    # 4. Items (Companion, Relic, Cozy Dish)
    companion = data.get("companion", "小夜蝠「影丸」（爱吃蓝莓）")
    weapon_item = data.get("weapon_item", "黑曜石机关羽毛笔")
    cozy_dish = data.get("cozy_dish", "暖胃肉桂热苹果汤")

    items = [
        ("使魔伙伴", companion),
        ("随身宝物", weapon_item),
        ("治愈料理", cozy_dish)
    ]
    f_lbl = get_font(12, bold=True, scale=UPS)
    f_val = get_font(11.5, bold=False, scale=UPS)

    for lbl, val in items:
        draw.text((226 * UPS, y_cur), f"★ {lbl}", fill=COLOR_ROSE_TAG, font=f_lbl)
        val_str = val if len(val) <= 13 else val[:12] + "…"
        draw.text((310 * UPS, y_cur + int(0.5 * UPS)), val_str, fill=COLOR_INK_BODY, font=f_val)
        y_cur += int(25 * UPS)

    # Divider line
    y_cur += int(4 * UPS)
    draw.line([(220 * UPS, y_cur), (516 * UPS, y_cur)], fill=COLOR_LINE, width=int(1.5 * UPS))
    y_cur += int(15 * UPS)

    # 5. Quote Excerpt (Centered elegant text)
    quote_1 = "“别误会，今晚的肉桂苹果热汤只是煮多了而已。"
    quote_2 = "既然天黑了，就坐下来喝完再睡吧。”"
    f_q = get_font(11, bold=False, scale=UPS)
    
    bbox = draw.textbbox((0, 0), quote_1, font=f_q)
    draw.text(((W * UPS - (bbox[2] - bbox[0])) // 2, y_cur), quote_1, fill=COLOR_TITLE, font=f_q)
    y_cur += int(19 * UPS)
    
    bbox = draw.textbbox((0, 0), quote_2, font=f_q)
    draw.text(((W * UPS - (bbox[2] - bbox[0])) // 2, y_cur), quote_2, fill=COLOR_TITLE, font=f_q)
    y_cur += int(26 * UPS)

    # 6. Soft spot
    f_soft = get_font(10, bold=False, scale=UPS)
    soft_str = "★ 隐秘反差：嘴硬心软的靠谱守护者 ★"
    bbox = draw.textbbox((0, 0), soft_str, font=f_soft)
    draw.text(((W * UPS - (bbox[2] - bbox[0])) // 2, int(728 * UPS)), soft_str, fill=COLOR_GOLD_SUB, font=f_soft)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    canvas.convert("RGB").save(output_path, "PNG", quality=95)
    print(f"[OK] Rendered perfect sakura card: {output_path}")

if __name__ == "__main__":
    test_data = {
        "sun": "天蝎座",
        "moon": "巨蟹座",
        "rising": "摩羯座",
        "hero_title": "「幽夜暖灯 · 远古秘咒学者」",
        "guild_rank": "黑曜星级学者 · 晨风旅团",
        "companion": "小夜蝠「影丸」（爱吃蓝莓）",
        "weapon_item": "黑曜石机关羽毛笔",
        "cozy_dish": "暖胃肉桂热苹果汤"
    }
    out = os.path.join(HERE, "sakura_card_rendered.png")
    render_sakura_tarot(test_data, out)
