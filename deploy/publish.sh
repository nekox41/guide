#!/usr/bin/env bash
# 原子切换静态站点，旧版本继续保留以便回滚。
set -euo pipefail

archive=${1:?请提供构建归档路径}
release_name=${2:?请提供唯一发布版本名}
[[ "$release_name" =~ ^[a-zA-Z0-9-]+$ ]] || exit 2
site_root=/var/www/guide.aameow.com
release_path="$site_root/releases/$release_name"
previous=$(readlink -f "$site_root/current")
sudo test ! -e "$release_path"
sudo mkdir -p "$release_path"
sudo tar -xzf "$archive" -C "$release_path" --no-same-owner

# 保留旧页面仍可能请求的资源，避免版本切换时图片或脚本失效。
for resource in .gitbook zh assets media; do
    if sudo test -d "$previous/$resource"; then
        sudo mkdir -p "$release_path/$resource"
        sudo cp -an "$previous/$resource/." "$release_path/$resource/"
    fi
done
sudo chmod -R a+rX "$release_path"
sudo test -s "$release_path/index.html"
sudo nginx -t
sudo ln -s "$release_path" "$site_root/current-next"
sudo mv -Tf "$site_root/current-next" "$site_root/current"
if ! curl --fail --silent --show-error --resolve guide.aameow.com:443:127.0.0.1 https://guide.aameow.com/ -o /dev/null; then
    sudo ln -s "$previous" "$site_root/current-rollback"
    sudo mv -Tf "$site_root/current-rollback" "$site_root/current"
    echo '访问验证失败，已恢复旧版本。' >&2
    exit 1
fi
printf '当前版本：%s\n上一个版本：%s\n' "$release_path" "$previous"
