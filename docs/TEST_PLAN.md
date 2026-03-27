# Test Plan - TTS Project

**日期**: 2026-03-27  
**Phase**: 4 - 測試  
**專案**: 高品質簡報配音系統 (edge-tts)

---

## 1. 測試目標

驗證 TTS 系統功能正確性、錯誤處理能力、文本處理邏輯。

---

## 2. 測試範圍

| 類型 | 範圍 |
|------|------|
| 單元測試 | TextProcessor, ErrorHandler, PresentationTTS, AsyncSynthesizer |
| 整合測試 | CLI 介面 |
| E2E 測試 | 完整合成流程 |

---

## 3. 測試策略

| 類型 | 方法 | 工具 | 覆蓋率目標 |
|------|------|------|-----------|
| 單元測試 | White-box | pytest | >= 80% |
| 整合測試 | Black-box | 手動測試 | - |
| E2E測試 | User story | edge-tts | - |

### 測試金字塔

```
        ┌─────────────┐
        │   E2E      │  ← 少量
        │  Integration│  ← 適量
        │    Unit    │  ← 大量 (80%)
        └─────────────┘
```

### 關鍵路徑

1. **核心路徑**: TextProcessor → AsyncSynthesizer → Output
2. **錯誤處理路徑**: ErrorHandler L1-L4 分類
3. **CLI 路徑**: CLI → TTS Engine → Output
4. **輸入驗證路徑**: validate_input → split_text → synthesize
5. **非同步處理路徑**: synthesize_async → synthesize_batch → gather results
6. **錯誤恢復路徑**: retry_3x → fallback → circuit_break

### Critical Path 覆蓋

| 路徑 | 測試案例 | 覆蓋 |
|------|----------|------|
| 核心路徑 | TC-001~TC-005, TC-012 | ✅ |
| 錯誤處理路徑 | TC-006~TC-009 | ✅ |
| CLI 路徑 | TC-010~TC-011 | ✅ |
| 輸入驗證路徑 | TC-001~TC-003 | ✅ |
| 非同步處理路徑 | TC-012 | ✅ |
| 錯誤恢復路徑 | TC-006~TC-009 | ✅ |

### Regression Tests

| ID | 測試名稱 | 功能 |
|----|----------|------|
| RT-01 | test_validate_input_valid | 正常輸入驗證 |
| RT-02 | test_validate_input_empty | 空輸入處理 |
| RT-03 | test_validate_input_none | None 輸入處理 |
| RT-04 | test_split_text_short | 短文字分段 |
| RT-05 | test_split_text_long | 長文字分段 |
| RT-06 | test_error_classify_l1 | L1 分類 |
| RT-07 | test_error_classify_l2 | L2 分類 |
| RT-08 | test_error_classify_l3 | L3 分類 |
| RT-09 | test_error_classify_l4 | L4 分類 |

### Smoke Tests

| ID | 測試名稱 | 功能 |
|----|----------|------|
| ST-01 | test_init_default | 預設初始化 |
| ST-02 | test_init_custom | 自訂初始化 |
| ST-03 | test_synthesize_empty | 空文字合成 |

---

## 4. 測試環境

- Python 3.8+
- edge-tts 套件
- 網路連接（存取 Microsoft Edge TTS）

---

## 5. 測試案例清單

| ID | 案例名稱 | 優先級 | 對應需求 |
|----|----------|--------|----------|
| TC-001 | 有效輸入驗證 | P0 | FR-01 |
| TC-002 | 空輸入驗證 | P0 | FR-01 |
| TC-003 | 過長輸入驗證 | P0 | FR-01 |
| TC-004 | 短文字分段 | P0 | FR-03 |
| TC-005 | 長文字分段 | P0 | FR-03 |
| TC-006 | L1 錯誤分類 | P0 | FR-06 |
| TC-007 | L2 錯誤分類 | P0 | FR-06 |
| TC-008 | L3 錯誤分類 | P0 | FR-06 |
| TC-009 | L4 錯誤分類 | P0 | FR-06 |
| TC-010 | 預設初始化 | P1 | FR-04 |
| TC-011 | 自訂參數初始化 | P1 | FR-04 |
| TC-012 | 空文字合成 | P1 | FR-02 |

---

## 6. 風險與緩解

| 風險 | 影響 | 緩解措施 |
|------|------|----------|
| edge-tts 服務中斷 | 高 | 錯誤處理 L1-L4 |
| 網路不穩定 | 中 | 重試機制 3 次 |
| 測試環境限制 | 中 | 單元測試隔離 edge-tts |

---

*Test Plan - Phase 4*
*最後更新: 2026-03-27*