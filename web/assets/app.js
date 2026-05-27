const mappingInput = document.getElementById("mappingInput");
const requirementInput = document.getElementById("requirementInput");
const requirementSection = document.getElementById("requirementSection");
const summaryCard = document.getElementById("summaryCard");
const versionCard = document.getElementById("versionCard");
const requirementCard = document.getElementById("requirementCard");
const builderAiContextCard = document.getElementById("builderAiContextCard");
const builderSchemaAssistCard = document.getElementById("builderSchemaAssistCard");
const sqlOutput = document.getElementById("sqlOutput");
const draftSqlOutput = document.getElementById("draftSqlOutput");
const normalizedMappingOutput = document.getElementById("normalizedMappingOutput");
const mappingDiagnosisList = document.getElementById("mappingDiagnosisList");
const ruleProfileList = document.getElementById("ruleProfileList");
const issuesList = document.getElementById("issuesList");
const fieldChecksList = document.getElementById("fieldChecksList");
const formMessage = document.getElementById("formMessage");
const loadDemoBtn = document.getElementById("loadDemoBtn");
const inlineDownloadTemplateBtn = document.getElementById("inlineDownloadTemplateBtn");
const generateBtn = document.getElementById("generateBtn");
const copySqlBtn = document.getElementById("copySqlBtn");
const copyCompareSqlBtn = document.getElementById("copyCompareSqlBtn");
const copyOptimizedSqlBtn = document.getElementById("copyOptimizedSqlBtn");
const modeSelect = document.getElementById("modeSelect");
const builderModeSegment = document.getElementById("builderModeSegment");
const builderModeSegmentButtons = Array.from(document.querySelectorAll("[data-mode-value]"));
const builderEnhancementSection = document.getElementById("builderEnhancementSection");
const excelInput = document.getElementById("excelInput");
const builderMappingUploadCard = document.querySelector(".builder-mapping-upload-card");
const mappingUploadTitle = document.getElementById("mappingUploadTitle");
const mappingUploadDescription = document.getElementById("mappingUploadDescription");
const mappingUploadHint = document.getElementById("mappingUploadHint");
const mappingUploadButtonText = document.getElementById("mappingUploadButtonText");
const builderSkillSelect = document.getElementById("builderSkillSelect");
const builderSchemaAssistCheckbox = document.getElementById("builderSchemaAssistCheckbox");
const builderSchemaAssistSection = document.getElementById("builderSchemaAssistSection");
const builderSchemaFileInput = document.getElementById("builderSchemaFileInput");
const downloadBuilderSchemaTemplateBtn = document.getElementById("downloadBuilderSchemaTemplateBtn");
const analyzeBuilderSchemaBtn = document.getElementById("analyzeBuilderSchemaBtn");
const builderSchemaInput = document.getElementById("builderSchemaInput");
const builderSchemaMessage = document.getElementById("builderSchemaMessage");

const builderModeBtn = document.getElementById("builderModeBtn");
const compareModeBtn = document.getElementById("compareModeBtn");
const insightModeBtn = document.getElementById("insightModeBtn");
const schemaModeBtn = document.getElementById("schemaModeBtn");
const builderView = document.getElementById("builderView");
const compareView = document.getElementById("compareView");
const insightView = document.getElementById("insightView");
const schemaView = document.getElementById("schemaView");

const refreshTasksBtn = document.getElementById("refreshTasksBtn");
const taskSelect = document.getElementById("taskSelect");
const historyVersionSelect = document.getElementById("historyVersionSelect");
const loadHistoryBtn = document.getElementById("loadHistoryBtn");
const compareBtn = document.getElementById("compareBtn");
const compareSummaryCard = document.getElementById("compareSummaryCard");
const historyMappingOutput = document.getElementById("historyMappingOutput");
const historySqlOutput = document.getElementById("historySqlOutput");
const mappingImpactList = document.getElementById("mappingImpactList");
const compareEnhancementSection = document.getElementById("compareEnhancementSection");
const compareRequirementSection = document.getElementById("compareRequirementSection");
const compareRequirementInput = document.getElementById("compareRequirementInput");
const compareMappingInput = document.getElementById("compareMappingInput");
const compareAiContextCard = document.getElementById("compareAiContextCard");
const compareSkillSelect = document.getElementById("compareSkillSelect");
const currentCompareSqlOutput = document.getElementById("currentCompareSqlOutput");
const sqlDiffOutput = document.getElementById("sqlDiffOutput");
const mappingDiffOutput = document.getElementById("mappingDiffOutput");

const sqlInsightInput = document.getElementById("sqlInsightInput");
const sqlInsightFileInput = document.getElementById("sqlInsightFileInput");
const analyzeSqlBtn = document.getElementById("analyzeSqlBtn");
const sqlInsightMessage = document.getElementById("sqlInsightMessage");
const insightSkillSelect = document.getElementById("insightSkillSelect");
const insightSchemaAssistCheckbox = document.getElementById("insightSchemaAssistCheckbox");
const insightSchemaAssistSection = document.getElementById("insightSchemaAssistSection");
const insightSchemaFileInput = document.getElementById("insightSchemaFileInput");
const analyzeInsightSchemaBtn = document.getElementById("analyzeInsightSchemaBtn");
const insightSchemaInput = document.getElementById("insightSchemaInput");
const insightSchemaMessage = document.getElementById("insightSchemaMessage");
const insightAiContextCard = document.getElementById("insightAiContextCard");
const insightSchemaAssistCard = document.getElementById("insightSchemaAssistCard");
const sqlPurposeList = document.getElementById("sqlPurposeList");
const sqlStructureCard = document.getElementById("sqlStructureCard");
const sqlSuggestionList = document.getElementById("sqlSuggestionList");
const optimizedSqlOutput = document.getElementById("optimizedSqlOutput");
const optimizedSqlDiffOutput = document.getElementById("optimizedSqlDiffOutput");

const schemaInput = document.getElementById("schemaInput");
const schemaFileInput = document.getElementById("schemaFileInput");
const downloadSchemaTemplateBtn = document.getElementById("downloadSchemaTemplateBtn");
const analyzeSchemaBtn = document.getElementById("analyzeSchemaBtn");
const schemaMessage = document.getElementById("schemaMessage");
const schemaFieldsOutput = document.getElementById("schemaFieldsOutput");
const schemaPurposeCard = document.getElementById("schemaPurposeCard");
const schemaKeyFieldsCard = document.getElementById("schemaKeyFieldsCard");
const schemaReuseList = document.getElementById("schemaReuseList");

const SQL_INSIGHT_SAMPLE = `WITH orders AS (
    SELECT
        *
    FROM ods_order_detail_di
    WHERE dt = '\${biz_date}'
      AND order_status = 'success'
)
INSERT OVERWRITE TABLE dws_product_sales_day
PARTITION (dt = '\${biz_date}')
SELECT
    product_id,
    COUNT(DISTINCT order_id) AS order_cnt,
    COUNT(DISTINCT user_id) AS buyer_cnt,
    SUM(pay_amt) AS sales_amt
FROM orders
GROUP BY
    product_id;`;
const SCHEMA_SAMPLE = `CREATE TABLE dwd_account_trade_detail_di (
    trade_id STRING COMMENT '交易流水号',
    user_id STRING COMMENT '客户号',
    account_id STRING COMMENT '账户号',
    product_id STRING COMMENT '产品编号',
    trade_dt STRING COMMENT '交易日期',
    trade_time STRING COMMENT '交易时间',
    trade_amt DECIMAL(18,2) COMMENT '交易金额',
    channel_code STRING COMMENT '渠道编码',
    city_name STRING COMMENT '城市名称',
    dt STRING COMMENT '分区日期'
)
COMMENT '账户交易明细表'
PARTITIONED BY (dt STRING);`;

