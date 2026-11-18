#!/usr/bin/env python3
"""Generate deterministic SVG diagrams and a 3D Wikipedia-style typographic globe for Humanizer-zh-HK."""

from __future__ import annotations

import html
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT / "assets"

SERIF_FONT = (
    "'Songti TC', 'Noto Serif CJK HK', 'Source Han Serif TC', "
    "'PMingLiU', 'Hiragino Mincho ProN', Georgia, serif"
)
SANS_FONT = (
    "'PingFang HK', 'Noto Sans CJK HK', 'Heiti TC', "
    "'Microsoft JhengHei', -apple-system, BlinkMacSystemFont, sans-serif"
)
MONO_FONT = "'SFMono-Regular', Menlo, Monaco, Consolas, monospace"


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def rot_x(v: tuple[float, float, float], angle_rad: float) -> tuple[float, float, float]:
    x, y, z = v
    c, s = math.cos(angle_rad), math.sin(angle_rad)
    return (x, y * c - z * s, y * s + z * c)


def rot_z(v: tuple[float, float, float], angle_rad: float) -> tuple[float, float, float]:
    x, y, z = v
    c, s = math.cos(angle_rad), math.sin(angle_rad)
    return (x * c - y * s, x * s + y * c, z)


def transform_vec(
    v: tuple[float, float, float], tilt_x: float, tilt_z: float
) -> tuple[float, float, float]:
    return rot_z(rot_x(v, tilt_x), tilt_z)


def sphere_point(r: float, phi: float, lam: float) -> tuple[float, float, float]:
    return (
        r * math.cos(phi) * math.sin(lam),
        -r * math.sin(phi),
        r * math.cos(phi) * math.cos(lam),
    )


def project_point(
    p: tuple[float, float, float], cx: float, cy: float, cam_d: float
) -> tuple[float, float]:
    x, y, z = p
    s = cam_d / (cam_d - z)
    return (cx + x * s, cy + y * s)


def lerp_rgb(c1: tuple[int, int, int], c2: tuple[int, int, int], t: float) -> str:
    t = max(0.0, min(1.0, t))
    r = round(c1[0] + (c2[0] - c1[0]) * t)
    g = round(c1[1] + (c2[1] - c1[1]) * t)
    b = round(c1[2] + (c2[2] - c1[2]) * t)
    return f"#{r:02X}{g:02X}{b:02X}"


