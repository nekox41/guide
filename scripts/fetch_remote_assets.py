"""将中文文档引用的远程图片缓存到仓库，供离线构建使用。"""
import hashlib
import io
import json
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from PIL import Image
from build_site import convert

ROOT = Path(__file__).resolve().parents[1]
target_directory = ROOT / 'assets/upstream'
target_directory.mkdir(exist_ok=True)
urls = set()
existing = {
    hashlib.sha256(p.read_bytes()).hexdigest(): p
    for folder in (ROOT / '.gitbook/assets', ROOT / 'zh/.gitbook/assets')
    for p in folder.iterdir() if p.is_file()
}
manifest_path = target_directory / 'index.json'
manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
for source in (ROOT / 'zh').rglob('*.md'):
    for image in BeautifulSoup(convert(source.read_text()), 'html.parser').find_all('img'):
        url = image.get('src', '')
        if urlsplit(url).scheme in ('https', 'http'):
            urls.add(url)
for url in sorted(urls):
    key = hashlib.sha256(url.encode()).hexdigest()[:16]
    target = ROOT / manifest[key] if key in manifest else target_directory / (key + '.img')
    content = target.read_bytes() if target.exists() else None
    try:
        with Image.open(io.BytesIO(content or b'')) as image:
            image.verify()
    except Exception:
        # 少数旧链接返回存储元数据，需要显式请求媒体正文。
        parts = urlsplit(url)
        query = dict(parse_qsl(parts.query))
        query['alt'] = 'media'
        download_url = urlunsplit(parts._replace(query=urlencode(query)))
        with urlopen(Request(download_url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=45) as response:
            content = response.read()
        with Image.open(io.BytesIO(content)) as image:
            image.verify()
        target.write_bytes(content)
    original = existing.get(hashlib.sha256(content).hexdigest())
    if original and target.parent == target_directory and target != original:
        target.unlink()
        target = original
    manifest[key] = target.relative_to(ROOT).as_posix()
    print(f'{urlsplit(url).hostname}: {target.name}', flush=True)
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