let demoSamplesCache = null;
let skillsCache = [];
let activeWorkspace = "builder";
let schemaUploadState = null;
let builderSchemaUploadState = null;
let builderSchemaAnalysisCache = null;
let insightSchemaUploadState = null;
let insightSchemaAnalysisCache = null;
let deepseekConfigStatus = null;

const RULE_MODE_UPLOAD_CONFIG = {
    title: "上传 Excel Mapping",
    description: "支持 `.xlsx`，系统会自动解析为标准 Mapping JSON 并回填到编辑区。",
    buttonText: "选择 Excel 文件",
    accept: ".xlsx",
    placeholder: "请粘贴标准 Mapping JSON，或上传 Excel Mapping 文件。",
};

const DEEPSEEK_MODE_UPLOAD_CONFIG = {
    title: "上传 Mapping 文件",
    description: "支持：✓ Excel  ✓ CSV  ✓ Markdown  ✓ JSON。系统会先加载原始内容，再由智能体自动判断结构并分析。",
    buttonText: "选择 Mapping 文件",
    accept: ".xlsx,.csv,.md,.markdown,.json,.txt,text/plain,application/json",
    placeholder: "请粘贴 Mapping 内容，或上传 Excel / CSV / Markdown / JSON 文件。智能体增强模式下会自动分析结构并尽量修复格式问题。",
};

function getCurrentGenerationMode() {
    return modeSelect.value || "rule";
}

function setCurrentGenerationMode(mode) {
    modeSelect.value = mode;
    builderModeSegmentButtons.forEach((button) => {
        button.classList.toggle("segment-button-active", button.dataset.modeValue === mode);
    });
    updateBuilderUploadUI();
}

async function fetchDemoSamples() {
    if (demoSamplesCache) {
        return demoSamplesCache;
    }
    const response = await fetch("/api/demo-samples");
    const data = await response.json();
    if (!response.ok) {
        throw new Error(data.error || "展示样例加载失败");
    }
    demoSamplesCache = data;
    return data;
}

async function loadSkills() {
    const response = await fetch("/api/skills");
    const data = await response.json();
    if (!response.ok) {
        throw new Error(data.error || "Skill 列表加载失败");
    }
    skillsCache = data.skills || [];
    populateSkillSelect(builderSkillSelect);
    populateSkillSelect(compareSkillSelect);
    populateSkillSelect(insightSkillSelect);
}

async function loadDeepSeekConfigStatus() {
    const response = await fetch("/api/deepseek-config");
    const data = await response.json();
    if (!response.ok) {
        throw new Error(data.error || "智能体模型配置加载失败");
    }
    deepseekConfigStatus = data;
}

function getBuilderUploadConfig() {
    return getCurrentGenerationMode() === "deepseek" ? DEEPSEEK_MODE_UPLOAD_CONFIG : RULE_MODE_UPLOAD_CONFIG;
}

function updateBuilderUploadUI() {
    const config = getBuilderUploadConfig();
    mappingUploadTitle.textContent = config.title;
    mappingUploadDescription.textContent = config.description;
    mappingUploadButtonText.textContent = config.buttonText;
    excelInput.setAttribute("accept", config.accept);
    mappingInput.setAttribute("placeholder", config.placeholder);
    builderMappingUploadCard.classList.toggle("deepseek-upload-card", getCurrentGenerationMode() === "deepseek");
    inlineDownloadTemplateBtn.classList.toggle("hidden", getCurrentGenerationMode() === "deepseek");
    if (!excelInput.value) {
        mappingUploadHint.textContent = "未选择任何文件";
    }
}

function populateSkillSelect(select) {
    const current = select.value || "none";
    select.innerHTML = "";
    skillsCache.forEach((skill) => {
        const option = document.createElement("option");
        option.value = skill.id;
        option.textContent = skill.name;
        select.appendChild(option);
    });
    select.value = skillsCache.some((item) => item.id === current) ? current : "none";
}

async function loadDemoByCurrentMode() {
    if (activeWorkspace === "builder") {
        const demoType = getCurrentGenerationMode() === "deepseek" ? "deepseek" : "rule";
        await loadBuilderDemo(demoType);
        return;
    }
    if (activeWorkspace === "compare") {
        await loadCompareDemo();
        return;
    }
    if (activeWorkspace === "insight") {
        sqlInsightInput.value = SQL_INSIGHT_SAMPLE;
        insightSchemaUploadState = null;
        insightSchemaAnalysisCache = null;
        insightSkillSelect.value = skillsCache.some((item) => item.id === "product_aggregation") ? "product_aggregation" : "none";
        insightSchemaAssistCheckbox.checked = true;
        insightSchemaInput.value = SCHEMA_SAMPLE;
        resetSqlInsightOutputs();
        updateEnhancementVisibility();
        syncInsightPreviewState();
        setSqlInsightMessage("SQL 分析样例、Skill 和表结构样例已加载，可直接点击“分析并优化 SQL”。", "ok");
        return;
    }
    schemaUploadState = null;
    schemaInput.value = SCHEMA_SAMPLE;
    resetSchemaOutputs();
    setSchemaMessage("表结构分析样例已加载，可直接点击“分析表结构”。", "ok");
}

async function loadBuilderDemo(type) {
    const samples = await fetchDemoSamples();
    const sample = type === "deepseek" ? samples.builder_deepseek : samples.builder_rule;
    switchMode("builder");
    setCurrentGenerationMode(sample.mode);
    builderSkillSelect.value = sample.skill_id || "none";
    requirementInput.value = sample.requirement || "";
    mappingInput.value = JSON.stringify(sample.mapping, null, 2);
    compareMappingInput.value = JSON.stringify(sample.mapping, null, 2);
    compareRequirementInput.value = sample.requirement || "";
    builderSchemaUploadState = null;
    builderSchemaAnalysisCache = null;
    builderSchemaAssistCheckbox.checked = type === "deepseek";
    builderSchemaInput.value = type === "deepseek" ? SCHEMA_SAMPLE : "";
    setBuilderSchemaMessage("", "");
    resetBuilderOutputs();
    updateEnhancementVisibility();
    setMessage(`${sample.title}已加载，可直接点击“生成 SQL”进行演示。`, "ok");
}

async function loadCompareDemo() {
    setMessage("正在准备版本对比展示样例...", "");
    const response = await fetch("/api/demo-compare-setup", { method: "POST" });
    const data = await response.json();
    if (!response.ok) {
        throw new Error(data.error || "版本对比样例准备失败");
    }

    setCurrentGenerationMode(data.current.mode || "deepseek");
    compareSkillSelect.value = data.current.skill_id || "none";
    requirementInput.value = data.current.requirement || "";
    compareRequirementInput.value = data.current.requirement || "";
    compareMappingInput.value = JSON.stringify(data.current.mapping, null, 2);
    switchMode("compare");
    await loadVersionTasks();
    taskSelect.value = data.task_name;
    await loadVersionsForTask(data.task_name);
    historyVersionSelect.value = String(data.selected_version_no);
    await loadHistoryVersion();
    currentCompareSqlOutput.textContent = "等待点击对比按钮生成当前 SQL...";
    sqlDiffOutput.textContent = "等待对比结果...";
    mappingDiffOutput.textContent = "等待对比结果...";
    setMessage("版本对比样例已准备完成，可直接展示需求变化和 Mapping 变更带来的 SQL 差异。", "ok");
}

