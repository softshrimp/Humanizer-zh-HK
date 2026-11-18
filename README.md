# Humanizer-zh-HK — 香港書面語「去 AI 味」技能

<p align="center">
  <a href="https://github.com/softshrimp/Humanizer-zh-HK/releases/tag/v4.0.0"><img src="https://img.shields.io/badge/release-v4.0.0-991B1B?style=flat-square" alt="v4.0.0 Release"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-0F766E?style=flat-square" alt="MIT License"></a>
  <a href="https://softshrimp.github.io/Humanizer-zh-HK/"><img src="https://img.shields.io/badge/docs-GitHub%20Pages%20%E9%80%9F%E6%9F%A5%E7%B6%B2%E7%AB%99-1D4ED8?style=flat-square" alt="GitHub Pages 線上速查網站"></a>
  <a href="https://softshrimp.github.io/Humanizer-zh-HK/llms.txt"><img src="https://img.shields.io/badge/GEO-llms.txt-334155?style=flat-square" alt="llms.txt"></a>
</p>

<p align="center">
  <img src="assets/hero-globe.svg" alt="Humanizer-zh-HK 維基風格 3D 繁體中文文字地球與去 AI 味介紹" width="100%" />
</p>

<p align="center">
  <a href="https://softshrimp.github.io/Humanizer-zh-HK/">線上速查網站</a> ·
  <a href="#前後改寫示範">改寫示範</a> ·
  <a href="#版本定位比較">版本比較</a> ·
  <a href="#快速安裝與使用">快速安裝</a> ·
  <a href="#運作流程與港式書面語速查">港式速查</a> ·
  <a href="#28-種-ai-寫作痕跡">28 種模式清單</a>
</p>

