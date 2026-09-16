# template7-review 视觉抽取规格（医生点评风 · 前沿荟萃学术风）

> 提取自「胰腺外科金大夫」公众号前沿荟萃文献解读文章（2026-09 抓取原文 HTML）。
> 正文结构从栏目眉题（前沿荟萃）到免责声明；原文前置插入图片已忽略。

## 一、适用场景

文献解读、临床研究速递（III 期结果揭晓/会议 LBA 报道）、会议数据点评、医生署名点评文章。
特征：编号章节 + 中英双题 + 浅色数据卡 + 来源标注 + 医生点评模块收尾。

## 二、双色 Token

| Token | 蓝色（默认） | 紫色 |
|-------|------------|------|
| 主色 PRIMARY（编号/章节标题/点评人/链接） | `#2F6EBA` | `#5c4a7a` |
| 浅底 CARD_BG（数据卡底） | `#EEF6FF` | `#F3EFF8` |
| 浅边 CARD_BORDER（数据卡底边 2px） | `#7BB7FC` | `#B8A8D6` |
| 金棕点缀 BROWN（来源标注/点评装饰线，两版通用） | `#B4956F` | `#B4956F` |
| 灰底 GRAY_BG（缩写块/点评卡，两版通用） | `#EDEDED` | `#EDEDED` |
| 正文 TEXT | `#3e3e3e` | `#3e3e3e` |
| 标题深色 | `#1a1a1a` | `#1a1a1a` |
| 次级灰 SUB | `#888` | `#888` |
| foot 深底卡 | `#2F6EBA` | `#4a3a63` |
| foot 浅标题色 | `#bcd9f7` | `#cfc0e4` |
| foot 边框/淡灰 | `#e3eefb` / `#90a2b3` | `#efe9f6` / `#a09aae` |

暖阳强调 `#f4a261`（foot"8个癌种+1个罕见病"）两版保留，不替换。

## 三、字体

- 标题栈：`'PingFangSC-light','PingFang SC',sans-serif`
- 文章主标题：18px 加粗 `#1a1a1a`，justify
- 正文：15px / line-height 1.75 / justify（与 house 默认 14px/line-height 2 略有差异，以本系列 15px 为准）
- 章节编号：30px 主色，line-height 1.3
- 章节中文标题：18px 主色加粗；英文副题 12px `#888` letter-spacing 1px
- 来源标注 / 点评参考文献：12px 金棕 / `#888`

## 四、模块顺序（正文容器内）

1. 品牌头部（固定区域）：72px 圆 logo + 品牌行（沿用各系列惯例）
2. 栏目眉题：居中双行 —— 栏目名 20px 主色加粗 letter-spacing 6px + 英文栏目副题 12px `#888` letter-spacing 3px
3. 文章标题 + 元信息（账号/日期/地域，12px `#888`）
4. 开篇介绍（前沿荟萃导语）：上期回顾 → 本期概述 → 研究登记号（NCT 号加粗），每段 3-4 行
5. 编号章节 ×N：`ReviewChapterHeader`（01/02/03…）→ 小节 `ReviewSubTitle` → 正文段/`ReviewPointList`/`ReviewDataCard` → `ReviewSourceNote`
6. 缩写说明块 `ReviewAbbrev`（最后一章末尾）
7. 参考文献 `ReviewRefList`
8. 医生点评模块 `DoctorReviewCard`（正文之后、foot 之前）
9. foot（review_foot_template.html 蓝版 / review_foot_purple.html 紫版，结构=template3 v3 母版，文案逐字一致）

## 五、组件清单（review_components.html）

| 组件 | 结构要点 |
|------|---------|
| ReviewChapterHeader | flex row；左编号列 `padding-right:15px;border-right:1px solid 主色`，30px 主色编号；右列 `flex:100 100 0%;padding:0 12px;border-right:3px solid 主色`，18px 主色加粗中文题 + 12px 灰英文题 |
| ReviewSubTitle | 16px 加粗 `#1a1a1a`，margin 16px 0 8px |
| ReviewBodyText | 15px / 1.75 / justify / `#3e3e3e` |
| ReviewDataCard | 浅底 + `border-bottom:2px` 浅边 + `padding:21px`；关键句 15px 主色加粗，补充说明深色 |
| ReviewSourceNote | 12px 金棕 `#B4956F` 居中，紧跟配图/数据卡 |
| ReviewPointList | `（1）（2）…` 加粗小标题 + 正文说明，15px |
| ReviewAbbrev | 灰底 `#EDEDED` padding 18px 20px，13px `#666` |
| ReviewRefList | 13px `#666`，编号悬挂；链接 `color:主色;text-decoration:none` |
| DoctorReviewCard | 见下节 |
| ReviewDivider | 自然风 emoji 🌿，仅一级模块间克制使用 |

## 六、DoctorReviewCard 医生点评模块（核心组件）

结构（忠实还原原文）：

1. 外框：`width:90%` 居中 + `border-left:1px solid #B4956F` + `padding-left:27px`
2. 金棕递减装饰条：4 个 inline-block 色块 20/15/10/5px × 3px，`margin:0 5px`
3. 灰底点评卡：`background:#EDEDED;padding:25px`
4. 医生信息行（flex row）：
   - 照片占位：**默认医生 icon**，`88×88` 圆形 `object-fit:cover` + 3px 白边 + 微阴影
     默认 src：`https://img0.baidu.com/it/u=2342311582,115606744&fm=253&fmt=auto&app=138&f=JPEG?w=759&h=443`
   - 右侧：点评人姓名 15px 主色加粗 + 职称/机构 12px `#888`
5. 点评正文：15px / 1.8 / justify，2-4 段
6. 点评参考文献：12px `#888`

**照片替换规则：**
- 提供真实医生照片时，仅替换 `img` 的 `src`（HTML 注释 `【医生照片占位】` 为定位锚点），尺寸保持 88×88 圆形裁切
- 如需横版工作照：将头像节点替换为 `width:100%;border-radius:8px` 整图，置于灰底卡顶部、医生信息行之前（尺寸与正文图片元素一致）

## 七、与其它系列的区别

- vs template3：学术编号章节头 + 中英双题，无卡片错落/胶囊标签；正文 15px
- vs template6-med：无三色警示体系/对照表；以文献解读叙事 + 医生署名收尾
- foot 与 template3 同构（v3 深色卡片版），换色即可

## 八、生成红线

- 文中数据（OS/PFS/ORR/HR/CI/p 值）必须与素材原文逐字一致，不得编造或四舍五入
- 研究性治疗不等同于已批准；境外已批/国内未上市按三段式披露惯例
- foot 文案逐字一致，禁止改写；色值随蓝/紫替换
- 医生点评内容须来自医生本人授权/署名材料；未经确认的点评不得代写代署
