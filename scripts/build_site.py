"""Build the Chinese GitBook sources into a standalone static website."""
import argparse
import html
import re
import shutil
import hashlib
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit, parse_qs

import markdown
from bs4 import BeautifulSoup
from PIL import Image
from render_site import render, icon

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'zh'


def page_url(path):
    relative = path.relative_to(SOURCE)
    if relative.name == 'README.md':
        return '/' + str(relative.parent).replace('\\', '/').replace('.', '').strip('/') + ('/' if relative.parent != Path('.') else '')
    return '/' + relative.with_suffix('.html').as_posix()


def convert(text):
    text = re.sub(r'\A---\n.*?\n---\n', '', text, flags=re.S)
    def directive(match):
        command = match[1].strip()
        if command.startswith('hint '):
            style = re.search(r'style="(\w+)"', command)[1]
            label = {'info': '阅读提示', 'warning': '请留意', 'danger': '重要提醒'}.get(style, '提示')
            return f'\n<div class="aa-hint" data-kind="{style}" markdown="1">\n\n<span class="aa-hint__label">{label}</span>\n\n'
        if command == 'endhint':
            return '\n</div>\n'
        if command.startswith('embed '):
            url = re.search(r'url="([^"]+)"', command)[1]
            parts = urlsplit(url)
            video = parts.path.strip('/') if parts.hostname == 'youtu.be' else parse_qs(parts.query).get('v', [''])[0]
            if video and parts.hostname in ('youtu.be', 'www.youtube.com', 'youtube.com'):
                return f'\n<div class="aa-video" data-video="{html.escape(video)}"><p>本节视频教程 · <span lang="en">YouTube</span><br>点击后加载外部视频，正文阅读不受影响。</p><button class="aa-control" type="button" data-video-load>加载视频 ↗</button><a class="aa-text-link" href="{html.escape(url)}" target="_blank" rel="noopener noreferrer">前往视频页面</a></div>\n'
            return f'\n[查看视频]({url})\n'
        if command.startswith(('content-ref ', 'endcontent-ref', 'column', 'endcolumn')):
            return '\n'
        raise ValueError(f'Unsupported GitBook directive: {command}')
    text = re.sub(r'\{%\s*(.*?)\s*%\}', directive, text)
    # GitBook 导出的旧提示框缩进会被 Markdown 误判成代码。
    text = re.sub(r'(?m)^ +(<div data-gb-custom-block.*</div>)$', r'\n\1\n', text)
    text = text.replace('\\\n', '  \n')
    text = re.sub(r'<(details|figure)(\s[^>]*)?>', lambda m: m[0][:-1] + ' markdown="1">', text)
    return markdown.markdown(text, extensions=['extra', 'toc', 'sane_lists'], tab_length=2)


