"""中文文档站的布局模板。"""
import html

ICONS = {
    'book': '<path d="M12 6C8 3 4 4 2 5v15c3-2 6-2 10 0 4-2 7-2 10 0V5c-3-1-6-2-10 1Zm0 0v14"/>',
    'search': '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/>',
    'arrow': '<path d="M4 12h16m-6-6 6 6-6 6"/>',
    'moon': '<path d="M20 15A9 9 0 0 1 9 4a9 9 0 1 0 11 11Z"/>',
    'flower': '<path d="M12 9c-7-10-11 0-4 3-11 2-4 11 1 4 0 11 10 8 6 1 10 4 11-6 3-6 7-8-3-11-6-2Z"/><circle cx="12" cy="13" r="2"/>',
    'build': '<path d="m14 6 4-4 4 4-4 4M16 8 5 19l-3-3L13 5M3 3l4 1 2 4-4 2-3-4Z"/>',
    'star': '<path d="m12 3 3 6 7 1-5 5 1 7-6-3-6 3 1-7-5-5 7-1Z"/>',
    'solo': '<circle cx="12" cy="7" r="4"/><path d="M4 21v-3a8 8 0 0 1 16 0v3"/>',
    'duo': '<circle cx="8" cy="7" r="3"/><path d="M2 21v-3a6 6 0 0 1 12 0v3M16 4a3 3 0 0 1 0 6m1 4a5 5 0 0 1 5 5v2"/>',
    'close': '<path d="m6 6 12 12M6 18 18 6"/>',
}


def icon(name):
    return f'<svg class="aa-icon" viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'


def home(asset_base):
    cards = [
        ('basics/', 'book', '01', '基础知识', '从气球管理到三傻捕获，把每一个基础步骤慢慢理清。', '机制 · 操作 · 实战'),
        ('builds/', 'build', '02', '配装指南', '战甲、武器与增幅器，找到适合当前阶段的配置。', '入门配装 · 进阶配装'),
        ('advanced/', 'star', '03', '进阶技巧', '理解祭坛周期与关键时机，让每一轮狩猎更从容。', '周期 · 时机 · 效率'),
        ('solo-strats/', 'solo', '04', '单人攻略', '跟着 Volt 与 Wisp 的流程，练习独立完成狩猎。', '路线 · 图针 · 流程'),
        ('duo-strats/', 'duo', '05', '双人攻略', '两个人的分工与配合，把默契写进每一个阶段。', '分工 · 配合 · 实战'),
        ('vocabulary.html', 'search', '06', '术语手册', '遇到不熟悉的简称，来这里找一找它的意思。', '简称 · 名词 · 对照'),
    ]
    grid = ''.join(f'<a class="aa-card" href="/{url}"><div class="aa-card__top"><span class="aa-card__icon">{icon(symbol)}</span><span lang="en">{number} / GUIDE</span></div><h3>{title}</h3><p>{desc}</p><span class="aa-card__footer">{foot} ↗</span></a>' for url,symbol,number,title,desc,foot in cards)
    art = f'<img class="aa-hero__portrait" src="{asset_base}/brand/aa-portrait-960.webp" srcset="{asset_base}/brand/aa-portrait-640.webp 640w, {asset_base}/brand/aa-portrait-960.webp 960w" sizes="(min-width: 768px) 24rem, 90vw" width="960" height="960" loading="lazy" decoding="async" alt="aa：粉色长发与猫耳、细圆框眼镜，穿白色衬衫，在浅蓝花卉背景前双手轻握">'
    return f'''<section class="aa-hero" aria-labelledby="home-title"><div class="aa-hero__copy"><p class="aa-eyebrow"><span lang="en">A LITTLE GUIDE TO EIDOLON</span> · 中文手册</p><h1 class="aa-hero__title" id="home-title"><span>夜色很长，</span><span>我们<em>慢慢学。</em></span></h1><p class="aa-hero__description">从第一次踏上夜晚的平原，到熟练完成每一轮狩猎。关于夜灵的机制、配装与实战，都认真地整理在这里。</p><p class="aa-quote">不着急，先把这一页看完吧。</p><div class="aa-hero__actions"><a class="aa-btn" href="/basics/">开始阅读 {icon('arrow')}</a><a class="aa-text-link" href="/builds/">寻找适合的配装 ↗</a></div></div><div class="aa-hero__art">{art}<p class="aa-hero__note">今天也，一点点进步。</p></div></section>
<section class="aa-section" aria-labelledby="explore"><div class="aa-section__heading"><h2 id="explore">翻开你需要的那一章</h2><p>从基础开始，也可以直接寻找答案。</p></div><div class="aa-grid">{grid}</div></section>
<section class="aa-section" aria-labelledby="route"><div class="aa-section__heading"><h2 id="route">第一次来？沿着这条小路走。</h2><p>给刚刚开始的你</p></div><div class="aa-route"><a class="aa-route__step" href="/basics/how-to-capture-tridolon.html"><span class="aa-route__number">01</span><div>认识三傻捕获<span>先了解完整流程</span></div></a><a class="aa-route__step" href="/builds/beginner-builds/"><span class="aa-route__number">02</span><div>准备入门配装<span>让装备先准备好</span></div></a><a class="aa-route__step" href="/basics/lure-management.html"><span class="aa-route__number">03</span><div>学会气球管理<span>把关键机制练熟</span></div></a></div></section>'''


