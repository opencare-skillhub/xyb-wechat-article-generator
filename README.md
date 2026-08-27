# 小胰宝公众号文章生成器

一个基于 Kiro Skill 的微信公众号文章自动排版工具，专为"小胰宝"公益科普项目设计。

## 功能

- 将 Markdown/文本素材自动转换为微信公众号兼容的 inline style HTML
- **六套版式系列**：v3.1 生机微光（默认，卡片错落 + 高对比阅读优化）、莫兰迪柔和卡片风、中国风/特展版式风、瑞慈医疗服务版、病历记录风、med 说明书解读风
- 每系列 9 套配色（8 套莫兰迪色系 + Tiffany蓝绿）
- v3.1 可读性铁律：正文用深色 token，浅色仅用于边框/装饰，杜绝"浅字叠浅底"
- 内置多种排版组件（错位标题卡、胶囊标签、大字号数据卡、气泡时间轴、CSS几何分隔线等）
- 自动附加固定底部区域（组织介绍、社交媒体、签名卡片）
- 输出可直接粘贴到135编辑器使用

## 目录结构

```
xyb-wechat-article-generator/
├── README.md                    # 项目说明
├── skill.md                     # Kiro Skill 定义文件
├── assets/
│   ├── template3/               # 模板系列3：生机微光 v3.1（默认，10套配色）
│   │   ├── xyb3_template.html               # 🌿 治愈翡翠绿+琥珀暖阳（默认旗舰）
│   │   ├── foot_template.html               # 📌 v3 foot 母版（深色卡片版基准）
│   │   ├── xyb3_template_morandi.html       # 🤎 莫兰迪暖棕+陶土暖阳
│   │   ├── xyb3_template_morandi_blue.html  # 🔵 雾霾蓝+琥珀暖阳
│   │   ├── xyb3_template_morandi_gray.html  # ⚪ 高级灰+琥珀暖阳
│   │   ├── xyb3_template_morandi_pink.html  # 🩷 豆沙粉+蜜桃暖阳
│   │   ├── xyb3_template_morandi_red.html   # 🔴 赭红+鎏金暖阳
│   │   ├── xyb3_template_morandi_purple.html # 🟣 烟紫+琥珀暖阳
│   │   ├── xyb3_template_morandi_green.html  # 🟢 灰绿自然+琥珀暖阳
│   │   └── xyb3_template_tiffany.html        # 💎 蒂芙尼蓝绿+珊瑚暖阳
│   ├── template1/               # 模板系列1：莫兰迪柔和卡片风（9套配色 + foot母版）
│   │   ├── foot_template.html              # 📌 foot 强调版母版（固定footer基准）
│   │   ├── xyb_template.html              # 🌿 森林绿（默认）
│   │   ├── xyb_template_morandi.html      # 🤎 莫兰迪暖棕
│   │   ├── xyb_template_morandi_blue.html # 🔵 莫兰迪蓝
│   │   ├── xyb_template_morandi_gray.html # ⚪ 莫兰迪灰
│   │   ├── xyb_template_morandi_pink.html # 🩷 莫兰迪粉
│   │   ├── xyb_template_morandi_red.html  # 🔴 莫兰迪红
│   │   ├── xyb_template_morandi_purple.html # 🟣 莫兰迪紫
│   │   ├── xyb_template_morandi_green.html  # 🟢 莫兰迪绿
│   │   └── xyb_template_tiffany.html       # 💎 Tiffany蓝绿
│   ├── template2/               # 模板系列2：中国风/特展版式风（10套配色）
│   │   ├── xyb2_template.html              # 🏮 朱砂深红（默认，中国风）
│   │   ├── xyb2_template_morandi.html      # 🤎 莫兰迪暖棕
│   │   ├── xyb2_template_morandi_blue.html # 🔵 莫兰迪蓝
│   │   ├── xyb2_template_morandi_gray.html # ⚪ 莫兰迪灰
│   │   ├── xyb2_template_morandi_pink.html # 🩷 莫兰迪粉
│   │   ├── xyb2_template_morandi_red.html  # 🔴 莫兰迪红
│   │   ├── xyb2_template_morandi_purple.html # 🟣 莫兰迪紫
│   │   ├── xyb2_template_morandi_green.html  # 🟢 莫兰迪绿
│   │   └── xyb2_template_tiffany.html       # 💎 Tiffany蓝绿
│   ├── template5-khub/          # 模板系列5：病历记录风（衬线字体+粗黑边框+暖米底）
│   │   ├── khub_template.html               # 📋 病历档案风主模板
│   │   ├── khub_components.html             # 🧩 组件库（SectionCard/Blockquote/ColorBar等）
│   │   ├── khub_foot_template.html          # 📌 病历风格 foot 母版
│   │   └── khub_template_spec.md            # 📐 视觉抽取规格
│   ├── template6-med/           # 模板系列6：med 说明模版（深蓝权威风，说明书/用药指南）
│   │   ├── med_template.html                # 🩺 说明书解读主模板
│   │   ├── med_components.html              # 🧩 组件库（对照表/警示框/风险标签/清单）
│   │   ├── med_foot_template.html           # 📌 深蓝权威版 foot 母版
│   │   └── med_template_spec.md             # 📐 视觉抽取规格
│   └── images/                  # 图片资源
├── examples/                    # 示例输出
│   ├── 云南白药_公众号_blue.html
│   └── 化疗贫血科学管理_公众号_purple.html
└── output/                      # 生成文件输出目录
```

