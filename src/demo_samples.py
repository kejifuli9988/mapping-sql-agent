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
    "requirement": "",
    "skill_id": "none",
}


DEEPSEEK_SAMPLE: dict[str, Any] = {
    "title": "智能体增强样例",
    "description": "适合演示结合托管清算需求、Skill 和表结构上下文生成对账 SQL。",
    "mode": "deepseek",
    "mapping": {
        "task_name": "dws_custody_clearing_reconcile_day_demo",
        "target_table": "dws_custody_clearing_reconcile_day",
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
        "filters": [
            "cl.dt = '${biz_date}'",
            "cl.clear_dt = '${biz_date}'",
            "cl.clear_status in ('success', 'fail')",
        ],
        "target_columns": [
            {"name": "dt", "expression": "'${biz_date}'"},
            {"name": "product_id", "expression": "cl.product_id"},
            {"name": "product_name", "expression": "dp.product_name"},
            {"name": "clear_status", "expression": "cl.clear_status"},
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