async function parseMappingFile(file) {
    if (!file) {
        mappingUploadHint.textContent = "未选择任何文件";
        return;
    }
    const mode = getCurrentGenerationMode();
    if (mode !== "deepseek" && !file.name.toLowerCase().endsWith(".xlsx")) {
        mappingUploadHint.textContent = "未选择任何文件";
        setMessage("规则模式当前仅支持上传 .xlsx Mapping 文件。", "error");
        excelInput.value = "";
        return;
    }
    mappingUploadHint.textContent = file.name;
    setExcelState(true);
    setMessage(`正在加载 Mapping 文件：${file.name}`, "");
    try {
        const buffer = await file.arrayBuffer();
        const endpoint = mode === "deepseek" ? "/api/load-mapping-file" : "/api/parse-excel";
        const payload = {
            filename: file.name,
            file_base64: arrayBufferToBase64(buffer),
        };
        if (mode === "deepseek") {
            payload.mode = "deepseek";
        }
        const response = await fetch(endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || "Mapping 文件加载失败");
        }
        mappingInput.value = data.mapping_text;
        compareMappingInput.value = data.mapping_text;
        setMessage(data.message || "Mapping 文件加载成功。", "ok");
    } catch (error) {
        mappingUploadHint.textContent = "未选择任何文件";
        setMessage(error.message || "Mapping 文件加载失败。", "error");
    } finally {
        setExcelState(false);
        excelInput.value = "";
    }
}

async function generateSql() {
    const raw = mappingInput.value.trim();
    if (!raw) {
        setMessage("请先输入 Mapping 内容。", "error");
        return;
    }

    setLoadingState(true);
    generateBtn.textContent = "处理中...";
    setMessage("正在生成 SQL 并执行规范校验...", "");

    try {
        const aiConfig = buildAiConfig("builder");
        if (aiConfig.enabled && builderSchemaAssistCheckbox.checked) {
            await ensureBuilderSchemaAnalysis();
            if (builderSchemaAnalysisCache) {
                aiConfig.use_schema_assist = true;
                aiConfig.schema_analysis = builderSchemaAnalysisCache;
            }
        }
        const data = await streamJsonRequest(
            "/api/generate-stream",
            {
                mapping_text: raw,
                ai_config: aiConfig,
            }
        );
        renderBuilderResult(data);
        await loadVersionTasks();
    } catch (error) {
        summaryCard.textContent = "生成失败";
        versionCard.textContent = "当前还没有生成版本。";
        requirementCard.textContent = "当前未启用需求增强。";
        builderAiContextCard.textContent = "本次未成功生成增强上下文信息。";
        if (builderSchemaAnalysisCache) {
            builderSchemaAssistCard.textContent = formatBuilderSchemaAssistCard(builderSchemaAnalysisCache, false);
        }
        sqlOutput.textContent = "请检查 Mapping 内容后重试。";
        draftSqlOutput.textContent = "未生成草稿。";
        normalizedMappingOutput.textContent = "未生成修复后的 Mapping。";
        renderIssues(mappingDiagnosisList, ["当前没有 Mapping 诊断结果。"]);
        renderIssues(ruleProfileList, ["当前没有规则配置结果。"]);
        renderIssues(issuesList, [error.message || "生成失败"]);
        renderIssues(fieldChecksList, ["当前没有字段检查结果。"]);
        setMessage(error.message || "生成失败", "error");
    } finally {
        setLoadingState(false);
        generateBtn.textContent = "生成 SQL";
    }
}

function renderBuilderResult(data) {
    summaryCard.textContent = data.summary;
    builderAiContextCard.textContent = formatAiContextCard(
        data.selected_skill_detail,
        data.memory_items_used || [],
        data.memory_enabled,
        data.requested_ai_enabled,
        data.fallback_used
    );
    sqlOutput.textContent = data.sql;
    draftSqlOutput.textContent = data.draft_sql || "当前为规则模式，没有单独草稿。";
    normalizedMappingOutput.textContent = data.normalized_mapping
        ? JSON.stringify(data.normalized_mapping, null, 2)
        : "没有可展示的修复结果。";
    renderIssues(mappingDiagnosisList, resolveMappingDiagnosis(data));
    renderIssues(ruleProfileList, data.rule_profile || ["未返回规则配置说明。"]);
    renderIssues(issuesList, data.style_issues || ["未返回规范校验结果。"]);
    renderIssues(fieldChecksList, data.field_checks || ["未返回字段检查结果。"]);
    if (data.schema_analysis_used) {
        builderSchemaAnalysisCache = data.schema_analysis_used;
    }
    builderSchemaAssistCard.textContent = formatBuilderSchemaAssistCard(
        data.schema_analysis_used || builderSchemaAnalysisCache,
        Boolean(data.schema_analysis_used)
    );
    updateVersionCard(data.version_record);
    updateRequirementCard(data.user_requirement || "");
    compareMappingInput.value = JSON.stringify(data.normalized_mapping, null, 2);
    if (data.user_requirement) {
        compareRequirementInput.value = data.user_requirement;
    }

    if (data.fallback_used) {
        setMessage(`智能体模型调用失败，已自动回退到规则模式：${data.fallback_reason}`, "error");
    } else if (data.mapping_repaired) {
        setMessage("Mapping 已自动修复并完成 SQL 生成，同时已保存为新版本。", "ok");
    } else {
        setMessage("SQL 生成完成，并已自动保存新版本。", "ok");
    }
}

async function loadVersionTasks() {
    try {
        const response = await fetch("/api/version-tasks");
        const data = await response.json();
        const tasks = data.tasks || [];
        taskSelect.innerHTML = '<option value="">请选择任务</option>';
        tasks.forEach((task) => {
            const option = document.createElement("option");
            option.value = task.task_name;
            option.textContent = `${task.task_name}（${task.version_count} 个版本）`;
            taskSelect.appendChild(option);
        });
    } catch {
        setMessage("版本任务列表加载失败。", "error");
    }
}

async function loadVersionsForTask(taskName) {
    historyVersionSelect.innerHTML = '<option value="">请选择版本</option>';
    compareSummaryCard.textContent = "请选择历史版本。";
    historyMappingOutput.textContent = "请选择任务和版本后查看历史 Mapping。";
    historySqlOutput.textContent = "请选择任务和版本后查看历史 SQL。";
    compareAiContextCard.textContent = "等待对比后展示当前 Skill / Memory 上下文。";
    renderIssues(mappingImpactList, ["等待对比结果..."]);

    if (!taskName) {
        return;
    }

    try {
        const response = await fetch(`/api/versions?task_name=${encodeURIComponent(taskName)}`);
        const data = await response.json();
        const versions = data.versions || [];
        versions.forEach((version) => {
            const option = document.createElement("option");
            option.value = String(version.version_no);
            const requirementNote = version.user_requirement ? "含需求" : "无需求";
            option.textContent =
                `v${String(version.version_no).padStart(4, "0")} | ${version.created_at} | ${version.mode} | ${requirementNote}`;
            historyVersionSelect.appendChild(option);
        });
        compareSummaryCard.textContent = versions.length > 0
            ? "版本列表已加载，请手动选择要对比的历史版本。"
            : "当前任务还没有历史版本。";
    } catch {
        compareSummaryCard.textContent = "版本列表加载失败。";
    }
}

