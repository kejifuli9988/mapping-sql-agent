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
const skillModeBtn = document.getElementById("skillModeBtn");
const schemaModeBtn = document.getElementById("schemaModeBtn");
const builderView = document.getElementById("builderView");
const compareView = document.getElementById("compareView");
const insightView = document.getElementById("insightView");
const skillView = document.getElementById("skillView");
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

const skillList = document.getElementById("skillList");
const newSkillBtn = document.getElementById("newSkillBtn");
const skillEditorModeTag = document.getElementById("skillEditorModeTag");
const skillIdInput = document.getElementById("skillIdInput");
const skillNameInput = document.getElementById("skillNameInput");
const skillDescriptionInput = document.getElementById("skillDescriptionInput");
const skillPatternInput = document.getElementById("skillPatternInput");
const skillExamplesInput = document.getElementById("skillExamplesInput");
const skillRulesInput = document.getElementById("skillRulesInput");
const saveSkillBtn = document.getElementById("saveSkillBtn");
const deleteSkillBtn = document.getElementById("deleteSkillBtn");
const skillMessage = document.getElementById("skillMessage");
const skillScenarioInput = document.getElementById("skillScenarioInput");
const skillSourceInput = document.getElementById("skillSourceInput");
const skillRequirementInput = document.getElementById("skillRequirementInput");
const generateSkillDraftBtn = document.getElementById("generateSkillDraftBtn");
const loadCustodySkillDemoBtn = document.getElementById("loadCustodySkillDemoBtn");
const skillDraftPreview = document.getElementById("skillDraftPreview");

const SQL_INSIGHT_SAMPLE = `WITH clearing AS (
    SELECT
        *
    FROM dwd_custody_clearing_detail_di
    WHERE dt = '\${biz_date}'
),
trade_base AS (
    SELECT
        trade_id,
        trade_amt
    FROM dwd_custody_trade_detail_di
    WHERE dt = '\${biz_date}'
)
INSERT OVERWRITE TABLE dws_custody_clearing_reconcile_day
PARTITION (dt = '\${biz_date}')
SELECT
    c.product_id,
    c.clear_status,
    COUNT(DISTINCT c.clear_id) AS clear_cnt,
    SUM(c.clear_amt) AS clear_amt,
    SUM(t.trade_amt) AS trade_amt,
    SUM(c.clear_amt - t.trade_amt) AS diff_amt
FROM clearing c
LEFT JOIN trade_base t
    ON c.trade_id = t.trade_id
GROUP BY
    c.product_id,
    c.clear_status;`;
