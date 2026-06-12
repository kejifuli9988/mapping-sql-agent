from __future__ import annotations

from copy import deepcopy
from typing import Any


RULE_SAMPLE: dict[str, Any] = {
    "title": "模板生成样例",
    "description": "适合演示基于托管清算 Mapping 自动生成标准 SQL 的流程。",
    "mode": "rule",
    "mapping": {
        "task_name": "dws_custody_product_clearing_day_demo",
        "target_table": "dws_custody_product_clearing_day",
        "target_partition": "dt='${biz_date}'",
        "sources": [
            {"name": "dwd_custody_clearing_detail_di", "alias": "cl"},
            {"name": "dim_custody_product_df", "alias": "dp"},
        ],
        "joins": [
            {
                "type": "left",
                "right_alias": "dp",
                "condition": "cl.product_id = dp.product_id",
            }
        ],
        "filters": [
            "cl.dt = '${biz_date}'",
            "cl.clear_status in ('success', 'fail')",
        ],
        "target_columns": [
            {"name": "dt", "expression": "'${biz_date}'"},
            {"name": "product_id", "expression": "cl.product_id"},
            {"name": "product_name", "expression": "dp.product_name"},
            {"name": "clear_amt", "expression": "SUM(cl.clear_amt)"},
            {"name": "clear_cnt", "expression": "COUNT(DISTINCT cl.clear_id)"},
            {
                "name": "fail_cnt",
                "expression": "SUM(CASE WHEN cl.clear_status = 'fail' THEN 1 ELSE 0 END)",
            },
        ],
    },
    "requirement": "请生成托管产品清算日汇总 SQL，按产品输出产品名称、清算金额、清算笔数和失败笔数，并只保留指定业务日期分区数据。",
    "skill_id": "none",
}


DEEPSEEK_SAMPLE: dict[str, Any] = {
    "title": "智能体增强样例",
    "description": "适合演示结合托管清算需求、Skill 和表结构上下文生成对账 SQL。",
    "mode": "deepseek",
    "mapping_text": """[字段需求]
序号 | 字段英文名 | 字段中文名 | 业务口径说明 | 来源系统 | 来源表 | 来源字段 | DA试算逻辑 | 备注
1 |  | 产品编号 | 托管产品唯一标识 | 托管清算 | dwd_custody_clearing_detail_di | product_id | product_id | 
2 |  | 产品名称 | 产品展示名称 | 产品维表 | dim_custody_product_df | product_name | product_name | 需通过 product_id 关联维表获取
3 |  | 清算状态 | 清算处理状态 | 托管清算 | dwd_custody_clearing_detail_di | clear_status | clear_status | 需区分 success、fail、processing
4 |  | 交易金额 | 交易侧汇总金额 | 托管交易 | dwd_custody_trade_detail_di | trade_amt | SUM(trade_amt) | 与清算金额做差异核对
5 |  | 清算金额 | 清算侧汇总金额 | 托管清算 | dwd_custody_clearing_detail_di | clear_amt | SUM(clear_amt) | 
6 |  | 差异金额 | 清算金额减交易金额 | 托管清算 | dwd_custody_clearing_detail_di | clear_amt | SUM(clear_amt - trade_amt) | 需关联交易明细表
7 |  | 清算笔数 | 清算流水笔数 | 托管清算 | dwd_custody_clearing_detail_di | clear_id | COUNT(DISTINCT clear_id) | 
8 |  | 失败笔数 | 清算失败流水笔数 | 托管清算 | dwd_custody_clearing_detail_di | clear_status | SUM(CASE WHEN clear_status = 'fail' THEN 1 ELSE 0 END) | 

[源表结构]
表名 | 中文说明 | 关键字段 | 分区字段 | 更新频率
dwd_custody_clearing_detail_di | 托管清算明细事实表 | clear_id, trade_id, product_id, account_id, clear_status, clear_amt, clear_dt | dt | T+1
dwd_custody_trade_detail_di | 托管交易明细事实表 | trade_id, product_id, trade_amt, trade_dt | dt | T+1
dim_custody_product_df | 托管产品维表 | product_id, product_name, product_type | dt | T+1

[加工逻辑]
1. 以托管清算明细表为主表，统计指定业务日期的清算结果
2. 通过 trade_id 关联托管交易明细表，获取交易金额并计算差异金额
3. 通过 product_id 关联产品维表，补充产品名称
4. 结果按产品编号、产品名称、清算状态汇总
5. 所有事实表均使用 dt='${biz_date}' 过滤""",
    "schema_text": """[table] dwd_custody_clearing_detail_di
表用途：托管清算明细事实表
更新频率：T+1
分区字段：dt
字段名 | 类型 | 说明
clear_id | STRING | 清算流水号
trade_id | STRING | 交易流水号
product_id | STRING | 产品编号
account_id | STRING | 托管账户号
clear_status | STRING | 清算状态
clear_amt | DECIMAL(18,2) | 清算金额
clear_dt | STRING | 清算日期
dt | STRING | 分区日期

[table] dwd_custody_trade_detail_di
表用途：托管交易明细事实表
更新频率：T+1
分区字段：dt
字段名 | 类型 | 说明
trade_id | STRING | 交易流水号
product_id | STRING | 产品编号
trade_amt | DECIMAL(18,2) | 交易金额
trade_dt | STRING | 交易日期
dt | STRING | 分区日期

[table] dim_custody_product_df
表用途：托管产品维表
更新频率：T+1
分区字段：dt
字段名 | 类型 | 说明
product_id | STRING | 产品编号
product_name | STRING | 产品名称
product_type | STRING | 产品类型
dt | STRING | 分区日期""",
    "requirement": "请生成托管清算对账日汇总 SQL，按产品和清算状态统计交易金额、清算金额、差异金额、清算笔数和失败笔数，只保留指定业务日期分区，并保留可用于核对的产品维度。",
    "skill_id": "custody_clearing_reconcile",
}


