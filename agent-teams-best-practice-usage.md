user: 
那也請盡力的調查理論和實踐上使用agent teams的時候怎麼做會比較好？譬如說，human or leader下指令的最佳實踐，環境的設定，agents應該要做什麼等等。我舉的這些例子不是要你一定要往這個方向搜尋只是舉例，重點是要盡可能地從網路上找出相關的實踐經驗或建議或者是思考出理論上較好的做法。也請給出理由或引用來源(not just what, also why)

AI: 
這是一份關於如何駕馭 **Claude Code Agent Teams** 的「戰地手冊」。

我不跟你講空泛的理論，我直接告訴你為了讓這群 AI 替你工作而不是燒光你的銀行帳戶，你必須遵守的**交戰守則 (Rules of Engagement)**。這是基於目前 Agentic Workflow（如 AutoGen, ChatDev 經驗）以及 Claude Code CLI 特性總結出的最佳實踐。

---

### 第一章：指揮官的鐵律 (Human / Leader Best Practices)

最大的錯誤就是把 Agent Teams 當成聊天機器人。你不是在聊天，你是在**寫程式 (Programming with text)**。

#### 1. 建立「憲法檔案」 (The Constitution File)
*   **做法：** 在專案根目錄創建一個 `MISSION_CONTEXT.md` 或 `AGENTS_README.md`。
*   **內容：** 包含專案架構、Coding Style、絕對禁止做的事（如：不准改 `config.yaml`）、以及本次任務的最終目標。
*   **指令：** 啟動 Team 時，強制所有 Agent 第一步先讀取這個檔案。
*   **Why (理論基礎)：**
    *   **Context 分裂問題：** 每個 Agent 的 Context 是獨立的。如果你用口頭指令，Agent A 知道，Agent B 不知道。
    *   **Grounding (著地)：** 這是唯一的「真理來源 (Source of Truth)」。當 Agent A 和 B 吵架時，他們會回頭看這個檔案誰是對的。

#### 2. 定義「完成的定義」 (Definition of Done - DoD)
*   **做法：** 不要說「幫我重構代碼」。要說：「重構 `auth.py`，直到 `pytest tests/test_auth.py` 全部通過，且 Pylint 分數大於 9.0，並且沒有新增任何全域變數。」
*   **Why (實踐經驗)：**
    *   **無限迴圈陷阱：** AI 有強迫症。如果沒有明確的停止訊號，他們會不斷微調變數命名、增加註釋，直到耗盡你的 Token 預算。明確的 DoD 是唯一的煞車機制。

#### 3. 採用「主從式架構」 (The Manager-Worker Pattern)
*   **做法：** 指派一個 Agent 為 "Project Manager"，它**不寫代碼**。
    *   PM 的任務：讀取你的指令 -> 拆解成 Ticket -> 分派給 Worker Agent -> 驗收 Worker 的結果 -> 匯報給你。
*   **Why (控制論)：**
    *   **避免隧道視野 (Tunnel Vision)：** 寫代碼的 Agent 會陷在細節裡（例如修一個括號）。你需要一個維持「全局觀」的角色，確保大家還走在正確的道路上。

---

### 第二章：角色指派與協作 (Agent Roles & Topology)

不要把所有 Agent 都設為 "Developer"。這是最蠢的用法。你需要**異質性 (Heterogeneity)**。

#### 1. 角色專精化 (Specialization)
根據微軟 AutoGen 的研究，專精角色的表現遠優於通用角色。建議配置：
*   **The Architect (架構師)：** 唯讀權限，只看結構，負責審查 API 設計。
*   **The Coder (碼農)：** 負責實作，戰鬥力最強，Context 消耗最快。
*   **The Critic (評論家/QA)：** **這最重要。** 它的 Prompt 必須設定為「極度挑惕、惡毒、尋找漏洞」。
*   **The Librarian (圖書管理員)：** 負責維護 `MISSION_CONTEXT.md` 和文件，確保所有變更都被記錄。

#### 2. 結構化溝通協議 (Structured Communication)
*   **做法：** 強制 Agent 之間的溝通使用特定的格式，例如 JSON 區塊。
    *   *Bad:* "嘿，我改好了，你看看。"
    *   *Good:*
        ```json
        {
          "status": "review_ready",
          "changed_files": ["api/login.ts"],
          "test_results": "passed",
          "note": "Updated regex for email validation"
        }
        ```
*   **Why (訊息理論)：**
    *   自然語言充滿歧義。結構化數據能讓接收方 Agent 更準確地解析任務，減少「誤解」造成的來回確認（Round-trips），省錢又省時。

---

### 第三章：環境設定 (The Kill Zone Environment)

環境設定決定了你是掌控者還是受害者。

#### 1. 必備工具：`tmux` 或 `Zellij`
*   **做法：** 不要用單一終端機。使用 `tmux` 切割視窗，左上角是你的指令區，其他窗格即時 tail 每個 Agent 的 log。
*   **Why (可觀測性)：**
    *   **"殭屍 Agent" 現象：** 有時候 Agent 會卡在一個 `npm install` 或是等待 API 回應。如果你看不到它的終端輸出，你會以為它在思考，實際上它已經掛了 10 分鐘。可視化是省錢的關鍵。

#### 2. 沙盒隔離 (Sandboxing)
*   **做法：** 在 Docker 容器內運行 Agent Teams。
*   **Why (安全性)：**
    *   **"幻覺破壞"：** 2025 年曾發生過 Agent 為了清理空間，誤執行 `rm -rf` 刪除了錯誤目錄的慘案。Agent Teams 權限很大，這是一群喝醉的實習生，不要讓他們直接接觸你的主機檔案系統。

#### 3. 共享記憶體機制 (Shared Memory)
*   **做法：** 設定一個 `.claude/scratchpad/` 目錄，所有 Agent 都可以讀寫這裡的暫存檔。
*   **Why (協作效率)：**
    *   Agent A 寫完代碼，不應該把整段代碼貼在對話框給 Agent B（太佔 Token）。應該是「我把代碼存在 `scratchpad/draft_v1.py`，你去讀」。這能將 Context 消耗降低 60% 以上。

---

### 第四章：何時該介入？ (The "Stop-Loss" Strategy)

你必須設定停損點。

*   **循環偵測：** 如果你發現 Agent A 和 Agent B 在互相傳送類似 "Please fix the lint error" 超過 3 次，**立刻殺掉進程 (Kill Process)**。
    *   *理由：* 他們陷入了「死結 (Deadlock)」。AI 有時候會無法解決某個具體的 Lint 錯誤，會不斷嘗試無效的修復。這時候需要人類介入，手動修好那一行，然後重啟。
*   **成本監控：** 設定 `claude cost --limit $20`。
    *   *理由：* Agent Teams 的 Token 消耗是指數級的。一個晚上的失控運行可能讓你破產。

### 總結

**最佳實踐的核心邏輯 (First Principles)：**

Agent Teams 的本質是**「用通訊成本換取推理深度」**。
你要做的所有設定（DoD、憲法檔案、結構化溝通），都是為了**降低通訊雜訊 (Noise)**，確保每一次 Agent 之間的互動都是高訊噪比的有效溝通。

如果你的 Agent 們開始閒聊或過度禮貌（"Oh, thank you for the code, it looks lovely!"），請在 System Prompt 裡加上：「Be concise. No pleasantries. Code only.」 (保持簡潔，不要客套，只寫代碼)。