async function loadHistoryVersion() {
    const taskName = taskSelect.value;
    const versionNo = historyVersionSelect.value;
    if (!taskName || !versionNo) {
        compareSummaryCard.textContent = "请选择任务和历史版本。";
        compareAiContextCard.textContent = "等待对比后展示当前 Skill / Memory 上下文。";
        return;
    }

    try {
        const response = await fetch(
            `/api/version-detail?task_name=${encodeURIComponent(taskName)}&version_no=${encodeURIComponent(versionNo)}`
        );
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || "历史版本加载失败");
        }

        const requirementText = data.user_requirement ? ` | 需求：${data.user_requirement}` : " | 未记录业务需求";
        compareSummaryCard.textContent =
            `${data.task_name} | 历史版本 v${String(data.version_no).padStart(4, "0")} | ${data.created_at} | ${data.mode}${requirementText}`;
        historyMappingOutput.textContent = JSON.stringify(data.mapping, null, 2);
        historySqlOutput.textContent = data.sql;
        renderIssues(mappingImpactList, ["等待点击版本对比后生成影响分析。"]);
    } catch (error) {
        compareSummaryCard.textContent = error.message || "历史版本加载失败";
        historyMappingOutput.textContent = "没有可展示的历史 Mapping。";
        historySqlOutput.textContent = "没有可展示的历史 SQL。";
        renderIssues(mappingImpactList, ["没有可展示的影响分析。"]);
    }
}

async function compareWithCurrentMapping() {
    const taskName = taskSelect.value;
    const versionNo = historyVersionSelect.value;
    const raw = compareMappingInput.value.trim();
    if (!taskName || !versionNo) {
        compareSummaryCard.textContent = "请先选择任务和历史版本。";
        return;
    }
    if (!raw) {
        compareSummaryCard.textContent = "请先输入当前待对比的 Mapping。";
        return;
    }

    compareBtn.disabled = true;
    compareBtn.textContent = "处理中...";

    try {
        const data = await streamJsonRequest(
            "/api/compare-with-current-stream",
            {
                task_name: taskName,
                version_no: Number(versionNo),
                mapping_text: raw,
                ai_config: buildAiConfig("compare"),
            }
        );
        const currentRequirementText = data.current.user_requirement
            ? ` | 当前需求：${data.current.user_requirement}`
            : " | 当前未填写需求";
        compareSummaryCard.textContent =
            `${data.task_name} | 历史版本 v${String(data.historical.version_no).padStart(4, "0")} vs 当前输入 Mapping${currentRequirementText}`;
        historyMappingOutput.textContent = JSON.stringify(data.historical.mapping, null, 2);
        historySqlOutput.textContent = data.historical.sql;
        currentCompareSqlOutput.textContent = data.current.sql;
        compareAiContextCard.textContent = formatAiContextCard(
            data.current.selected_skill_detail,
            data.current.memory_items_used || [],
            data.current.memory_enabled,
            data.current.requested_ai_enabled,
            data.current.fallback_used
        );
        compareMappingInput.value = JSON.stringify(data.current.mapping, null, 2);
        renderIssues(mappingImpactList, data.mapping_impacts || ["未返回 Mapping 变更影响分析。"]);
        renderDiff(sqlDiffOutput, data.sql_diff);
        renderDiff(mappingDiffOutput, data.mapping_diff);
    } catch (error) {
        compareSummaryCard.textContent = error.message || "对比失败";
        currentCompareSqlOutput.textContent = "没有可展示的当前 SQL。";
        compareAiContextCard.textContent = "本次未成功生成增强上下文信息。";
        sqlDiffOutput.textContent = "没有可展示的 SQL 差异。";
        mappingDiffOutput.textContent = "没有可展示的 Mapping 差异。";
        renderIssues(mappingImpactList, ["没有可展示的影响分析。"]);
    } finally {
        compareBtn.disabled = false;
        compareBtn.textContent = "开始版本对比";
    }
}

async function analyzeSqlInsight() {
    const raw = sqlInsightInput.value.trim();
    if (!raw) {
        setSqlInsightMessage("请先输入待分析的 SQL。", "error");
        return;
    }

    analyzeSqlBtn.disabled = true;
    analyzeSqlBtn.textContent = "分析中...";
    setSqlInsightMessage("正在分析 SQL 语义并生成优化建议...", "");

    try {
        const aiConfig = buildAiConfig("insight");
        if (insightSchemaAssistCheckbox.checked) {
            await ensureInsightSchemaAnalysis();
            if (insightSchemaAnalysisCache) {
                aiConfig.use_schema_assist = true;
                aiConfig.schema_analysis = insightSchemaAnalysisCache;
            }
        }
        const response = await fetch("/api/sql-insight", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                sql_text: raw,
                ai_config: aiConfig,
            }),
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || "SQL 分析失败");
        }
        renderIssues(sqlPurposeList, data.purpose_analysis || ["未返回 SQL 作用分析。"]);
        sqlStructureCard.textContent = formatStructureBreakdown(data.structure_breakdown || {});
        renderIssues(sqlSuggestionList, data.optimization_suggestions || ["未返回优化建议。"]);
        optimizedSqlOutput.textContent = data.optimized_sql || raw;
        renderDiff(optimizedSqlDiffOutput, data.sql_diff || []);
        insightAiContextCard.textContent = formatAiContextCard(
            data.selected_skill_detail,
            data.memory_items_used || [],
            data.memory_enabled,
            data.requested_ai_enabled,
            data.fallback_used
        );
        insightSchemaAssistCard.textContent = formatSchemaAssistCard(
            insightSchemaAssistCheckbox,
            data.schema_analysis_used || insightSchemaAnalysisCache,
            Boolean(data.schema_analysis_used),
            "优化"
        );
        if (data.fallback_used) {
            setSqlInsightMessage(`智能体模型调用失败，已回退为规则分析：${data.fallback_reason}`, "error");
        } else {
            setSqlInsightMessage("SQL 拆解与优化建议已生成。", "ok");
        }
    } catch (error) {
        renderIssues(sqlPurposeList, [error.message || "SQL 分析失败"]);
        sqlStructureCard.textContent = "没有可展示的结构拆解。";
        renderIssues(sqlSuggestionList, ["没有可展示的优化建议。"]);
        optimizedSqlOutput.textContent = "没有可展示的优化 SQL。";
        renderDiff(optimizedSqlDiffOutput, []);
        setSqlInsightMessage(error.message || "SQL 分析失败", "error");
    } finally {
        analyzeSqlBtn.disabled = false;
        analyzeSqlBtn.textContent = "分析并优化 SQL";
    }
}

async function loadSqlInsightFile(file) {
    if (!file) {
        return;
    }
    const lowerName = file.name.toLowerCase();
    if (!lowerName.endsWith(".sql") && !lowerName.endsWith(".txt")) {
        setSqlInsightMessage("当前仅支持上传 .sql 或 .txt 文件。", "error");
        sqlInsightFileInput.value = "";
        return;
    }
    sqlInsightInput.value = await file.text();
    setSqlInsightMessage(`已加载文件：${file.name}`, "ok");
    sqlInsightFileInput.value = "";
}

async function ensureBuilderSchemaAnalysis() {
    if (!builderSchemaAssistCheckbox.checked) {
        builderSchemaAnalysisCache = null;
        return;
    }
    const hasInput = builderSchemaUploadState || builderSchemaInput.value.trim();
    if (!hasInput) {
        builderSchemaAssistCard.textContent = "已启用生成前表结构分析，但当前未提供表结构内容。";
        return;
    }
    if (builderSchemaAnalysisCache) {
        return;
    }
    await analyzeBuilderSchema(true);
}