COMPARE_SAMPLE: dict[str, Any] = {
    "title": "版本对比样例",
    "description": "适合演示同一清算汇总任务在不同版本中的口径演进。",
    "mode": "compare",
    "history": [
        {
            "version": "v1_product_summary",
            "mapping": {
                "task_name": "dws_custody_clearing_compare_demo",
                "target_table": "dws_custody_product_clearing_day",
                "target_partition": "dt='${biz_date}'",
                "sources": [{"name": "dwd_custody_clearing_detail_di", "alias": "cl"}],
                "filters": ["cl.dt = '${biz_date}'"],
                "target_columns": [
                    {"name": "dt", "expression": "'${biz_date}'"},
                    {"name": "product_id", "expression": "cl.product_id"},
                    {"name": "clear_amt", "expression": "SUM(cl.clear_amt)"},
                    {"name": "clear_cnt", "expression": "COUNT(DISTINCT cl.clear_id)"},
                ],
            },
            "requirement": "按产品汇总每日托管清算金额和清算笔数。",
            "skill_id": "product_clearing_summary",
        },
        {
            "version": "v2_status_reconcile",
            "mapping": {
                "task_name": "dws_custody_clearing_compare_demo",
                "target_table": "dws_custody_clearing_reconcile_day",
                "target_partition": "dt='${biz_date}'",
                "sources": [
                    {"name": "dwd_custody_clearing_detail_di", "alias": "cl"},
                    {"name": "dwd_custody_trade_detail_di", "alias": "tr"},
                ],
                "joins": [
                    {"type": "left", "right_alias": "tr", "condition": "cl.trade_id = tr.trade_id"}
                ],
                "filters": ["cl.dt = '${biz_date}'"],
                "target_columns": [
                    {"name": "dt", "expression": "'${biz_date}'"},
                    {"name": "product_id", "expression": "cl.product_id"},
                    {"name": "clear_status", "expression": "cl.clear_status"},
                    {"name": "trade_amt", "expression": "SUM(tr.trade_amt)"},
                    {"name": "clear_amt", "expression": "SUM(cl.clear_amt)"},
                    {"name": "diff_amt", "expression": "SUM(cl.clear_amt - tr.trade_amt)"},
                    {"name": "clear_cnt", "expression": "COUNT(DISTINCT cl.clear_id)"},
                ],
            },
            "requirement": "在产品汇总基础上增加清算状态和交易金额核对，输出清算差异金额。",
            "skill_id": "custody_clearing_reconcile",
        },
    ],
    "current": {
        "version": "v3_failure_kpi",
        "mapping": {
            "task_name": "dws_custody_clearing_compare_demo",
            "target_table": "dws_custody_clearing_kpi_day",
            "target_partition": "dt='${biz_date}'",
            "sources": [
                {"name": "dwd_custody_clearing_detail_di", "alias": "cl"},
                {"name": "dwd_custody_trade_detail_di", "alias": "tr"},
                {"name": "dim_custody_product_df", "alias": "dp"},
            ],
            "joins": [
                {"type": "left", "right_alias": "tr", "condition": "cl.trade_id = tr.trade_id"},
                {"type": "left", "right_alias": "dp", "condition": "cl.product_id = dp.product_id"},
            ],
            "filters": ["cl.dt = '${biz_date}'"],
            "target_columns": [
                {"name": "dt", "expression": "'${biz_date}'"},
                {"name": "product_id", "expression": "cl.product_id"},
                {"name": "product_name", "expression": "dp.product_name"},
                {"name": "clear_status", "expression": "cl.clear_status"},
                {"name": "fail_reason", "expression": "cl.fail_reason"},
                {"name": "trade_amt", "expression": "SUM(tr.trade_amt)"},
                {"name": "clear_amt", "expression": "SUM(cl.clear_amt)"},
                {"name": "diff_amt", "expression": "SUM(cl.clear_amt - tr.trade_amt)"},
                {"name": "clear_cnt", "expression": "COUNT(DISTINCT cl.clear_id)"},
                {
                    "name": "fail_cnt",
                    "expression": "SUM(CASE WHEN cl.clear_status = 'fail' THEN 1 ELSE 0 END)",
                },
            ],
        },
        "requirement": "增加失败原因维度，形成托管清算 KPI 与失败原因分析结果，便于定位清算差异和失败集中场景。",
        "skill_id": "clearing_failure_analysis",
    },
}


def get_demo_samples() -> dict[str, Any]:
    return {
        "builder_rule": deepcopy(RULE_SAMPLE),
        "builder_deepseek": deepcopy(DEEPSEEK_SAMPLE),
        "compare": deepcopy(COMPARE_SAMPLE),
    }
