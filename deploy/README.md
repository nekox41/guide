# 中文站点部署

仅将 `zh/` 的 Markdown 构建为网页，按中文 `SUMMARY.md` 生成导航，复制页面引用的图片。英文页面不会发布。GitBook 提示框、折叠内容、视频与内部链接由构建脚本转换。

新版视觉遵循 `AGENTS.md`：奶油白与深灰紫明暗主题、粉蓝导览卡片、aa 阅读角色、可关闭的花瓣、键盘搜索、分层目录及阅读进度。样式位于 `assets/css/`，交互为 `assets/js/` 中的原生 ES Modules；主题变量统一保存在 `tokens.css`。

首页人物现使用用户提供的 `粉彩花语中的粉发猫娘.png` 的完整 WebP 导出物，替代原 SVG 手绘人物。导航与网站图标统一使用原画同角色头像，输出 ICO、PNG favicon、Apple Touch Icon 与应用图标；生成母版和提示词见 `assets/brand/README.md`。运行 `.venv/bin/python scripts/prepare_brand_assets.py` 可重建网页图片和图标。原始 PNG、封装 SVG 均保留不覆盖。

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-site.txt
.venv/bin/python scripts/build_site.py
.venv/bin/python scripts/verify_site.py dist
```

输出位于 `dist/`。重新构建前可指定新的空目录：`--output /tmp/guide-release`。缺失的原文图片会在构建时报告，并显示占位文字。

图片通过内容哈希生成本地路径，静态图片转为 WebP，教学 GIF 保留动画。图片带尺寸、延迟加载和替代文字。`assets/upstream/index.json` 将远程图片映射到仓库内的本地文件；新增远程图片后先运行 `.venv/bin/python scripts/fetch_remote_assets.py` 更新缓存，再提交资源及清单。正常构建无需连接 GitBook。

正文、图片、搜索、CSS 和脚本全部由本站提供。视频采用本地占位卡片，点击后才连接 YouTube；外部社区与资料链接仅在用户主动打开时访问。

服务器：`ubuntu@amd1ssh.aameow.com`，域名：`guide.aameow.com`。发布目录为 `/var/www/guide.aameow.com/releases/`，`current` 符号链接指向当前版本。上传新版本后切换链接即可更新；指回旧版本即可回滚。

构建并验证后，将 `dist/` 打包上传到服务器，使用 `deploy/publish.sh` 原子切换版本。该脚本须在服务器上运行，接受归档路径与唯一版本名，并在首页验证失败时恢复旧版本。示例：

```bash
tar -czf /tmp/guide-release.tar.gz -C dist .
scp /tmp/guide-release.tar.gz deploy/publish.sh ubuntu@amd1ssh.aameow.com:/tmp/
ssh ubuntu@amd1ssh.aameow.com 'bash /tmp/publish.sh /tmp/guide-release.tar.gz 20261105-aa-design'
```

发布脚本保留旧版本的图片和带哈希资源，以兼容尚未刷新的页面。模板包含 HTML/搜索索引重新验证缓存、哈希静态资源长期缓存和文本压缩；已有 HTTPS 配置应仅合入相关 location，保留 Certbot 证书设置。

若只更新界面与品牌资源，且确认 `media/` 与线上内容一致，可用 `tar --exclude='./media' ...` 制作增量归档；发布脚本会从上一版本复制缺少的带哈希图片。新增或改变攻略图片时应上传完整归档或将新增 `media/` 文件一并打包。

`guide.nginx.conf` 是首次启用 HTTP 的模板。正式配置在 `/etc/nginx/sites-available/guide.aameow.com`，由 Certbot 添加 HTTPS 和 HTTP 跳转。不要用模板覆盖正式 HTTPS 配置。

```bash
sudo nginx -t
sudo nginx -s reload
sudo certbot --nginx -d guide.aameow.com --redirect --non-interactive --agree-tos
sudo systemctl enable --now certbot.timer
sudo certbot renew --cert-name guide.aameow.com --dry-run --no-random-sleep-on-renew
```

证书使用服务器已有 ACME 账户。部署后检查首页、子页面、图片以及 HTTP 跳转；构建工具会检查本地 Markdown 链接和资源。

2026-11-05 已完成中文站点部署，证书初次有效期至 2027-02-03。服务器原有 Nginx 进程独立于 systemd 运行，部署时修复了空的 `/run/nginx.pid` 并通过 `nginx -s reload` 平滑重载。维护时应先检查实际主进程与服务状态，避免直接启动第二个 Nginx 实例。

新版视觉验收记录位于 `previews/`：包含桌面、手机、深色主题与正文截图，浏览器检查报告及 Lighthouse 摘要。本地移动端 Lighthouse 测得首页 Performance 93 / Accessibility 100、正文 Performance 100 / Accessibility 100，两页 CLS 均为 0；这些是本地模拟结果，实际网络表现取决于用户网络与服务器。明暗主题、键盘搜索与 Esc 关闭、主题偏好保存、手机目录、动效开关、减少动效模式均已检查；抽查 320–1440px 无横向溢出。全站 89 页通过本地资源、锚点与图片属性验证，页面加载无外部资源依赖。

首次视觉发布版本 `20261105-aa-design-v1` 的历史验收结果见 `previews/online-report.json`。当前线上版本为 `20261105-aa-original-v2`，已替换为用户原画与同角色网站图标。全站 89 页及 213 条 HTTPS 页面/资源路径全部返回 200；原画响应式图片、favicon 和应用图标清单均已验证。公网浏览器验收通过明暗主题、图标、搜索、动效开关及减少动效检查，见 `previews/brand-online-report.json`。本次本地移动端 Lighthouse 首页 Performance 99 / Accessibility 100，CLS 为 0，见 `previews/brand-lighthouse-summary.json`；截图使用 `previews/brand-*.png`。