async function analyzeBuilderSchema(silent = false) {
    if (!builderSchemaUploadState && !builderSchemaInput.value.trim()) {
        if (!silent) {
            setBuilderSchemaMessage("请先输入或上传表结构内容。", "error");
        }
        return;
    }

    analyzeBuilderSchemaBtn.disabled = true;
    if (!silent) {
        analyzeBuilderSchemaBtn.textContent = "分析中...";
        setBuilderSchemaMessage("正在分析表结构并推荐更适合的 Skill...", "");
    }

    try {
        const payload = builderSchemaUploadState
            ? {
                filename: builderSchemaUploadState.filename,
                file_base64: builderSchemaUploadState.fileBase64,
                ai_config: buildAiConfig("schema"),
            }
            : {
                filename: "",
                schema_text: builderSchemaInput.value.trim(),
                ai_config: buildAiConfig("schema"),
            };
        const response = await fetch("/api/schema-insight", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || "表结构分析失败");
        }
        builderSchemaAnalysisCache = data;
        renderBuilderSchemaAssistResult(data);
        if ((builderSkillSelect.value || "none") === "none" && (data.recommended_skills || []).length > 0) {
            builderSkillSelect.value = data.recommended_skills[0].id;
            syncBuilderPreviewState();
        }
        if (!silent) {
            setBuilderSchemaMessage("表结构分析完成，已可用于增强 SQL 生成。", "ok");
        }
    } catch (error) {
        builderSchemaAnalysisCache = null;
        builderSchemaAssistCard.textContent = error.message || "表结构分析失败。";
        if (!silent) {
            setBuilderSchemaMessage(error.message || "表结构分析失败。", "error");
        }
    } finally {
        analyzeBuilderSchemaBtn.disabled = false;
        analyzeBuilderSchemaBtn.textContent = "分析后辅助生成";
    }
}

async function loadBuilderSchemaFile(file) {
    if (!file) {
        return;
    }
    const lowerName = file.name.toLowerCase();
    if (lowerName.endsWith(".xlsx")) {
        const buffer = await file.arrayBuffer();
        builderSchemaUploadState = {
            filename: file.name,
            fileBase64: arrayBufferToBase64(buffer),
        };
        builderSchemaInput.value = `已上传表结构文件：${file.name}\n点击“分析后辅助生成”后将由后端解析并推荐 Skill。`;
    } else {
        builderSchemaUploadState = null;
        builderSchemaInput.value = await file.text();
    }
    builderSchemaAnalysisCache = null;
    setBuilderSchemaMessage(`已加载表结构文件：${file.name}`, "ok");
    builderSchemaFileInput.value = "";
}

async function ensureInsightSchemaAnalysis() {
    if (!insightSchemaAssistCheckbox.checked) {
        insightSchemaAnalysisCache = null;
        return;
    }
    const hasInput = insightSchemaUploadState || insightSchemaInput.value.trim();
    if (!hasInput) {
        insightSchemaAssistCard.textContent = "已启用生成前表结构分析，但当前未提供表结构内容。";
        return;
    }
    if (insightSchemaAnalysisCache) {
        return;
    }
    await analyzeInsightSchema(true);
}

async function analyzeInsightSchema(silent = false) {
    if (!insightSchemaUploadState && !insightSchemaInput.value.trim()) {
        if (!silent) {
            setInsightSchemaMessage("请先输入或上传表结构内容。", "error");
        }
        return;
    }

    analyzeInsightSchemaBtn.disabled = true;
    if (!silent) {
        analyzeInsightSchemaBtn.textContent = "分析中...";
        setInsightSchemaMessage("正在分析表结构并推荐更适合的 Skill...", "");
    }

    try {
        const payload = insightSchemaUploadState
            ? {
                filename: insightSchemaUploadState.filename,
                file_base64: insightSchemaUploadState.fileBase64,
                ai_config: buildAiConfig("insight-schema"),
            }
            : {
                filename: "",
                schema_text: insightSchemaInput.value.trim(),
                ai_config: buildAiConfig("insight-schema"),
            };
        const response = await fetch("/api/schema-insight", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || "表结构分析失败");
        }
        insightSchemaAnalysisCache = data;
        insightSchemaAssistCard.textContent = formatSchemaAssistCard(insightSchemaAssistCheckbox, data, false, "优化");
        if ((insightSkillSelect.value || "none") === "none" && (data.recommended_skills || []).length > 0) {
            insightSkillSelect.value = data.recommended_skills[0].id;
            syncInsightPreviewState();
        }
        if (!silent) {
            setInsightSchemaMessage("表结构分析完成，已可用于增强 SQL 拆解优化。", "ok");
        }
    } catch (error) {
        insightSchemaAnalysisCache = null;
        insightSchemaAssistCard.textContent = error.message || "表结构分析失败。";
        if (!silent) {
            setInsightSchemaMessage(error.message || "表结构分析失败。", "error");
        }
    } finally {
        analyzeInsightSchemaBtn.disabled = false;
        analyzeInsightSchemaBtn.textContent = "分析后辅助优化";
    }
}

async function loadInsightSchemaFile(file) {
    if (!file) {
        return;
    }
    const lowerName = file.name.toLowerCase();
    if (lowerName.endsWith(".xlsx")) {
        const buffer = await file.arrayBuffer();
        insightSchemaUploadState = {
            filename: file.name,
            fileBase64: arrayBufferToBase64(buffer),
        };
        insightSchemaInput.value = `已上传表结构文件：${file.name}\n点击“分析后辅助优化”后将由后端解析并推荐 Skill。`;
    } else {
        insightSchemaUploadState = null;
        insightSchemaInput.value = await file.text();
    }
    insightSchemaAnalysisCache = null;
    setInsightSchemaMessage(`已加载表结构文件：${file.name}`, "ok");
    insightSchemaFileInput.value = "";
    syncInsightPreviewState();
}

async function analyzeSchema() {
    if (!schemaUploadState && !schemaInput.value.trim()) {
        setSchemaMessage("请先输入或上传表结构内容。", "error");
        return;
    }

    analyzeSchemaBtn.disabled = true;
    analyzeSchemaBtn.textContent = "分析中...";
    setSchemaMessage("正在整理表结构并分析可复用场景...", "");

    try {
        const payload = schemaUploadState
            ? {
                filename: schemaUploadState.filename,
                file_base64: schemaUploadState.fileBase64,
                ai_config: buildAiConfig("schema"),
            }
            : {
                filename: "",
                schema_text: schemaInput.value.trim(),
                ai_config: buildAiConfig("schema"),
            };

        const response = await fetch("/api/schema-insight", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || "表结构分析失败");
        }
        renderSchemaResult(data);
    } catch (error) {
        schemaFieldsOutput.textContent = "没有可展示的表结构整理结果。";
        schemaPurposeCard.textContent = "没有可展示的表用途分析。";
        schemaKeyFieldsCard.textContent = "没有可展示的关键字段识别。";
        renderIssues(schemaReuseList, [error.message || "表结构分析失败"]);
        setSchemaMessage(error.message || "表结构分析失败", "error");
    } finally {
        analyzeSchemaBtn.disabled = false;
        analyzeSchemaBtn.textContent = "分析表结构";
    }
}

function renderSchemaResult(data) {
    schemaFieldsOutput.textContent = formatSchemaFields(data.fields || []);
    schemaPurposeCard.textContent = data.table_purpose || "未返回表用途分析。";
    schemaKeyFieldsCard.textContent = formatKeyFields(data.key_fields || {});
    renderIssues(schemaReuseList, data.reuse_suggestions || ["未返回可复用建议。"]);
    if (data.fallback_used) {
        setSchemaMessage(`智能体模型调用失败，已回退为规则分析：${data.fallback_reason}`, "error");
    } else {
        setSchemaMessage("表结构分析已完成。", "ok");
    }
}

function renderBuilderSchemaAssistResult(data) {
    builderSchemaAssistCard.textContent = formatBuilderSchemaAssistCard(data, false);
    syncBuilderPreviewState();
}

