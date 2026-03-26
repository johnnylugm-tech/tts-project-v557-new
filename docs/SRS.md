# Software Requirements Specification (SRS)

## 基於 edge-tts 之高品質簡報配音系統

**版本**: 1.0.0  
**日期**: 2026-03-27  
**狀態**: Draft  
**對應規格**: PDF 規格書（Python 簡報配音 TTS 程式）

---

## 1. 系統概述 (System Overview)

### 1.1 專案目標

構建一個基於 Microsoft Edge TTS 技術的高品質簡報配音系統，專為台灣市場設計，提供具有道地台灣國語腔調（zh-TW-HsiaoHsiaoNeural 音色）的語音合成服務。

### 1.2 系統範圍

| 範圍 | 說明 |
|------|------|
| **核心功能** | 文字轉語音（TTS）合成 |
| **目標用戶** | 簡報創作者、內容創作者、教育工作者 |
| **應用場景** | 專業簡報配音、有聲書、自動化內容產製 |

### 1.3 技術選型

| 項目 | 選擇 | 依據 |
|------|------|------|
| **語音引擎** | Microsoft Edge TTS (edge-tts) | PDF 規格書 Section 1 |
| **預設音色** | zh-TW-HsiaoHsiaoNeural | PDF 規格書 Section 2 |
| **Python 版本** | 3.8+ | PDF 規格書 Section 3 |
| **核心依賴** | edge-tts | PDF 規格書 Section 3 |

---

## 2. 功能需求 (Functional Requirements)

### 2.1 核心功能

| ID | 功能名稱 | 描述 | 優先級 |
|----|----------|------|--------|
| FR-01 | 文字輸入 | 接收用戶提供的文字輸入（中文為主） | P0 |
| FR-02 | 語音合成 | 將文字轉換為語音音訊 | P0 |
| FR-03 | 文本分段 | 將長文本智慧分割（800字元限制） | P0 |
| FR-04 | 參數調整 | 支援語速（rate）、音量（volume）調整 | P1 |
| FR-05 | 音色選擇 | 支援選擇不同音色 | P1 |
| FR-06 | 錯誤處理 | 支援重試機制（3次）與錯誤分類 | P0 |
| FR-07 | 非同步執行 | 支援非同步 API 調用 | P0 |
| FR-08 | 檔案輸出 | 輸出 MP3 音訊檔案 | P0 |
| FR-09 | 安全性 | 輸入驗證與錯誤訊息脫敏 | P1 |
| FR-10 | 可維護性 | 清晰架構與完整註解 | P1 |

### 2.2 詳細功能說明

#### FR-01: 文字輸入
- **輸入格式**: UTF-8 編碼的文字
- **支援語言**: 中文（繁体）、英文
- **長度限制**: 建議單次輸入不超過 20,000 字元

#### FR-02: 語音合成
- **技術**: Microsoft Edge TTS 神經網路語音合成
- **音色**: zh-TW-HsiaoHsiaoNeural（預設）
- **輸出格式**: MP3

#### FR-03: 文本分段
- **分段策略**: 根據中文句號（。）、問號（？）、感嘆號（！）及換行符進行智能分割
- **分段上限**: 800 字元（可配置）
- **目的**: 維持語義完整性，避免語調中斷

#### FR-04: 參數調整
| 參數 | 格式 | 範圍 | 預設值 |
|------|------|------|--------|
| rate | "+X%" 或 "-X%" | -50% ~ +50% | +0% |
| volume | "+X%" 或 "-X%" | -50% ~ +50% | +0% |

#### FR-05: 音色選擇
- 預設音色：zh-TW-HsiaoHsiaoNeural
- 可擴展支援其他中文音色

#### FR-06: 錯誤處理
| 錯誤等級 | 處理方式 |
|----------|----------|
| L1 (輸入錯誤) | 立即返回錯誤訊息 |
| L2 (工具錯誤) | 重試 3 次 |
| L3 (執行錯誤) | 降級處理 |
| L4 (系統錯誤) | 熔斷 + 警報 |

#### FR-07: 非同步執行
- 使用 asyncio 框架
- 支援流式輸出

#### FR-08: 檔案輸出
- 輸出目錄可配置
- 檔案命名格式：`chunk_{index:03d}.mp3`

---

## 3. 非功能性需求 (Non-Functional Requirements)

### 3.1 效能需求 (Performance Requirements)

| ID | 指標 | 目標值 | 說明 |
|----|------|--------|------|
| NFR-01 | 首位元組時間 (TTFB) | < 2 秒 | 網路正常情況下 |
| NFR-02 | 合成速度 | 即時反應 | WebSocket 流式傳輸 |
| NFR-03 | 並發支援 | 支援多任務 | 透過 AsyncExecutor |
| NFR-04 | 錯誤恢復時間 | < 5 秒 | 網路閃斷恢復 |

### 3.2 品質需求 (Quality Requirements)

| ID | 指標 | 目標值 | 說明 |
|----|------|--------|------|
| NFR-05 | 正確性 | 100% | 語音合成正確 |
| NFR-06 | 安全性 | 100% | 無安全漏洞 |
| NFR-07 | 可維護性 | > 70% | 程式碼品質 |
| NFR-08 | 測試覆蓋率 | > 80% | 單元測試覆蓋 |

### 3.3 可靠性需求 (Reliability Requirements)

| ID | 指標 | 目標值 | 說明 |
|----|------|--------|------|
| NFR-09 | 可用性 | 99% | 網路穩定時 |
| NFR-10 | 錯誤恢復 | 自動重試 | 3 次重試機制 |
| NFR-11 | 日誌記錄 | 完整 | 使用 logging 模組 |
| NFR-12 | 監控能力 | 完整 | 健康檢查接口 |

