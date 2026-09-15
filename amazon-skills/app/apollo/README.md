# Apollo 亚马逊应用能力集

从公开 Skill 清单的 131 个条目中筛选出 53 个直接面向 Amazon 的来源包，合并一组重复的竞品监控能力，整理为 **52 个独立 Skill**。

本目录是仓库整理成果，未安装到任何 Agent，未配置 API Key。每个 Skill 都采用同名目录、`SKILL.md`、`agents/openai.yaml`、`references/playbook.md` 和 `references/tool-routing.md`，并附 `LICENSE` / `NOTICE`；需要确定性处理的工作流另带 `scripts/` 或 `assets/`。复制单个完整目录即可保留其引用资源。

## 目录

| 分组 | 数量 | 范围 |
|---|---:|---|
| Amazon 采集与 VOC | 4 | 商品详情、轻量搜索、评论与媒体、VOC |
| Keepa 数据 | 3 | 条件筛选、商品搜索、历史价格与排名 |
| 卖家精灵数据 | 11 | 商品、类目、评论、优惠券与流量 |
| SIF 数据 | 4 | ASIN 关键词、流量结构、词的需求与竞争 |
| Sorftime 数据 | 22 | 类目、关键词、商品、评论、变体与趋势 |
| 运营与研究工作流 | 8 | 广告演示与计划、词库、HTML 简报、标题、竞品监控、选品报告与折扣计划 |

## Amazon 采集与 VOC

| Skill | 入口 |
|---|---|
| Amazon ASIN 商品详情采集 | [sealeap-apollo-amazon-product-details](sealeap-apollo-amazon-product-details/SKILL.md) |
| Amazon 评论与媒体采集 | [sealeap-apollo-amazon-review-media](sealeap-apollo-amazon-review-media/SKILL.md) |
| Amazon 轻量商品搜索 | [sealeap-apollo-amazon-product-search-lite](sealeap-apollo-amazon-product-search-lite/SKILL.md) |
| Amazon 评论 VOC 分析 | [sealeap-apollo-amazon-review-voc](sealeap-apollo-amazon-review-voc/SKILL.md) |

## Keepa 数据

| Skill | 入口 |
|---|---|
| Amazon Keepa 商品筛选 | [sealeap-apollo-keepa-product-finder](sealeap-apollo-keepa-product-finder/SKILL.md) |
| Amazon Keepa 历史趋势 | [sealeap-apollo-keepa-product-history](sealeap-apollo-keepa-product-history/SKILL.md) |
| Amazon Keepa 商品搜索 | [sealeap-apollo-keepa-product-search](sealeap-apollo-keepa-product-search/SKILL.md) |

## 卖家精灵数据

| Skill | 入口 |
|---|---|
| Amazon 卖家精灵 ASIN 商品详情 | [sealeap-apollo-sellersprite-asin-detail](sealeap-apollo-sellersprite-asin-detail/SKILL.md) |
| Amazon 卖家精灵 ASIN 优惠券趋势 | [sealeap-apollo-sellersprite-coupon-trend](sealeap-apollo-sellersprite-coupon-trend/SKILL.md) |
| Amazon 卖家精灵 竞品列表查询 | [sealeap-apollo-sellersprite-competitors](sealeap-apollo-sellersprite-competitors/SKILL.md) |
| Amazon 卖家精灵 类目市场研究 | [sealeap-apollo-sellersprite-market-research](sealeap-apollo-sellersprite-market-research/SKILL.md) |
| Amazon 卖家精灵 类目市场统计 | [sealeap-apollo-sellersprite-market-statistics](sealeap-apollo-sellersprite-market-statistics/SKILL.md) |
| Amazon 卖家精灵 商品池筛选 | [sealeap-apollo-sellersprite-product-search](sealeap-apollo-sellersprite-product-search/SKILL.md) |
| Amazon 卖家精灵 评论列表 | [sealeap-apollo-sellersprite-reviews](sealeap-apollo-sellersprite-reviews/SKILL.md) |
| Amazon 卖家精灵 ASIN 流量关键词 | [sealeap-apollo-sellersprite-traffic-keywords](sealeap-apollo-sellersprite-traffic-keywords/SKILL.md) |
| Amazon 卖家精灵 ASIN 流量关键词统计 | [sealeap-apollo-sellersprite-traffic-keyword-stats](sealeap-apollo-sellersprite-traffic-keyword-stats/SKILL.md) |
| Amazon 卖家精灵 ASIN 关联流量商品 | [sealeap-apollo-sellersprite-traffic-products](sealeap-apollo-sellersprite-traffic-products/SKILL.md) |
| Amazon 卖家精灵 ASIN 流量来源分析 | [sealeap-apollo-sellersprite-traffic-sources](sealeap-apollo-sellersprite-traffic-sources/SKILL.md) |

