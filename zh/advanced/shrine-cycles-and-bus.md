---
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/sc7MPTyiIfSwOeLlvpUg/advanced/shrine-cycles-and-bus
---

# 祭坛周期与班车

祭坛每隔固定的 2 秒检查一次是否激活，这被称为祭坛周期。

你的“班车”（Bus【待确认：社区惯用译法】）时间由**最后一个关节的击破时间（LLBT）**与**收尾耗时（CT）**相加得到。\
**班车时间 = LLBT + CT**

如果错过一班车，就必须等待下一个祭坛周期，最多可能损失 2 秒。

* **巨力使祭坛：**最早的班车为 **1:23.300**，错过后依次为 1:25.300、1:27.300 等。
* **水力使祭坛：**最早的班车为 **4:03.700**，之后依次为 **4:05.700**、4:07.700 等。

{% hint style="info" %}
**注意事项：**

* 这些班车时间基于稳定的 144 FPS，你的实际情况可能不同。
* 班车时间主要取决于 LLBT；如果收尾足够快，就不必特别关注 CT。
* 多数情况下很难赶上 4:03.700 这班车。竞速中更常见的目标是 4:05.700。
* 每次狩猎的第一轮（入夜前预加载的首轮）最早班车时间不同：第一座祭坛为 1:19.400，第二座祭坛为 3:59.800，之后同样每隔 2 秒一班。
* “班车”的比喻：祭坛按照预定周期激活，就像在车站等车；你的目标总是赶上最早的一班车。&#x20;
{% endhint %}

## 如何确定自己的班车时间

可以在 Discord 使用 Lead 的 [**ShrineCatBot**](https://discord.com/oauth2/authorize?client_id=1462504868383031500)，从你的 [**Idalon**](http://idalon.com) 日志中提取班车时间。该机器人已经接入 [**Eidolon Server**](https://discord.com/invite/mQhzbVv5bg)。

{% hint style="warning" %}
这些计算只是近似值，不要求你完全理解，主要供追求极限的玩家参考。
{% endhint %}

### **Discord 命令：**

<figure><img src="https://1960884447-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FMnWMWMKLrFw5Len33GHR%2Fuploads%2FCHfNOdxQ8NXjyl3STVcR%2Funknown.png?alt=media&#x26;token=fdba4c7b-4f0a-4c50-9854-605ad70ad909" alt=""><figcaption></figcaption></figure>

### **输出：**

<figure><img src="https://1960884447-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FMnWMWMKLrFw5Len33GHR%2Fuploads%2FZXryhn3ZXHSFd17YecPt%2Funknown.png?alt=media&#x26;token=805d4e52-be16-4df3-8364-c23e0a982aee" alt=""><figcaption></figcaption></figure>

从输出可知，<mark style="color:$warning;">**巨力使班车**</mark>大约为 <mark style="color:$warning;">**1:XX.300（XX = 23、25、27……）**</mark>，<mark style="color:green;">**水力使班车**</mark>大约为 <mark style="color:green;">**4:XX.700（原文列为 XX = 03、04、05……；待确认：应否为 03、05、07……）**</mark>。由于 XX 始终为**奇数**，可以重点关注小数部分（.000）。\
分析自己的实战日志时，你的班车时间可能并非 XX.300 和 XX.700。

#### **兆力使解除无敌的时间，以及巨力使／水力使班车示例**

144 FPS 限帧方式对比\
**IG**：游戏内限帧\
**RTSS**：RivaTuner Statistics Server\
**NVPC**：NVIDIA 控制面板\
**仅 NVPC / RTSS**：仅使用外部软件限帧，游戏内帧率设为无限制。

<figure><img src="https://1960884447-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FMnWMWMKLrFw5Len33GHR%2Fuploads%2Fkycu47LtBwvbdTzpiZxo%2Funknown.png?alt=media&#x26;token=6614be5d-dda0-4fc3-9f9b-8879ee4ff6d1" alt=""><figcaption><p>仅展示小数部分，平均值 ± 标准差</p></figcaption></figure>

* **RTSS+IG**：班车时间偏晚，最稳定。
* **仅 IG**：班车时间偏早，速度最快（难以赶上班车）。
* **NVCP+IG**：班车时间偏早，速度快，但不稳定。
* **仅 NVCP**：班车时间偏晚，速度较慢，但稳定（更容易赶上班车）。
* **仅 RTSS**：班车时间偏晚，速度较慢（兆力使阶段较轻松，也容易赶上班车）。
