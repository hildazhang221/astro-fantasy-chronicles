#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Astro-Fantasy Share Card Renderer (Japanese Light Novel / Healing Adventurer's Star License Edition)
Generates an ultra-aesthetic 1080x1440 card for Xiaohongshu / social sharing.
"""

import sys
import os
import json
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1440

# Color Palette: Warm Twilight + Soft Starry Glow + Cozy Cream + Amber Gold
BG_TOP = (18, 20, 38)
BG_BOTTOM = (32, 28, 52)
ACCENT_GOLD = (245, 205, 130)
ACCENT_PEACH = (255, 175, 145)
ACCENT_CYAN = (120, 220, 240)
ACCENT_MINT = (150, 230, 200)

CARD_BG = (28, 30, 56, 230)
INNER_BOX_BG = (20, 22, 42, 210)
BORDER_GOLD = (230, 190, 120, 190)
BORDER_SOFT = (75, 80, 120)
DIVIDER = (65, 70, 105)

TEXT_TITLE = (255, 240, 205)
TEXT_MAIN = (245, 245, 252)
TEXT_MUTED = (180, 185, 210)
TEXT_SUB = (145, 150, 180)

FONT_CANDS_REG = [
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/simhei.ttf",
    "C:/Windows/Fonts/simsun.ttc",
    "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
    "/System/Library/Fonts/PingFang.ttc"
]
FONT_CANDS_BOLD = [
    "C:/Windows/Fonts/msyhbd.ttc",
    "C:/Windows/Fonts/simhei.ttf",
    "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc",
    "/System/Library/Fonts/PingFang.ttc"
]

def get_font(bold=False, size=24):
    cands = FONT_CANDS_BOLD if bold else FONT_CANDS_REG
    for path in cands:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()

def draw_diamond(draw, cx, cy, radius, fill):
    points = [
        (cx, cy - radius),
        (cx + radius, cy),
        (cx, cy + radius),
        (cx - radius, cy)
    ]
    draw.polygon(points, fill=fill)

def draw_star(draw, cx, cy, r_out, r_in, fill):
    points = []
    for i in range(8):
        r = r_out if i % 2 == 0 else r_in
        angle = i * (math.pi / 4) - (math.pi / 2)
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(points, fill=fill)

def draw_gradient_background(draw):
    for y in range(H):
        ratio = y / float(H)
        r = int(BG_TOP[0] * (1 - ratio) + BG_BOTTOM[0] * ratio)
        g = int(BG_TOP[1] * (1 - ratio) + BG_BOTTOM[1] * ratio)
        b = int(BG_TOP[2] * (1 - ratio) + BG_BOTTOM[2] * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

def draw_cozy_celestial_decor(draw):
    cx, cy = W // 2, 400
    radius = 320
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], outline=(45, 48, 78), width=1)
    draw.ellipse([cx - radius + 20, cy - radius + 20, cx + radius - 20, cy + radius - 20], outline=(38, 40, 68), width=1)
    
    for i in range(12):
        angle = i * (2 * math.pi / 12)
        x = cx + int((radius - 10) * math.cos(angle))
        y = cy + int((radius - 10) * math.sin(angle))
        draw_diamond(draw, x, y, 4, (120, 110, 150))

def draw_wrapped_text(draw, text, font, color, x, y, max_width, line_spacing=10):
    lines = []
    paragraphs = text.split("\n")
    for para in paragraphs:
        # replace unrenderable glyphs safely
        clean_para = para.replace("✦", "★").replace("■", "●")
        cur = ""
        for char in clean_para:
            test_line = cur + char
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] > max_width:
                lines.append(cur)
                cur = char
            else:
                cur = test_line
        if cur:
            lines.append(cur)
    
    cur_y = y
    for line in lines:
        draw.text((x, cur_y), line, fill=color, font=font)
        bbox = draw.textbbox((0, 0), line, font=font)
        line_height = bbox[3] - bbox[1]
        cur_y += line_height + line_spacing
    return cur_y

def render_healing_card(data, output_path):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)
    
    # 1. Background
    draw_gradient_background(draw)
    draw_cozy_celestial_decor(draw)
    
    # 2. Main Outer Ornate Border
    margin = 38
    draw.rectangle([margin, margin, W - margin, H - margin], outline=BORDER_GOLD, width=2)
    draw.rectangle([margin + 6, margin + 6, W - margin - 6, H - margin - 6], outline=BORDER_SOFT, width=1)
    
    # Corner 8-point stars
    for cx, cy in [(margin, margin), (W - margin, margin), (margin, H - margin), (W - margin, H - margin)]:
        draw_star(draw, cx, cy, 9, 4, ACCENT_GOLD)

    # 3. Header: Guild License Badge
    font_badge = get_font(bold=True, size=21)
    badge_text = "ADVENTURER'S STAR LICENSE · 冒险者星之执照"
    bbox = draw.textbbox((0, 0), badge_text, font=font_badge)
    bw = bbox[2] - bbox[0]
    bx = (W - bw) // 2
    by = 70
    draw_star(draw, bx - 24, by + 12, 6, 3, ACCENT_GOLD)
    draw.text((bx, by), badge_text, fill=ACCENT_GOLD, font=font_badge)
    draw_star(draw, bx + bw + 24, by + 12, 6, 3, ACCENT_GOLD)
    
    # Astrological Signs Banner
    font_signs = get_font(bold=True, size=23)
    sun_sign = data.get("sun", "处女座")
    moon_sign = data.get("moon", "金牛座")
    rising_sign = data.get("rising", "双鱼座")
    signs_text = f"太阳 · {sun_sign}    |    月亮 · {moon_sign}    |    上升 · {rising_sign}"
    bbox = draw.textbbox((0, 0), signs_text, font=font_signs)
    draw.text(((W - (bbox[2] - bbox[0])) // 2, 115), signs_text, fill=ACCENT_CYAN, font=font_signs)
    
    # Divider
    draw.line([(120, 162), (W - 120, 162)], fill=DIVIDER, width=1)
    draw_diamond(draw, W // 2, 162, 5, ACCENT_PEACH)
    
    # 4. Hero Title & Class Box
    font_title = get_font(bold=True, size=46)
    hero_title = data.get("hero_title", "「晨露微光 · 暖雾草药师」")
    bbox = draw.textbbox((0, 0), hero_title, font=font_title)
    draw.text(((W - (bbox[2] - bbox[0])) // 2, 190), hero_title, fill=TEXT_TITLE, font=font_title)
    
    # Guild Rank & Affiliation
    font_sub = get_font(bold=False, size=21)
    guild_rank = data.get("guild_rank", "公会评级：秘银级学者 · 遗迹解读者")
    vibe_tag = data.get("vibe_tag", "所属阵营：微风旅团 · 自由探索者")
    sub_text = f"{guild_rank}   ·   {vibe_tag}"
    bbox = draw.textbbox((0, 0), sub_text, font=font_sub)
    draw.text(((W - (bbox[2] - bbox[0])) // 2, 260), sub_text, fill=TEXT_MUTED, font=font_sub)

    # 5. Cozy Travel Journal Box (旅途笔记 · 某日的晴空)
    box_x1, box_y1 = 75, 315
    box_x2, box_y2 = W - 75, 685
    
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    ov_draw.rounded_rectangle([box_x1, box_y1, box_x2, box_y2], radius=16, fill=INNER_BOX_BG, outline=BORDER_GOLD, width=1)
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)
    
    # Journal Header Tag
    font_tag = get_font(bold=True, size=20)
    tag_str = "【 旅 途 笔 记 · 某 日 的 晴 空 】"
    bbox = draw.textbbox((0, 0), tag_str, font=font_tag)
    draw.text(((W - (bbox[2] - bbox[0])) // 2, box_y1 + 24), tag_str, fill=ACCENT_GOLD, font=font_tag)
    
    # Novel Excerpt Content
    font_story = get_font(bold=False, size=22)
    story_excerpt = data.get("story_excerpt", 
        "“穿过晨雾弥漫的金雀花原野，微风里送来刚烤熟面包的焦香与薄荷气息。\n"
        "毛茸茸的小星灵狐正把脑袋埋在我的斗篷兜帽里打呼噜。\n"
        "翻开满是草药标本的旅行笔记，旅伴们正围在林间木桌旁分享温热的花草茶。\n"
        "哪怕只是为了这样平凡又温暖的晨光，今天的启程也充满了让人期待的奇迹呢。”"
    )
    draw_wrapped_text(draw, story_excerpt, font_story, TEXT_MAIN, box_x1 + 36, box_y1 + 75, max_width=(box_x2 - box_x1 - 72), line_spacing=12)

    # 6. Companions & Items Section (3 Columns)
    items_y = 718
    font_sec = get_font(bold=True, size=22)
    draw_diamond(draw, 88, items_y + 11, 4, ACCENT_GOLD)
    draw.text((102, items_y), "星之羁绊与随身宝物", fill=ACCENT_GOLD, font=font_sec)
    draw.line([(75, items_y + 35), (W - 75, items_y + 35)], fill=DIVIDER, width=1)
    
    item_cards = [
        ("【本命使魔伙伴】", data.get("companion", "懂得翻书的羽毛夜莺「墨墨」"), ACCENT_PEACH),
        ("【随身法杖/宝物】", data.get("weapon_item", "黄铜齿轮星轨刻度尺兼羽毛笔"), ACCENT_CYAN),
        ("【治愈幸运料理】", data.get("cozy_dish", "温热洋甘菊金桔茶配黄油曲奇"), ACCENT_MINT)
    ]
    
    col_w = (W - 150) // 3
    for idx, (ititle, idesc, icolor) in enumerate(item_cards):
        cx = 75 + idx * col_w
        font_ititle = get_font(bold=True, size=19)
        font_idesc = get_font(bold=False, size=18)
        draw.text((cx + 10, items_y + 55), ititle, fill=icolor, font=font_ititle)
        draw_wrapped_text(draw, idesc, font_idesc, TEXT_MAIN, cx + 10, items_y + 88, max_width=col_w - 20, line_spacing=8)

    # 7. Personality Vibe & Hidden Soft Spot
    vibe_y = 890
    draw_diamond(draw, 88, vibe_y + 11, 4, ACCENT_GOLD)
    draw.text((102, vibe_y), "冒险者特质与隐秘反差萌", fill=ACCENT_GOLD, font=font_sec)
    draw.line([(75, vibe_y + 35), (W - 75, vibe_y + 35)], fill=DIVIDER, width=1)
    
    font_vibe = get_font(bold=False, size=21)
    vibe_desc = data.get("personality_vibe", 
        "★ 旅途风貌：背包永远收纳得井井有条，嘴上碎碎念其实比谁都体贴同伴。\n★ 隐秘反差萌：一个人在月下独处时，会偷偷在日记本的空白边缘画可爱的小猫涂鸦。"
    )
    draw_wrapped_text(draw, vibe_desc, font_vibe, TEXT_MUTED, 75, vibe_y + 55, max_width=W - 150, line_spacing=10)

    # 8. Footer
    draw.line([(75, H - 120), (W - 75, H - 120)], fill=DIVIDER, width=1)
    font_foot = get_font(bold=False, size=18)
    foot_left = "★ 独属星盘物语 · 愿你的旅途常有微风与星光相伴"
    foot_right = "ASTRO CHRONICLES"
    draw.text((75, H - 90), foot_left, fill=ACCENT_GOLD, font=font_foot)
    bbox = draw.textbbox((0, 0), foot_right, font=font_foot)
    draw.text((W - 75 - (bbox[2] - bbox[0]), H - 90), foot_right, fill=ACCENT_GOLD, font=font_foot)

    # Save
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.convert("RGB").save(output_path, "PNG", quality=95)
    print(f"[OK] Healing card generated successfully: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        out_file = sys.argv[2] if len(sys.argv) > 2 else "healing_astro_demo.png"
        sample_data = {
            "sun": "处女座",
            "moon": "金牛座",
            "rising": "双鱼座",
            "hero_title": "「晨露微光 · 暖雾草药师」",
            "guild_rank": "公会评级：秘银级学者 · 遗迹解读者",
            "vibe_tag": "所属阵营：微风旅团 · 自由探索者",
            "story_excerpt": "“穿过晨雾弥漫的金雀花原野，微风里送来刚烤熟面包的焦香与薄荷气息。\n毛茸茸的小星灵狐正把脑袋埋在我的斗篷兜帽里打呼噜。\n翻开满是草药标本的旅行笔记，旅伴们正围在林间木桌旁分享温热的花草茶。\n哪怕只是为了这样平凡又温暖的晨光，今天的启程也充满了让人期待的奇迹呢。”",
            "companion": "懂得翻书的羽毛夜莺「墨墨」",
            "weapon_item": "黄铜齿轮星轨刻度尺兼羽毛笔",
            "cozy_dish": "温热洋甘菊金桔茶配黄油曲奇",
            "personality_vibe": "★ 旅途风貌：背包永远收纳得井井有条，嘴上碎碎念其实比谁都体贴同伴。\n★ 隐秘反差萌：一个人在月下独处时，会偷偷在日记本的空白边缘画可爱的小猫涂鸦。"
        }
        render_healing_card(sample_data, out_file)
    elif len(sys.argv) > 2:
        json_file = sys.argv[1]
        out_file = sys.argv[2]
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        render_healing_card(data, out_file)
    else:
        print("Usage: py -3 render_card.py reading.json out.png  OR  py -3 render_card.py --demo out.png")