## SIF 数据

| Skill | 入口 |
|---|---|
| Amazon SIF ASIN 关键词反查 | [sealeap-apollo-sif-asin-keywords](sealeap-apollo-sif-asin-keywords/SKILL.md) |
| Amazon SIF ASIN 流量结构概览 | [sealeap-apollo-sif-asin-summary](sealeap-apollo-sif-asin-summary/SKILL.md) |
| Amazon SIF 关键词需求概览 | [sealeap-apollo-sif-keyword-overview](sealeap-apollo-sif-keyword-overview/SKILL.md) |
| Amazon SIF 关键词流量竞争 | [sealeap-apollo-sif-keyword-traffic](sealeap-apollo-sif-keyword-traffic/SKILL.md) |

## Sorftime 数据

| Skill | 入口 |
|---|---|
| Amazon Sorftime 类目核心关键词 | [sealeap-apollo-sorftime-category-keywords](sealeap-apollo-sorftime-category-keywords/SKILL.md) |
| Amazon Sorftime 类目实时市场报告 | [sealeap-apollo-sorftime-category-report](sealeap-apollo-sorftime-category-report/SKILL.md) |
| Amazon Sorftime 类目历史市场报告 | [sealeap-apollo-sorftime-category-report-from-history](sealeap-apollo-sorftime-category-report-from-history/SKILL.md) |
| Amazon Sorftime 类目销量趋势 | [sealeap-apollo-sorftime-category-trend](sealeap-apollo-sorftime-category-trend/SKILL.md) |
| Amazon Sorftime 竞品关键词分析 | [sealeap-apollo-sorftime-competitor-product-keywords](sealeap-apollo-sorftime-competitor-product-keywords/SKILL.md) |
| Amazon Sorftime 关键词详情 | [sealeap-apollo-sorftime-keyword-detail](sealeap-apollo-sorftime-keyword-detail/SKILL.md) |
| Amazon Sorftime 关键词扩展 | [sealeap-apollo-sorftime-keyword-extends](sealeap-apollo-sorftime-keyword-extends/SKILL.md) |
| Amazon Sorftime 实时热搜关键词榜 | [sealeap-apollo-sorftime-keyword-list](sealeap-apollo-sorftime-keyword-list/SKILL.md) |
| Amazon Sorftime 历史热搜关键词榜 | [sealeap-apollo-sorftime-keyword-list-from-history](sealeap-apollo-sorftime-keyword-list-from-history/SKILL.md) |
| Amazon Sorftime 关键词搜索结果 | [sealeap-apollo-sorftime-keyword-search-results](sealeap-apollo-sorftime-keyword-search-results/SKILL.md) |
| Amazon Sorftime 关键词历史趋势 | [sealeap-apollo-sorftime-keyword-trend](sealeap-apollo-sorftime-keyword-trend/SKILL.md) |
| Amazon Sorftime 潜力商品筛选 | [sealeap-apollo-sorftime-potential-product](sealeap-apollo-sorftime-potential-product/SKILL.md) |
| Amazon Sorftime 买家评论洞察 | [sealeap-apollo-sorftime-product-customers-say](sealeap-apollo-sorftime-product-customers-say/SKILL.md) |
| Amazon Sorftime 商品详情 | [sealeap-apollo-sorftime-product-detail](sealeap-apollo-sorftime-product-detail/SKILL.md) |
| Amazon Sorftime 关键词排名趋势 | [sealeap-apollo-sorftime-product-ranking-trend-by-keyword](sealeap-apollo-sorftime-product-ranking-trend-by-keyword/SKILL.md) |
| Amazon Sorftime 商品评论 | [sealeap-apollo-sorftime-product-reviews](sealeap-apollo-sorftime-product-reviews/SKILL.md) |
| Amazon Sorftime 商品筛选 | [sealeap-apollo-sorftime-product-search](sealeap-apollo-sorftime-product-search/SKILL.md) |
| Amazon Sorftime 历史商品筛选 | [sealeap-apollo-sorftime-product-search-from-history](sealeap-apollo-sorftime-product-search-from-history/SKILL.md) |
| Amazon Sorftime ASIN 流量词反查 | [sealeap-apollo-sorftime-product-traffic-terms](sealeap-apollo-sorftime-product-traffic-terms/SKILL.md) |
| Amazon Sorftime 商品历史趋势 | [sealeap-apollo-sorftime-product-trend](sealeap-apollo-sorftime-product-trend/SKILL.md) |
| Amazon Sorftime 商品变体 | [sealeap-apollo-sorftime-product-variations](sealeap-apollo-sorftime-product-variations/SKILL.md) |
| Amazon Sorftime 相似商品特征 | [sealeap-apollo-sorftime-similar-product-feature](sealeap-apollo-sorftime-similar-product-feature/SKILL.md) |

