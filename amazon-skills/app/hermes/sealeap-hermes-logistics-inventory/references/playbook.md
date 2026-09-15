# 跨境物流与库存规划执行手册

## 可售库存投影

`projected_available(t) = sellable_now + receipts_available_by(t) - committed_not_already_excluded - forecast_demand_until(t)`。

先检查可售字段是否已经扣除了订单预留；不能再次扣减同一预留。收货数量只能从预计“可售日”加入。列出每日或每周行，避免只用总在途量掩盖早期缺货。

安全库存依赖需求与补货周期的波动、服务目标和资金约束；数据不足时给情景区间，不捏造标准差。补货量根据目标覆盖日库存缺口计算，再受 MOQ、箱规、资金与仓容约束。

## 物流报价表

`route, origin, destination, incoterm, quote_date, expires_at, currency, actual_weight, volumetric_weight, chargeable_weight, divisor, rounding_rule, transit_p50, transit_p90, customs_days, receiving_days, first_mile, clearance, duty, storage, handling, last_mile, return_cost, exclusions, evidence_id`

头程与末端费是否已含在报价、平台配送费或 3PL 服务包中必须逐项核对。没有 P50/P90 数据时记录承运商承诺区间，不伪装成统计分位数。

## 库龄与处置

按实际入库批次与当前平台费用分段计算。比较继续存放、折扣清货、调拨、退供、移除的预计净回收与现金时点；已发生采购成本与未来增量处置成本分开显示。

## 交付表

SKU、可售库存时间戳、在途批次/可售日、需求区间、最早缺货日、应急数量/费用、常规数量、资金需求、责任人、复核日期。明确所有数量是件还是可售套装。
