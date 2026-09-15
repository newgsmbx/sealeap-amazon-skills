# 工具选择与能力边界

先检查当前 Agent 暴露的工具、已安装连接和同口径本地材料。只选择本任务需要的能力；下面是已核对的路由，执行参数以当前 schema 或 CLI 帮助为准。身份、市场、配额、计费与实际数据响应在执行时另行确认。

## 已有 CLI 直连

先使用 `command -v ecomi` 定位；若不在 PATH，从已配置项目的 `.venv/bin/ecomi` 定位，不自动重装或读取凭证内容。

先运行 `ecomi mpstats --help` 核对选项。工具安装和帮助可用只证明接口存在，不证明已登录、有配额或能访问目标数据。

使用 `ecomi mpstats -m oz --list` 检查 Ozon endpoint。`--sku` 是 Ozon 商品 ID；`--path` 是类目路径；日期使用 `--d1` / `--d2`。品牌和卖家 endpoint 的参数从当前配置或官方文档读取；额外参数用 `--params` / `--body`，不臆造新 CLI 开关。

显式使用 `-m oz`。Python 方法名 `keyword_frequency` 对应 CLI endpoint `keyword_freq`；不要调用跨平台的 `keyword_wb_freq` 来冒充 Ozon 搜索频次。

- `item_keywords`：按当前 endpoint/method schema 填写业务输入。

已授权调用仍需尊重样本和费用范围。只在当前工具确实覆盖相同市场、实体、时间与指标时换用其他提供方；不能保留原指标名称却悄悄替换成含义不同的数据。

## 本任务不能被替换掉的语义

曝光排名不是转化；缺关键词端点时不以通用词扩写冒充反查。

接入检查只代表工具存在。新任务中必须根据真实返回记录成功、失败、空结果、字段缺失与数据时间；不得将本地格式校验标成在线业务验证。