def render(title, body, nav, toc, pagination, section, asset_base, is_home=False):
    css = ''.join(f'<link rel="stylesheet" href="{asset_base}/css/{name}.css">' for name in ('tokens','base','components','effects','utilities'))
    breadcrumb = f'<nav class="aa-breadcrumb" aria-label="当前位置"><a href="/">夜灵指南</a><span aria-hidden="true">/</span><span>{html.escape(section)}</span></nav>'
    if is_home:
        body = home(asset_base) + f'<section class="aa-section aa-article"><details><summary>关于本指南与社区</summary>{body}</details></section>'
        breadcrumb = ''
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light dark"><meta name="description" content="夜灵狩猎中文指南：Warframe 夜灵机制、入门与进阶配装、单人与双人实战攻略。"><title>{html.escape(title)} · 夜灵指南</title><link rel="icon" type="image/png" sizes="32x32" href="{asset_base}/brand/aa-icon-32.png"><link rel="icon" type="image/png" sizes="16x16" href="{asset_base}/brand/aa-icon-16.png"><link rel="icon" type="image/x-icon" href="{asset_base}/brand/favicon.ico"><link rel="apple-touch-icon" sizes="180x180" href="{asset_base}/brand/aa-icon-180.png"><link rel="manifest" href="/manifest.json"><script src="{asset_base}/js/theme.js"></script>{css}<script type="module" src="{asset_base}/js/main.js"></script></head>
<body><a class="aa-skip" href="#main">跳到正文</a><header class="aa-header"><div class="aa-header__inner"><a class="aa-brand" href="/"><span class="aa-brand__mark"><img src="{asset_base}/brand/aa-icon-96.png" width="44" height="44" loading="lazy" decoding="async" alt="aa 头像"></span><div><span class="aa-brand__name">夜灵指南</span><span class="aa-brand__caption" lang="en">EIDOLON FIELD NOTES</span></div></a><div class="aa-tools"><button class="aa-control" type="button" data-search-open aria-label="搜索指南">{icon('search')}<span class="aa-control__label">搜索指南</span><kbd>⌘ K</kbd></button><button class="aa-control" type="button" data-theme-toggle aria-label="切换明暗主题">{icon('moon')}</button><button class="aa-control" type="button" data-effects-toggle aria-label="切换花瓣与角色动效" aria-pressed="true">{icon('flower')}</button></div></div><div class="aa-progress" aria-hidden="true"></div></header>
<div class="aa-layout" {'data-home' if is_home else ''}><aside class="aa-sidebar" aria-label="指南目录"><details class="aa-sidebar__panel" data-menu><summary class="aa-sidebar__toggle">展开章节目录</summary><div class="aa-sidebar__intro">一本慢慢读的平原手册</div><nav class="aa-nav" aria-label="章节导航">{nav}</nav><p class="aa-sidebar__foot">从入门到进阶<br>每一次出发，都有一点收获。</p></details></aside><main class="aa-content" id="main" tabindex="-1">{breadcrumb}{body}{pagination}<footer class="aa-footer"><div>夜灵指南 · 中文版<br>献给每一位走进夜晚平原的你。</div><a href="/credits.html">鸣谢与贡献 ↗</a></footer></main><aside class="aa-toc" aria-label="本页目录"><p class="aa-toc__heading">在这一页</p>{toc}<a href="#main">回到页首 ↑</a></aside></div><span class="aa-signature" aria-hidden="true">aa</span>
<dialog class="aa-dialog" data-search-dialog aria-labelledby="search-title"><div class="aa-dialog__top"><h2 id="search-title">在书页里找一找</h2><button class="aa-control" type="button" data-search-close aria-label="关闭搜索">{icon('close')}</button></div><label class="aa-sr-only" for="search-input">搜索标题与正文</label><input class="aa-input" type="search" id="search-input" placeholder="例如：气球、Volt、增幅器……" autocomplete="off"><p class="aa-search__status" role="status">输入关键词，寻找你需要的那一页。</p><ul class="aa-results" aria-label="搜索结果"></ul></dialog></body></html>'''
