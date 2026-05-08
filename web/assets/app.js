const mappingInput = document.getElementById("mappingInput");
const requirementInput = document.getElementById("requirementInput");
const requirementSection = document.getElementById("requirementSection");
const summaryCard = document.getElementById("summaryCard");
const versionCard = document.getElementById("versionCard");
const requirementCard = document.getElementById("requirementCard");
const sqlOutput = document.getElementById("sqlOutput");
const draftSqlOutput = document.getElementById("draftSqlOutput");
const normalizedMappingOutput = document.getElementById("normalizedMappingOutput");
const mappingDiagnosisList = document.getElementById("mappingDiagnosisList");
const issuesList = document.getElementById("issuesList");
const formMessage = document.getElementById("formMessage");
const loadExampleBtn = document.getElementById("loadExampleBtn");
const downloadTemplateBtn = document.getElementById("downloadTemplateBtn");
const generateBtn = document.getElementById("generateBtn");
const copySqlBtn = document.getElementById("copySqlBtn");
const modeSelect = document.getElementById("modeSelect");
const deepseekModelSection = document.getElementById("deepseekModelSection");
const deepseekConfigSection = document.getElementById("deepseekConfigSection");
const apiKeyInput = document.getElementById("apiKeyInput");
const modelInput = document.getElementById("modelInput");
const excelInput = document.getElementById("excelInput");
const rememberKeyCheckbox = document.getElementById("rememberKeyCheckbox");
const clearKeyBtn = document.getElementById("clearKeyBtn");
const builderModeBtn = document.getElementById("builderModeBtn");
const compareModeBtn = document.getElementById("compareModeBtn");
const builderView = document.getElementById("builderView");
const compareView = document.getElementById("compareView");
const refreshTasksBtn = document.getElementById("refreshTasksBtn");
const taskSelect = document.getElementById("taskSelect");
const historyVersionSelect = document.getElementById("historyVersionSelect");
const loadHistoryBtn = document.getElementById("loadHistoryBtn");
const compareBtn = document.getElementById("compareBtn");
const versionsList = document.getElementById("versionsList");
const compareSummaryCard = document.getElementById("compareSummaryCard");
const historyMappingOutput = document.getElementById("historyMappingOutput");
const historySqlOutput = document.getElementById("historySqlOutput");
const compareRequirementSection = document.getElementById("compareRequirementSection");
const compareRequirementInput = document.getElementById("compareRequirementInput");
const compareMappingInput = document.getElementById("compareMappingInput");
const currentCompareSqlOutput = document.getElementById("currentCompareSqlOutput");
const sqlDiffOutput = document.getElementById("sqlDiffOutput");
const mappingDiffOutput = document.getElementById("mappingDiffOutput");

const STORAGE_KEY = "mapping-sql-agent.deepseek.api-key";

async function loadExample() {
    setMessage("正在加载示例 Mapping...", "");
    try {
        const response = await fetch("/api/example");
        const data = await response.json();
        mappingInput.value = JSON.stringify(data.mapping, null, 2);
        if (!compareMappingInput.value.trim()) {
            compareMappingInput.value = JSON.stringify(data.mapping, null, 2);
        }
        setMessage("示例 Mapping 已加载，可以直接生成 SQL。", "ok");
    } catch {
        setMessage("示例加载失败，请稍后重试。", "error");
    }
}

