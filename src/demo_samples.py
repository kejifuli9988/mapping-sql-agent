from __future__ import annotations

from copy import deepcopy
from typing import Any


RULE_SAMPLE: dict[str, Any] = {
    "title": "模板生成样例",
    "description": "适合演示仅依赖 Mapping 自动生成标准化 SQL 的流程。",
    "mode": "rule",
    "mapping": {
        "task_name": "dws_retail_product_sales_day_demo",
        "target_table": "dws_retail_product_sales_day",
        "target_partition": "dt='${biz_date}'",
        "sources": [
            {"name": "ods_order_detail_di", "alias": "od"},
            {"name": "dim_product_info_df", "alias": "dp"},
        ],
        "joins": [
            {
                "type": "left",
                "right_alias": "dp",
                "condition": "od.product_id = dp.product_id",
            }
        ],
        "filters": [
            "od.dt = '${biz_date}'",
            "od.order_status = 'success'",
        ],
        "target_columns": [
            {"name": "dt", "expression": "'${biz_date}'"},
            {"name": "product_id", "expression": "od.product_id"},
            {"name": "product_name", "expression": "dp.product_name"},
            {"name": "sales_amt", "expression": "SUM(od.pay_amt)"},
            {"name": "order_cnt", "expression": "COUNT(DISTINCT od.order_id)"},
        ],
    },
    "requirement": "",
    "skill_id": "none",
}


DEEPSEEK_SAMPLE: dict[str, Any] = {
    "title": "DeepSeek 增强样例",
    "description": "适合演示结合业务需求与 Mapping 生成更贴近业务口径的 SQL。",
    "mode": "deepseek",
    "mapping": {
        "task_name": "dws_retail_region_product_sales_day_demo",
        "target_table": "dws_retail_region_product_sales_day",
        "target_partition": "dt='${biz_date}'",
        "sources": [
            {"name": "ods_order_detail_di", "alias": "od"},
            {"name": "dim_product_info_df", "alias": "dp"},
            {"name": "dim_store_info_df", "alias": "ds"},
        ],
        "joins": [
            {
                "type": "left",
                "right_alias": "dp",
                "condition": "od.product_id = dp.product_id",
            },
            {
                "type": "left",
                "right_alias": "ds",
                "condition": "od.store_id = ds.store_id",
            },
        ],
        "filters": [
            "od.dt = '${biz_date}'",
            "od.order_status = 'success'",
            "od.pay_amt > 0",
        ],
        "target_columns": [
            {"name": "dt", "expression": "'${biz_date}'"},
            {"name": "region_name", "expression": "ds.region_name"},
            {"name": "product_id", "expression": "od.product_id"},
            {"name": "product_name", "expression": "dp.product_name"},
            {"name": "sales_amt", "expression": "SUM(od.pay_amt)"},
            {"name": "order_cnt", "expression": "COUNT(DISTINCT od.order_id)"},
            {"name": "buyer_cnt", "expression": "COUNT(DISTINCT od.user_id)"},
        ],
    },
    "requirement": (
        "请生成按大区和产品汇总的日销售 SQL，只统计支付成功订单。"
        " 需要输出销售额、订单数和购买用户数，并遵循银行数据中台 SQL 规范。"
    ),
    "skill_id": "product_aggregation",
}


COMPARE_HISTORY_V1: dict[str, Any] = {
    "task_name": "dws_sales_compare_judge_demo",
    "target_table": "dws_sales_compare_judge_demo",
    "target_partition": "dt='${biz_date}'",
    "sources": [
        {"name": "ods_order_detail_di", "alias": "od"},
        {"name": "dim_product_info_df", "alias": "dp"},
    ],
    "joins": [
        {
            "type": "left",
            "right_alias": "dp",
            "condition": "od.product_id = dp.product_id",
        }
    ],
    "filters": [
        "od.dt = '${biz_date}'",
        "od.order_status = 'success'",
    ],
    "target_columns": [
        {"name": "dt", "expression": "'${biz_date}'"},
        {"name": "product_id", "expression": "od.product_id"},
        {"name": "product_name", "expression": "dp.product_name"},
        {"name": "sales_amt", "expression": "SUM(od.pay_amt)"},
        {"name": "order_cnt", "expression": "COUNT(DISTINCT od.order_id)"},
    ],
}


