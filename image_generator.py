from PIL import Image, ImageDraw, ImageFont
import math
import os
from datetime import date
import io

def generate_progress_image(
    goal: str,
    start_date: date,
    goal_date: date,
    current_date: date,
    width: int,
    height: int,
    fill_color: str = "#ff6b35"
) -> bytes:
    BG_COLOR = "#000000"
    DOT_UNPASSED_COLOR = "#4a4a4a"
    DOT_PASSED_COLOR = fill_color
    TEXT_COLOR_PRIMARY = "#a0a0a0"
    TEXT_COLOR_HIGHLIGHT = fill_color
    
    total_days = (goal_date - start_date).days
    if total_days < 1:
        total_days = 1
        
    passed_days = (current_date - start_date).days
    passed_days = max(0, min(passed_days, total_days))
    
    remaining_days = total_days - passed_days
    progress_percent = int((passed_days / total_days) * 100) if total_days > 0 else 100
    
    img = Image.new('RGB', (width, height), color=BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Use bundled font for reliable rendering on Vercel/Render
    font_path = os.path.join(os.path.dirname(__file__), "font.ttf")
    try:
        font_large = ImageFont.truetype(font_path, 48)
        font_small = ImageFont.truetype(font_path, 36)
    except IOError:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    bbox_goal = draw.textbbox((0, 0), goal, font=font_large)
    goal_w = bbox_goal[2] - bbox_goal[0]
    goal_h = bbox_goal[3] - bbox_goal[1]
    
    cols = 15
    rows = math.ceil(total_days / cols)
    
    dot_radius = 16
    dot_spacing = 46
    
    grid_w = cols * dot_spacing - (dot_spacing - dot_radius*2)
    grid_h = rows * dot_spacing - (dot_spacing - dot_radius*2)
    
    start_x = (width - grid_w) // 2 + dot_radius
    start_y = (height - grid_h) // 2 + dot_radius
    
    goal_x = (width - goal_w) // 2
    goal_y = start_y - 120
    draw.text((goal_x, goal_y), goal, font=font_large, fill=TEXT_COLOR_PRIMARY)
    
    for i in range(total_days):
        r = i // cols
        c = i % cols
        
        cx = start_x + c * dot_spacing
        cy = start_y + r * dot_spacing
        
        color = DOT_PASSED_COLOR if i < passed_days else DOT_UNPASSED_COLOR
        
        draw.ellipse(
            (cx - dot_radius, cy - dot_radius, cx + dot_radius, cy + dot_radius),
            fill=color
        )
        
    progress_text_left = f"{remaining_days}d left "
    progress_text_right = f"· {progress_percent}%"
    
    bbox_left = draw.textbbox((0, 0), progress_text_left, font=font_small)
    bbox_right = draw.textbbox((0, 0), progress_text_right, font=font_small)
    
    left_w = bbox_left[2] - bbox_left[0]
    right_w = bbox_right[2] - bbox_right[0]
    total_w = left_w + right_w
    
    text_x = (width - total_w) // 2
    text_y = start_y + grid_h + 80
    
    draw.text((text_x, text_y), progress_text_left, font=font_small, fill=TEXT_COLOR_HIGHLIGHT)
    draw.text((text_x + left_w, text_y), progress_text_right, font=font_small, fill=TEXT_COLOR_PRIMARY)
    
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()
