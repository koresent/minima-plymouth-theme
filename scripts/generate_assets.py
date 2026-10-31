#!/usr/bin/env python3
import os
import numpy as np
from PIL import Image, ImageDraw

def generate_assets():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    theme_dir = os.path.dirname(script_dir)
    assets_dir = os.path.join(theme_dir, "assets")
    showcase_dir = os.path.join(theme_dir, ".github", "showcase")
    src_dir = os.path.join(theme_dir, "src")
    os.makedirs(assets_dir, exist_ok=True)
    os.makedirs(showcase_dir, exist_ok=True)

    tux_path = os.path.join(src_dir, "tux.png")
    if not os.path.exists(tux_path):
        tux_path = os.path.join(theme_dir, "tux.png")
    if not os.path.exists(tux_path):
        tux_path = os.path.join(theme_dir, "..", "tux.png")

    if not os.path.exists(tux_path):
        raise FileNotFoundError(f"Source tux.png not found at {tux_path}")

    bg0_hard = (29, 32, 33)      # #1d2021
    fg       = (235, 219, 178)   # #ebdbb2
    gray     = (168, 153, 132)   # #a89984
    green    = (184, 187, 38)    # #b8bb26

    tux_raw = Image.open(tux_path).convert("RGBA")
    arr = np.array(tux_raw, dtype=float)
    lum = arr[:, :, 0]
    alpha = arr[:, :, 3]

    norm_lum = np.clip((lum - 32.0) / (255.0 - 32.0), 0.0, 1.0)
    body_r, body_g, body_b = 60.0, 56.0, 54.0        # Gruvbox bg1
    cream_r, cream_g, cream_b = 235.0, 219.0, 178.0  # Gruvbox fg #ebdbb2

    r = body_r * (1.0 - norm_lum) + cream_r * norm_lum
    g = body_g * (1.0 - norm_lum) + cream_g * norm_lum
    b = body_b * (1.0 - norm_lum) + cream_b * norm_lum

    recolored = np.stack([r, g, b, alpha], axis=-1).astype(np.uint8)
    tux_gb = Image.fromarray(recolored, "RGBA")
    bbox = tux_gb.getbbox()
    tux_cropped = tux_gb.crop(bbox)

    h_1x = 150
    w_1x = int(tux_cropped.width * (h_1x / tux_cropped.height))
    tux_1x = tux_cropped.resize((w_1x, h_1x), Image.Resampling.LANCZOS)
    tux_1x.save(os.path.join(assets_dir, "logo.png"), "PNG", optimize=True)

    h_2x = 300
    w_2x = int(tux_cropped.width * (h_2x / tux_cropped.height))
    tux_2x = tux_cropped.resize((w_2x, h_2x), Image.Resampling.LANCZOS)
    tux_2x.save(os.path.join(assets_dir, "logo@2x.png"), "PNG", optimize=True)

    scale = 4
    bar_w, bar_h = 280, 4
    beam_w = 60

    t_img = Image.new("RGBA", (bar_w * scale, bar_h * scale), (0, 0, 0, 0))
    d_t = ImageDraw.Draw(t_img)
    d_t.rounded_rectangle([0, 0, bar_w * scale - 1, bar_h * scale - 1], radius=2 * scale, fill=(60, 56, 54, 255))
    track = t_img.resize((bar_w, bar_h), Image.Resampling.LANCZOS)
    track.save(os.path.join(assets_dir, "bar_track.png"), "PNG", optimize=True)

    b_img = Image.new("RGBA", (beam_w * scale, bar_h * scale), (0, 0, 0, 0))
    d_b = ImageDraw.Draw(b_img)
    d_b.rounded_rectangle([0, 0, beam_w * scale - 1, bar_h * scale - 1], radius=2 * scale, fill=(green[0], green[1], green[2], 255))
    beam = b_img.resize((beam_w, bar_h), Image.Resampling.LANCZOS)
    beam.save(os.path.join(assets_dir, "bar_beam.png"), "PNG", optimize=True)

    f_img = Image.new("RGBA", (bar_w * scale, bar_h * scale), (0, 0, 0, 0))
    d_f = ImageDraw.Draw(f_img)
    d_f.rounded_rectangle([0, 0, bar_w * scale - 1, bar_h * scale - 1], radius=2 * scale, fill=(green[0], green[1], green[2], 255))
    fill = f_img.resize((bar_w, bar_h), Image.Resampling.LANCZOS)
    fill.save(os.path.join(assets_dir, "bar_fill.png"), "PNG", optimize=True)

    cw, ch = 320 * scale, 42 * scale
    cap_img = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    d_cap = ImageDraw.Draw(cap_img)
    d_cap.rounded_rectangle(
        [0, 0, cw - 1, ch - 1],
        radius=21 * scale,
        fill=(40, 40, 40, 240),
        outline=(80, 73, 69, 255),
        width=int(1.2 * scale)
    )
    cap_final = cap_img.resize((320, 42), Image.Resampling.LANCZOS)
    cap_final.save(os.path.join(assets_dir, "input_capsule.png"), "PNG", optimize=True)

    lw, lh = 14 * scale, 16 * scale
    lock_img = Image.new("RGBA", (lw, lh), (0, 0, 0, 0))
    d_lock = ImageDraw.Draw(lock_img)
    shackle_box = [2.5 * scale, 1 * scale, 11.5 * scale, 10 * scale]
    d_lock.arc(shackle_box, start=180, end=0, fill=gray, width=int(1.6 * scale))
    body_box = [1.5 * scale, 6.5 * scale, 12.5 * scale, 15 * scale]
    d_lock.rounded_rectangle(body_box, radius=int(1.8 * scale), fill=gray)
    d_lock.ellipse([6 * scale, 8.5 * scale, 8 * scale, 10.5 * scale], fill=(40, 40, 40, 255))
    d_lock.rectangle([6.5 * scale, 10 * scale, 7.5 * scale, 12.5 * scale], fill=(40, 40, 40, 255))
    lock_final = lock_img.resize((14, 16), Image.Resampling.LANCZOS)
    lock_final.save(os.path.join(assets_dir, "lock.png"), "PNG", optimize=True)

    bullet_size = 8 * scale
    b_img = Image.new("RGBA", (bullet_size, bullet_size), (0, 0, 0, 0))
    d_b = ImageDraw.Draw(b_img)
    d_b.ellipse([scale, scale, bullet_size - scale - 1, bullet_size - scale - 1], fill=fg)
    b_final = b_img.resize((8, 8), Image.Resampling.LANCZOS)
    b_final.save(os.path.join(assets_dir, "bullet.png"), "PNG", optimize=True)

    pw, ph = 960, 540
    plx = pw // 2 - tux_1x.width // 2
    ply = int(ph * 0.42) - tux_1x.height // 2

    p_bar_x = pw // 2 - track.width // 2
    p_bar_y = ply + tux_1x.height + 38

    im_pass = Image.new("RGB", (pw, ph), bg0_hard)
    im_pass.paste(tux_1x, (plx, ply), tux_1x)
    p_cap_x = pw // 2 - cap_final.width // 2
    p_cap_y = ply + tux_1x.height + 38
    im_pass.paste(cap_final, (p_cap_x, p_cap_y), cap_final)
    p_lock_x = p_cap_x + 18
    p_lock_y = p_cap_y + cap_final.height // 2 - lock_final.height // 2
    im_pass.paste(lock_final, (p_lock_x, p_lock_y), lock_final)
    p_b_start_x = p_lock_x + lock_final.width + 14
    p_b_y = p_cap_y + cap_final.height // 2 - b_final.height // 2
    for i in range(8):
        bx = p_b_start_x + i * 14
        im_pass.paste(b_final, (bx, p_b_y), b_final)
    im_pass.save(os.path.join(showcase_dir, "preview_password.png"), "PNG", optimize=True)

    total_dist = bar_w + beam_w
    frames = []
    total_frames = 85

    for f in range(total_frames):
        frame = Image.new("RGB", (pw, ph), bg0_hard)
        frame.paste(tux_1x, (plx, ply), tux_1x)
        frame.paste(track, (p_bar_x, p_bar_y), track)

        pos = f / total_frames
        d = int(total_dist * pos)

        if d < beam_w:
            cur_w = max(1, d)
            cur_x = p_bar_x
        elif d <= bar_w:
            cur_w = beam_w
            cur_x = p_bar_x + (d - beam_w)
        else:
            cur_w = max(1, total_dist - d)
            cur_x = p_bar_x + bar_w - cur_w

        scaled_beam = beam.resize((cur_w, bar_h), Image.Resampling.LANCZOS)
        frame.paste(scaled_beam, (cur_x, p_bar_y), scaled_beam)
        frames.append(frame)

    frames[0].save(
        os.path.join(showcase_dir, "preview.gif"),
        save_all=True,
        append_images=frames[1:],
        duration=25,
        loop=0
    )

if __name__ == "__main__":
    generate_assets()
