"""验证已构建站点的中文页面、本地链接、锚点及图片依赖。"""
import argparse
from pathlib import Path
from urllib.parse import urlsplit, unquote

from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('directory', type=Path)
root = parser.parse_args().directory.resolve()
pages = {p: BeautifulSoup(p.read_text(), 'html.parser') for p in root.rglob('*.html')}
errors = []
for page, soup in pages.items():
    if soup.html.get('lang') != 'zh-CN':
        errors.append(f'{page}: 页面语言不是中文')
    if len(soup.find_all('h1')) != 1:
        errors.append(f'{page}: 页面须有一个一级标题')
    ids = [tag['id'] for tag in soup.select('[id]')]
    if len(ids) != len(set(ids)):
        errors.append(f'{page}: 存在重复 ID')
    for image in soup.find_all('img'):
        if not all(image.get(key) for key in ('alt', 'width', 'height', 'loading', 'decoding')):
            errors.append(f'{page}: 图片缺少替代文字、尺寸或加载属性')
    for tag in soup.find_all(True):
        for attribute in ('href', 'src'):
            if not tag.has_attr(attribute):
                continue
            url = urlsplit(tag[attribute])
            if url.scheme or url.netloc:
                if attribute == 'src' and url.scheme != 'data':
                    errors.append(f'{page}: 页面加载依赖外部资源 {url.hostname}')
                continue
            target = root / unquote(url.path).lstrip('/') if url.path else page
            if target.is_dir():
                target = target / 'index.html'
            if not target.is_file():
                errors.append(f'{page}: 目标不存在 {tag[attribute]}')
            elif url.fragment and target in pages and not pages[target].find(id=unquote(url.fragment)):
                errors.append(f'{page}: 锚点不存在 {tag[attribute]}')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'通过：{len(pages)} 个中文页面，本地链接、锚点、图片属性与资源依赖均正常。')