## 使用方法

### 在 Kiro 中使用

1. 在对话中通过 `#` 引用 skill
2. 提供素材内容和配色选择
3. 自动生成 HTML 文件

```
使用莫兰迪蓝模板，将 [素材] 生成公众号文章
```

### 发布到微信公众号

1. 打开 [135编辑器](https://www.135editor.com)
2. 点击"导入" → "HTML源码"
3. 粘贴生成的 HTML 代码
4. 微调后点"复制到公众号"
5. 在微信公众号后台粘贴发布

## 配色方案速查

| 关键词 | 色系 | 推荐场景 |
|--------|------|---------|
| 绿色/默认 | 🌿 森林绿 | 日常科普 |
| 暖棕/莫兰迪 | 🤎 暖棕 | 人文关怀 |
| 蓝色/学术 | 🔵 雾霾蓝 | 学术报告、临床数据 |
| 灰色 | ⚪ 高级灰 | 严肃话题、纪念 |
| 粉色 | 🩷 豆沙粉 | 心理关怀、女性话题 |
| 红色 | 🔴 赭红 | 重要警示 |
| 紫色/胰腺癌 | 🟣 烟紫 | 胰腺癌宣传月（11月） |
| 灰绿/营养 | 🟢 灰绿 | 营养科普 |
| Tiffany/活动 | 💎 蒂芙尼蓝 | 活动推广、节日 |

## 版式系列速查

| 系列 | 风格 | 适用场景 |
|------|------|---------|
| template3 | 🌿 生机微光（默认） | 日常科普、治愈系长文 |
| template1 | 🎨 莫兰迪柔和卡片 | 经典科普、叙事 |
| template2 | 🏮 中国风/特展 | 文化历史向专题 |
| template4-ruici | 🩺 瑞慈医疗服务 | 医院合作、体检筛查、服务指南 |
| template5-khub | 📋 病历记录风 | 个人叙事、深度科普、罕见病记录 |
| template6-med | 💊 med 说明模版 | 药品说明书解读、用药对照、紧急速查、患教说明 |

## 在其他 AI 工具中使用

### Claude (Anthropic)

在 Claude 对话中，将 `skill.md` 的内容作为 System Prompt 或对话开头粘贴，然后附上素材：

```
[粘贴 skill.md 全文]

---

请使用莫兰迪蓝配色，将以下内容生成公众号文章 HTML：

[粘贴素材内容]
```

也可以在 Claude Projects 中将 `skill.md` 和模板文件添加为 Project Knowledge，之后每次对话直接说：

```
使用蓝色模板，将以下内容生成公众号文章：[素材]
```

### OpenAI Codex / ChatGPT

**方式一：Custom Instructions**

将 `skill.md` 中的核心规则粘贴到 ChatGPT 的 "Custom Instructions" 或 GPTs 的 System Prompt 中。

**方式二：对话内使用**

```
你是一个微信公众号排版助手。请严格按照以下规则生成文章：
- 全部使用 inline style，不用 <style> 或 class
- 使用 <section> 标签
- 配色方案：主色 #4a6580，强调色 #8b5e5e，背景 #f0f4f8
- 字体：PingFangSC-light, letter-spacing:1px, line-height:2, font-size:14px

模板参考：
[粘贴 assets/template1/xyb_template_morandi_blue.html 的内容]

素材内容：
[粘贴你的素材]

请生成完整的公众号 HTML 代码。
```

**方式三：创建 GPTs**

1. 在 ChatGPT 中创建一个 GPT
2. 将 `skill.md` 作为 Instructions
3. 上传 `assets/template1/` 和 `assets/template2/` 下的模板文件作为 Knowledge
4. 用户只需说"使用蓝色模板生成文章"即可

### OpenClaw

在 OpenClaw 中创建 Agent 时：

1. **System Prompt**：粘贴 `skill.md` 全文
2. **Knowledge Base**：上传 `assets/template1/` 和 `assets/template2/` 目录下的所有模板文件
3. **使用时**：直接输入素材内容和配色选择

```yaml
# OpenClaw Agent 配置示例
name: 小胰宝公众号生成器
system_prompt: |
  [skill.md 内容]
knowledge_files:
  - assets/template1/xyb_template.html
  - assets/template1/xyb_template_morandi_blue.html
  - assets/template2/xyb2_template.html          # 中国风/特展版式
  - assets/template2/xyb2_template_morandi_purple.html
  # ... 其他模板（两个系列共 19 个文件）
```

### Hermes (Nous Research)

Hermes 模型支持 System Prompt + Tool Use。推荐配置：

```
<|im_start|>system
你是小胰宝公众号文章生成器。

[粘贴 skill.md 核心规则部分]

可用配色：绿色(#2d6a4f)、蓝色(#4a6580)、紫色(#5c4a7a)、粉色(#8c5c6c)、灰色(#5c5c5c)、红色(#7a4a4a)、Tiffany(#0abab5)

用户提供素材后，直接输出完整 inline style HTML 代码。
<|im_end|>
<|im_start|>user
使用蓝色模板，将以下内容生成公众号文章：
[素材内容]
<|im_end|>
```

### 通用提示词（适用于任何 LLM）

如果你使用的 AI 工具不在上述列表中，可以使用以下通用提示词：

```
你是一个微信公众号 HTML 排版助手。请根据我的素材生成文章，规则如下：

1. 全部使用 inline style（style=""），不用 <style> 标签
2. 使用 <section> 标签而非 <div>
3. 字体：font-family:'PingFangSC-light','PingFang SC',sans-serif
4. 正文：font-size:14px; letter-spacing:1px; line-height:2
5. 配色：主色[填入主色]，强调色[填入强调色]，背景[填入背景色]
6. 数据必须与原文一致，不得编造
7. 输出纯 HTML，不要 <!DOCTYPE> 等外壳标签

素材：
[你的内容]
```

---

## 关于小胰宝

小胰宝是一个面向胰腺肿瘤患者及家属的开源公益项目，归属小X宝社区和天工开物基金会管理。

- 官网：www.xiaoyibao.com.cn
- 社区：info.xiao-x-bao.com.cn
- 小红书：@小胰宝宝
- 公众号：@小胰宝助手
- 播客：小宇宙 @微光成炬 胰路同心
