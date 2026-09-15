# 经济输入

金额统一到同一可售单位和币种。`net_revenue_per_unit` 是扣除折扣和收入端税费后的净收入；`ad_revenue_per_order` 是与广告 ACOS 分母一致的每单归因销售额。两者可能不同，必须说明原因；多件订单先换成同一单位。

JSON 顶层需包含 `currency`、`net_revenue_per_unit`、`ad_revenue_per_order`、`target_acos`、`ad_cvr`、`unit_costs`、`evidence`。

- `unit_costs` 必须含 `purchase`、`inbound`、`platform`、`fulfillment`、`storage`、`returns`、`other`。零也需证据；费用不能在净收入端和成本端重复扣除。
- 每个数值用 `{value, label, evidence_id}`；金额额外带 `currency`。label 为 FACT / ESTIMATE / ASSUMPTION / UNKNOWN。
- `evidence` 为数组，每项有 `id`、`source`、`collected_at`、`data_period`。
- ACOS 与 CVR 用 0–1 小数，null 表示未知。目标 ACOS 通常是 ASSUMPTION，需说明经营依据。

脚本拒绝混币、负值、非有限数、重复 JSON 键、非法比率和零收入分母。缺值与证据不足返回 HOLD；CALCULATED 只表示输入足以按公式计算。
