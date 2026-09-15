# 折扣计划输入

顶层字段：`store_ref`（用户指定的店铺别名）、`marketplace`、`snapshot_at`、`evidence_id`、`activities`、`targets`。

- activities：每项含 `promotion_id`、`status`、`items`。items 每项含 `sku` 和 `discount_percent`；此脚本只处理百分比折扣。
- targets：每项含 `sku`、`target_percent`，活动不唯一时需 `promotion_id`。
- 折扣百分比使用 0–100 数字，缺失用 null，不能从当前价反推。

输出 DRAFT / HOLD / NO_CHANGE，始终带 `submitted: false`。活动歧义、未知前值、未知状态或降低运行中折扣保持 HOLD。提交时必须在对应店铺重读状态，并核对此前导出的前值。