async function loadSchemaFile(file) {
    if (!file) {
        return;
    }
    const lowerName = file.name.toLowerCase();
    if (lowerName.endsWith(".xlsx")) {
        const buffer = await file.arrayBuffer();
        schemaUploadState = {
            filename: file.name,
            fileBase64: arrayBufferToBase64(buffer),
        };
        schemaInput.value = `已上传 Excel 表结构文件：${file.name}\n点击“分析表结构”后将由后端解析第一张工作表。`;
        setSchemaMessage(`已加载 Excel 文件：${file.name}`, "ok");
    } else {
        schemaUploadState = null;
        schemaInput.value = await file.text();
        setSchemaMessage(`已加载文件：${file.name}`, "ok");
    }
    schemaFileInput.value = "";
}

async function streamJsonRequest(url, payload) {
    const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    });
    if (!response.ok || !response.body) {
        const data = await response.json().catch(() => ({}));
        throw new Error(data.error || "流式请求失败");
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let buffer = "";
    let resultPayload = null;
    while (true) {
        const { value, done } = await reader.read();
        if (done) {
            break;
        }
        buffer += decoder.decode(value, { stream: true });
        const chunks = buffer.split("\n\n");
        buffer = chunks.pop() || "";

        chunks.forEach((chunk) => {
            if (!chunk.startsWith("data: ")) {
                return;
            }
            let event;
            try {
                event = JSON.parse(chunk.slice(6));
            } catch {
                return;
            }
            if (event.type === "result") {
                resultPayload = event.payload;
            } else if (event.type === "error") {
                throw new Error(event.payload.message || "流式请求失败");
            }
        });
    }

    if (!resultPayload) {
        throw new Error("流式结果为空。");
    }
    return resultPayload;
}

function buildAiConfig(scope) {
    const requirement =
        scope === "builder" ? requirementInput.value.trim()
        : scope === "compare" ? compareRequirementInput.value.trim()
        : "";
    const skillId =
        scope === "compare" ? compareSkillSelect.value
        : scope === "insight" || scope === "insight-schema" ? insightSkillSelect.value
        : builderSkillSelect.value;
    const normalizedSkillId = skillId || "none";
    const includeMemory = normalizedSkillId !== "none";
    return {
        enabled: scope === "insight" || scope === "insight-schema" || getCurrentGenerationMode() === "deepseek",
        user_requirement: requirement,
        skill_id: normalizedSkillId,
        include_memory: includeMemory,
    };
}

function renderIssues(target, items) {
    target.innerHTML = "";
    items.forEach((item) => {
        const li = document.createElement("li");
        li.textContent = item;
        if (item.startsWith("PASS") || item.startsWith("未发现")) {
            li.classList.add("ok");
        }
        target.appendChild(li);
    });
}

function renderDiff(target, lines) {
    target.innerHTML = "";
    if (!lines || lines.length === 0) {
        target.textContent = "没有差异。";
        return;
    }
    lines.forEach((line) => {
        const span = document.createElement("span");
        span.textContent = `${diffPrefix(line.type)} ${line.text}`;
        span.className = diffClass(line.type);
        target.appendChild(span);
    });
}

function formatStructureBreakdown(structure) {
    return [
        `SELECT:\n${structure.select || "未识别到该结构。"}`,
        `FROM:\n${structure.from || "未识别到该结构。"}`,
        `JOIN:\n${structure.join || "未识别到该结构。"}`,
        `WHERE:\n${structure.where || "未识别到该结构。"}`,
        `GROUP BY:\n${structure.group_by || "未识别到该结构。"}`,
        `ORDER BY:\n${structure.order_by || "未识别到该结构。"}`,
        `WINDOW:\n${structure.window || "未识别到该结构。"}`,
    ].join("\n\n");
}

function formatSchemaFields(fields) {
    if (!fields || fields.length === 0) {
        return "未识别到字段列表。";
    }
    return fields
        .map((field) => `${field.name} | ${field.type || "string"} | ${field.description || "-"}`)
        .join("\n");
}

function formatKeyFields(keyFields) {
    const sections = [
        ["主键候选", keyFields.primary_candidates || []],
        ["Join Key", keyFields.join_keys || []],
        ["时间字段", keyFields.time_fields || []],
        ["分区字段", keyFields.partition_fields || []],
        ["指标字段", keyFields.metric_fields || []],
        ["维度字段", keyFields.dimension_fields || []],
    ];
    return sections
        .map(([title, values]) => `${title}：${values.length > 0 ? values.join("、") : "未识别"}`)
        .join("\n");
}

function formatAiContextCard(skillDetail, memoryItems, memoryEnabled, aiEnabled, fallbackUsed) {
    if (!aiEnabled) {
        return "当前为规则模式，未启用 Skill / Memory 增强。";
    }
    const skillName = skillDetail && skillDetail.name ? skillDetail.name : "无";
    const skillDesc = skillDetail && skillDetail.description
        ? skillDetail.description
        : "当前未注入特定业务模式。";
    const fallbackHint = fallbackUsed ? "智能体模型调用失败，已回退为规则生成。\n" : "";
    if (!memoryEnabled) {
        return `${fallbackHint}Skill：${skillName}\n说明：${skillDesc}\nMemory：未注入（当前未选择 Skill）`;
    }
    const memoryTitles = (memoryItems || []).map((item) => item.title).filter(Boolean);
    const memoryText = memoryTitles.length > 0 ? memoryTitles.join("、") : "已随 Skill 自动注入，但当前没有可展示条目";
    return `${fallbackHint}Skill：${skillName}\n说明：${skillDesc}\nMemory：已随 Skill 自动注入\n记忆条目：${memoryText}`;
}

function formatBuilderSchemaAssistCard(schemaAnalysis, usedInGeneration) {
    return formatSchemaAssistCard(builderSchemaAssistCheckbox, schemaAnalysis, usedInGeneration, "生成");
}

function formatSchemaAssistCard(checkbox, schemaAnalysis, usedInGeneration, actionName) {
    if (!checkbox.checked) {
        return "当前未启用生成前表结构分析。";
    }
    if (!schemaAnalysis) {
        return "已启用生成前表结构分析，待分析后展示表用途、推荐 Skill 和可复用场景。";
    }
    const recommendedSkills = (schemaAnalysis.recommended_skills || []).map((item) => item.name).join("、") || "暂无明确推荐";
    const suggestions = (schemaAnalysis.reuse_suggestions || []).join("；") || "暂无可复用建议";
    const usageHint = usedInGeneration
        ? `本次 SQL 已使用表结构分析结果增强${actionName}。`
        : `当前表结构分析结果已保留，可继续用于增强 SQL ${actionName}。`;
    return `${usageHint}\n表用途：${schemaAnalysis.table_purpose || "未识别"}\n推荐 Skill：${recommendedSkills}\n可复用场景：${suggestions}`;
}

function diffClass(type) {
    if (type === "added") {
        return "diff-added";
    }
    if (type === "removed") {
        return "diff-removed";
    }
    return "diff-same";
}

function diffPrefix(type) {
    if (type === "added") {
        return "+";
    }
    if (type === "removed") {
        return "-";
    }
    return " ";
}

function resolveMappingDiagnosis(data) {
    if (data.mapping_diagnosis && data.mapping_diagnosis.length > 0) {
        return data.mapping_diagnosis;
    }
    if (data.mapping_repaired) {
        return ["Mapping 已自动修复，但未返回额外诊断说明。"];
    }
    return ["未发现 Mapping 结构问题。"];
}

function updateVersionCard(versionRecord) {
    if (!versionRecord) {
        versionCard.textContent = "当前还没有生成版本。";
        return;
    }
    versionCard.textContent =
        `已保存版本 v${String(versionRecord.version_no).padStart(4, "0")} | ${versionRecord.created_at} | ${versionRecord.task_name}`;
}

