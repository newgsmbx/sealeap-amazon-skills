# Sorftime 工具路由

直接能力：`mcp__sorftime_server__category_report_from_history`。

当前声明：

```ts
declare const tools: { mcp__sorftime_server__category_report_from_history(args: {
  // Amazon marketplace site.
  amz_site?: "Unknow" | "US" | "GB" | "DE" | "FR" | "CA" | "JP" | "ES" | "IT" | "MX" | "AE" | "BR" | "SA";
  // View historical data; after specifying start_date, this specifies the end date. Supports a max combination of 40 days.
  end_date: string;
  // Sub-category node_id, query this specific sub-category data; data type: string.
  node_id: string;
  // View historical data; specify the start date in yyyy-MM-dd format.
  start_date: string;
}): Promise<CallToolResult>; };
```

必填与可选字段由上面声明确定。业务需要的站点或窗口仍须明确；`Unknow` 不作为有效站点替代。

## 实际执行

先复用范围匹配的授权导出或历史结果，再选择当前可用连接器。下列映射只验证了接口声明或本地代码，未验证在线鉴权、配额和真实返回。运行时重新查看工具 schema；存在同名工具也不等于字段、窗口、分页语义相同。

保留原始响应与业务状态，工具错误不得转成空数组。未提供的筛选器只可在已取得的样本上筛选，并披露样本边界。没有可用通路时交付缺口和可用数据分析，不编造接口或用其他数据源冒充指定提供方。
