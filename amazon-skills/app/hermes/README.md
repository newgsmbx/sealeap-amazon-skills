# Hermes 应用专家能力集

Hermes（赫尔墨斯）是本集合的平台代号。10 个独立 Skill 覆盖跨境经营的 9 个业务领域与浏览器操作，均使用 `sealeap-hermes-...` 名称。

本集合由 **1 个原生浏览器 Skill 的迁移优化版**和 **9 个从专家主提示词拆解重写的业务 Skill**组成。这一数量是整理后的能力数量，不表示来源包原本有 10 个 Skill。

| Skill | 用途 | 入口 |
|---|---|---|
| 平台进入与经营规划 | 平台、站点、经营模式和试点决策 | [market-entry](sealeap-hermes-market-entry/SKILL.md) |
| 选品、竞品与单位经济 | 需求、评论、供应和贡献测算 | [product-research](sealeap-hermes-product-research/SKILL.md) |
| 多语言 Listing | 产品事实、关键词和创意草稿 | [listing-localization](sealeap-hermes-listing-localization/SKILL.md) |
| 广告诊断与实验 | 指标拆解、归因、预算与回退 | [advertising-diagnostics](sealeap-hermes-advertising-diagnostics/SKILL.md) |
| 物流与库存 | 仓配比较、到货时点与补货 | [logistics-inventory](sealeap-hermes-logistics-inventory/SKILL.md) |
| 合规、税务与 IP | 适用性和证据初筛 | [compliance-review](sealeap-hermes-compliance-review/SKILL.md) |
| 收款与现金流 | 费用、汇率、回款和资金缺口 | [payments-cashflow](sealeap-hermes-payments-cashflow/SKILL.md) |
| 品牌与独立站 | 网站体验、内容与获客验证 | [brand-dtc-growth](sealeap-hermes-brand-dtc-growth/SKILL.md) |
| 客服与售后 | 多语言回复、退货和争议材料 | [customer-service](sealeap-hermes-customer-service/SKILL.md) |
| 浏览器采集 | 版本识别、页面操作和证据留存 | [browser-research](sealeap-hermes-browser-research/SKILL.md) |

每个文件夹包含 `SKILL.md`、`agents/openai.yaml`、`references/playbook.md`、`LICENSE` 与 `NOTICE`。少数 Skill 带有实际需要的额外参考和脚本；复制整个 Skill 文件夹即可保留资源，不依赖同级其他 Skill。

```text
使用 sealeap-hermes-product-research。
目标：评估这个商品在指定站点是否值得试销。
先复用已提供且口径一致的数据；缺少成本、供应或市场证据时说明缺口。
输出竞品与规格比较、单位经济、下行情景和验证任务。
```

数据通路按现有能力选择卖家精灵、SIF、Sorftime、平台 API 或授权导出；帮助命令可用不代表在线鉴权、配额与实际数据已验证。浏览器适配先识别工具和 CLI 版本，缺少运行时则明确说明。

原有泛化阈值改为可解释的情景参数；业务数据保留来源、时间、范围与 FACT / ESTIMATE / ASSUMPTION / UNKNOWN。平台政策、服务费用和法律适用性在实际执行时重新核对。

## 许可

各 Skill 保留适用的 MIT 版权与许可文本，并在 NOTICE 中说明改编。品牌用语的清理不替代授权判断；平台商标、第三方数据与商品素材仍受各自权利和条款约束。上游声明按许可保留，集合代号不表示其背书。
