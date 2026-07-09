---
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/sc7MPTyiIfSwOeLlvpUg/advanced/shrine-cycles-and-bus
---

# Shrine Cycles & Bus

The Shrine activates on a fixed 2 second interval, known as the Shrine Cycle.

Your Bus is the combined time of your **Last Limb Break Time (LLBT)** and **Capshot Time (CT)**.\
**Bus = LLBT + CT**

If you miss a bus, you’ll be forced to wait for the next Shrine Cycle, potentially losing up to 2 seconds.

* **Garry Shrine:** Earliest bus is **1:23.300**. Miss it, and you'll hit 1:25.300, 1:27.300, etc.
* **Harry Shrine:** Earliest bus is **4:03.700**, followed by **4:05.700**, 4:07.700, etc.

{% hint style="info" %}
**Important Notes:**

* These buses are based on a stable 144 FPS, your mileage may vary.
* The bulk of the bus metric is just LLBT, if you have fast Capshots you don't have to pay attention to them.
* The 4:03.700 bus is hard to hit in most cases. In speedruns, 4:05.700 is more typical.
* The first set of each hunt (preload set) follows different earliest buses: 1:19.400 for the first Shrine and 3:59.800 for the second (and every 2s from there).
* Why we call it a bus: it can be thought of as a bus stop, we wait for predetermined shrine cycles in the same way one waits for a bus to arrive (you always want to take the earliest bus possible).&#x20;
{% endhint %}

## How to Find Your Own Bus:

You can extract them from your [**idalon**](http://idalon.com) logs using Lead’s [**ShrineCatBot**](https://discord.com/oauth2/authorize?client_id=1462504868383031500) on Discord. This bot is already integrated with the [**Eidolon Server**](https://discord.com/invite/mQhzbVv5bg).

{% hint style="warning" %}
These calculations are just approximations. You are not expected to understand them, these are mainly useful for the most dedicated hunters.
{% endhint %}

### **Discord command:**

<figure><img src="https://1960884447-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FMnWMWMKLrFw5Len33GHR%2Fuploads%2FCHfNOdxQ8NXjyl3STVcR%2Funknown.png?alt=media&#x26;token=fdba4c7b-4f0a-4c50-9854-605ad70ad909" alt=""><figcaption></figcaption></figure>

### **Output:**

<figure><img src="https://1960884447-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FMnWMWMKLrFw5Len33GHR%2Fuploads%2FZXryhn3ZXHSFd17YecPt%2Funknown.png?alt=media&#x26;token=805d4e52-be16-4df3-8364-c23e0a982aee" alt=""><figcaption></figcaption></figure>

From that output you can interpret that the <mark style="color:$warning;">**Garry Bus**</mark> is around <mark style="color:$warning;">**1.XX.300 (XX = 23, 25, 27…)**</mark> and the <mark style="color:green;">**Harry Bus**</mark> around <mark style="color:green;">**4:XX.700 (XX = 03, 04, 05…)**</mark>. Since XX is always an **odd number**, you can focus on the decimal part (.000) exclusively.\
If you analyze your own runs, you may find your buses to be different from XX.300 and XX.700

#### **Example Terry’s Vulnerability Times & Buses for Garry and Harry**

144 FPS Cap Comparison\
**IG**: In-game\
**RTSS**: RivaTuner Statistics Server\
**NVPC**: NVIDIA Control Panel\
**NVPC / RTSS ONLY**: only external software used, in-game framerate set to unlimited

<figure><img src="https://1960884447-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FMnWMWMKLrFw5Len33GHR%2Fuploads%2Fkycu47LtBwvbdTzpiZxo%2Funknown.png?alt=media&#x26;token=6614be5d-dda0-4fc3-9f9b-8879ee4ff6d1" alt=""><figcaption><p>Only decimals, average ± standard deviation</p></figcaption></figure>

* **RTSS+IG**: High bus, most consistent
* **IG only**: Low bus, fastest (hard to bus)
* **NVCP+IG**: Low bus, fast but inconsistent
* **NVCP only**: High bus, slow but consistent (easier to bus)
* **RTSS only**: High bus, slow (easy Terry, easy to bus)
