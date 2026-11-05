# aa 原画与网站图标

首页角色使用根目录 `粉彩花语中的粉发猫娘.png` 的等比例 WebP 导出物；原画不改动。根目录 `aa_catgirl_recreation.svg` 是同图的 PNG 封装，不用于网页内联。

`aa-avatar-master.png` 使用内置 imagegen 工具，以原画为身份与画风参考生成头像近景，作为导航图标、浏览器 favicon 和触屏图标的统一母版。生成后仅进行尺寸与文件格式导出。

重新导出：

```bash
.venv/bin/python scripts/prepare_brand_assets.py
```

头像生成提示词：

> Use case: identity-preserve. Asset type: favicon / website avatar master. Use the attached image as the exact identity and watercolor pencil style reference. Create one square close-up avatar for the same pink-haired catgirl. Frame the entire head and both pink cat ears with a small comfortable margin, center the face. Preserve her soft pink hair, grey-blue eye, long bangs covering the other eye, thin round glasses, dark crossed hair clip, dark bow with a small pale flower. Pale mist-blue background matching the reference, subtle cream edge. Keep the original quiet gentle expression and pastel pencil/watercolor texture; simplify only fine background flower detail so the face and glasses stay readable when downscaled to a tiny browser favicon. Head and a little white collar only, no torso, no extra characters, no text, no signature, no typography. Do not invent a new face, do not recolor the eyes or hair.
