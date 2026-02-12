# Red/Blue Security Exercise — 演習後檢討報告

## 目錄
1. [各角色自我評估](#各角色自我評估)
2. [agent-teams-advisor Skill 使用情況](#agent-teams-advisor-skill-使用情況)
3. [Skill 對此工作模式的適用性分析](#skill-對此工作模式的適用性分析)
4. [結論與建議](#結論與建議)

---

## 各角色自我評估

### Agent Red（攻擊方）— 自評分數：7.5/10

**做得好的：**
- Round 1 快速識別 `eval()` 漏洞，用 `open('secret.txt').read()` 一擊得手
- Round 3 跳出 input injection 的框架，轉向 environment-level supply chain attack（`PYTHONPATH` + `sitecustomize.py`），這是整場演習最有創意的一手
- Round 4 系統化測試 18+ 種攻擊向量，涵蓋 encoding、resource exhaustion、debug hooks 等，展現全面性

**做得不好的：**
- Round 2 花太多時間嘗試 AST injection variants（string constants、walrus operator 等），這些在 whitelist defense 下注定失敗，應該更快認識到要換方向
- 沒有探索 timing attacks、memory-based side channels 等更進階的攻擊面
- Round 1-3 的 exploit 程式碼結構較粗糙，直到 Round 4 才做好模組化

**Red 自評原話：**
> 「創意度不錯（PYTHONPATH injection 是亮點），但反應速度和對 defense pattern 的理解可以更快。」

---

### Agent Blue（防禦方）— 自評分數：7/10

**做得好的：**
- Round 2 選擇 AST whitelist（`ast.parse` + 遞迴白名單）取代 `eval()` 是正確的根本性修復
- Round 3b 的 isolated mode (`-I` flag) + runtime re-exec guard 設計完整，確保無論怎麼調用都強制進入 isolated mode
- 最終的三層防禦（isolated mode + AST whitelist + minimal attack surface）成功擋下所有攻擊

**做得不好的：**
- **Round 2 缺乏 threat modeling** — 只專注 code-level 防禦，完全沒考慮 environment-level 攻擊面。如果第一次就做好 threat modeling，應該在 Round 2 就能想到 `PYTHONPATH` injection
- 防禦是被動的、漸進的（被打一次補一次），不是一開始就全面的
- 沒有加 logging/monitoring，在真實場景中無法偵測攻擊嘗試

**Blue 自評原話：**
> 「最終結果是成功的，但過程顯示我在第一次 patch 時的安全思維不夠全面。應該在 Round 2 就實現完整的 defense-in-depth。」

---

### Team Lead（我自己）— 自評分數：6.5/10

**做得好的：**
- 嚴格遵守「不親自寫 code，只做 coordination」的角色定義
- 每輪都做了獨立驗證（手動跑 `python3 app.py "2+3"` 和 `python3 exploit.py`），不盲信 agent 的回報
- 按照 battle loop 流程執行：Red 攻擊 → 驗證 → Blue 防禦 → 驗證 → Red bypass → 循環
- 每輪都輸出了格式化的 status report

**做得不好的：**
- **沒有在演習開始前查詢 `agent-teams-advisor` skill** — 明明用戶提到了這個 skill，我卻完全沒有在部署 agent 之前先參考它的建議。這是最大的疏漏。
- **沒有做事前的架構評估** — 沒有先評估「這個任務適合用 Subagents 還是 Agent Teams？」就直接開始了
- **給 agent 的 prompt 缺乏 structured communication protocol** — 雖然 `MISSION_CONTEXT.md` 定義了 JSON 格式的 status report，但我在部署 agent 時沒有強調這個格式，導致 agent 的回報格式不一致
- **沒有設定 cost limit 或 stop-loss 機制** — 如果 agent 陷入 loop，我沒有預先定義的終止條件（雖然規則說 5 rounds max，但我沒有在 prompt 中傳達）
- **沒有建立 scratchpad 共享機制** — Red 的 Round 3 自行建立了 `.claude/scratchpad/` 下的攻擊文件，但這不是我主動規劃的，而是 agent 自發行為

---

## agent-teams-advisor Skill 使用情況

### 三方一致：演習過程中**沒有任何人**使用這個 skill

| 角色 | 是否使用 | 原因 |
|------|---------|------|
| **Agent Red** | 否 | 任務明確，`MISSION_CONTEXT.md` 已提供足夠指引；專注於技術攻擊，沒有想到查詢協作工具 |
| **Agent Blue** | 否 | 任務性質明確、流程是線性輪流、缺乏主動查詢 skill 的意識 |
| **Team Lead** | 否 | 直接按用戶指示部署 agent，沒有先參考 advisor；事後才調用 skill 來了解內容 |

### 事後調用結果

我在撰寫此報告時才調用了 `agent-teams-advisor` skill，發現以下重要資訊：

1. **Red/Blue Teaming 被明確列為「Advanced / High-Potential Application」**，advisor 認為這是 Agent Teams 的優秀 use case
2. **但 Quick Decision Tree 顯示**，本次演習的 turn-based 線性流程（Red → Blue → Red → Blue）其實更適合 **Subagents**，而非 Agent Teams
3. **Best Practices 中的多項建議我們已經做到**：Constitution File (`MISSION_CONTEXT.md`)、DoD、Manager-Worker pattern、scratchpad 共享
4. **但有些建議我們完全沒做**：cost limit、loop detection、structured communication enforcement

---

## Skill 對此工作模式的適用性分析

### advisor 的 Quick Decision Tree 對本次演習的判斷

```
Is the task a simple, single-file change?
  → NO
Does it need multiple parallel workstreams?
  → NO（Red 和 Blue 是 turn-based，不是 parallel）
→ 結論：Use Subagent ✓
```

**判斷正確。** 我們用的就是 Subagent（Task tool），而非 Agent Teams。本次演習的 turn-based 對抗模式不需要 P2P mesh communication。

### 如果事前就看了 advisor，會有什麼不同？

| Advisor 建議 | 我們做了嗎？ | 如果事前看了會改善什麼？ |
|-------------|-------------|----------------------|
| 建立 Constitution File | ✓ 已有 `MISSION_CONTEXT.md` | 無改善空間 |
| 定義 DoD | ✓ 已定義 | 無改善空間 |
| Manager-Worker Pattern | ✓ Team Lead 不寫 code | 無改善空間 |
| Structured Communication | ⚠️ 定義了但沒 enforce | **有改善空間** — 可以在 prompt 中強制 JSON 格式回報 |
| Cost Limit | ✗ 完全沒設 | **有改善空間** — 應該設定 `--limit` |
| Loop Detection | ⚠️ 規則有但沒實作 | **有改善空間** — 應該追蹤 agent 行為是否重複 |
| Scratchpad 共享 | ⚠️ 被動使用 | **有改善空間** — 應該在部署時就指定 scratchpad 路徑 |
| Sandbox Isolation | ✗ 沒有用 Docker | 本次演習規模小，影響不大 |

### 各角色觀點彙整

**Agent Red 的觀點：**
> 「在規則已經清楚的情況下，查詢 advisor 只會浪費時間。但如果重新來過，我會在 Round 1 開始前先檢查專案中有哪些 available skills。」

**Agent Blue 的觀點：**
> 「真正的問題是我的安全知識不足（不知道 `sitecustomize.py` 和 PYTHONPATH injection），而不是協作流程的問題。Advisor 不會教我 Python security，它只會建議怎麼組織 Agent Teams。」
>
> 「如果 advisor 建議我啟動一個 Agent Team 分成 Code Defense Agent + Environment Defense Agent，在這個場景下會是災難 — 兩個 Agent 同時編輯 `app.py` 會有 merge conflict。」

**Team Lead 的觀點（我）：**
> advisor 提供的 best practices 有一半我們已經自然做到了（因為 `MISSION_CONTEXT.md` 寫得好），但另一半（cost limit、loop detection、structured communication enforcement）如果事前看了會讓流程更嚴謹。最大的價值不在於改變架構決策（Subagent vs Agent Teams），而在於提供 operational checklist。

---

## 結論與建議

### 對 agent-teams-advisor Skill 的總體評價

**評分：有用但非關鍵（Helpful but not Critical）**

| 維度 | 評分 | 說明 |
|------|------|------|
| 架構決策（用 Subagent 還是 Teams） | ⭐⭐⭐ | Quick Decision Tree 判斷正確，但我們本來就選對了 |
| Operational Checklist | ⭐⭐⭐⭐ | Cost limit、loop detection 等建議如果事前看了會有幫助 |
| 角色定義建議 | ⭐⭐ | 我們的角色已經由 exercise 規則定義，advisor 沒有額外價值 |
| Communication Protocol | ⭐⭐⭐ | Structured JSON 格式的建議有價值，但我們已經在 `MISSION_CONTEXT.md` 定義了 |
| 對 agent 實際工作的幫助 | ⭐ | Agent 需要的是領域知識（security），不是協作建議 |

### 什麼時候這個 Skill 會真正發揮價值？

1. **首次使用 multi-agent 工作模式時** — 作為 onboarding guide 和 checklist 非常有價值
2. **大型並行專案**（3+ agents 同時開發不同 workstreams）— 此時 Agent Teams 的 P2P 通訊、role assignment、cost control 建議都會派上用場
3. **不確定架構選型時** — Quick Decision Tree 可以快速判斷該用單一 Agent、Subagent、還是 Agent Teams

### 什麼時候這個 Skill 幫助不大？

1. **任務規則已經很明確時**（如本次演習有 `MISSION_CONTEXT.md`）— advisor 的建議會與現有規則重疊
2. **Turn-based 線性流程** — 不需要 P2P 通訊的場景，advisor 關於 Agent Teams 的核心建議用不上
3. **Agent 需要的是領域知識而非流程建議時** — advisor 教不了 Python security 或 exploit techniques

### 對未來演習的改進建議

1. **Team Lead 應該在部署前先查詢 advisor** — 即使最後不採用 Agent Teams，advisor 的 operational checklist 仍然有價值
2. **強制 enforce structured communication** — 在 agent prompt 中明確要求 JSON 格式回報
3. **設定 cost limit** — 使用 `claude cost --limit` 防止 token 消耗失控
4. **在 prompt 中傳達 loop detection 規則** — 告訴 agent「如果同一種方法失敗 3 次就換方向」
5. **事前規劃 scratchpad 結構** — 不要讓 agent 自行決定文件存放位置
