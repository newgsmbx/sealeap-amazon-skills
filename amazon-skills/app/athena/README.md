# Athena · 雅典娜

现有 **38 个业务 Skill + 1 个本地搜索 Skill，共 39 个入口**。原有 226 项业务能力与 1 项搜索能力均保留，通过入口内的细分模式按需读取。

这次按任务合并同类查询、地区变体和文档动作；各数据源、市场、权限与指标定义保持独立。每个包包含 `SKILL.md`、`agents/openai.yaml`、`references/playbook.md`、`references/tool-routing.md` 与本包的能力索引。复制完整包即可保留相关能力。

## 先找技能或旧名称

```bash
python3 sealeap-athena-find-skills/scripts/find_skills.py 'Amazon 广告报表' --limit 5
python3 sealeap-athena-find-skills/scripts/find_skills.py '$sealeap-athena-temu-eu-product' --limit 1
```

命令在当前集合目录执行，完全离线。结果返回合并后的入口与 `matched_capabilities`，其中 `guide_path` 指向具体模式。旧名称通过本地搜索兼容，不再保留 227 个独立目录，也不表示宿主会自动注册这些别名。

## 入口目录

| 入口 | 保留能力数 | 范围 |
|---|---:|---|
| [1688 货源发现与规格比价](sealeap-athena-1688-sourcing-research/SKILL.md) | 4 | 以图、关键词与热度检索作为不同模式；规格、MOQ 和报价口径逐项核对。 |
| [1688 采购与履约](sealeap-athena-1688-procurement/SKILL.md) | 1 | 采购写入与只读找货源保持独立入口，沿用实际授权范围。 |
| [Amazon 商品检索与筛选](sealeap-athena-amazon-product-discovery/SKILL.md) | 7 | 关键词、图片、条件和历史筛选按需路由；保留不同数据源的样本与筛选语义。 |
| [Amazon 商品情报与竞品比较](sealeap-athena-amazon-product-intelligence/SKILL.md) | 6 | 详情、比较、当前/历史价格排名与销量校准分别读取对应参考文件。 |
| [Amazon 细分市场与机会评估](sealeap-athena-amazon-market-assessment/SKILL.md) | 8 | 保留关键词/ASIN 两类市场入口、样本冻结、容量与竞争口径。 |
| [Amazon 关键词与搜索流量研究](sealeap-athena-amazon-keyword-traffic/SKILL.md) | 12 | 保留 ABA、反查、拓词、趋势、SERP 与 AI 回答观察的独立指标定义；不把可见度当点击份额。 |
| [Amazon 评论与反馈分析](sealeap-athena-amazon-review-insights/SKILL.md) | 3 | 公开评论、市场主题与自家账户反馈分模式，保留权限和采样差异。 |
| [Amazon Listing、素材与定价管理](sealeap-athena-amazon-listing-management/SKILL.md) | 6 | 查询、草稿、上传、批量提交与价格修改分别路由；明确每次外部写入的对象和授权。 |
| [Amazon 店铺报表、订单与履约](sealeap-athena-amazon-store-operations/SKILL.md) | 5 | 订单读取不隐含履约授权；授权检查、报表和政策核对作为相应任务模式。 |
| [Amazon 广告报表、诊断与管理](sealeap-athena-amazon-advertising-operations/SKILL.md) | 4 | 报表、专项洞察和广告变更分模式；广告 API 与 SP-API 的授权独立。 |
| [TikTok 商品与店铺研究](sealeap-athena-tiktok-commerce-research/SKILL.md) | 14 | 商品、店铺及内容关联分别取证，按市场与数据提供方保留样本边界。 |
| [TikTok 视频、直播与达人分析](sealeap-athena-tiktok-content-creator-research/SKILL.md) | 11 | 公开研究与已授权达人合作数据分别处理；研究不隐含发布或联络。 |
| [TikTok 内容账户与视频管理](sealeap-athena-tiktok-content-management/SKILL.md) | 3 | 内容账号授权与 TikTok Shop 授权独立；视频发布/关联按实际权限执行。 |
| [TikTok Shop 商品与经营分析](sealeap-athena-tiktok-shop-catalog-analytics/SKILL.md) | 3 | 保留店铺主体、地区、商品 schema 和经营指标口径。 |
| [TikTok Shop 订单、物流与售后](sealeap-athena-tiktok-shop-order-fulfillment/SKILL.md) | 4 | 查询、发货、退货和退款各有独立执行条件与回读要求。 |
| [Temu 市场、商品与店铺研究](sealeap-athena-temu-market-research/SKILL.md) | 7 | 第三方样本与官方账户数据分开；图片相似不等于同规格。 |
| [Temu 商品与价格管理](sealeap-athena-temu-product-pricing/SKILL.md) | 7 | 先确定美国/欧洲/全球区，再读取地区流程与 schema；不跨区复用端点或账号。 |
| [Temu 促销与广告管理](sealeap-athena-temu-growth-operations/SKILL.md) | 6 | 地区、促销类型与广告预算仍分别验证，保留各动作授权。 |
| [Temu 订单、发货与取消](sealeap-athena-temu-order-fulfillment/SKILL.md) | 9 | 订单查询不隐含发货/取消；每个地区维护独立操作参考。 |
| [Temu 退货与退款](sealeap-athena-temu-after-sales/SKILL.md) | 3 | 售后资金动作保留独立入口与地区差异。 |
| [Temu 合规材料与税务凭据](sealeap-athena-temu-compliance/SKILL.md) | 2 | 按地区、品类与用途判断，不能泛化认证结论或税务适用性。 |
| [Shopee 市场与商品研究](sealeap-athena-shopee-market-research/SKILL.md) | 2 | 保持公开研究与商家账户管理的权限区别。 |
| [Shopee 账户、店铺与事件配置](sealeap-athena-shopee-account-management/SKILL.md) | 6 | 账户健康、商户/店铺资料与事件订阅按模式处理，配置写入保留授权。 |
| [Shopee 商品目录与媒体管理](sealeap-athena-shopee-catalog-media/SKILL.md) | 5 | 商品、全球映射、分类和媒体的资源 ID 与上传要求分别保存。 |
| [Shopee 促销、广告与内容运营](sealeap-athena-shopee-growth-operations/SKILL.md) | 11 | 各促销类型保留适用条件和叠加限制；广告/直播/视频使用独立参考与授权。 |
| [Shopee 订单、仓配与售后](sealeap-athena-shopee-order-fulfillment/SKILL.md) | 6 | 保留 FBS/SBS、头程与尾程差异；发货退款分别核验。 |
| [Shopee 收款与结算](sealeap-athena-shopee-payments/SKILL.md) | 1 | 资金与结算保留独立入口，不与一般订单查询混为同一操作。 |
| [专利检索与文献获取](sealeap-athena-patent-discovery/SKILL.md) | 6 | 文字与视觉检索区分外观/技术专利；先确认文献身份和访问能力。 |
| [专利文档解析与翻译](sealeap-athena-patent-document-analysis/SKILL.md) | 8 | 按摘要、说明书、权利要求和附图选择参考；提取/翻译不替代法律解释。 |
| [专利法律状态、家族与引用](sealeap-athena-patent-status-landscape/SKILL.md) | 4 | 被引与在先引用方向、家族与法律状态独立保留，不把状态摘要当 FTO。 |
| [商品知识产权与受限品初筛](sealeap-athena-ip-compliance-screen/SKILL.md) | 7 | 版权、商标、外观、技术专利、诉讼和受限品分模式；所有结论仅初筛。 |
| [商品视觉分析与图片创作](sealeap-athena-commerce-visual-design/SKILL.md) | 8 | 分析与生成分模式；保留产品事实、素材权利、生成工具能力和调用费用边界。 |
| [电商文案与标题质检](sealeap-athena-commerce-copywriting/SKILL.md) | 2 | 通用草稿与 Amazon 标题核验分模式；保留平台语言、产品事实和规则。 |
| [商品视频素材、生成与核验](sealeap-athena-commerce-product-video/SKILL.md) | 3 | 授权素材获取、分镜与生成分模式；保留下载权利、模型限制和费用范围。 |
| [Walmart/Ozon 等平台商品研究](sealeap-athena-marketplace-research/SKILL.md) | 26 | 只合并研究入口；Walmart、Ozon、Etsy、eBay、Shopify 与 Mercado Libre 各用独立参考，禁止跨平台替代字段与混算指标。 |
| [公开搜索、热点与需求趋势](sealeap-athena-web-demand-research/SKILL.md) | 4 | 检索、搜索兴趣和 AI 回答观察按证据类型区分，保留时间与来源。 |
| [ERP 经营数据核对](sealeap-athena-erp-operating-data/SKILL.md) | 1 | 官方授权连接或用户导出；保留 ERP 指标与 Amazon 指标的区别。 |
| [电商多步骤任务编排](sealeap-athena-commerce-workflow/SKILL.md) | 1 | 按任务选择所需业务 Skill，不默认加载全部能力。 |
| [本地技能与旧名称检索](sealeap-athena-find-skills/SKILL.md) | 1 | 保留搜索入口，增加旧名称/能力到新入口及具体参考文件的映射。 |

## 工具和验证边界

原有 85 项具体数据路由仍保存在对应能力的工具说明与结构化索引中；其余按当前宿主、官方账户连接或授权导出处理。接口存在、格式校验或合并完成都不证明账户已授权、额度可用或线上动作成功。

同一入口中的模式独立选择，尤其保留 Temu 地区差异、平台账户权限、专利引用方向、第三方估计口径，以及查询和发布/退款/资金动作的区别。

原名称完整对应关系见 [迁移索引](MIGRATION.md) 与 [结构化映射](migration.json)，39 个入口及细分能力见 [catalog.json](catalog.json)。本次验证结果见 [VALIDATION.md](VALIDATION.md)。