async function parseExcelFile(file) {
    if (!file) {
        return;
    }
    if (!file.name.toLowerCase().endsWith(".xlsx")) {
        setMessage("当前仅支持上传 .xlsx 文件。", "error");
        excelInput.value = "";
        return;
    }

    setExcelState(true);
    setMessage(`正在解析 Excel Mapping：${file.name}`, "");

    try {
        const buffer = await file.arrayBuffer();
        const response = await fetch("/api/parse-excel", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                filename: file.name,
                file_base64: arrayBufferToBase64(buffer)
            })
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || "Excel 解析失败");
        }
        mappingInput.value = data.mapping_text;
        compareMappingInput.value = data.mapping_text;
        setMessage(data.message || "Excel Mapping 解析成功。", "ok");
    } catch (error) {
        setMessage(error.message || "Excel 解析失败。", "error");
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
    setMessage("正在生成 SQL 并执行规范校验...", "");

    try {
        const response = await fetch("/api/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                mapping_text: raw,
                ai_config: buildAiConfig(requirementInput.value.trim())
            })
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || "生成失败");
        }

        summaryCard.textContent = data.summary;
        sqlOutput.textContent = data.sql;
        draftSqlOutput.textContent = data.draft_sql || "当前为规则模式，没有单独草稿。";
        normalizedMappingOutput.textContent = data.normalized_mapping
            ? JSON.stringify(data.normalized_mapping, null, 2)
            : "没有可展示的修复结果。";
        renderIssues(mappingDiagnosisList, resolveMappingDiagnosis(data));
        renderIssues(issuesList, data.style_issues);
        updateVersionCard(data.version_record);
        updateRequirementCard(data.user_requirement || "");
        compareMappingInput.value = JSON.stringify(data.normalized_mapping, null, 2);
        if (data.user_requirement) {
            compareRequirementInput.value = data.user_requirement;
        }

        if (data.fallback_used) {
            setMessage(`DeepSeek 调用失败，已自动回退到规则模式：${data.fallback_reason}`, "error");
        } else if (data.mapping_repaired) {
            setMessage("Mapping 已自动修复并完成 SQL 生成，同时已保存为新版本。", "ok");
        } else {
            setMessage("SQL 生成完成，并已自动保存新版本。", "ok");
        }

        await loadVersionTasks();
    } catch (error) {
        summaryCard.textContent = "生成失败";
        versionCard.textContent = "当前还没有生成版本。";
        requirementCard.textContent = "当前未启用需求增强。";
        sqlOutput.textContent = "请检查 Mapping 内容后重试。";
        draftSqlOutput.textContent = "未生成草稿。";
        normalizedMappingOutput.textContent = "未生成修复后的 Mapping。";
        renderIssues(mappingDiagnosisList, ["当前没有 Mapping 诊断结果。"]);
        renderIssues(issuesList, [error.message || "生成失败"]);
        setMessage(error.message || "生成失败", "error");
    } finally {
        setLoadingState(false);
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
    versionsList.innerHTML = "<li>请选择任务后查看版本历史。</li>";

    if (!taskName) {
        return;
    }

    try {
        const response = await fetch(`/api/versions?task_name=${encodeURIComponent(taskName)}`);
        const data = await response.json();
        const versions = data.versions || [];

        versionsList.innerHTML = "";
        versions.forEach((version) => {
            const listItem = document.createElement("li");
            const requirementNote = version.user_requirement ? " | 含需求" : " | 无需求";
            listItem.textContent =
                `v${String(version.version_no).padStart(4, "0")} | ${version.created_at} | ${version.mode}${requirementNote}`;
            versionsList.appendChild(listItem);

            const option = document.createElement("option");
            option.value = String(version.version_no);
            option.textContent = `v${String(version.version_no).padStart(4, "0")}`;
            historyVersionSelect.appendChild(option);
        });

        if (versions.length > 0) {
            historyVersionSelect.value = String(versions[versions.length - 1].version_no);
            await loadHistoryVersion();
        }
    } catch {
        versionsList.innerHTML = "<li>版本列表加载失败。</li>";
    }
}

async function loadHistoryVersion() {
    const taskName = taskSelect.value;
    const versionNo = historyVersionSelect.value;
    if (!taskName || !versionNo) {
        compareSummaryCard.textContent = "请选择任务和历史版本。";
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
            `${data.task_name} | 历史版本 v${String(data.version_no).padStart(4, "0")} | ` +
            `${data.created_at} | ${data.mode}${requirementText}`;
        historyMappingOutput.textContent = JSON.stringify(data.mapping, null, 2);
        historySqlOutput.textContent = data.sql;

        if (!compareMappingInput.value.trim()) {
            compareMappingInput.value = JSON.stringify(data.mapping, null, 2);
        }
        if (data.user_requirement && !compareRequirementInput.value.trim()) {
            compareRequirementInput.value = data.user_requirement;
        }
    } catch (error) {
        compareSummaryCard.textContent = error.message || "历史版本加载失败";
        historyMappingOutput.textContent = "没有可展示的历史 Mapping。";
        historySqlOutput.textContent = "没有可展示的历史 SQL。";
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

    try {
        const response = await fetch("/api/compare-with-current", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                task_name: taskName,
                version_no: Number(versionNo),
                mapping_text: raw,
                ai_config: buildAiConfig(compareRequirementInput.value.trim())
            })
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || "对比失败");
        }

        const currentRequirementText = data.current.user_requirement
            ? ` | 当前需求：${data.current.user_requirement}`
            : " | 当前未填写需求";
        compareSummaryCard.textContent =
            `${data.task_name} | 历史版本 v${String(data.historical.version_no).padStart(4, "0")} ` +
            `vs 当前输入 Mapping${currentRequirementText}`;
        historyMappingOutput.textContent = JSON.stringify(data.historical.mapping, null, 2);
        historySqlOutput.textContent = data.historical.sql;
        currentCompareSqlOutput.textContent = data.current.sql;
        compareMappingInput.value = JSON.stringify(data.current.mapping, null, 2);
        renderDiff(sqlDiffOutput, data.sql_diff);
        renderDiff(mappingDiffOutput, data.mapping_diff);
    } catch (error) {
        compareSummaryCard.textContent = error.message || "对比失败";
        currentCompareSqlOutput.textContent = "没有可展示的当前 SQL。";
        sqlDiffOutput.textContent = "没有可展示的 SQL 差异。";
        mappingDiffOutput.textContent = "没有可展示的 Mapping 差异。";
    }
}

