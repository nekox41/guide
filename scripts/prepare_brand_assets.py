"""从用户原画和头像母版导出网页图片及网站图标，不覆盖原始素材。"""
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / 'assets/brand'
TARGET.mkdir(parents=True, exist_ok=True)

with Image.open(ROOT / '粉彩花语中的粉发猫娘.png') as source:
    portrait = ImageOps.exif_transpose(source).convert('RGB')
    for size in (640, 960):
        portrait.resize((size, size), Image.Resampling.LANCZOS).save(
            TARGET / f'aa-portrait-{size}.webp', 'WEBP', quality=90, method=6)

with Image.open(TARGET / 'aa-avatar-master.png') as source:
    avatar = ImageOps.exif_transpose(source).convert('RGB')
    if avatar.width != avatar.height:
        raise ValueError('头像母版应为正方形，避免导出时改变构图。')
    for size in (16, 32, 48, 96, 180, 192, 512):
        avatar.resize((size, size), Image.Resampling.LANCZOS).save(
            TARGET / f'aa-icon-{size}.png', optimize=True)
    avatar.resize((256, 256), Image.Resampling.LANCZOS).save(
        TARGET / 'favicon.ico', sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
print('已导出完整原画的 WebP 版本与多尺寸网站图标。')
