# 代理維護指南（Guide for agents）

本文件說明如何在不破壞套件結構或提示詞品質的前提下修改 Humanizer-zh-HK。

## 儲存庫內容

Humanizer-zh-HK 是一份以 Markdown 編寫的代理技能（Agent Skill）。根目錄的 `SKILL.md` 是代理實際讀取的唯一提示詞檔案，整個專案無須編譯步驟。

保持技能跨平台通用，切勿寫入只限單一代理工具使用的專屬指令。

## 核心檔案

- `SKILL.md`：唯一技能真值來源，包含可攜式 YAML 元數據、AI 腔成因說明，以及分屬七大類（A 至 G）、按強度與出現頻率排列的 28 種模式。§1 至 §26 與上游 `blader/humanizer` v4.0.0 編號逐一對齊，§27 至 §28 為香港書面語專屬規則。
- `README.md`：安裝方式、使用說明及 28 種模式總表。
- `CHANGELOG.md`：版本更新紀錄，最新置頂。
- `.claude-plugin/plugin.json`：Claude 插件設定，將技能載入路徑指向根目錄 `SKILL.md`。
- `.claude-plugin/marketplace.json`：供使用者將本儲存庫加入 Claude 插件市集。
- `.cursor-plugin/plugin.json`：Cursor 插件設定；不設 `skills` 欄位，讓 Cursor 直接讀取根目錄 `SKILL.md`。
- `package.json`：pi 套件設定，`pi.skills` 指向根目錄；切勿加入頂層 `version` 欄位。
- `agents/openai.yaml`：OpenAI 相容代理的顯示名稱、簡介與預設提示詞。
- `scripts/validate-package.py`：零外部依賴套件檢查腳本，核對版本、描述、模式編號、引用及改寫範例品質。

## 修改守則

務必保持 `SKILL.md` 與 `README.md` 同步。

- **模式編號：** 模式必須由 1 開始連續編號，不得跳號。§1 至 §26 對應上游 `blader/humanizer` 模式編號；除非現有模式完全無法涵蓋，否則優先將新痕跡併入現有模式。若增刪或重排模式，必須同步更新 `README.md` 表格、章節標題及 `SKILL.md` 內所有 `§` 引用。
- **版本一致：** `SKILL.md` 的 `metadata.version`、`CHANGELOG.md` 首個版本標題、`.claude-plugin/plugin.json` 及 `.cursor-plugin/plugin.json` 必須使用同一版本號；切勿在 `SKILL.md` 加入頂層 `version` 欄位。
- **描述一致：** 各插件設定檔的 `description` 必須與 `SKILL.md` 描述的首句完全一致。
- **篇幅控制：** 每次呼叫技能都會完整讀取 `SKILL.md`，總字數上限為 16,000 字元（空白分詞上限 5,500），新增字句必須物有所值。
- **以身作則：** `SKILL.md` 與 `README.md` 的所有「改寫後」範例必須採用規範香港書面語及直角引號「`「…」`」，不得出現破折號（`——`、`—`）、西式彎引號（`“...”`）或 §12、§27 所列禁用套話與非港式詞彙，且不得遺漏或篡改「改寫前」的事實與數字。
- **提交前檢查：** 執行 `python3 scripts/validate-package.py` 確認全部檢查通過。