def build_hero_globe() -> str:
    w, h = 1200, 540
    cx, cy = 272.0, 278.0
    r = 180.0
    cam_d = 3.55 * r
    tilt_x = math.radians(17.0)
    tilt_z = math.radians(-10.0)
    limb_r = r * math.sqrt(cam_d**2 / (cam_d**2 - r**2))

    # Key light from upper-left-front
    lx, ly, lz = -0.40, -0.46, 0.79
    l_norm = math.sqrt(lx * lx + ly * ly + lz * lz)
    lx, ly, lz = lx / l_norm, ly / l_norm, lz / l_norm

    corpus = (
        "香港書面語實事求是刪繁就簡保留事實數據準確主謂分明"
        "按年上升服務質素軟件網絡項目預設透過渠道公帑按揭屋苑"
        "憑藉製造範圍農曆聯繫特徵佔比拒絕空話直陳重點新聞報告"
        "商業文書直角引號審慎克制清晰自然真憑實據去蕪存菁簡明"
    )

    lines: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
        "  <defs>",
        # Concave shaded interior of the hollow Wikipedia-style sphere
        '    <radialGradient id="hollowInterior" cx="46%" cy="40%" r="64%">',
        '      <stop offset="0%" stop-color="#D2CAB8"/>',
        '      <stop offset="55%" stop-color="#DFD8C8"/>',
        '      <stop offset="100%" stop-color="#ECE7DB"/>',
        "    </radialGradient>",
        '    <radialGradient id="floorShadow" cx="50%" cy="50%" r="50%">',
        '      <stop offset="0%" stop-color="#1E293B" stop-opacity="0.20"/>',
        '      <stop offset="65%" stop-color="#1E293B" stop-opacity="0.06"/>',
        '      <stop offset="100%" stop-color="#1E293B" stop-opacity="0"/>',
        "    </radialGradient>",
        '    <linearGradient id="accentPill" x1="0%" y1="0%" x2="100%" y2="0%">',
        '      <stop offset="0%" stop-color="#991B1B"/>',
        '      <stop offset="100%" stop-color="#B91C1C"/>',
        "    </linearGradient>",
        "  </defs>",
        # Outer card
        f'  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="20" fill="#FAF8F4" stroke="#E4DEC9" stroke-width="1.5"/>',
        # Soft shadow under globe
        f'  <ellipse cx="{cx:.1f}" cy="{cy + limb_r + 16:.1f}" rx="{limb_r * 0.78:.1f}" ry="16" fill="url(#floorShadow)"/>',
        # Hollow interior shell (visible through the open top crown)
        f'  <circle cx="{cx:.1f}" cy="{cy:.1f}" r="{limb_r:.1f}" fill="url(#hollowInterior)" stroke="#C6BDA9" stroke-width="1.2"/>',
    ]

    dphi_deg = 9.0
    lat_degs = list(range(-72, 73, 9))  # 17 latitude rings
    char_idx = 0

    def in_open_crown(phi_deg: float, lam_deg: float) -> bool:
        # Irregular Wikipedia-style stepped top-right cutout exposing the hollow interior
        if phi_deg >= 54:
            return True
        if phi_deg >= 45 and (-28 <= lam_deg <= 105):
            return True
        if phi_deg >= 36 and (-8 <= lam_deg <= 86):
            return True
        if phi_deg >= 27 and (14 <= lam_deg <= 64):
            return True
        return False

    back_tiles: list[tuple[float, str]] = []
    front_tiles: list[tuple[float, str]] = []

    for ring_i, phi_deg in enumerate(lat_degs):
        phi = math.radians(phi_deg)
        n_lon = max(8, round(40 * math.cos(phi)))
        dlam_deg = 360.0 / n_lon
        offset_deg = (ring_i % 2) * (dlam_deg * 0.5)

        for j in range(n_lon):
            lam_deg = -180.0 + j * dlam_deg + offset_deg
            # Normalize to [-180, 180)
            if lam_deg >= 180.0:
                lam_deg -= 360.0
            lam = math.radians(lam_deg)

            ch = corpus[char_idx % len(corpus)]
            char_idx += 1

            p0 = sphere_point(r, phi, lam)
            tu0 = (math.cos(lam), 0.0, -math.sin(lam))
            tv0 = (
                math.sin(phi) * math.sin(lam),
                math.cos(phi),
                math.sin(phi) * math.cos(lam),
            )

            p = transform_vec(p0, tilt_x, tilt_z)
            tu = transform_vec(tu0, tilt_x, tilt_z)
            tv = transform_vec(tv0, tilt_x, tilt_z)

            x, y, z = p
            nz = z / r

            # Exact 2D perspective Jacobian
            s = cam_d / (cam_d - z)
            sp = cam_d / ((cam_d - z) ** 2)
            a = s * tu[0] + x * sp * tu[2]
            b = s * tu[1] + y * sp * tu[2]
            c = s * tv[0] + x * sp * tv[2]
            d = s * tv[1] + y * sp * tv[2]
            tx, ty = cx + x * s, cy + y * s

            # Build slightly inset curved spherical quad polygon for each tile
            shrink = 0.94
            hp = math.radians(dphi_deg * 0.5 * shrink)
            hl = math.radians(dlam_deg * 0.5 * shrink)
            corners_angles = [
                (phi + hp, lam - hl),
                (phi + hp, lam),
                (phi + hp, lam + hl),
                (phi, lam + hl),
                (phi - hp, lam + hl),
                (phi - hp, lam),
                (phi - hp, lam - hl),
                (phi, lam - hl),
            ]
            pts = []
            for cp, cl in corners_angles:
                q = transform_vec(sphere_point(r, cp, cl), tilt_x, tilt_z)
                qx, qy = project_point(q, cx, cy, cam_d)
                pts.append(f"{qx:.1f},{qy:.1f}")
            poly_pts = " ".join(pts)

            if nz < -0.10:
                # Inside back-wall tiles visible mainly through the open crown
                tile_op = 0.28 if y < cy + 10 else 0.16
                glyph_op = 0.20 if y < cy + 10 else 0.10
                tile_svg = (
                    f'    <g opacity="{tile_op:.2f}">\n'
                    f'      <polygon points="{poly_pts}" fill="#CDC4B0" stroke="#B7AD98" stroke-width="0.6"/>\n'
                    f'      <g transform="matrix({a:.4f},{b:.4f},{c:.4f},{d:.4f},{tx:.2f},{ty:.2f})">'
                    f'<text x="0" y="0" text-anchor="middle" dominant-baseline="central" '
                    f'font-family="{esc(SERIF_FONT)}" font-size="18.2" font-weight="600" '
                    f'fill="#475569" opacity="{glyph_op:.2f}">{esc(ch)}</text></g>\n'
                    f"    </g>"
                )
                back_tiles.append((z, tile_svg))
            elif nz > 0.04:
                if in_open_crown(phi_deg, lam_deg):
                    continue
                nx, ny, nzu = x / r, y / r, z / r
                lit = max(0.0, nx * lx + ny * ly + nzu * lz)
                # Ivory tile shading from crisp white highlight to warm stone shadow
                tile_fill = lerp_rgb((223, 216, 200), (255, 254, 250), 0.18 + 0.82 * lit)
                edge_col = lerp_rgb((178, 169, 152), (212, 204, 188), lit)
                ink_col = lerp_rgb((71, 85, 105), (15, 23, 42), min(1.0, lit * 1.15))
                glyph_op = min(0.98, 0.25 + (nz - 0.04) * 1.35)
                tile_svg = (
                    f'    <g>\n'
                    f'      <polygon points="{poly_pts}" fill="{tile_fill}" stroke="{edge_col}" stroke-width="0.75"/>\n'
                    f'      <g transform="matrix({a:.4f},{b:.4f},{c:.4f},{d:.4f},{tx:.2f},{ty:.2f})">'
                    f'<text x="0" y="0" text-anchor="middle" dominant-baseline="central" '
                    f'font-family="{esc(SERIF_FONT)}" font-size="18.8" font-weight="700" '
                    f'fill="{ink_col}" opacity="{glyph_op:.3f}">{esc(ch)}</text></g>\n'
                    f"    </g>"
                )
                front_tiles.append((z, tile_svg))

    back_tiles.sort(key=lambda item: item[0])
    front_tiles.sort(key=lambda item: item[0])

    lines.append('  <g id="globe-back-interior">')
    lines.extend(item[1] for item in back_tiles)
    lines.append("  </g>")

    lines.append('  <g id="globe-front-shell">')
    lines.extend(item[1] for item in front_tiles)
    lines.append("  </g>")

    # Peeling AI-cliché puzzle chips drifting off the open upper-right crown
    peeling_chips = [
        (382, 72, -14, "✕ 賦能", 0.95),
        (446, 54, 10, "✕ 同比", 0.88),
        (438, 112, -7, "✕ 閉環", 0.92),
        (488, 88, 16, "✕ ——", 0.78),
        (460, 154, 6, "✕ 細想一下", 0.84),
    ]
    lines.append('  <g id="peeled-ai-tells">')
    for chip_x, chip_y, rot_deg, label, op in peeling_chips:
        chip_w = 24 + len(label) * 13
        lines.append(
            f'    <g transform="translate({chip_x},{chip_y}) rotate({rot_deg})" opacity="{op}">'
        )
        lines.append(
            f'      <rect x="0" y="0" width="{chip_w}" height="25" rx="6" fill="#FEF2F2" stroke="#FCA5A5" stroke-width="1.15"/>'
        )
        lines.append(
            f'      <text x="{chip_w / 2:.1f}" y="13" text-anchor="middle" dominant-baseline="central" '
            f'font-family="{esc(SANS_FONT)}" font-size="12" font-weight="700" fill="#B91C1C">{esc(label)}</text>'
        )
        lines.append("    </g>")
    lines.append("  </g>")

    # Right-side editorial hero copy (x >= 578, safely clear of globe & chips)
    rx = 578
    lines.extend(
        [
            '  <g id="hero-copy">',
            f'    <rect x="{rx}" y="76" width="272" height="28" rx="14" fill="url(#accentPill)"/>',
            f'    <text x="{rx + 136}" y="90.5" text-anchor="middle" dominant-baseline="central" '
            f'font-family="{esc(SANS_FONT)}" font-size="12" font-weight="700" letter-spacing="0.6" fill="#FFFFFF">'
            f'SIGNS OF AI WRITING · v4.0.0</text>',
            f'    <text x="{rx}" y="156" font-family="{esc(SERIF_FONT)}" font-size="48" font-weight="800" fill="#0F172A">Humanizer-zh-HK</text>',
            f'    <text x="{rx}" y="200" font-family="{esc(SANS_FONT)}" font-size="22" font-weight="700" fill="#1E293B">香港書面語去 AI 寫作痕跡技能</text>',
            f'    <line x1="{rx}" y1="224" x2="1150" y2="224" stroke="#E2DDD0" stroke-width="1.2"/>',
            f'    <text x="{rx}" y="260" font-family="{esc(SANS_FONT)}" font-size="16" fill="#334155">'
            f'基於 blader/humanizer v4.0.0，清除 28 種 AI 結構套路、</text>',
            f'    <text x="{rx}" y="288" font-family="{esc(SANS_FONT)}" font-size="16" fill="#334155">'
            f'內地黑話、兩岸詞錯置與簡轉繁錯字，還原地道港式書面語。</text>',
            f'    <text x="{rx}" y="318" font-family="{esc(SANS_FONT)}" font-size="15" font-weight="600" fill="#0F766E">'
            f'專注文章、商業報告與新聞稿 · 100% 保留原文事實與數字</text>',
        ]
    )

    stats = [
        (578, "28 種", "AI 寫作痕跡（A–G）", "#B91C1C", "#FEF2F2", "#FECACA"),
        (774, "港式書面語", "正字 · 詞彙 · 直角引號", "#0F766E", "#F0FDFA", "#99F6E4"),
        (970, "跨平台通用", "Claude / Codex / Antigravity", "#1D4ED8", "#EFF6FF", "#BFDBFE"),
    ]
    for sx, top_lbl, sub_lbl, accent, bg, bd in stats:
        lines.extend(
            [
                f'    <rect x="{sx}" y="362" width="180" height="84" rx="12" fill="{bg}" stroke="{bd}" stroke-width="1.2"/>',
                f'    <text x="{sx + 16}" y="394" font-family="{esc(SANS_FONT)}" font-size="21" font-weight="800" fill="{accent}">{esc(top_lbl)}</text>',
                f'    <text x="{sx + 16}" y="423" font-family="{esc(SANS_FONT)}" font-size="12.5" font-weight="600" fill="#334155">{esc(sub_lbl)}</text>',
            ]
        )

    lines.append("  </g>")
    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def build_before_after_demo() -> str:
    w, h = 1200, 466
    lines: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
        f'  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="18" fill="#FAF8F4" stroke="#E4DEC9" stroke-width="1.5"/>',
        f'  <text x="36" y="42" font-family="{esc(SANS_FONT)}" font-size="21" font-weight="800" fill="#0F172A">改寫效果對照：產品發佈公告</text>',
        f'  <text x="1164" y="42" text-anchor="end" font-family="{esc(SANS_FONT)}" font-size="13.5" font-weight="600" fill="#64748B">清除結構套路與非港式詞彙 · 字數精簡 34%</text>',
        # Left Before card
        '  <rect x="34" y="64" width="540" height="368" rx="14" fill="#FFFDFD" stroke="#FECACA" stroke-width="1.5"/>',
        '  <rect x="34" y="64" width="540" height="44" rx="14" fill="#FEF2F2"/>',
        '  <rect x="34" y="94" width="540" height="14" fill="#FEF2F2"/>',
        '  <line x1="34" y1="108" x2="574" y2="108" stroke="#FECACA" stroke-width="1"/>',
        f'  <text x="56" y="92" font-family="{esc(SANS_FONT)}" font-size="15.5" font-weight="700" fill="#991B1B">改寫前：AI 腔與外地詞彙混雜（7 處破綻）</text>',
    ]

    before_lines = [
        [("我們非常高興地宣佈，共享草稿今天正式上線了！🚀", "#B91C1C", "700")],
        [
            ("過去數月團隊一直淹沒在 final_v7.docx 的海洋中", "#334155", "400"),
            ("——", "#B91C1C", "700"),
        ],
        [
            ("我們深知必須改變。這", "#334155", "400"),
            ("不僅僅是一項功能，更是一場", "#B91C1C", "700"),
        ],
        [
            ("協作革新", "#B91C1C", "700"),
            ("，全方位", "#334155", "400"),
            ("賦能", "#B91C1C", "700"),
            ("團隊實現", "#334155", "400"),
            ("降本增效", "#B91C1C", "700"),
            ("，對同一份", "#334155", "400"),
        ],
        [
            ("檔案進行", "#B91C1C", "700"),
            ("實時編輯，批註精準錨定句子，採用率預計", "#334155", "400"),
        ],
        [
            ("同比", "#B91C1C", "700"),
            ("大幅提升。", "#334155", "400"),
            ("細想一下。", "#B91C1C", "700"),
        ],
    ]
    y0 = 142
    for idx, spans in enumerate(before_lines):
        y = y0 + idx * 30
        parts = [
            f'  <text x="56" y="{y}" font-family="{esc(SANS_FONT)}" font-size="15">'
        ]
        for txt, col, wt in spans:
            parts.append(f'<tspan fill="{col}" font-weight="{wt}">{esc(txt)}</tspan>')
        parts.append("</text>")
        lines.append("".join(parts))

    bad_pills = [
        (56, 336, 132, "§4/§20 鋪墊＋🚀"),
        (198, 336, 108, "§8 濫用破折號"),
        (316, 336, 130, "§1 不是X而是Y"),
        (56, 372, 146, "§12 賦能／降本增效"),
        (212, 372, 132, "§11 進行虛化動詞"),
        (354, 372, 136, "§27 同比 / §2 收尾"),
    ]
    for px, py, pw, plbl in bad_pills:
        lines.extend(
            [
                f'  <rect x="{px}" y="{py}" width="{pw}" height="26" rx="6" fill="#FEE2E2" stroke="#FCA5A5" stroke-width="1"/>',
                f'  <text x="{px + pw / 2:.1f}" y="{py + 13.5}" text-anchor="middle" dominant-baseline="central" '
                f'font-family="{esc(SANS_FONT)}" font-size="12" font-weight="600" fill="#991B1B">{esc(plbl)}</text>',
            ]
        )

    lines.extend(
        [
            '  <circle cx="600" cy="248" r="22" fill="#0F172A"/>',
            f'  <text x="600" y="249" text-anchor="middle" dominant-baseline="central" '
            f'font-family="{esc(SANS_FONT)}" font-size="20" font-weight="800" fill="#FFFFFF">→</text>',
        ]
    )

    lines.extend(
        [
            '  <rect x="626" y="64" width="540" height="368" rx="14" fill="#F8FCFA" stroke="#BBF7D0" stroke-width="1.5"/>',
            '  <rect x="626" y="64" width="540" height="44" rx="14" fill="#ECFDF5"/>',
            '  <rect x="626" y="94" width="540" height="14" fill="#ECFDF5"/>',
            '  <line x1="626" y1="108" x2="1166" y2="108" stroke="#BBF7D0" stroke-width="1"/>',
            f'  <text x="648" y="92" font-family="{esc(SANS_FONT)}" font-size="15.5" font-weight="700" fill="#065F46">改寫後：地道香港書面語（直接陳述事實）</text>',
        ]
    )

    after_lines = [
        "團隊共享草稿功能今日正式推出。",
        "過去數月，我們團隊內部仍靠傳閱 final_v7.docx",
        "一類檔案改稿，相當費時。現在兩人可同時編輯",
        "同一份文件，即時看見對方的修改；批註亦會緊貼",
        "所標示的句子，即使前後改動也不會移位。",
        "新功能即日起免費開放，預計使用率將按年顯著上升。",
    ]
    for idx, line in enumerate(after_lines):
        y = 144 + idx * 31
        lines.append(
            f'  <text x="648" y="{y}" font-family="{esc(SANS_FONT)}" font-size="15.5" font-weight="500" fill="#0F172A">{esc(line)}</text>'
        )

    good_pills = [
        (648, 336, 174, "✓ 保留全部具體事實與檔名"),
        (832, 336, 186, "✓ 「同比」轉為港式「按年」"),
        (648, 372, 198, "✓ 刪去破折號、黑話與感嘆句"),
        (856, 372, 184, "✓ 主謂清晰，句長自然交替"),
    ]
    for px, py, pw, plbl in good_pills:
        lines.extend(
            [
                f'  <rect x="{px}" y="{py}" width="{pw}" height="26" rx="6" fill="#DCFCE7" stroke="#86EFAC" stroke-width="1"/>',
                f'  <text x="{px + pw / 2:.1f}" y="{py + 13.5}" text-anchor="middle" dominant-baseline="central" '
                f'font-family="{esc(SANS_FONT)}" font-size="12" font-weight="600" fill="#065F46">{esc(plbl)}</text>',
            ]
        )

    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def build_pattern_taxonomy() -> str:
    w, h = 1200, 504
    lines: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
        f'  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="18" fill="#FAF8F4" stroke="#E4DEC9" stroke-width="1.5"/>',
        f'  <text x="36" y="42" font-family="{esc(SANS_FONT)}" font-size="21" font-weight="800" fill="#0F172A">28 種 AI 寫作痕跡分佈圖（七大類 × 觸發強度）</text>',
        '  <rect x="802" y="23" width="166" height="28" rx="14" fill="#FEE2E2" stroke="#FCA5A5" stroke-width="1"/>',
        f'  <text x="885" y="37.5" text-anchor="middle" dominant-baseline="central" font-family="{esc(SANS_FONT)}" font-size="12.5" font-weight="700" fill="#991B1B">紅標：見一次即改（12 種）</text>',
        '  <rect x="978" y="23" width="186" height="28" rx="14" fill="#FEF3C7" stroke="#FCD34D" stroke-width="1"/>',
        f'  <text x="1071" y="37.5" text-anchor="middle" dominant-baseline="central" font-family="{esc(SANS_FONT)}" font-size="12.5" font-weight="700" fill="#92400E">黃標：多見或按語境改（16 種）</text>',
        '  <line x1="36" y1="64" x2="1164" y2="64" stroke="#E4DEC9" stroke-width="1.2"/>',
    ]

    categories = [
        ("A", "鋪墊造勢，不直接陳述", "§1–§5", 5, "#DC2626", "#FEF2F2", "#FECACA",
         "不是X而是Y · 單句收尾 · 高深金句 · 鋪墊開場 · 與空氣爭辯", "見一次即改"),
        ("B", "按規則套節奏與句式", "§6–§11", 6, "#D97706", "#FFFBEB", "#FDE68A",
         "三連排比 · 重複主語 · 破折號濫用 · 限定詞 · 歐化被動／進行", "節奏與句法"),
        ("C", "誇大拔高與借用權威", "§12–§18", 7, "#EA580C", "#FFF7ED", "#FED7AA",
         "套話與黑話 · 里程碑拔高 · 意義尾巴 · 樓書腔 · 避用是有", "浮誇與套話"),
        ("D", "按規則套格式與標點", "§19–§21", 3, "#0284C7", "#F0F9FF", "#BAE6FD",
         "裝飾性粗體清單 · Emoji／箭頭標題 · 西式彎引號「“…” → 「…」」", "排版與標點"),
        ("E", "對話殘留與草稿痕跡", "§22–§25", 4, "#B91C1C", "#FEF2F2", "#FECACA",
         "聊天殘留（§22 直刪）· 知識截止揣測 · 首句重複標題 · 自述文件", "草稿與殘留"),
        ("F", "搞錯讀者對象", "§26", 1, "#4F46E5", "#EEF2FF", "#C7D2FE",
         "回覆知情讀者時重頭交代背景與排查過程（改為結論先行）", "回覆語境"),
        ("G", "非港式用詞與簡繁轉碼", "§27–§28", 2, "#0F766E", "#F0FDFA", "#99F6E4",
         "兩岸詞彙錯置（同比→按年、軟體→軟件）· 簡繁錯字（憑藉、範圍）", "港式專項必改"),
    ]

    start_y = 82
    row_h = 52
    row_gap = 7
    bar_x = 300
    max_bar_w = 154

    for i, (code, title, sec, cnt, color, bg, bd, summary, badge) in enumerate(categories):
        y = start_y + i * (row_h + row_gap)
        lines.append(
            f'  <rect x="36" y="{y}" width="1128" height="{row_h}" rx="10" fill="#FFFFFF" stroke="#E5E7EB" stroke-width="1"/>'
        )
        lines.append(
            f'  <rect x="48" y="{y + 10}" width="32" height="32" rx="8" fill="{bg}" stroke="{bd}" stroke-width="1.2"/>'
        )
        lines.append(
            f'  <text x="64" y="{y + 26.5}" text-anchor="middle" dominant-baseline="central" '
            f'font-family="{esc(SANS_FONT)}" font-size="15" font-weight="800" fill="{color}">{esc(code)}</text>'
        )
        lines.append(
            f'  <text x="92" y="{y + 21}" font-family="{esc(SANS_FONT)}" font-size="14.5" font-weight="700" fill="#0F172A">{esc(title)}</text>'
        )
        lines.append(
            f'  <text x="92" y="{y + 39}" font-family="{esc(MONO_FONT)}" font-size="11.5" font-weight="600" fill="#64748B">{esc(sec)} · {cnt} 項模式</text>'
        )

        bar_w = round((cnt / 7.0) * max_bar_w)
        lines.append(
            f'  <rect x="{bar_x}" y="{y + 16}" width="{max_bar_w}" height="20" rx="6" fill="#F1F5F9"/>'
        )
        lines.append(
            f'  <rect x="{bar_x}" y="{y + 16}" width="{bar_w}" height="20" rx="6" fill="{color}" opacity="0.88"/>'
        )
        lines.append(
            f'  <text x="{bar_x + max_bar_w + 12}" y="{y + 26.5}" dominant-baseline="central" '
            f'font-family="{esc(SANS_FONT)}" font-size="13" font-weight="700" fill="#334155">{cnt}</text>'
        )

        lines.append(
            f'  <text x="498" y="{y + 26.5}" dominant-baseline="central" '
            f'font-family="{esc(SANS_FONT)}" font-size="13" fill="#334155">{esc(summary)}</text>'
        )

        is_strong = badge in ("見一次即改", "港式專項必改")
        p_bg = "#FEE2E2" if is_strong else "#F8FAFC"
        p_bd = "#FCA5A5" if is_strong else "#CBD5E1"
        p_fg = "#991B1B" if is_strong else "#475569"
        lines.append(
            f'  <rect x="1048" y="{y + 13}" width="102" height="26" rx="13" fill="{p_bg}" stroke="{p_bd}" stroke-width="1"/>'
        )
        lines.append(
            f'  <text x="1099" y="{y + 26.5}" text-anchor="middle" dominant-baseline="central" '
            f'font-family="{esc(SANS_FONT)}" font-size="11.5" font-weight="700" fill="{p_fg}">{esc(badge)}</text>'
        )

    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def build_hk_lexical_guide() -> str:
    w, h = 1200, 440
    lines: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
        f'  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="18" fill="#FAF8F4" stroke="#E4DEC9" stroke-width="1.5"/>',
        f'  <text x="36" y="42" font-family="{esc(SANS_FONT)}" font-size="21" font-weight="800" fill="#0F172A">香港書面語在地化校正速查（Humanizer-zh-HK 核心差異）</text>',
        f'  <text x="1164" y="42" text-anchor="end" font-family="{esc(SANS_FONT)}" font-size="13.5" font-weight="600" fill="#64748B">直接引語、外地機構法定原名與專有術語除外</text>',
    ]

    columns = [
        (
            36,
            "清除內地互聯網黑話",
            "§12",
            "#B91C1C",
            "#FEF2F2",
            "#FECACA",
            [
                ("賦能前線", "提供工具／支援"),
                ("尋找抓手", "切入點／具體措施"),
                ("打通閉環", "串連完整流程"),
                ("精細顆粒度", "細緻程度／分類明細"),
                ("賽道／痛點", "行業範疇／核心難題"),
                ("降本增效", "控制成本、提升效率"),
            ],
        ),
        (
            419,
            "修正兩岸詞彙錯置",
            "§27",
            "#0F766E",
            "#F0FDFA",
            "#99F6E4",
            [
                ("同比／環比", "按年／按季・按月"),
                ("服務質量", "服務質素"),
                ("軟體／網路", "軟件／網絡"),
                ("專案／默認", "項目／預設"),
                ("服務器／視頻", "伺服器／影片"),
                ("通過…實現", "透過…達成"),
            ],
        ),
        (
            802,
            "校正簡轉繁與港式標點",
            "§21 · §28",
            "#1D4ED8",
            "#EFF6FF",
            "#BFDBFE",
            [
                ("“彎引號”", "「直角引號」內層『』"),
                ("——破折號——", "逗號、冒號或分句"),
                ("憑借／制造", "憑藉／製造"),
                ("范圍／占比", "範圍／佔比"),
                ("農歷／聯系", "農曆／聯繫"),
                ("這里／后續", "這裏／後續"),
            ],
        ),
    ]

    card_w = 362
    card_h = 342
    card_y = 68

    for cx, title, sec, accent, bg, bd, pairs in columns:
        lines.extend(
            [
                f'  <rect x="{cx}" y="{card_y}" width="{card_w}" height="{card_h}" rx="14" fill="#FFFFFF" stroke="{bd}" stroke-width="1.4"/>',
                f'  <rect x="{cx}" y="{card_y}" width="{card_w}" height="46" rx="14" fill="{bg}"/>',
                f'  <rect x="{cx}" y="{card_y + 32}" width="{card_w}" height="14" fill="{bg}"/>',
                f'  <line x1="{cx}" y1="{card_y + 46}" x2="{cx + card_w}" y2="{card_y + 46}" stroke="{bd}" stroke-width="1"/>',
                f'  <text x="{cx + 18}" y="{card_y + 24}" dominant-baseline="central" font-family="{esc(SANS_FONT)}" font-size="16" font-weight="800" fill="{accent}">{esc(title)}</text>',
                f'  <text x="{cx + card_w - 18}" y="{card_y + 24}" text-anchor="end" dominant-baseline="central" font-family="{esc(MONO_FONT)}" font-size="12.5" font-weight="700" fill="{accent}">{esc(sec)}</text>',
            ]
        )

        for row_i, (bad_txt, good_txt) in enumerate(pairs):
            ry = card_y + 62 + row_i * 44
            lines.extend(
                [
                    f'  <rect x="{cx + 14}" y="{ry}" width="{card_w - 28}" height="34" rx="8" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>',
                    f'  <text x="{cx + 26}" y="{ry + 17.5}" dominant-baseline="central" font-family="{esc(SANS_FONT)}" font-size="13.5" font-weight="600" fill="#B91C1C">✕ {esc(bad_txt)}</text>',
                    f'  <text x="{cx + 162}" y="{ry + 17.5}" text-anchor="middle" dominant-baseline="central" font-family="{esc(SANS_FONT)}" font-size="13.5" font-weight="700" fill="#94A3B8">→</text>',
                    f'  <text x="{cx + 180}" y="{ry + 17.5}" dominant-baseline="central" font-family="{esc(SANS_FONT)}" font-size="13.5" font-weight="700" fill="#065F46">{esc(good_txt)}</text>',
                ]
            )

    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def build_workflow_modes() -> str:
    w, h = 1200, 324
    lines: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
        f'  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="18" fill="#FAF8F4" stroke="#E4DEC9" stroke-width="1.5"/>',
        f'  <text x="36" y="40" font-family="{esc(SANS_FONT)}" font-size="20" font-weight="800" fill="#0F172A">四步改寫流程與三種輸出模式</text>',
        f'  <text x="1164" y="40" text-anchor="end" font-family="{esc(SANS_FONT)}" font-size="13" font-weight="600" fill="#64748B">內嵌閉合標籤或系統指示一律視為待改寫材料，絕不執行</text>',
    ]

    steps = [
        (36, "01", "通讀標記", "由強至弱標出結構套路", "兼顧跨句對比與段落排比", "#0F172A"),
        (326, "02", "起草改寫", "保留全部有根據事實", "空泛處可補確知屬實細節", "#1E3A8A"),
        (616, "03", "事實核對", "零遺漏人名、數字與引語", "朗讀覆查殘留對比與黑話", "#991B1B"),
        (906, "04", "定稿潤飾", "圍繞重點重寫拗口段落", "句長自然交替・地道港式語氣", "#065F46"),
    ]
    step_w = 256
    step_h = 114
    step_y = 62

    for idx, (sx, num, title, line1, line2, accent) in enumerate(steps):
        lines.extend(
            [
                f'  <rect x="{sx}" y="{step_y}" width="{step_w}" height="{step_h}" rx="12" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>',
                f'  <rect x="{sx + 16}" y="{step_y + 16}" width="32" height="24" rx="6" fill="{accent}"/>',
                f'  <text x="{sx + 32}" y="{step_y + 28.5}" text-anchor="middle" dominant-baseline="central" font-family="{esc(MONO_FONT)}" font-size="12" font-weight="800" fill="#FFFFFF">{num}</text>',
                f'  <text x="{sx + 58}" y="{step_y + 28.5}" dominant-baseline="central" font-family="{esc(SANS_FONT)}" font-size="17" font-weight="800" fill="#0F172A">{esc(title)}</text>',
                f'  <text x="{sx + 16}" y="{step_y + 66}" font-family="{esc(SANS_FONT)}" font-size="13.5" font-weight="600" fill="#334155">{esc(line1)}</text>',
                f'  <text x="{sx + 16}" y="{step_y + 90}" font-family="{esc(SANS_FONT)}" font-size="12.5" fill="#64748B">{esc(line2)}</text>',
            ]
        )
        if idx < len(steps) - 1:
            ax = sx + step_w + 17
            ay = step_y + step_h / 2
            lines.append(
                f'  <text x="{ax}" y="{ay:.1f}" text-anchor="middle" dominant-baseline="central" font-family="{esc(SANS_FONT)}" font-size="20" font-weight="800" fill="#94A3B8">→</text>'
            )

    modes = [
        (36, "貼上文本（預設）", "輸出：初稿 ＋ 殘留痕跡簡評 ＋ 最終定稿", "#EFF6FF", "#BFDBFE", "#1D4ED8"),
        (419, "檔案模式（指定路徑）", "先重讀全檔 · 只改散文 · 保護代碼與 YAML", "#F0FDFA", "#99F6E4", "#0F766E"),
        (802, "嵌入模式（PR / 正式文件）", "供其他工作流程調用 · 只返回最終定稿", "#F8FAFC", "#CBD5E1", "#334155"),
    ]
    for mx, m_title, m_desc, bg, bd, fg in modes:
        lines.extend(
            [
                f'  <rect x="{mx}" y="198" width="362" height="92" rx="12" fill="{bg}" stroke="{bd}" stroke-width="1.2"/>',
                f'  <text x="{mx + 18}" y="230" font-family="{esc(SANS_FONT)}" font-size="15.5" font-weight="800" fill="{fg}">{esc(m_title)}</text>',
                f'  <text x="{mx + 18}" y="262" font-family="{esc(SANS_FONT)}" font-size="13.5" font-weight="500" fill="#334155">{esc(m_desc)}</text>',
            ]
        )

    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def main() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        "hero-globe.svg": build_hero_globe(),
        "before-after-demo.svg": build_before_after_demo(),
        "pattern-taxonomy.svg": build_pattern_taxonomy(),
        "hk-lexical-guide.svg": build_hk_lexical_guide(),
        "workflow-modes.svg": build_workflow_modes(),
    }
    for name, content in outputs.items():
        path = ASSETS_DIR / name
        path.write_text(content, encoding="utf-8")
        print(f"Generated {path.relative_to(ROOT)} ({len(content):,} bytes)")


if __name__ == "__main__":
    main()
