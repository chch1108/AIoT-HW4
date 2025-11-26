# AIoT HW4 – 多人格兩階段思考回應系統

本專案依照 HW4 規格打造一個遊戲式對話體驗，核心特色如下：

- 五種人格模組（傲嬌式、職場黑話、魯迅憤青、貓咪主子、佛系斯多葛）
- 兩階段 Chain-of-Thought：Stage1 內心戲 + Stage2 對外回覆
- 「偷看內心」UI：預設遮罩 Stage1，按下按鈕才顯示
- RPG 風格好感度系統：回合上限、目標值、Good/Bad Ending
- Streamlit 前端：人格切換、紀錄顯示、結局彈窗

## 專案結構

```
.
├── aiot_hw4/
│   ├── __init__.py
│   ├── engines.py        # 兩階段推理與 RPG 引擎
│   ├── orchestrator.py   # 流程控制與狀態管理
│   └── personas.py       # 人格模組與加減分邏輯
├── app.py                # Streamlit 介面
├── project.md            # 規格文件
├── README.md             # 本檔
└── requirements.txt      # 相依套件
```

## 執行方式

```bash
pip install -r requirements.txt
streamlit run app.py
```

瀏覽器開啟後即可：

1. 從下拉選擇人格
2. 輸入訊息並送出
3. 觀看 Stage2 回應並視需要「偷看內心」
4. 觀察回合與好感度，觸發每個人格的 Good/Bad Ending

## 啟用 LLM 模式

預設使用手寫模板，也可接上 Google Gemini 讓人格回覆更豐富：

1. 取得 Google Generative AI 金鑰，於 Streamlit secrets（或環境變數）設定 `GENAI_API_KEY` 或 `GOOGLE_API_KEY`
2. （可選）設定 `GENAI_MODEL_NAME` 指定模型，若未設定會依序嘗試 `gemini-2.0-flash`、`gemini-1.5-flash-latest`、`gemini-1.5-flash`
3. 重新部署或執行，介面會顯示「LLM 模式啟用」提示

若金鑰缺失或 API 呼叫失敗，系統會自動退回模板模式，確保遊戲流程不中斷。