### 3.4 安全需求 (Security Requirements)

根據 Constitution 原則，必須包含以下 4 個安全面向：

| ID | 安全項目 | 對應 Constitution | 說明 |
|----|----------|-------------------|------|
| SEC-01 | Authentication 身份驗證 | ✅ 包含 | 用戶身份驗證机制 |
| SEC-02 | Authorization 授權控制 | ✅ 包含 | 權限管理與訪問控制 |
| SEC-03 | Encryption 加密傳輸 | ✅ 包含 | SSL/TLS 加密傳輸 |
| SEC-04 | Data Protection 資料保護 | ✅ 包含 | 敏感資訊保護 |

---

## 4. 系統架構 (System Architecture)

### 4.1 四層架構

根據 PDF 規格書 Section 2，系統採用四層架構：

```
┌─────────────────────────────────────┐
│     接入通訊層 (WebSocket)          │
├─────────────────────────────────────┤
│   文本分析與處理層 (分段)           │
├─────────────────────────────────────┤
│     合成引擎層 (edge-tts)           │
├─────────────────────────────────────┤
│   後處理與匯出層 (MP3)              │
└─────────────────────────────────────┘
```

### 4.2 核心類別設計

| 類別 | 職責 | 對應模組 |
|------|------|----------|
| `PresentationTTS` | TTS 引擎核心 | Core Modules |
| `_preprocess_text()` | 文本分段 | Data Processing |
| `_synthesize_chunk()` | 非同步合成 | Async Execution |
| 錯誤處理 | L1-L4 分類 | Error Handling |

---

## 5. 介面規格 (Interface Specifications)

### 5.1 API 設計

```python
class PresentationTTS:
    def __init__(
        self,
        voice: str = "zh-TW-HsiaoHsiaoNeural",
        rate: str = "+0%",
        volume: str = "+0%"
    ):
        """
        初始化 TTS 引擎
        對應 SKILL.md - Core Modules
        """
        pass

    def _preprocess_text(self, text: str) -> List[str]:
        """
        文本分段
        對應 SKILL.md - Data Processing
        """
        pass

    async def _synthesize_chunk(
        self,
        chunk: str,
        index: int,
        output_dir: str
    ) -> Optional[str]:
        """
        非同步合成
        對應 SKILL.md - Async Executor
        """
        pass
```

### 5.2 錯誤碼

| 錯誤碼 | 說明 |
|--------|------|
| E001 | 文字輸入為空 |
| E002 | 文字超出長度限制 |
| E003 | 網路連接失敗 |
| E004 | 合成失敗 |
| E005 | 檔案寫入失敗 |

---

## 6. 數據需求 (Data Requirements)

### 6.1 輸入數據

| 欄位 | 類型 | 說明 |
|------|------|------|
| text | string | 要合成的文字 |
| voice | string | 選擇的音色 |
| rate | string | 語速調整 |
| volume | string | 音量調整 |

### 6.2 輸出數據

| 欄位 | 類型 | 說明 |
|------|------|------|
| audio_files | list[string] | 生成的 MP3 檔案路徑 |
| duration | float | 總時長（秒） |
| status | string | 執行狀態 |

---

## 7. 驗收標準 (Acceptance Criteria)

### 7.1 功能驗收

| ID | 驗收項目 | 測試方法 |
|----|----------|----------|
| AC-01 | 可成功合成中文文字為語音 | 輸入文字，檢查 MP3 輸出 |
| AC-02 | 文本正確分段（800字元） | 輸入 >800 字，檢查分段數量 |
| AC-03 | 參數調整生效 | 調整 rate/volume，檢查輸出差異 |
| AC-04 | 錯誤處理正常 | 模擬網路錯誤，檢查重試行為 |

### 7.2 品質驗收

| ID | 驗收項目 | 目標值 |
|----|----------|--------|
| QC-01 | 單元測試覆蓋率 | > 80% |
| QC-02 | Quality Gate 通過率 | > 80% |
| QC-03 | Constitution 得分 | > 60/100 |

---

## 8. 風險與假設 (Risks and Assumptions)

### 8.1 風險

| ID | 風險描述 | 影響 | 緩解措施 |
|----|----------|------|----------|
| R1 | 網路不穩定導致合成失敗 | 高 | 重試機制 + 錯誤分類 |
| R2 | edge-tts API 變更 | 中 | 版本控制 |
| R3 | 長文本記憶體問題 | 中 | 分段處理 |

### 8.2 假設

| ID | 假設說明 |
|----|----------|
| A1 | 用戶有穩定的網路連接 |
| A2 | Python 3.8+ 環境已安裝 |
| A3 | edge-tts 服務可正常存取 |

---

## 9. 附錄 (Appendix)

### 9.1 參考文獻

- PDF 規格書：Python 簡報配音 TTS 程式
- Methodology-v2 SKILL.md (v5.56)
- edge-tts 官方文檔

### 9.2 術語表

| 術語 | 說明 |
|------|------|
| TTS | Text-to-Speech，文字轉語音 |
| edge-tts | 微軟 Edge 瀏覽器內建 TTS 技術 |
| WebSocket | 網路通訊協議，支援流式傳輸 |
| chunk | 文本分段後的區塊 |

---

*本文件對應 PDF 規格書 + Methodology-v2 Phase 1 規範*
*SRS 版本: 1.0.0*
*最後更新: 2026-03-27*