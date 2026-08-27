# med 说明模版：结构与视觉抽取规格 v1.0

## 提取来源与边界

来源：RASONQUE (daraxonrasib) 官方说明书 vs 病友总结 — 差异对比与患者提醒（基于 FDA 批准说明书 2026年8月版生成的文章）。

- 原文文体：**药品说明书解读 / 医学对照**——用于说明书要点解读、官方 vs 非官方对比、用药指南翻译、紧急情况速查、患教说明文。
- 核心设计语言：**深蓝 `#2c5f7c` 医学权威色** + 白底圆角卡片 + 三色风险标签/警示框体系 + 编号清单。
- 原文使用 `class` + `<style>`（独立网页版），模版统一转译为**全部 inline style + `<section>` 标签**，保证公众号编辑器可用。

## 视觉 Token

| 名称 | 值 | 用途 |
|---|---|---|
| 深蓝主色 | `#2c5f7c` | 表头、章节底线、序号圆、品牌字、强调色 |
| 深蓝深底 | `#1a3a4a` | 封面渐变起点、头部渐变 |
| 红（高危） | `#c0392b` | 警告框标题、风险标签、hl-danger 高亮 |
| 橙（中危） | `#e67e22` | 注意框标题、risk-medium 标签 |
| 绿（常规） | `#27ae60` | 信息框标题、risk-safe |
| 蓝（低危） | `#3498db` | risk-low 标签 |
| 页面底色 | `#f5f5f5` | 页面背景 |
| 卡片白 | `#ffffff` | 内容卡片底色 |
| 正文色 | `#1a1a1a` | 正文文字 |
| 次文字 | `#555` | 说明文字、表头说明 |
| 警告浅底 | `#fdecea` | 警告框底色（红） |
| 注意浅底 | `#fef5e7` | 注意框底色（橙） |
| 信息浅底 | `#eafaf1` | 信息框底色（绿） |
| 高亮黄 | `#fff3cd` | `.hl` 文本高亮底 |
| 危险高亮底 | `#fdecea` | `.hl-danger` 底 + 红字 |

## 字体与段落

- **字体栈**：`-apple-system, BlinkMacSystemFont, "Helvetica Neue", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif`
- **H1 标题**：22px，line-height 1.5，白色（封面深蓝渐变上）
- **H2 章节标题**：19px，`#2c3e50`，底部 2px 深蓝底线
- **H3 小节标题**：16px，`#2c5f7c`
- **正文**：15px，line-height 1.8，`#1a1a1a`
- **表格**：14px；表头深蓝底白字；行边框 `#e0e0e0`；隔行 `#fafafa`
- **警示框正文**：14px，`#3e3e3e`，标题色随框类型
- 每段 1–3 句，一段只传达一个意思；移动端 3–4 行为一段。

## 模块顺序

1. **品牌头部**：白底 + 72px 圆形 logo（深蓝细边框）+ 品牌行「小胰宝 · XX科普」
2. **封面标题卡**：深蓝渐变（`#1a3a4a → #2c5f7c`）+ 标签行 + H1 + 副标题，底部 16px 圆角
3. **安全警告横幅**（可选）：红色整条，用于高风险药物或"官方 vs 民间"文体开篇
4. **对照表格**：三列 `MedCompareTable`（对比项 / ✅ 官方 / ⚠️ 病友），用于说明书差异
5. **警示框体系**：`MedWarningBox`(红) / `MedCautionBox`(橙) / `MedInfoBox`(绿)——高风险、注意、常规信息分区
6. **风险标签**：行内圆角标签（紧急=红 / 注意=橙 / 低危=蓝）用于速查表
7. **编号清单**：`MedChecklist` 深蓝圆圈序号 + 加粗条目标题
8. **附录**：用药指南全文翻译（H3 小节 + 警示框 + 信息框）
9. **Foot**：关于小胰宝标题条 → 三段介绍 → 尾图 → 关注我们 → 底部寄语卡片 → 免责声明

## 组件清单

| 组件 | 名称 | 用途 |
|---|---|---|
| SectionCard | MedSectionCard | 白底圆角卡片，承载章节内容 |
| SectionHeader | MedSectionHeader | 章节标题（深蓝底线） |
| SubTitle | MedSubTitle | H3 小节标题 |
| CompareTable | MedCompareTable | 三列对照表（深蓝表头） |
| CompareRow | MedCompareRow | 表格行（键/官方/对照） |
| WarningBox | MedWarningBox | 红色高危警告框 |
| CautionBox | MedCautionBox | 橙色注意框 |
| InfoBox | MedInfoBox | 绿色信息框 |
| RiskTag | MedRiskTag | 行内风险标签（红/橙/蓝） |
| Checklist | MedChecklist | 编号清单容器 |
| ChecklistItem | MedChecklistItem | 清单条目（圆圈序号） |
| Divider | MedDivider | 自然风 emoji 分隔线 |

## 图片规则

- 图片统一 `width:100%;height:auto;display:block`。
- 品牌条 logo 使用小胰宝固定地址：`https://picgo-1302991947.cos.ap-guangzhou.myqcloud.com/images/Pop%20Mart%20Character%20Front%20View%20(2).png`
- 尾图固定地址：`https://mmbiz.qpic.cn/mmbiz_jpg/1qperl0JnD1AhzWq7ibcKBsg70ppkibibHbNMCWDZqCBxLQ9UdIQdBCNK6VTXWQm8oicQKKfjJnx9d0YJefkOibraLw/640?wx_fmt=jpeg&from=appmsg&tp=webp&wxfrom=5&wx_lazy=1`
- 禁止为装饰编造医学/临床图片；药物实拍、说明书截图等需真实来源。

## 与 template4-ruici 的区别

| 特性 | template4-ruici | template6-med |
|---|---|---|
| 色系 | 医疗主绿 #3a7945 + 薄荷卡底 | 医学深蓝 #2c5f7c 权威感 |
| 适用文体 | 医院合作/体检筛查/服务指南 | 说明书解读/用药对照/紧急速查 |
| 卡片风格 | 薄荷浅底 + 白卡叙事流 | 白卡 + 深蓝底线 + 三色风险体系 |
| 核心组件 | Hero/预约 CTA/往期回顾 | 对照表/警示框/风险标签/编号清单 |
| 分隔 | 浅蓝分隔 + 尾饰 | 自然风 emoji （克制） |

## 使用路由

用户指定"说明书""用药指南""Medication Guide""用药对照""官方 vs 病友""紧急速查""药物安全""患教说明"时使用 `template6-med`。