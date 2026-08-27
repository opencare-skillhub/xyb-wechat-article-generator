# Khub 版本模板：结构与视觉抽取规格 v1.0

## 提取来源与边界

来源：Khub 公众号文章 `确诊后，我让AI读完了自己的基因组｜三天，26份报告，和一些没人告诉过我的事.html`。

- 原文视觉系统：**"病历记录"（Patient Practice Record）**风格，模拟医学档案的排版质感。
- 核心设计语言：衬线字体标题 + 粗黑边框卡片 + 暖米色背景 + 深绿强调色。
- 原文使用 `<table>` 布局实现微信兼容，模板保留 `<table>` 布方式。

## 视觉 Token

| 名称 | 值 | 用途 |
|---|---|---|
| 暖米背景 | `#faf7ef` | 页面底色 |
| 卡片白 | `#fffdf8` | 内容卡片底色 |
| 深绿 | `#0b5e45` | 品牌条背景、标题、强调文字 |
| 粗黑 | `#151515` | 卡片边框（2px）、正文文字 |
| 黄色 | `#f7c90d` | 引用块左边框、底部色条 |
| 警示红 | `#c94b3f` | 疾病名强调、底部色条 |
| 蓝色 | `#3d7daa` | 底部色条 |
| 暖灰 | `#5b5a54` | 免责声明文字、编号标签 |
| 白半透 | `rgba(255,255,255,0.28)` | 头部数据表边框 |

## 字体与段落

- **标题 H1**：`Georgia, "Songti SC", STSong, "Noto Serif CJK SC", serif`，28px，weight 900，line-height 1.4，letter-spacing -1px，颜色 `#fffdf8`（深绿底上）
- **标题 H2**：同上字体系列，22-23px，weight 900，line-height 1.3，颜色 `#0b5e45`（卡片内）
- **正文**：`"PingFang SC", "Microsoft YaHei", sans-serif`，15px，line-height 1.8，颜色 `#151515`
- **强调文字**：`color: #0b5e45`（绿色）或 `color: #c94b3f`（红色，用于疾病名）
- **免责声明**：13px，`#5b5a54`
- 每段 1–3 句，一段只传达一个意思。

## 模块顺序

1. **品牌条头部**：深绿背景 + 底部粗黑线 + logo + 标签行 + H1 标题 + 副标题 + 可选头部数据表
2. **导语卡片**：白底粗黑边框 + 粗体导语 + 正文
3. **正文**：章节标题卡片（编号 + 粗黑底线 + H2）+ 段落 + 可选图片/数据表/引用块
4. **免责声明卡片**：白底粗黑边框
5. **底部四色条**：绿(40%) + 黄(22%) + 红(16%) + 蓝(22%)
6. **尾语**：居中标签 + 摘要
7. **Foot**：白底粗黑边框卡片 + 社区信息

## 组件清单

| 组件 | 名称 | 用途 |
|---|---|---|
| SectionCard | KhubSectionCard | 白底粗黑边框卡片，承载所有内容块 |
| SectionHeader | KhubSectionHeader | 章节标题（编号 + 类别 + H2） |
| BodyParagraph | KhubBodyParagraph | 15px/1.8 正文段落 |
| StrongGreen | KhubStrongGreen | 深绿强调文字 |
| StrongRed | KhubStrongRed | 红色强调（疾病/警示） |
| Blockquote | KhubBlockquote | 黄色左边框引用块 |
| DataTable | KhubDataTable | 双列数据对比表 |
| HeaderDataRow | KhubHeaderDataRow | 头部数据行（白半透边框） |
| ColorBar | KhubColorBar | 底部四色条 |
| ImageFrame | KhubImageFrame | 图片容器 |

## 图片规则

- 图片统一 `width:100%;height:auto;display:block`。
- 使用 `<table>` 包裹图片实现居中，不保留固定像素尺寸。
- 品牌条 logo 使用小胰宝固定地址。
- 不上传患者隐私、检查报告、身份信息、Token 或 AppID。

## 与 template3 的区别

| 特性 | template3 | template5-khub |
|---|---|---|
| 标题字体 | PingFang SC 无衬线 | Georgia/Songti 衬线 |
| 卡片边框 | 无边框/微阴影 | 2px 粗黑边框 |
| 背景色 | 灰白渐变 | 暖米色 #faf7ef |
| 强调色 | 暖阳橙/琥珀 | 深绿 #0b5e45 |
| 引用块 | 无特殊样式 | 黄色左边框 |
| 底部装饰 | 深色卡片 | 四色横条 |
| 整体风格 | 治愈系杂志 | 病历档案风