def build(output):
    output.mkdir(parents=True, exist_ok=True)
    pages = sorted(p for p in SOURCE.rglob('*.md') if p.name != 'SUMMARY.md')
    assets = set()
    warnings = set()
    image_sizes = {}
    prepared_assets = {}
    remote_manifest = json.loads((ROOT / 'assets/upstream/index.json').read_text())
    asset_hash = hashlib.sha256()
    for file in sorted((ROOT / 'assets').rglob('*')):
        if file.is_file() and 'upstream' not in file.relative_to(ROOT / 'assets').parts and file.name != 'aa-avatar-master.png':
            asset_hash.update(file.relative_to(ROOT).as_posix().encode())
            asset_hash.update(file.read_bytes())
    asset_base = '/assets/' + asset_hash.hexdigest()[:12]
    def rewrite(markup, current):
        soup = BeautifulSoup(markup, 'html.parser')
        for tag in soup.find_all(True):
            for attr in ('href', 'src', 'poster'):
                value = tag.get(attr)
                if not value:
                    continue
                parts = urlsplit(value)
                remote_image = tag.name == 'img' and attr == 'src' and parts.scheme in ('http', 'https')
                if (parts.scheme or parts.netloc or not parts.path) and not remote_image:
                    continue
                raw = unquote(parts.path)
                if remote_image or '.gitbook/assets/' in raw:
                    if remote_image:
                        remote_key = hashlib.sha256(value.encode()).hexdigest()[:16]
                        asset = ROOT / remote_manifest[remote_key]
                    else:
                        asset_name = raw.split('.gitbook/assets/', 1)[1]
                        candidates = [(current.parent / raw).resolve(), SOURCE / '.gitbook/assets' / asset_name, ROOT / '.gitbook/assets' / asset_name]
                        asset = next((p for p in candidates if p.is_file()), candidates[1])
                    if not asset.is_file():
                        warnings.add(f'{current.relative_to(SOURCE)}: missing asset {asset.name}')
                        if tag.name == 'img':
                            tag.replace_with(soup.new_string('[原文图片缺失]'))
                        continue
                    assets.add(asset)
                    if asset not in prepared_assets:
                        digest = hashlib.sha256(asset.read_bytes()).hexdigest()[:16]
                        with Image.open(asset) as image:
                            image_sizes[asset] = image.size
                            suffix = '.webp' if not getattr(image, 'is_animated', False) else '.' + image.format.lower()
                            relative = Path('media') / (digest + suffix)
                            destination = output / relative
                            destination.parent.mkdir(parents=True, exist_ok=True)
                            if suffix == '.webp':
                                image.convert('RGBA' if image.mode == 'RGBA' else 'RGB').save(destination, 'WEBP', quality=92, method=6)
                            else:
                                shutil.copy2(asset, destination)
                            prepared_assets[asset] = '/' + relative.as_posix()
                    target = prepared_assets[asset]
                    if tag.name == 'img':
                        if asset not in image_sizes:
                            with Image.open(asset) as image:
                                image_sizes[asset] = image.size
                        tag['width'], tag['height'] = map(str, image_sizes[asset])
                        tag['loading'], tag['decoding'] = 'lazy', 'async'
                        if not tag.get('alt'):
                            caption = tag.find_parent('figure')
                            caption = caption.find('figcaption') if caption else None
                            heading = soup.find('h1')
                            caption_text = caption.get_text(' ', strip=True) if caption else ''
                            tag['alt'] = caption_text or ((heading.get_text(' ', strip=True) if heading else current.stem) + '配图')
                else:
                    path = (current.parent / raw).resolve()
                    if path.is_dir():
                        path = path / 'README.md'
                    if path.suffix == '.md':
                        if not path.is_relative_to(SOURCE) or not path.is_file():
                            raise FileNotFoundError(f'{current}: {value}')
                        target = page_url(path)
                    else:
                        continue
                tag[attr] = target + ('?' + parts.query if parts.query else '') + ('#' + parts.fragment if parts.fragment else '')
        for table in soup.find_all('table'):
            wrapper = soup.new_tag('div', attrs={'class': 'aa-table', 'tabindex': '0', 'role': 'region', 'aria-label': '数据表格，可横向滚动'})
            table.wrap(wrapper)
        for pre in soup.find_all('pre'):
            pre['tabindex'] = '0'
            pre['role'] = 'region'
            pre['aria-label'] = '代码或格式化内容，可横向滚动'
        for hint in soup.select('[data-gb-custom-block][data-tag="hint"]'):
            hint['class'] = ['aa-hint']
            hint['data-kind'] = hint.get('data-style', 'info')
            label = soup.new_tag('span', attrs={'class': 'aa-hint__label'})
            label.string = '阅读提示'
            hint.insert(0, label)
        for mark in soup.find_all('mark'):
            # GitBook 私有颜色变量无法直接在浏览器中解释。
            mark.unwrap()
        return str(soup)
    nav = rewrite(convert((SOURCE / 'SUMMARY.md').read_text()), SOURCE / 'SUMMARY.md')
    nav = BeautifulSoup(re.sub(r'<h1.*?</h1>', '', nav, flags=re.S), 'html.parser')
    nav_links = [(a['href'], a.get_text(' ', strip=True)) for a in nav.select('a')]
    for li in list(nav.select('li')):
        child_list = li.find('ul', recursive=False)
        anchor = li.find('a', recursive=False)
        if child_list and anchor:
            group = nav.new_tag('details')
            summary = nav.new_tag('summary')
            summary.string = anchor.get_text(' ', strip=True)
            overview = nav.new_tag('li')
            overview.append(anchor.extract())
            child_list.insert(0, overview)
            group.append(summary)
            group.append(child_list.extract())
            li.append(group)
    search_index = []
    for page in pages:
        body = rewrite(convert(page.read_text()), page)
        soup = BeautifulSoup(body, 'html.parser')
        heading = soup.find('h1')
        title = heading.get_text() if heading else page.stem
        url = page_url(page)
        search_index.append({'url': url, 'title': title, 'text': soup.get_text(' ', strip=True)})
        current_nav = BeautifulSoup(str(nav), 'html.parser')
        for anchor in current_nav.select('a'):
            if anchor.get('href') == url:
                anchor['aria-current'] = 'page'
                for parent in anchor.parents:
                    if parent.name == 'details':
                        parent['open'] = ''
        section = {'builds': '配装指南', 'basics': '基础知识', 'advanced': '进阶技巧', 'solo-strats': '单人攻略', 'duo-strats': '双人攻略'}.get(page.relative_to(SOURCE).parts[0], title)
        toc = ''.join(f'<a href="#{html.escape(h["id"])}">{html.escape(h.get_text(" ", strip=True))}</a>' for h in soup.select('h2[id]'))
        pagination = ''
        ordered_urls = [link[0] for link in nav_links]
        if url in ordered_urls:
            index = ordered_urls.index(url)
            links = []
            for position, label in ((index-1, '上一篇'), (index+1, '下一篇')):
                if 0 <= position < len(nav_links):
                    href, text = nav_links[position]
                    links.append(f'<a href="{html.escape(href)}"><small>{label}</small>{html.escape(text)} {icon("arrow")}</a>')
            pagination = '<nav class="aa-pagination" aria-label="相邻章节">' + ''.join(links) + '</nav>'
        if page == SOURCE / 'README.md' and heading:
            heading.name = 'h2'
        body = '<article class="aa-article">' + str(soup) + '</article>'
        document = render(title, body, str(current_nav), toc, pagination, section, asset_base, page == SOURCE / 'README.md')
        target = output / (url.lstrip('/') + ('index.html' if url.endswith('/') else ''))
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(document)
    shutil.copytree(ROOT / 'assets', output / asset_base.lstrip('/'), dirs_exist_ok=True, ignore=shutil.ignore_patterns('upstream', 'aa-avatar-master.png'))
    shutil.copy2(ROOT / 'assets/brand/favicon.ico', output / 'favicon.ico')
    manifest = {
        'name': '夜灵指南', 'short_name': '夜灵指南', 'lang': 'zh-CN',
        'start_url': '/', 'display': 'standalone',
        'icons': [{'src': f'{asset_base}/brand/aa-icon-{size}.png', 'sizes': f'{size}x{size}', 'type': 'image/png'} for size in (192, 512)],
    }
    (output / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False))
    (output / 'search-index.json').write_text(json.dumps(search_index, ensure_ascii=False))
    print(f'Built {len(pages)} Chinese pages and {len(assets)} referenced assets in {output}')
    for warning in sorted(warnings):
        print(f'WARNING: {warning}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'dist')
    build(parser.parse_args().output.resolve())
