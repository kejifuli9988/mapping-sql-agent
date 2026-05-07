# Mapping SQL Agent

一个面向数据开发场景的本地智能体原型：开发人员只需提供 `mapping` 文档，系统即可生成符合行内数据中台规范风格的 SQL 初稿，并输出规则校验结果，减少人工从需求到 SQL 的重复转换成本。

## 项目目标

结合题目背景，本项目解决以下问题：

1. 降低开发人员根据 Mapping 文档手写 SQL 的成本。
2. 将 SQL 规范内置到生成流程中，减少拼写、类型、逻辑遗漏等问题。
3. 让 Mapping 文档变成唯一输入源，减少文档与代码脱节。
4. 将通用 Join、过滤、聚合、插入模板沉淀为可复用能力。

## 核心能力

1. 仅提供 Mapping 文档即可生成 SQL。
2. SQL 输出遵循统一规范：
   - SQL 关键字大写
   - 表名、字段名、小写别名统一小写
   - 使用 `WITH` 分层组织来源表
   - `INSERT OVERWRITE TABLE` 输出目标表
   - 每个目标字段单独一行，便于评审
   - 显式 `JOIN`、`WHERE`、`GROUP BY`
3. 生成后自动执行规则校验，提示潜在问题。

## 目录结构

```text
.
├── README.md
├── main.py
├── examples
│   └── mapping_sales_summary.json
└── src
    ├── __init__.py
    ├── agent.py
    ├── mapping_loader.py
    ├── sql_generator.py
    └── sql_style.py
```

## Mapping 文档格式

当前原型使用 JSON 作为结构化 Mapping 文档输入，便于演示和扩展。后续可对接 Excel、Markdown、Word 导出的 Mapping。

示例字段说明：

- `task_name`: 任务名称
- `target_table`: 目标表
- `target_partition`: 目标分区
- `sources`: 来源表定义
- `joins`: 关联关系
- `filters`: 过滤条件
- `target_columns`: 目标字段与映射表达式

示例见 [examples/mapping_sales_summary.json](/C:/Users/Guozheyu/Documents/Codex/2026-04-28/1-mapping-sql-mapping-sql-2-2/examples/mapping_sales_summary.json)。

## 快速开始

```bash
python main.py --mapping examples/mapping_sales_summary.json
```

## Web 界面启动

```bash
python webapp.py --host 127.0.0.1 --port 8000
```

启动后打开 [http://127.0.0.1:8000](http://127.0.0.1:8000) 即可使用页面版智能体。

页面支持：

1. 加载示例 Mapping
2. 粘贴或编辑 JSON Mapping
3. 上传 `.xlsx` Excel Mapping，并自动解析回填
4. 下载 Excel Mapping 模板
5. 一键生成 SQL
6. 展示规范校验结果
7. 一键复制生成 SQL
8. 将 DeepSeek API Key 保存到浏览器本地缓存

## DeepSeek 增强模式

页面版已经支持可选的 DeepSeek 增强模式：

1. 在页面中将“生成模式”切换为 `DeepSeek 增强`
2. 输入 `DeepSeek API Key`
3. 模型默认使用 `deepseek-v4-flash`
4. 点击“生成 SQL”

如果 DeepSeek 调用失败，系统会自动回退到本地规则模式，保证演示不中断。

当 Mapping 输入不是合法 JSON 时：

1. 规则模式会直接给出解析报错
2. DeepSeek 增强模式会尝试自动修复 Mapping
3. 页面会展示 Mapping 诊断和修复后的 Mapping

你也可以使用环境变量：

```bash
set DEEPSEEK_API_KEY=你的key
python webapp.py --host 127.0.0.1 --port 8000
```

## 输出内容

程序会输出三部分：

1. 任务摘要
2. SQL 生成结果
3. 规范校验结果

## 设计思路

### 1. 智能体分层

- `MappingLoader`: 负责解析 Mapping 文档
- `SQLGenerator`: 负责按模板和规则组装 SQL
- `SQLStyleChecker`: 负责规范校验
- `MappingSQLAgent`: 负责串联整个流程

### 2. 为什么先做“规则优先”

真实数据开发场景下，字段映射、聚合、Join、分区写入等内容大多有稳定结构。先使用规则引擎生成可审阅 SQL，再逐步接入大模型补充复杂推理，整体更稳、更便于在行内场景落地。

### 3. 后续可扩展方向

1. 支持读取 Excel Mapping 文档。
2. 接入大模型完成自然语言规则补全。
3. 自动对比 Mapping 变更与历史 SQL，输出增量修改建议。
4. 对接行内代码仓库与评审流程，形成生成、校验、审查闭环。

## 适合作为答辩时的表达

可以将本项目描述为：

> 一个以 Mapping 文档为单一事实来源、面向数据中台 SQL 开发的智能体原型。它把 Mapping 解析、SQL 生成、规范约束和结果校验合并到同一链路中，降低人工编码与评审成本，并为后续接入大模型与企业规范沉淀提供基础底座。