function updateRequirementCard(userRequirement) {
    requirementCard.textContent = userRequirement || "当前未启用需求增强。";
}

function syncBuilderPreviewState() {
    if (getCurrentGenerationMode() === "deepseek") {
        const requirement = requirementInput.value.trim();
        const selectedSkill = skillsCache.find((item) => item.id === (builderSkillSelect.value || "none")) || null;
        const memoryPreviewItems = builderSkillSelect.value !== "none"
            ? [{ title: "待生成后展示具体条目" }]
            : [];
        requirementCard.textContent = requirement || "当前已启用需求增强，待生成后会展示本次需求说明。";
        builderAiContextCard.textContent = formatAiContextCard(
            selectedSkill,
            memoryPreviewItems,
            builderSkillSelect.value !== "none",
            true,
            false
        );
        builderSchemaAssistCard.textContent = formatBuilderSchemaAssistCard(builderSchemaAnalysisCache, false);
        return;
    }
    requirementCard.textContent = "当前未启用需求增强。";
    builderAiContextCard.textContent = "当前为规则模式，未启用 Skill / Memory 增强。";
    builderSchemaAssistCard.textContent = "当前未启用生成前表结构分析。";
}

function syncComparePreviewState() {
    if (getCurrentGenerationMode() === "deepseek") {
        const selectedSkill = skillsCache.find((item) => item.id === (compareSkillSelect.value || "none")) || null;
        const memoryPreviewItems = compareSkillSelect.value !== "none"
            ? [{ title: "待对比后展示具体条目" }]
            : [];
        compareAiContextCard.textContent = formatAiContextCard(
            selectedSkill,
            memoryPreviewItems,
            compareSkillSelect.value !== "none",
            true,
            false
        );
        return;
    }
    compareAiContextCard.textContent = "当前为规则模式，未启用 Skill / Memory 增强。";
}

function syncInsightPreviewState() {
    const selectedSkill = skillsCache.find((item) => item.id === (insightSkillSelect.value || "none")) || null;
    const memoryPreviewItems = insightSkillSelect.value !== "none"
        ? [{ title: "待分析后展示具体条目" }]
        : [];
    insightAiContextCard.textContent = formatAiContextCard(
        selectedSkill,
        memoryPreviewItems,
        insightSkillSelect.value !== "none",
        true,
        false
    );
    insightSchemaAssistCard.textContent = formatSchemaAssistCard(
        insightSchemaAssistCheckbox,
        insightSchemaAnalysisCache,
        false,
        "优化"
    );
}

function updateEnhancementVisibility() {
    const isDeepSeek = getCurrentGenerationMode() === "deepseek";
    updateBuilderUploadUI();
    builderEnhancementSection.classList.toggle("hidden", !isDeepSeek);
    builderSchemaAssistSection.classList.toggle("hidden", !isDeepSeek || !builderSchemaAssistCheckbox.checked);
    insightSchemaAssistSection.classList.toggle("hidden", !insightSchemaAssistCheckbox.checked);
    requirementSection.classList.toggle("hidden", !isDeepSeek);
    compareRequirementSection.classList.toggle("hidden", activeWorkspace !== "compare" || !isDeepSeek);
    compareEnhancementSection.classList.toggle("hidden", activeWorkspace !== "compare" || !isDeepSeek);
    syncBuilderPreviewState();
    syncComparePreviewState();
    syncInsightPreviewState();
}

function updateDemoButtonLabel() {
    if (activeWorkspace === "compare") {
        loadDemoBtn.textContent = "加载版本对比样例";
        return;
    }
    if (activeWorkspace === "insight") {
        loadDemoBtn.textContent = "加载 SQL 分析样例";
        return;
    }
    if (activeWorkspace === "schema") {
        loadDemoBtn.textContent = "加载表结构分析样例";
        return;
    }
    if (getCurrentGenerationMode() === "deepseek") {
        loadDemoBtn.textContent = "加载智能体增强样例";
        return;
    }
    loadDemoBtn.textContent = "加载生成 SQL 样例";
}

function setMessage(text, type) {
    formMessage.textContent = text;
    formMessage.className = `form-message ${type}`.trim();
}

function setSqlInsightMessage(text, type) {
    sqlInsightMessage.textContent = text;
    sqlInsightMessage.className = `form-message ${type}`.trim();
}

function setSchemaMessage(text, type) {
    schemaMessage.textContent = text;
    schemaMessage.className = `form-message ${type}`.trim();
}

function setBuilderSchemaMessage(text, type) {
    builderSchemaMessage.textContent = text;
    builderSchemaMessage.className = `form-message ${type}`.trim();
}

function setInsightSchemaMessage(text, type) {
    insightSchemaMessage.textContent = text;
    insightSchemaMessage.className = `form-message ${type}`.trim();
}

function setLoadingState(isLoading) {
    generateBtn.disabled = isLoading;
    loadDemoBtn.disabled = isLoading;
    inlineDownloadTemplateBtn.disabled = isLoading;
    modeSelect.disabled = isLoading;
    excelInput.disabled = isLoading;
    builderSkillSelect.disabled = isLoading;
    builderSchemaAssistCheckbox.disabled = isLoading;
    builderSchemaFileInput.disabled = isLoading;
    if (downloadBuilderSchemaTemplateBtn) {
        downloadBuilderSchemaTemplateBtn.disabled = isLoading;
    }
    analyzeBuilderSchemaBtn.disabled = isLoading;
    builderSchemaInput.disabled = isLoading;
    requirementInput.disabled = isLoading;
    compareRequirementInput.disabled = isLoading;
    compareSkillSelect.disabled = isLoading;
    refreshTasksBtn.disabled = isLoading;
    loadHistoryBtn.disabled = isLoading;
    compareBtn.disabled = isLoading;
    analyzeSqlBtn.disabled = isLoading;
    sqlInsightFileInput.disabled = isLoading;
    insightSkillSelect.disabled = isLoading;
    insightSchemaAssistCheckbox.disabled = isLoading;
    insightSchemaFileInput.disabled = isLoading;
    analyzeInsightSchemaBtn.disabled = isLoading;
    insightSchemaInput.disabled = isLoading;
    analyzeSchemaBtn.disabled = isLoading;
    downloadSchemaTemplateBtn.disabled = isLoading;
    schemaFileInput.disabled = isLoading;
}

function setExcelState(isLoading) {
    excelInput.disabled = isLoading;
    inlineDownloadTemplateBtn.disabled = isLoading;
}

function resetBuilderOutputs() {
    summaryCard.textContent = "等待生成";
    versionCard.textContent = "当前还没有生成版本。";
    requirementCard.textContent = "当前未启用需求增强。";
    builderAiContextCard.textContent = "当前为规则模式，未启用 Skill / Memory 增强。";
    sqlOutput.textContent = "等待生成 SQL...";
    draftSqlOutput.textContent = "AI 模式下会展示规则引擎草稿，便于对比。";
    normalizedMappingOutput.textContent = "如果输入存在格式问题，AI 修复后的 Mapping 会展示在这里。";
    renderIssues(mappingDiagnosisList, ["等待诊断结果..."]);
    renderIssues(ruleProfileList, ["等待加载规范规则..."]);
    renderIssues(issuesList, ["等待校验结果..."]);
    renderIssues(fieldChecksList, ["等待字段检查结果..."]);
    builderSchemaAssistCard.textContent = "当前未启用生成前表结构分析。";
}

