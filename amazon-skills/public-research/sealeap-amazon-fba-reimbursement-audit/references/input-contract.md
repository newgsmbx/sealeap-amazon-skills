# 赔偿对账输入

仅供离线核算，不读取发票内容、平台状态或银行到账。references/input.example.json 是 SYNTHETIC 演示数据。

## JSON

scope 包含 store_id、marketplace、currency、as_of（ISO 日期）。records 是非空列表，每项：

| 字段 | 含义 |
|---|---|
| event_id / sku | 唯一损失事件及商品；多笔付款先净额对账 |
| currency | 必须与 scope.currency 一致，不做隐式汇率换算 |
| event_stage | before_customer_order 才参与计算；其余进入人工队列 |
| affected_units | 本案真实损失的可售单位数量，正整数；不是在库量 |
| documented_unit_cost | 对应同一可售单位的采购/制造成本；必须有凭证 |
| already_reimbursed_net | 已赔净额；明确没有赔偿才能填 0 |
| policy_unit_cap | 当前本案政策的单件金额上限，由执行者核验，不使用内置常数 |
| evidence_ids | 非空成本证据 ID 列表；脚本不证明其真实性 |
| policy_eligibility_verified / unit_basis_verified | 只有已核验才填 true |
| reimbursement_window_status | 当前核验为 open 才纳入复核合计；closed/unknown 为 HOLD |

数值可用 JSON 数字或十进制字符串；金额非负。null/缺失保留 HOLD，不按零处理。输入重复键、重复事件、混合币种、布尔数值、负值、NaN 或 Infinity 都不能产生有效可申报结果。

## 算法和边界

核对基数 = min(凭证单位成本, 当前政策单件上限) × 损失单位数。
差额 = 核对基数 − 已赔净额。复核候选额 = max(0, 差额)。

仅 PASS 行进入 review_candidate_total_for_pass_rows；excluded_records 明确其余数量。存在 HOLD 时不能把小计称全量可追回金额。上限、资格及凭证是输入声明，必须人工/账户证据核实。单件上限未知时停止计算。

stdout 输出 JSON；退出码 0=计算完成，2=存在缺口，1=输入无效。PASS 不代表赔偿获批。
