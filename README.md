# 小胰宝公众号文章生成器

一个基于 Kiro Skill 的微信公众号文章自动排版工具，专为"小胰宝"公益科普项目设计。

## 功能

- 将 Markdown/文本素材自动转换为微信公众号兼容的 inline style HTML
- 支持 9 套配色方案（莫兰迪色系 + Tiffany蓝绿）
- 内置 10 种排版组件（标题卡片、数据卡片、信息框、时间线等）
- 自动附加固定底部区域（组织介绍、社交媒体、签名卡片）
- 输出可直接粘贴到135编辑器使用

## 目录结构

```
xyb-wechat-article-generator/
├── README.md                    # 项目说明
├── skill.md                     # Kiro Skill 定义文件
├── assets/
│   ├── templates/               # HTML 模板文件（9套配色）
│   │   ├── xyb_template.html              # 🌿 森林绿（默认）
│   │   ├── xyb_template_morandi.html      # 🤎 莫兰迪暖棕
│   │   ├── xyb_template_morandi_blue.html # 🔵 莫兰迪蓝
│   │   ├── xyb_template_morandi_gray.html # ⚪ 莫兰迪灰
│   │   ├── xyb_template_morandi_pink.html # 🩷 莫兰迪粉
│   │   ├── xyb_template_morandi_red.html  # 🔴 莫兰迪红
│   │   ├── xyb_template_morandi_purple.html # 🟣 莫兰迪紫
│   │   ├── xyb_template_morandi_green.html  # 🟢 莫兰迪绿
│   │   ├── xyb_template_emerald_amber.html  # 💚🧡 翡翠绿+琥珀（治愈系）
│   │   ├── xyb_template_dawn_warm.html      # 🌅 晨曦暖阳（问答+清单）
│   │   ├── xyb_template_clinical_blue.html  # 🌊 雾蓝学术（导航+灯塔+VS对照）
│   │   ├── xyb_template_soft_pink.html      # 🌸 藕粉人文（信纸+树洞）
│   │   ├── xyb_template_oasis_green.html    # 🌳 生命绿洲（方案+药物档案）
│   │   ├── xyb_template_emergency_red.html  # 🚨 急症警示（信号灯+急救步骤）
│   │   ├── xyb_template_ai_tech.html        # 🌌 AI前沿（深色霓虹科技）
│   │   ├── xyb_template_event_flash.html    # 🎯 活动快讯（倒计时+报名）
│   │   ├── xyb_template_lab_report.html     # 🧾 化验单（报告单表格解读）
│   │   ├── xyb_template_metro_journey.html  # 🚇 胰路地铁（线路图+打卡）
│   │   ├── xyb_template_mindfulness.html    # 🧘 正念疗愈（呼吸引导+金句墙）
│   │   ├── xyb_template_story_narrative.html # 📖 叙事长文（章节+首字下沉）
│   │   ├── xyb_template_expert.html         # 👨‍⚕️ 米白诊间（名片+对话体）
│   │   ├── xyb_template_data_compare.html   # 📊 靛紫数据（对比矩阵+阶梯）
│   │   ├── xyb_template_hotlist_rumor.html  # 🔥 热搜辟谣榜（拟物榜单）
│   │   ├── xyb_template_trial_boarding.html # ✈️ 登机牌（临床试验拟物）
│   │   ├── xyb_template_pill_week.html      # 💊 药盒周历（7格用药管理）
│   │   ├── xyb_template_rx_prescription.html # ℞ 老式处方笺（复古拟物）
│   │   └── xyb_template_tiffany.html       # 💎 Tiffany蓝绿
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
| 翡翠绿/琥珀 | 💚🧡 翡翠绿+琥珀暖阳 | 治愈系、生命力、医疗人文 |
| 暖阳/晨曦 | 🌅 琥珀暖阳 | 暖调科普、行动清单、问答 |
| 雾蓝/学术增强 | 🌊 雾霾蓝 | 临床研究深度解读、数据灯塔 |
| 藕粉/人文 | 🌸 藕粉+灰绿 | 心理关怀、患者故事、纪念 |
| 森林绿/方案 | 🌳 森林绿 | 治疗方案、指南解读、药物科普 |
| 赭红/警示 | 🚨 赭红 | 急症识别、就医红线、误区辟谣 |
| 深空蓝/AI | 🌌 深空蓝+霓虹青 | 新技术、新药、AI前沿（深色模式） |
| 亮橙/活动 | 🎯 亮橙 | 直播预告、志愿者招募、活动回顾 |
| 报告单/蓝灰 | 🧾 医师蓝 | 化验单解读、指标科普 |
| 地铁蓝/旅程 | 🚇 地铁蓝 | 治疗旅程、随访规划、康复阶段 |
| 灰绿/正念 | 🧘 灰绿+雾紫 | 心理支持、正念练习、家属关怀 |
| 暖棕/叙事 | 📖 奶油米白+暖棕 | 患者故事、深度报道、纪念专题 |
| 米白/诊间 | 👨‍⚕️ 米白+医师蓝 | 名医访谈、指南解读、专家答疑 |
| 靛紫/数据 | 📊 深靛+数据紫 | 药物横评、方案对比、决策辅助 |
| 热搜/辟谣 | 🔥 热搜红橙 | 误区辟谣合集、传言盘点 |
| 航空蓝/试验 | ✈️ 航空蓝 | 临床试验招募、入组流程 |
| 青绿/药盒 | 💊 医药青绿 | 用药管理、化疗间期护理 |
| 墨蓝/处方笺 | ℞ 米黄纸+蓝黑墨水 | 用药科普、医嘱叮嘱 |
| Tiffany/活动 | 💎 蒂芙尼蓝 | 活动推广、节日 |

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
[粘贴 assets/templates/xyb_template_morandi_blue.html 的内容]

素材内容：
[粘贴你的素材]

请生成完整的公众号 HTML 代码。
```

**方式三：创建 GPTs**

1. 在 ChatGPT 中创建一个 GPT
2. 将 `skill.md` 作为 Instructions
3. 上传 `assets/templates/` 下的模板文件作为 Knowledge
4. 用户只需说"使用蓝色模板生成文章"即可

### OpenClaw

在 OpenClaw 中创建 Agent 时：

1. **System Prompt**：粘贴 `skill.md` 全文
2. **Knowledge Base**：上传 `assets/templates/` 目录下的所有模板文件
3. **使用时**：直接输入素材内容和配色选择

```yaml
# OpenClaw Agent 配置示例
name: 小胰宝公众号生成器
system_prompt: |
  [skill.md 内容]
knowledge_files:
  - assets/templates/xyb_template.html
  - assets/templates/xyb_template_morandi_blue.html
  # ... 其他模板
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
