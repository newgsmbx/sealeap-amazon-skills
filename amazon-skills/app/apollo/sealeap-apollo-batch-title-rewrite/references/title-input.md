# 标题检查输入

输入为 UTF-8 CSV，必需列为 `sku,marketplace,product_type,title,highlight`。原列被保留，结果新增字符数、check_status 和 issues。

policy.json 需指定：

- `marketplace`：已核验站点代码。
- `product_types`：适用的明确类目类型数组，不能用无证据的全类目通配。
- `title_max`、`highlight_max`：当前模板的正整数上限。
- `count_method`：codepoints 或 utf16；与实际模板的计数方式核对。
- `verified`：是否已核对政策适用性。
- `source`、`checked_at`：政策或实际模板依据与核对时间。
- 可选 `highlight_required`、`banned_characters`、`banned_phrases`、`max_word_repeat`、`repeat_exempt_words`。

PASS 仅表示所填规则的本地检查通过；HOLD 表示规则未核验或行不在适用范围；FAIL 表示检测到规则内问题。脚本不证明产品陈述真实性、品牌规范、类目合规或线上接受状态。输出新文件，禁止覆盖输入。
