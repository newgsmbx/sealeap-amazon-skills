# SQP 归一化输入

本脚本接收经过字段映射的 JSON，不自动猜测 CSV 列名。保存原始导出和映射记录在任务目录；不要把私有经营数据放进 Skill。

## 范围

scope 必填 account_id、marketplace、view（BRAND/ASIN）、entity_id、report_definition、timezone。
window_start/window_end 是目标完整分析窗口的 ISO 日期。
periods 每项包含唯一 id、start、end、complete、mature。首尾含当天，周期必须互斥且覆盖目标窗口；缺口/未成熟产生 HOLD，重叠或越界拒绝。不得按天数切分已有汇总报告。

## 记录

rows 每项包含 period_id、query，以及：

- query_volume；
- market_impressions、entity_impressions；
- market_clicks、entity_clicks；
- market_cart_adds、entity_cart_adds；
- market_purchases、entity_purchases。

计数是非负整数，空白转 null。零必须来自实际报表。每个 query + period_id 只允许一行。若行或周期附有范围字段，必须与 scope 一致。归一化前核对每份原始文件的店铺/实体/视图；不能删除不同 ASIN 的标识后拼在一起。

只去查询首尾空格，不擅自合并近义词、大小写变体或翻译词。查询在某期没出现可能是截断/筛选/未覆盖，不能自动添全零行。

## 输出含义

observed_partial_counts 是已观测小计；full_window_counts 只有同一指标覆盖全部完整、成熟周期才有值，否则 null。
metrics_fraction 是 0–1 比例，不是百分数。分母为零时 null，不产生无穷大。
脚本不汇总 median price、query score、导出份额或多个实体的市场分母。

合成示例购买份额为 (1+90)/(10+100)=0.827273，而非两期份额均值。退出码 0=完整，2=缺口或空报告，1=输入冲突。