COMPARE_HISTORY_V2: dict[str, Any] = {
    "task_name": "dws_sales_compare_judge_demo",
    "target_table": "dws_sales_compare_judge_demo",
    "target_partition": "dt='${biz_date}'",
    "sources": [
        {"name": "ods_order_detail_di", "alias": "od"},
        {"name": "dim_product_info_df", "alias": "dp"},
        {"name": "dim_store_info_df", "alias": "ds"},
    ],
    "joins": [
        {
            "type": "left",
            "right_alias": "dp",
            "condition": "od.product_id = dp.product_id",
        },
        {
            "type": "left",
            "right_alias": "ds",
            "condition": "od.store_id = ds.store_id",
        },
    ],
    "filters": [
        "od.dt = '${biz_date}'",
        "od.order_status = 'success'",
        "od.pay_amt > 100",
    ],
    "target_columns": [
        {"name": "dt", "expression": "'${biz_date}'"},
        {"name": "city_name", "expression": "ds.city_name"},
        {"name": "product_id", "expression": "od.product_id"},
        {"name": "product_name", "expression": "dp.product_name"},
        {"name": "sales_amt", "expression": "SUM(od.pay_amt)"},
        {"name": "order_cnt", "expression": "COUNT(DISTINCT od.order_id)"},
    ],
}


COMPARE_CURRENT: dict[str, Any] = {
    "task_name": "dws_sales_compare_judge_demo",
    "target_table": "dws_sales_compare_judge_demo",
    "target_partition": "dt='${biz_date}'",
    "sources": [
        {"name": "ods_order_detail_di", "alias": "od"},
        {"name": "dim_product_info_df", "alias": "dp"},
        {"name": "dim_store_info_df", "alias": "ds"},
        {"name": "dim_pay_channel_df", "alias": "pc"},
    ],
    "joins": [
        {
            "type": "left",
            "right_alias": "dp",
            "condition": "od.product_id = dp.product_id",
        },
        {
            "type": "left",
            "right_alias": "ds",
            "condition": "od.store_id = ds.store_id",
        },
        {
            "type": "left",
            "right_alias": "pc",
            "condition": "od.pay_channel_code = pc.pay_channel_code",
        },
    ],
    "filters": [
        "od.dt = '${biz_date}'",
        "od.order_status = 'success'",
        "od.pay_amt > 100",
        "ds.store_type = 'direct'",
    ],
    "target_columns": [
        {"name": "dt", "expression": "'${biz_date}'"},
        {"name": "city_name", "expression": "ds.city_name"},
        {"name": "product_id", "expression": "od.product_id"},
        {"name": "product_name", "expression": "dp.product_name"},
        {"name": "pay_channel_name", "expression": "pc.pay_channel_name"},
        {"name": "sales_amt", "expression": "SUM(od.pay_amt)"},
        {"name": "order_cnt", "expression": "COUNT(DISTINCT od.order_id)"},
        {"name": "buyer_cnt", "expression": "COUNT(DISTINCT od.user_id)"},
    ],
}


COMPARE_SAMPLE: dict[str, Any] = {
    "title": "版本对比样例",
    "description": (
        "适合演示需求变化和 Mapping 变更如何触发 SQL 自动追踪。"
        " 历史版本从“按产品汇总”逐步变化为“按城市汇总且限制金额”，"
        " 当前版本再新增支付渠道维度和直营网点过滤条件。"
    ),
    "task_name": "dws_sales_compare_judge_demo",
    "history_versions": [
        {
            "version_label": "v0001",
            "mode": "rule",
            "user_requirement": "",
            "mapping": COMPARE_HISTORY_V1,
        },
        {
            "version_label": "v0002",
            "mode": "deepseek",
            "user_requirement": "请按城市和产品汇总销售额，只统计支付成功且金额大于100的订单。",
            "mapping": COMPARE_HISTORY_V2,
        },
    ],
    "current": {
        "mode": "deepseek",
        "skill_id": "kpi_metrics",
        "requirement": (
            "在原有按城市和产品汇总的基础上，新增支付渠道维度，"
            "只统计直营网点订单，并输出销售额、订单数、购买用户数。"
        ),
        "mapping": COMPARE_CURRENT,
    },
}


def get_demo_samples() -> dict[str, Any]:
    return {
        "builder_rule": deepcopy(RULE_SAMPLE),
        "builder_deepseek": deepcopy(DEEPSEEK_SAMPLE),
        "compare": deepcopy(COMPARE_SAMPLE),
    }