function resetSqlInsightOutputs() {
    setSqlInsightMessage("", "");
    setInsightSchemaMessage("", "");
    renderIssues(sqlPurposeList, ["等待分析结果..."]);
    sqlStructureCard.textContent = "等待分析结果...";
    renderIssues(sqlSuggestionList, ["等待优化建议..."]);
    optimizedSqlOutput.textContent = "等待分析结果...";
    optimizedSqlDiffOutput.textContent = "等待分析结果...";
    insightAiContextCard.textContent = "等待选择 Skill 或执行分析。";
    insightSchemaAssistCard.textContent = "当前未启用生成前表结构分析。";
}

function resetSchemaOutputs() {
    setSchemaMessage("", "");
    schemaFieldsOutput.textContent = "等待分析结果...";
    schemaPurposeCard.textContent = "等待分析结果...";
    schemaKeyFieldsCard.textContent = "等待分析结果...";
    renderIssues(schemaReuseList, ["等待分析结果..."]);
}

function arrayBufferToBase64(buffer) {
    let binary = "";
    const bytes = new Uint8Array(buffer);
    const chunkSize = 0x8000;
    for (let index = 0; index < bytes.length; index += chunkSize) {
        const chunk = bytes.subarray(index, index + chunkSize);
        binary += String.fromCharCode(...chunk);
    }
    return btoa(binary);
}

function switchMode(mode) {
    activeWorkspace = mode;
    builderView.classList.toggle("hidden", mode !== "builder");
    compareView.classList.toggle("hidden", mode !== "compare");
    insightView.classList.toggle("hidden", mode !== "insight");
    schemaView.classList.toggle("hidden", mode !== "schema");
    builderModeBtn.classList.toggle("mode-pill-active", mode === "builder");
    compareModeBtn.classList.toggle("mode-pill-active", mode === "compare");
    insightModeBtn.classList.toggle("mode-pill-active", mode === "insight");
    schemaModeBtn.classList.toggle("mode-pill-active", mode === "schema");
    updateEnhancementVisibility();
    updateDemoButtonLabel();
}

function flashCopiedButton(button) {
    const originalText = button.textContent;
    button.textContent = "已复制";
    window.setTimeout(() => {
        button.textContent = originalText;
    }, 1400);
}

async function copySqlFromOutput(outputElement, emptyMessages, button) {
    const content = outputElement.textContent.trim();
    if (!content || emptyMessages.includes(content)) {
        setMessage("当前没有可复制的 SQL。", "error");
        return;
    }
    try {
        await navigator.clipboard.writeText(content);
        if (button) {
            flashCopiedButton(button);
        }
        setMessage("SQL 已复制到剪贴板。", "ok");
    } catch {
        setMessage("复制失败，请手动复制。", "error");
    }
}

loadDemoBtn.addEventListener("click", async () => {
    try {
        await loadDemoByCurrentMode();
    } catch (error) {
        setMessage(error.message || "展示样例加载失败。", "error");
    }
});
inlineDownloadTemplateBtn.addEventListener("click", () => {
    window.location.href = "/api/template.xlsx";
});
downloadBuilderSchemaTemplateBtn?.addEventListener("click", () => {
    window.location.href = "/api/schema-template.xlsx";
});
downloadSchemaTemplateBtn.addEventListener("click", () => {
    window.location.href = "/api/schema-template.xlsx";
});
generateBtn.addEventListener("click", generateSql);
copySqlBtn.addEventListener("click", () => copySqlFromOutput(sqlOutput, [
    "等待生成 SQL...",
    "请检查 Mapping 内容后重试。",
], copySqlBtn));
copyCompareSqlBtn.addEventListener("click", () => copySqlFromOutput(currentCompareSqlOutput, [
    "等待对比生成结果...",
    "等待点击对比按钮生成当前 SQL...",
    "没有可展示的当前 SQL。",
], copyCompareSqlBtn));
copyOptimizedSqlBtn.addEventListener("click", () => copySqlFromOutput(optimizedSqlOutput, [
    "等待分析结果...",
    "没有可展示的优化 SQL。",
], copyOptimizedSqlBtn));
excelInput.addEventListener("change", (event) => parseMappingFile(event.target.files[0]));
modeSelect.addEventListener("change", updateEnhancementVisibility);
modeSelect.addEventListener("change", updateDemoButtonLabel);
builderModeSegment.addEventListener("click", (event) => {
    const button = event.target.closest("[data-mode-value]");
    if (!button) {
        return;
    }
    setCurrentGenerationMode(button.dataset.modeValue || "rule");
    updateEnhancementVisibility();
    updateDemoButtonLabel();
});
builderSkillSelect.addEventListener("change", syncBuilderPreviewState);
builderSchemaAssistCheckbox.addEventListener("change", () => {
    if (!builderSchemaAssistCheckbox.checked) {
        builderSchemaAnalysisCache = null;
    }
    updateEnhancementVisibility();
});
builderSchemaFileInput.addEventListener("change", (event) => loadBuilderSchemaFile(event.target.files[0]));
analyzeBuilderSchemaBtn.addEventListener("click", () => analyzeBuilderSchema(false));
builderSchemaInput.addEventListener("input", () => {
    builderSchemaUploadState = null;
    builderSchemaAnalysisCache = null;
    syncBuilderPreviewState();
});
requirementInput.addEventListener("input", syncBuilderPreviewState);
compareSkillSelect.addEventListener("change", syncComparePreviewState);
compareRequirementInput.addEventListener("input", syncComparePreviewState);
insightSkillSelect.addEventListener("change", syncInsightPreviewState);
insightSchemaAssistCheckbox.addEventListener("change", () => {
    if (!insightSchemaAssistCheckbox.checked) {
        insightSchemaAnalysisCache = null;
    }
    updateEnhancementVisibility();
});
insightSchemaFileInput.addEventListener("change", (event) => loadInsightSchemaFile(event.target.files[0]));
analyzeInsightSchemaBtn.addEventListener("click", () => analyzeInsightSchema(false));
insightSchemaInput.addEventListener("input", () => {
    insightSchemaUploadState = null;
    insightSchemaAnalysisCache = null;
    syncInsightPreviewState();
});
builderModeBtn.addEventListener("click", () => switchMode("builder"));
compareModeBtn.addEventListener("click", async () => {
    switchMode("compare");
    await loadVersionTasks();
});
insightModeBtn.addEventListener("click", () => switchMode("insight"));
schemaModeBtn.addEventListener("click", () => switchMode("schema"));
refreshTasksBtn.addEventListener("click", loadVersionTasks);
taskSelect.addEventListener("change", (event) => loadVersionsForTask(event.target.value));
historyVersionSelect.addEventListener("change", loadHistoryVersion);
loadHistoryBtn.addEventListener("click", loadHistoryVersion);
compareBtn.addEventListener("click", compareWithCurrentMapping);
analyzeSqlBtn.addEventListener("click", analyzeSqlInsight);
sqlInsightFileInput.addEventListener("change", (event) => loadSqlInsightFile(event.target.files[0]));
analyzeSchemaBtn.addEventListener("click", analyzeSchema);
schemaFileInput.addEventListener("change", (event) => loadSchemaFile(event.target.files[0]));
schemaInput.addEventListener("input", () => {
    schemaUploadState = null;
});

async function initialize() {
    await loadDeepSeekConfigStatus();
    await loadSkills();
    setCurrentGenerationMode(getCurrentGenerationMode());
    switchMode("builder");
    updateEnhancementVisibility();
    updateDemoButtonLabel();
    await loadVersionTasks();
    resetBuilderOutputs();
    resetSqlInsightOutputs();
    resetSchemaOutputs();
}

initialize().catch((error) => {
    setMessage(error.message || "初始化失败。", "error");
});