## 运营与研究工作流

| Skill | 入口 |
|---|---|
| Amazon 广告规则离线演示 | [sealeap-apollo-ads-demo](sealeap-apollo-ads-demo/SKILL.md) |
| Amazon 广告推进方案 | [sealeap-apollo-ad-planning](sealeap-apollo-ad-planning/SKILL.md) |
| Amazon ASIN 分层关键词库 | [sealeap-apollo-keyword-library](sealeap-apollo-keyword-library/SKILL.md) |
| Amazon ASIN 深度调研简报 | [sealeap-apollo-asin-research-brief](sealeap-apollo-asin-research-brief/SKILL.md) |
| Amazon 批量标题与商品亮点 | [sealeap-apollo-batch-title-rewrite](sealeap-apollo-batch-title-rewrite/SKILL.md) |
| Amazon 竞品快照与变化监控 | [sealeap-apollo-competitor-monitor](sealeap-apollo-competitor-monitor/SKILL.md) |
| Amazon 选品研究与决策报告 | [sealeap-apollo-product-research](sealeap-apollo-product-research/SKILL.md) |
| Amazon 价格折扣核查与计划 | [sealeap-apollo-price-discounts](sealeap-apollo-price-discounts/SKILL.md) |

## 筛选与整理说明

- 收录标准是技能本身直接操作或分析 Amazon 数据、商品或运营流程。1688/Alibaba 货源、其他电商平台、Google Trends、通用社媒与企业用量虽可能辅助跨境经营，不归为本次亚马逊专属 Skill。78 个非直接相关条目未纳入。
- “Keepa 商品详情”来源包实际提供 Product Finder，已按商品筛选命名。一个“商品分析报告”来源包实际提供竞品监控，已与另一监控包合并；没有据此虚构独立报告接口。
- 公开文件按能力重新编写，清理来源品牌、作者/店铺身份、个人路径、登录说明、网关地址、凭据变量和示例经营数据。原始下载、哈希与包映射只保存在仓库忽略的私有资料目录。
- 数据提供方的名称保留为真实路由依据；本集合不表示得到提供方背书。提供方的鉴权、费用、窗口和指标语义以执行时能力为准。

## 能力与验证边界

44 个数据 Skill 提供查询与证据处理流程；22 个 Sorftime 路由已对照会话工具声明，11 个卖家精灵路由已对照本地适配器定义。Keepa 按官方文档区分三种能力。SIF 的部分能力需要授权导出或进一步验证的连接器，不宣称所有端点已可直接执行。

8 个工作流保留研究与运营方法，并附离线经济测算、标题检查、折扣计划、SQLite 快照、报告渲染和合成广告演示脚本。原有特定机器的运行环境与专属网关未迁移为默认依赖；后台自动取数、真实广告执行、折扣提交和 Excel 生成需由执行环境按手册接入。

业务标签使用 FACT / ESTIMATE / ASSUMPTION / UNKNOWN；关键证据不足时为 HOLD。离线检查通过不表示在线账户、数据、页面操作或业务写入已经验证。

## 使用示例

```text
使用 sealeap-apollo-keyword-library。
目标站点、ASIN 和数据窗口沿用我提供的信息。
先复用已有数据，再建立产品边界、竞品池和分层关键词库；缺失指标保留未知。
```

本目录的独立编写成果遵循随包 MIT 许可与 NOTICE。来源材料和第三方服务不因整理而改变各自权利或服务条件。

## 整理验证

52/52 个 Skill 格式校验通过；25 项离线行为测试和 8 次命令行验证通过。隔离的无头浏览器验证了演示页规则变化、参数保存与重载、桌面和手机布局，以及报告缺失值和快照变化显示。来源品牌、账户与凭据残留扫描和内部链接检查均通过。在线数据、账户鉴权及真实业务写入未测试。