const SCHEMA_SAMPLE = `CREATE TABLE dwd_custody_clearing_detail_di (
    clear_id STRING COMMENT '清算流水号',
    trade_id STRING COMMENT '交易流水号',
    product_id STRING COMMENT '产品编号',
    account_id STRING COMMENT '托管账户号',
    trade_dt STRING COMMENT '交易日期',
    clear_dt STRING COMMENT '清算日期',
    clear_time STRING COMMENT '清算时间',
    clear_status STRING COMMENT '清算状态',
    trade_amt DECIMAL(18,2) COMMENT '交易金额',
    clear_amt DECIMAL(18,2) COMMENT '清算金额',
    diff_amt DECIMAL(18,2) COMMENT '差异金额',
    fail_reason STRING COMMENT '失败原因',
    dt STRING COMMENT '分区日期'
)
COMMENT '托管清算明细表'
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
let activeBuilderDemoType = "";
let selectedSkillEditorId = "none";
const customSkillSelects = new WeakMap();

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
    renderSkillManager();
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
    syncCustomSkillSelect(select);
}

function syncCustomSkillSelect(select) {
    if (!select) {
        return;
    }
    select.classList.add("native-skill-select");
    let widget = customSkillSelects.get(select);
    if (!widget) {
        const root = document.createElement("div");
        root.className = "custom-skill-select";
        const trigger = document.createElement("button");
        trigger.type = "button";
        trigger.className = "custom-skill-trigger";
        trigger.setAttribute("aria-haspopup", "listbox");
        trigger.setAttribute("aria-expanded", "false");
        const menu = document.createElement("div");
        menu.className = "custom-skill-menu";
        menu.setAttribute("role", "listbox");
        root.append(trigger, menu);
        select.insertAdjacentElement("afterend", root);
        trigger.addEventListener("click", (event) => {
            event.stopPropagation();
            closeOtherSkillMenus(root);
            const open = !root.classList.contains("custom-skill-select-open");
            root.classList.toggle("custom-skill-select-open", open);
            trigger.setAttribute("aria-expanded", String(open));
        });
        customSkillSelects.set(select, { root, trigger, menu });
        widget = customSkillSelects.get(select);
    }

    const selected = skillsCache.find((item) => item.id === (select.value || "none"));
    widget.trigger.textContent = selected ? selected.name : "无";
    widget.menu.innerHTML = "";
    skillsCache.forEach((skill) => {
        const option = document.createElement("button");
        option.type = "button";
        option.className = "custom-skill-option";
        option.classList.toggle("custom-skill-option-active", skill.id === select.value);
        option.textContent = skill.name;
        option.setAttribute("role", "option");
        option.setAttribute("aria-selected", String(skill.id === select.value));
        option.addEventListener("click", () => {
            select.value = skill.id;
            select.dispatchEvent(new Event("change", { bubbles: true }));
            widget.root.classList.remove("custom-skill-select-open");
            widget.trigger.setAttribute("aria-expanded", "false");
            syncCustomSkillSelect(select);
        });
        widget.menu.appendChild(option);
    });
}

function closeOtherSkillMenus(currentRoot = null) {
    document.querySelectorAll(".custom-skill-select-open").forEach((root) => {
        if (root === currentRoot) {
            return;
        }
        root.classList.remove("custom-skill-select-open");
        const trigger = root.querySelector(".custom-skill-trigger");
        if (trigger) {
            trigger.setAttribute("aria-expanded", "false");
        }
    });
}

function renderSkillManager() {
    if (!skillList) {
        return;
    }
    skillList.innerHTML = "";
    skillsCache.forEach((skill) => {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "skill-list-item";
        button.classList.toggle("skill-list-item-active", skill.id === selectedSkillEditorId);
        button.innerHTML = `
            <strong></strong>
            <span></span>
        `;
        button.querySelector("strong").textContent = skill.name || "未命名 Skill";
        button.querySelector("span").textContent = skill.id || "-";
        button.addEventListener("click", () => loadSkillIntoEditor(skill.id));
        skillList.appendChild(button);
    });
    if (!skillsCache.some((item) => item.id === selectedSkillEditorId)) {
        selectedSkillEditorId = skillsCache[0]?.id || "none";
    }
    if (!skillIdInput.value && skillsCache.length > 0) {
        loadSkillIntoEditor(selectedSkillEditorId);
    }
}

function loadSkillIntoEditor(skillId) {
    const skill = skillsCache.find((item) => item.id === skillId) || skillsCache[0] || {
        id: "",
        name: "",
        description: "",
        sql_pattern: "",
        examples: [],
        business_rules: [],
    };
    selectedSkillEditorId = skill.id || "";
    skillIdInput.value = skill.id || "";
    skillNameInput.value = skill.name || "";
    skillDescriptionInput.value = skill.description || "";
    skillPatternInput.value = skill.sql_pattern || "";
    skillExamplesInput.value = (skill.examples || []).join("\n");
    skillRulesInput.value = (skill.business_rules || []).join("\n");
    skillEditorModeTag.textContent = skill.id === "none" ? "只读" : "编辑";
    deleteSkillBtn.disabled = skill.id === "none";
    renderSkillManager();
    setSkillMessage("", "");
}

function clearSkillEditor() {
    selectedSkillEditorId = "";
    skillIdInput.value = "";
    skillNameInput.value = "";
    skillDescriptionInput.value = "";
    skillPatternInput.value = "";
    skillExamplesInput.value = "";
    skillRulesInput.value = "";
    skillEditorModeTag.textContent = "新建";
    deleteSkillBtn.disabled = true;
    renderSkillManager();
    setSkillMessage("请填写或生成 Skill 草稿后保存。", "");
}

function collectSkillForm() {
    return {
        id: skillIdInput.value.trim(),
        name: skillNameInput.value.trim(),
        description: skillDescriptionInput.value.trim(),
        sql_pattern: skillPatternInput.value.trim(),
        examples: splitLines(skillExamplesInput.value),
        business_rules: splitLines(skillRulesInput.value),
    };
}

function fillSkillForm(skill) {
    selectedSkillEditorId = skill.id || "";
    skillIdInput.value = skill.id || "";
    skillNameInput.value = skill.name || "";
    skillDescriptionInput.value = skill.description || "";
    skillPatternInput.value = skill.sql_pattern || "";
    skillExamplesInput.value = (skill.examples || []).join("\n");
    skillRulesInput.value = (skill.business_rules || []).join("\n");
    skillDraftPreview.textContent = JSON.stringify(skill, null, 2);
    skillEditorModeTag.textContent = "草稿";
    deleteSkillBtn.disabled = true;
    renderSkillManager();
}

function splitLines(text) {
    return text
        .split("\n")
        .map((item) => item.trim())
        .filter(Boolean);
}

async function saveSkill() {
    const skill = collectSkillForm();
    if (!skill.name) {
        setSkillMessage("请先填写 Skill 名称。", "error");
        return;
    }
    saveSkillBtn.disabled = true;
    saveSkillBtn.textContent = "保存中...";
    try {
        const response = await fetch("/api/skills/save", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ skill }),
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || "Skill 保存失败");
        }
        skillsCache = data.skills || [];
        selectedSkillEditorId = data.skill.id;
        populateSkillSelect(builderSkillSelect);
        populateSkillSelect(compareSkillSelect);
        populateSkillSelect(insightSkillSelect);
        loadSkillIntoEditor(selectedSkillEditorId);
        setSkillMessage("Skill 已保存，并已同步到各模块选择器。", "ok");
    } catch (error) {
        setSkillMessage(error.message || "Skill 保存失败。", "error");
    } finally {
        saveSkillBtn.disabled = false;
        saveSkillBtn.textContent = "保存 Skill";
    }
}

async function deleteSkill() {
    const skillId = skillIdInput.value.trim();
    if (!skillId || skillId === "none") {
        setSkillMessage("系统默认 Skill 不允许删除。", "error");
        return;
    }
    deleteSkillBtn.disabled = true;
    try {
        const response = await fetch("/api/skills/delete", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ skill_id: skillId }),
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || "Skill 删除失败");
        }
        skillsCache = data.skills || [];
        selectedSkillEditorId = "none";
        populateSkillSelect(builderSkillSelect);
        populateSkillSelect(compareSkillSelect);
        populateSkillSelect(insightSkillSelect);
        loadSkillIntoEditor("none");
        setSkillMessage("Skill 已删除。", "ok");
    } catch (error) {
        setSkillMessage(error.message || "Skill 删除失败。", "error");
    } finally {
        deleteSkillBtn.disabled = false;
    }
}

async function generateSkillDraft() {
    generateSkillDraftBtn.disabled = true;
    generateSkillDraftBtn.textContent = "生成中...";
    setSkillMessage("正在根据业务场景生成 Skill 草稿...", "");
    try {
        const response = await fetch("/api/skills/generate-draft", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                scenario: skillScenarioInput.value.trim(),
                schema_text: skillSourceInput.value.trim(),
                requirement: skillRequirementInput.value.trim(),
            }),
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || "Skill 草稿生成失败");
        }
        fillSkillForm(data.skill);
        setSkillMessage("Skill 草稿已生成，可继续编辑后保存。", "ok");
    } catch (error) {
        setSkillMessage(error.message || "Skill 草稿生成失败。", "error");
    } finally {
        generateSkillDraftBtn.disabled = false;
        generateSkillDraftBtn.textContent = "生成 Skill 草稿";
    }
}

function loadCustodySkillDemo() {
    skillScenarioInput.value = "托管清算场景下，按产品、交易日期、清算日期和清算状态统计清算金额、成功笔数、失败笔数和差异金额，并识别清算失败原因。";
    skillSourceInput.value = `CREATE TABLE dwd_custody_clearing_detail_di (
    product_id STRING COMMENT '产品编号',
    account_id STRING COMMENT '托管账户号',
    trade_dt STRING COMMENT '交易日期',
    clear_dt STRING COMMENT '清算日期',
    clear_status STRING COMMENT '清算状态',
    trade_amt DECIMAL(18,2) COMMENT '交易金额',
    clear_amt DECIMAL(18,2) COMMENT '清算金额',
    diff_amt DECIMAL(18,2) COMMENT '差异金额',
    fail_reason STRING COMMENT '失败原因',
    dt STRING COMMENT '分区日期'
);`;
    skillRequirementInput.value = "要求优先使用 dt 或 clear_dt 过滤，金额字段使用 SUM，状态字段需要区分成功、失败和处理中，输出结果要便于对账复核。";
    skillDraftPreview.textContent = "托管清算样例已加载，可点击“生成 Skill 草稿”。";
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
        insightSkillSelect.value = skillsCache.some((item) => item.id === "custody_clearing_reconcile") ? "custody_clearing_reconcile" : "none";
        insightSchemaAssistCheckbox.checked = true;
        insightSchemaInput.value = SCHEMA_SAMPLE;
        resetSqlInsightOutputs();
        updateEnhancementVisibility();
        syncInsightPreviewState();
        setSqlInsightMessage("SQL 分析样例、Skill 和表结构样例已加载，可直接点击“分析并优化 SQL”。", "ok");
        return;
    }
    if (activeWorkspace === "skill") {
        loadCustodySkillDemo();
        setSkillMessage("托管清算 Skill 样例已加载，可生成草稿后保存。", "ok");
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
    activeBuilderDemoType = type;
    setMessage(`${sample.title}已加载，可直接点击“生成 SQL”进行演示。`, "ok");
}

function resetBuilderInputsAfterModeSwitch(nextMode) {
    const nextType = nextMode === "deepseek" ? "deepseek" : "rule";
    activeBuilderDemoType = "";
    mappingInput.value = "";
    compareMappingInput.value = "";
    requirementInput.value = "";
    compareRequirementInput.value = "";
    builderSkillSelect.value = "none";
    builderSchemaAssistCheckbox.checked = false;
    builderSchemaInput.value = "";
    builderSchemaUploadState = null;
    builderSchemaAnalysisCache = null;
    setBuilderSchemaMessage("", "");
    resetBuilderOutputs();
    updateEnhancementVisibility();
    syncBuilderPreviewState();
    setMessage("已切换生成模式，输入区已重置为空白。需要演示数据时可点击“加载样例”。", "");
}

async function loadCompareDemo() {
    setMessage("正在准备版本对比展示样例...", "");
    const response = await fetch("/api/demo-compare-setup", { method: "POST" });
    const data = await response.json();
    if (!response.ok) {
        throw new Error(data.error || "版本对比样例准备失败");
    }

    switchMode("compare");
    setCurrentGenerationMode(data.current.mode || "deepseek");
    compareSkillSelect.value = data.current.skill_id || "none";
    requirementInput.value = data.current.requirement || "";
    compareRequirementInput.value = data.current.requirement || "";
    compareMappingInput.value = JSON.stringify(data.current.mapping, null, 2);

    if (!Array.from(taskSelect.options).some((option) => option.value === data.task_name)) {
        const option = document.createElement("option");
        option.value = data.task_name;
        option.textContent = `${data.task_name}（${(data.versions || []).length} 个版本）`;
        taskSelect.appendChild(option);
    }
    taskSelect.value = data.task_name;

    historyVersionSelect.innerHTML = '<option value="">请选择版本</option>';
    (data.versions || []).forEach((version) => {
        const option = document.createElement("option");
        option.value = String(version.version_no);
        const requirementNote = version.user_requirement ? "含需求" : "无需求";
        option.textContent =
            `v${String(version.version_no).padStart(4, "0")} | ${version.created_at} | ${version.mode} | ${requirementNote}`;
        historyVersionSelect.appendChild(option);
    });
    historyVersionSelect.value = String(data.selected_version_no);
    try {
        await loadHistoryVersion();
    } catch {
        compareSummaryCard.textContent = "版本对比样例已加载，历史版本详情可手动点击查看。";
    }

    compareSkillSelect.value = data.current.skill_id || "none";
    compareRequirementInput.value = data.current.requirement || "";
    compareMappingInput.value = JSON.stringify(data.current.mapping, null, 2);
    syncComparePreviewState();
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
        enabled: scope === "compare" || scope === "insight" || scope === "insight-schema" || getCurrentGenerationMode() === "deepseek",
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
    syncCustomSkillSelect(builderSkillSelect);
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
    syncCustomSkillSelect(compareSkillSelect);
    if (activeWorkspace === "compare") {
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
    syncCustomSkillSelect(insightSkillSelect);
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
    compareRequirementSection.classList.toggle("hidden", activeWorkspace !== "compare");
    compareEnhancementSection.classList.toggle("hidden", activeWorkspace !== "compare");
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
    if (activeWorkspace === "skill") {
        loadDemoBtn.textContent = "加载 Skill 样例";
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

function setSkillMessage(text, type) {
    skillMessage.textContent = text;
    skillMessage.className = `form-message ${type}`.trim();
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
    newSkillBtn.disabled = isLoading;
    saveSkillBtn.disabled = isLoading;
    deleteSkillBtn.disabled = isLoading || skillIdInput.value === "none";
    generateSkillDraftBtn.disabled = isLoading;
    loadCustodySkillDemoBtn.disabled = isLoading;
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
    skillView.classList.toggle("hidden", mode !== "skill");
    schemaView.classList.toggle("hidden", mode !== "schema");
    builderModeBtn.classList.toggle("mode-pill-active", mode === "builder");
    compareModeBtn.classList.toggle("mode-pill-active", mode === "compare");
    insightModeBtn.classList.toggle("mode-pill-active", mode === "insight");
    skillModeBtn.classList.toggle("mode-pill-active", mode === "skill");
    schemaModeBtn.classList.toggle("mode-pill-active", mode === "schema");
    if (mode === "skill") {
        renderSkillManager();
    }
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
mappingInput.addEventListener("input", () => {
    activeBuilderDemoType = "";
});
modeSelect.addEventListener("change", updateEnhancementVisibility);
modeSelect.addEventListener("change", updateDemoButtonLabel);
builderModeSegment.addEventListener("click", (event) => {
    const button = event.target.closest("[data-mode-value]");
    if (!button) {
        return;
    }
    const nextMode = button.dataset.modeValue || "rule";
    if (nextMode === getCurrentGenerationMode()) {
        return;
    }
    setCurrentGenerationMode(nextMode);
    resetBuilderInputsAfterModeSwitch(nextMode);
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
skillModeBtn.addEventListener("click", () => switchMode("skill"));
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
document.addEventListener("click", () => closeOtherSkillMenus());
document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
        closeOtherSkillMenus();
    }
});
newSkillBtn.addEventListener("click", clearSkillEditor);
saveSkillBtn.addEventListener("click", saveSkill);
deleteSkillBtn.addEventListener("click", deleteSkill);
generateSkillDraftBtn.addEventListener("click", generateSkillDraft);
loadCustodySkillDemoBtn.addEventListener("click", loadCustodySkillDemo);

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