function buildAiConfig(userRequirement) {
    return {
        enabled: modeSelect.value === "deepseek",
        api_key: apiKeyInput.value.trim(),
        model: modelInput.value.trim() || "deepseek-v4-flash",
        user_requirement: userRequirement || ""
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
        `已保存版本 v${String(versionRecord.version_no).padStart(4, "0")} | ` +
        `${versionRecord.created_at} | ${versionRecord.task_name}`;
}

function updateRequirementCard(userRequirement) {
    requirementCard.textContent = userRequirement
        ? userRequirement
        : "当前未启用需求增强。";
}

function updateRequirementVisibility() {
    const isDeepSeek = modeSelect.value === "deepseek";
    deepseekModelSection.classList.toggle("hidden", !isDeepSeek);
    deepseekConfigSection.classList.toggle("hidden", !isDeepSeek);
    requirementSection.classList.toggle("hidden", !isDeepSeek);
    compareRequirementSection.classList.toggle("hidden", !isDeepSeek);
}

function setMessage(text, type) {
    formMessage.textContent = text;
    formMessage.className = `form-message ${type}`.trim();
}

function setLoadingState(isLoading) {
    generateBtn.disabled = isLoading;
    loadExampleBtn.disabled = isLoading;
    downloadTemplateBtn.disabled = isLoading;
    modeSelect.disabled = isLoading;
    apiKeyInput.disabled = isLoading;
    modelInput.disabled = isLoading;
    excelInput.disabled = isLoading;
    rememberKeyCheckbox.disabled = isLoading;
    clearKeyBtn.disabled = isLoading;
    requirementInput.disabled = isLoading;
    compareRequirementInput.disabled = isLoading;
    generateBtn.textContent = isLoading ? "生成中..." : "生成 SQL";
}

function setExcelState(isLoading) {
    excelInput.disabled = isLoading;
}

function arrayBufferToBase64(buffer) {
    let binary = "";
    const bytes = new Uint8Array(buffer);
    const chunkSize = 0x8000;
    for (let i = 0; i < bytes.length; i += chunkSize) {
        const chunk = bytes.subarray(i, i + chunkSize);
        binary += String.fromCharCode(...chunk);
    }
    return btoa(binary);
}

function restoreApiKey() {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (!saved) {
        rememberKeyCheckbox.checked = false;
        return;
    }
    apiKeyInput.value = saved;
    rememberKeyCheckbox.checked = true;
}

function persistApiKey() {
    if (!rememberKeyCheckbox.checked) {
        localStorage.removeItem(STORAGE_KEY);
        return;
    }
    if (apiKeyInput.value.trim()) {
        localStorage.setItem(STORAGE_KEY, apiKeyInput.value.trim());
    }
}

function clearStoredApiKey() {
    localStorage.removeItem(STORAGE_KEY);
    apiKeyInput.value = "";
    rememberKeyCheckbox.checked = false;
    setMessage("浏览器本地缓存中的 API Key 已清除。", "ok");
}

function switchMode(mode) {
    const builderActive = mode === "builder";
    builderView.classList.toggle("hidden", !builderActive);
    compareView.classList.toggle("hidden", builderActive);
    builderModeBtn.classList.toggle("mode-pill-active", builderActive);
    compareModeBtn.classList.toggle("mode-pill-active", !builderActive);
}

loadExampleBtn.addEventListener("click", loadExample);
downloadTemplateBtn.addEventListener("click", () => {
    window.location.href = "/api/template.xlsx";
});
generateBtn.addEventListener("click", generateSql);
copySqlBtn.addEventListener("click", async () => {
    const content = sqlOutput.textContent.trim();
    if (!content || content === "等待生成 SQL..." || content === "请检查 Mapping 内容后重试。") {
        setMessage("当前没有可复制的 SQL。", "error");
        return;
    }
    try {
        await navigator.clipboard.writeText(content);
        setMessage("SQL 已复制到剪贴板。", "ok");
    } catch {
        setMessage("复制失败，请手动复制。", "error");
    }
});
excelInput.addEventListener("change", (event) => parseExcelFile(event.target.files[0]));
rememberKeyCheckbox.addEventListener("change", persistApiKey);
apiKeyInput.addEventListener("input", persistApiKey);
clearKeyBtn.addEventListener("click", clearStoredApiKey);
modeSelect.addEventListener("change", updateRequirementVisibility);
builderModeBtn.addEventListener("click", () => switchMode("builder"));
compareModeBtn.addEventListener("click", async () => {
    switchMode("compare");
    compareMappingInput.value = mappingInput.value.trim() || compareMappingInput.value;
    compareRequirementInput.value = requirementInput.value.trim() || compareRequirementInput.value;
    await loadVersionTasks();
});
refreshTasksBtn.addEventListener("click", loadVersionTasks);
taskSelect.addEventListener("change", (event) => loadVersionsForTask(event.target.value));
loadHistoryBtn.addEventListener("click", loadHistoryVersion);
compareBtn.addEventListener("click", compareWithCurrentMapping);

restoreApiKey();
switchMode("builder");
updateRequirementVisibility();
loadExample();
loadVersionTasks();
