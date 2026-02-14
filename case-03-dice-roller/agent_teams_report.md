# Agent Teams 測試報告

## 產出成果
- **dice_roller.py** — 丟骰子 script，支援自訂面數/顆數、輸入驗證、CLI 介面
- **test_dice_roller.py** — 20 個 pytest 測試，全部通過

## 團隊運作時間線

| 階段 | 事件 |
|------|------|
| 1 | Coder 快速完成初版 dice_roller.py |
| 2 | Tester 等待 coder 完成（team lead 介入推了一下） |
| 3 | Tester 撰寫 18 個測試，全部通過 |
| 4 | Reviewer 進行第一輪 review，發現 `num_faces` 缺少驗證 |
| 5 | Coder 修正程式碼加入 ValueError 驗證 |
| 6 | Tester 配合更新測試，增加到 20 個 |
| 7 | Reviewer 第二輪 review，LGTM 通過 |

## Agent Teams 功能評估

### 優點
- **任務依賴管理有效** — blockedBy 機制確保了正確的執行順序
- **跨角色溝通成功** — reviewer 發現問題後，coder 和 tester 都能收到並回應
- **迭代改進流程順暢** — review → 修改 → 重新測試 → 再 review 的循環運作良好
- **並行意識** — 三個 agent 各司其職，不互相干擾

### 需注意的地方
- **需要 team lead 介入** — tester 沒有自動偵測到 coder 完成，需要手動推一下
- **idle 通知較多** — 等待期間會收到大量 idle notification，資訊噪音偏高
- **關閉不夠即時** — 發送 shutdown 後，成員還會繼續發送一些閒聊訊息才關閉
- **溝通有冗餘** — 成員之間會重複傳遞已知資訊（例如多人重複告知 reviewer 可以開始）

## 總結

Agent Teams 功能**基本可用**，適合需要多角色協作的任務。核心的任務管理、訊息傳遞、依賴控制都能正常運作。但目前 team lead 還是需要適時介入協調，不能完全放手讓團隊自主運行。對於這種小型任務來說，用 Agent Teams 的 overhead 偏高，更適合用在真正需要並行處理的大型複雜任務上。