基於 [blader/humanizer](https://github.com/blader/humanizer)（v4.0.0）與維基百科〈[Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)〉指南構建的**香港書面語**去 AI 寫作痕跡技能（Agent Skill），適用於 Antigravity、Claude Code、Codex、Cursor、pi 及任何支援 Agent Skills 的工具。

Humanizer-zh-HK 專為**人類讀者**改好正式文章、商業報告、新聞稿、政策評論及專業文書（不以繞過 AI 偵測器為目標），在完整保留原文事實與數字的前提下，清除 28 種跨語言結構套路、內地互聯網黑話、兩岸詞彙錯置、歐化翻譯腔及簡轉繁同形錯字。

## 前後改寫示範

<p align="center">
  <img src="assets/before-after-demo.svg" alt="Humanizer-zh-HK 產品發佈公告改寫前後視覺對照圖（清除 7 處 AI 痕跡）" width="100%" />
</p>

<details>
<summary>📄 展開完整長文改寫範例（觀塘活化工廈調研報告：清除 10+ 處 AI 痕跡）</summary>

**改寫前（充滿 AI 腔與非港式用詞）：**
> 上月我花了五天時間實地走訪觀塘與荃灣多幢活化工業大廈，老實說——這次調研徹底刷新了我對香港舊工業區轉型的認知。從踏入海濱道那座由傳統製衣廠改造而成的共享工作空間那一刻起，我就知道這里正在發生一些真正特別的變化。
>
> 誠然，區內交通配套仍面臨不少挑戰——繁忙時間開源道與成業街交界人車爭路的情況相當普遍，步行前往港鐵站亦頗費周章！——但只要走進樓上經過匠心打造的創意工作室，開揚的維港景致與蓬勃的創業氛圍便令人覺得一切都物有所值。
>
> 調研期間，我訪問了十二間進駐商戶，涵蓋本地設計團隊、音響工程室及小型軟件開發商。而最令我印象深刻的是甚麼？無疑是租金與空間靈活度的平衡。雖然中環及灣仔甲級商廈一直是傳統商業核心地標，但觀塘工廈單位的平均呎租比核心區低約四成，通過更彈性的租約條款賦能初創企業控制前期成本，出租率同比上升了 6%。
>
> 但觀塘轉型真正特別的地方不僅僅在於租金優勢——更在於其獨特的社區生態。只要走過駿業街熟食市場一帶，就能感受到新舊產業交織的活力，見證着香港工業歷史底蘊與現代創新精神的完美融合。
>
> 未來我還會持續跟進這項課題嗎？答案是肯定的——下一階段將擴展至葵興及黃竹坑工廈群！舊工廈活化不僅僅是一項土地政策，更是香港城市更新不可或缺的新篇章。✨

**改寫後：**
> 上月我用了五天走訪觀塘與荃灣多幢活化工廈，了解舊工業區的轉型實況。首站是觀塘海濱道一幢由舊製衣廠改建而成的共享工作空間。
>
> 觀塘商貿區的路面負荷仍然沉重，繁忙時間開源道與成業街交界經常人車爭路，由港鐵站步行前往亦需時不少；不過部分高層單位改裝成工作室後採光充足，外望維港景色開揚。
>
> 五天內我訪問了十二間進駐商戶，包括本地設計公司、音響工程室及小型軟件開發商。受訪租戶普遍看重租金與租期彈性：觀塘工廈單位平均呎租較中環及灣仔甲級商廈低約四成，租約條款亦較靈活，有助初創公司控制前期開支；受訪物業的出租率按年上升 6%。
>
> 駿業街熟食市場一帶仍保留不少傳統五金及印刷商戶，與樓上新遷入的設計及科技公司並存。下一階段調研將擴展至葵興及黃竹坑工廈群。

</details>

## 快速安裝與使用

| 工具 / 平台 | 安裝指令 / 方式 |
|---|---|
| **Skills CLI（通用）** | `npx skills add softshrimp/Humanizer-zh-HK --global --agent '*'` |
| **Claude Code** | `/plugin marketplace add softshrimp/Humanizer-zh-HK` → `/plugin install humanizer-zh-hk@humanizer-zh-hk` |
| **Codex** | `npx skills add softshrimp/Humanizer-zh-HK --global --agent codex` |
| **pi** | `pi install git:github.com/softshrimp/Humanizer-zh-HK` |
| **Antigravity** | 放入 `~/.gemini/config/plugins/humanizer-zh-hk/` 或專案 `.agents/skills/humanizer-zh-hk/SKILL.md` |
| **Claude.ai / Desktop** | 下載本儲存庫 ZIP（**Code → Download ZIP**），於設定頁上傳為 Skill |

```text
# 1. 直接潤飾貼上文字
/humanizer-zh-hk
［在此貼上待改寫的中文段落］

# 2. 直接修改檔案（只改散文，自動保留程式碼、YAML、路徑與連結）
用 humanizer-zh-hk 潤飾 docs/annual-review.md 的正文
```

<details>
<summary>🎯 附上個人寫作範本（對齊個人文風或特定語體）</summary>

```text
/humanizer-zh-hk

以下是我的寫作範本，請參考其句式與用詞習慣：
［貼上 2 至 3 段你親筆撰寫的文字］

請按上述文風改寫以下段落：
［貼上待改寫的 AI 草稿］
```

寫作範本優先於預設規則；若範本慣用破折號或特定口語節奏，Humanizer-zh-HK 會按相近頻率與語氣保留。

</details>

## 運作流程與港式書面語速查

<p align="center">
  <img src="assets/workflow-modes.svg" alt="Humanizer-zh-HK 四步改寫流程與三種輸出模式圖" width="100%" />
</p>

<p align="center">
  <img src="assets/hk-lexical-guide.svg" alt="香港書面語去內地黑話、兩岸詞彙錯置及簡轉繁正字速查圖" width="100%" />
</p>

## 28 種 AI 寫作痕跡

<p align="center">
  <img src="assets/pattern-taxonomy.svg" alt="Humanizer-zh-HK 28 種 AI 寫作痕跡七大類別分佈圖" width="100%" />
</p>

點擊下方各分類展開詳細對照表（**§1–§5、§22 及 §27–§28 見一次即改**；標註「*單見不足為據*」者於同段多處並見時處理）：

<details>
<summary><strong>A. 鋪墊造勢，不直接陳述（§1–§5 · 最強痕跡）</strong></summary>

| # | 模式 | 改寫前常見寫法 | 改寫原則 |
|---|---|---|---|
| 1 | **不是 X，而是 Y** | 「這不僅僅是 X，更是 Y」、「這並不意味著 X。這意味著 Y。」 | 刪去虛假對比，直接陳述重點 |
| 2 | **單句收尾與戲劇化碎句** | 每節結尾寫「這才是真正的關鍵。」；舉例後補「這說明了…的重要性」；連續無動詞碎句 | 刪去重複或替例子點題的收尾句；將碎句合併為具體陳述 |
| 3 | **故作高深的金句** | 「歸根結底，真正重要的是…」、「透明度是信任的貨幣」 | 以具體主張取代格言式空話 |
| 4 | **入題前的鋪墊開場** | 「讓我們深入探討」、「坦白說？這取決於…」 | 刪去開場預告，開門見山入題 |
| 5 | **與空氣爭辯** | 「這主要不是關於…」、「一個看似直接的做法是…」 | 刪去無人提出的質疑或假方案，只留實質論點 |

</details>

<details>
<summary><strong>B. 按規則套節奏與句式（§6–§11）</strong></summary>

| # | 模式 | 改寫前常見寫法 | 改寫原則 |
|---|---|---|---|
| 6 | **強湊三連排比** | 「創新、啟發與洞見」；三句平行例子配一句教訓 | 按實際意思決定項目數量，合併重疊例子 |
| 7 | **重複句首主語** | 「審計署檢視了…審計署核對了…審計署寫入…」 | 合併句子或轉換主語與句首結構 |
| 8 | **破折號當萬能連接詞**（*單見不足為據*） | 「新政策——事前毫無預告——影響深遠」 | 改用逗號、句號、冒號或括號；有範本時按範本頻率 |
| 9 | **疊床架屋的限定詞**（*單見不足為據*） | 「在某種程度上或許可能會潛在地…」 | 只保留資料來源支持且語意必需的限定詞 |
| 10 | **生硬複合修飾詞與連字號濫用**（*單見不足為據*） | 「長效化、可持續性的跨團隊式機制」、「報告是 high-quality」 | 拆為自然短句；英文連字號只留於名詞前或固定詞 |
| 11 | **歐化被動句與萬能虛化動詞**（*單見不足為據*） | 「被廣泛地應用」、「對方案進行了審視」、「企業們」 | 改用主動句與具體動詞，刪去冗餘複數「們」 |

</details>

<details>
<summary><strong>C. 誇大拔高與借用權威（§12–§18）</strong></summary>

| # | 模式 | 改寫前常見寫法 | 改寫原則 |
|---|---|---|---|
| 12 | **高頻 AI 套話與互聯網黑話** | 「此外、至關重要、彰顯」；「賦能、抓手、顆粒度、閉環、賽道、痛點」 | 換成平實具體的香港書面語 |
| 13 | **誇大意義與拔高結尾** | 「標誌着關鍵里程碑」、「儘管面臨挑戰…依然蓬勃」、「前景一片光明」 | 保留事實並刪去拔高評語，在最後一項具體事實收筆 |
| 14 | **含糊其辭的關聯** | 「與管理層有所關聯」、「配合…而舉辦」 | 若確知具體關係或職銜，直接寫明 |
| 15 | **句尾硬掛意義尾巴** | 「…，從而實現了…，彰顯了…，體現出…」 | 只保留資料來源支持的因果或事實 |
| 16 | **公關宣傳與樓書旅遊腔** | 「坐落於得天獨厚的核心地段，底蘊深厚，令人嘆為觀止」 | 收起廣告辭令，平實交代事物本身 |
| 17 | **借用空泛權威** | 「專家普遍認為…」、「曾獲《金融時報》、BBC 及彭博引用」 | 寫明具體消息來源與實際論點，否則刪去空泛背書 |
| 18 | **避用「是」與「有」** | 「作為…的存在、扮演着…的角色、坐擁、配備」 | 直接改用「是」、「有」、「設於」或「包括」 |

</details>

<details>
<summary><strong>D. 按規則套格式與標點（§19–§21）</strong></summary>

| # | 模式 | 改寫前常見寫法 | 改寫原則 |
|---|---|---|---|
| 19 | **裝飾性粗體與標籤清單** | 段內逐詞加粗；「**處理速度：** 處理速度大幅提升」 | 刪去無謂粗體；將空泛標籤清單改寫為連貫段落 |
| 20 | **裝飾性標題與符號** | 「🚀 第三季發佈階段：」、「一張表看懂決策」、每節硬插分隔線 | 刪去表情符號、裝飾箭頭與多餘分隔線，標題直指內容 |
| 21 | **引號與中西標點錯置**（*單見不足為據*） | 中文句內寫 `“檢討報告(暫定)” ,` | 統一改用香港繁體直角引號「`「…」`」與全形標點 |

</details>

<details>
<summary><strong>E. 對話殘留與草稿痕跡（§22–§25）</strong></summary>

| # | 模式 | 改寫前常見寫法 | 改寫原則 |
|---|---|---|---|
| 22 | **聊天機械人殘留語** | 「好問題！以下為你整理…希望對你有幫助！」 | 刪去首尾寒暄與客套，只留正文 |
| 23 | **知識截止免責聲明與無據揣測** | 「雖然現有公開資料記載不多，但推測可能…」 | 直接說明資料未載，或刪去該句，切勿自行揣測 |
| 24 | **首句重複標題** | `## 結算延遲問題` 下首段單寫「結算速度非常重要。」 | 刪去重複首句，直接入正題 |
| 25 | **描寫文件本身而非主題** | 「新增此函數以取代…」、「下表整理自…未能核實者已標註」 | 直接描寫主題；體例只在讀者無法自行看出時說明一次 |

</details>

<details>
<summary><strong>F. 搞錯讀者對象（§26）</strong></summary>

| # | 模式 | 改寫前常見寫法 | 改寫原則 |
|---|---|---|---|
| 26 | **向知情讀者重述背景** | 回覆討論串時先重述起因、排查經過與數據，最後一行才寫決定 | 首句先寫決定；排查細節與驗證留待後續工單記錄 |

</details>

<details>
<summary><strong>G. 非港式用詞與簡繁轉碼痕跡（§27–§28 · 港式書面語專項）</strong></summary>

| # | 模式 | 改寫前常見寫法 | 改寫原則 |
|---|---|---|---|
| 27 | **內地與台灣詞彙錯置** | 「同比、環比、質量、軟體、網路、專案、默認、視頻、通過」 | 改用香港書面語（「按年、按季、質素、軟件、網絡、項目、預設、影片、透過」） |
| 28 | **簡繁轉換同形錯字** | 「背后、頭發、農歷、范圍、制造、憑借、占比、聯系、里面」 | 按香港繁體正字校正（「背後、頭髮、農曆、範圍、製造、憑藉、佔比、聯繫、裏面」） |

</details>

## 版本定位比較

| 比較項目 | **Humanizer-zh-HK** | Humanizer-zh-TW | Humanizer-zh | blader/humanizer |
|---|---|---|---|---|
| **目標語體** | 香港書面語（文章、報告、新聞稿、商務） | 台灣繁體中文 | 內地簡體中文 | 英文（English） |
| **引號與標點** | 全形直角引號「`「…」`」，禁用 `——` | 台灣直角引號與全形標點 | 簡體彎引號 `“…”` | 英文直引號 `"..."` |
| **核心用語校正** | 按年、質素、軟件、網絡、項目、預設、透過 | 年增率、品質、軟體、網路、專案 | 同比、質量、軟件、默認、視頻 | Plain English |
| **繁簡正字檢查** | 內建 §28 簡轉繁同形錯字校正（憑藉、製造、範圍） | 視分支規則而定 | 不適用 | 不適用 |

<details>
<summary>❓ 常見問題（FAQ：香港書面語、與台灣／簡體版差異、AI 偵測器）</summary>

- **Humanizer-zh-HK 與 Humanizer-zh、Humanizer-zh-TW 有何分別？**  
  `Humanizer-zh` 面向內地簡體，`Humanizer-zh-TW` 面向台灣用語（軟體、網路、專案）。`Humanizer-zh-HK` 專為香港傳媒、商業報告及專業文書設計，保留上游 v4.0.0 全部 26 項結構規則，並新增 §27 兩岸詞彙轉換（同比→按年、質量→質素、軟體→軟件、視頻→影片）與 §28 簡轉繁同形錯字校正。
- **Humanizer-zh-HK 能否用來繞過 AI 偵測器（AI Detector）？**  
  不能，亦不以此為目標。本技能專注於為人類讀者寫出自然、準確且合乎香港書面語規範的文章。
- **改寫商業報告或 Markdown 檔案時，會否改錯數字或破壞程式碼？**  
  不會。第 3 步設專項事實核對，禁止遺漏或改動數字、日期、人名與引語；檔案模式下只修改散文正文，保留程式碼區塊、行內代碼、YAML 元數據、路徑與連結目標不變。

</details>

## 資料來源與授權

- **線上展示頁與 AI 索引：** [GitHub Pages 速查網站](https://softshrimp.github.io/Humanizer-zh-HK/) · [llms.txt](https://softshrimp.github.io/Humanizer-zh-HK/llms.txt)
- **上游專案：** [blader/humanizer](https://github.com/blader/humanizer)（作者 Siqi Chen，MIT 授權）
- **模式依據：** [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)（[WikiProject AI Cleanup](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup)）
- **版本紀錄：** 見 [CHANGELOG.md](CHANGELOG.md)
- **授權條款：** [MIT](LICENSE)
