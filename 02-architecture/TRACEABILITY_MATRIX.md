# TRACEABILITY_MATRIX.md - 需求追蹤矩陣

**日期**: 2026-03-27  
**Phase**: 2 - 架構設計  
**用途**: 內部需求追蹤（區別於 SPEC_TRACKING.md 對照外部 PDF）

---

## 追蹤說明

本矩陣追蹤 **內部需求** 從定義到實作到測試的完整生命週期。

---

## 需求 → 實作追蹤

| 需求 ID | 需求名稱 | 對應模組 | 對應類別/方法 | 測試案例 |
|---------|----------|----------|---------------|----------|
| REQ-001 | 文字輸入 | TextProcessor | parse_input() | TC-001 |
| REQ-002 | 語音合成 | AsyncSynthesizer | synthesize() | TC-002 |
| REQ-003 | 文本分段 | TextProcessor | split_text() | TC-003 |
| REQ-004 | 參數調整 | PresentationTTS | set_params() | TC-004 |
| REQ-005 | 音色選擇 | PresentationTTS | set_voice() | TC-005 |
| REQ-006 | 錯誤處理 L1 | ErrorHandler | classify_l1() | TC-006 |
| REQ-007 | 錯誤處理 L2 | ErrorHandler | classify_l2() | TC-007 |
| REQ-008 | 錯誤處理 L3 | ErrorHandler | classify_l3() | TC-008 |
| REQ-009 | 錯誤處理 L4 | ErrorHandler | classify_l4() | TC-009 |
| REQ-010 | 非同步執行 | AsyncSynthesizer | async_synthesize() | TC-010 |
| REQ-011 | MP3 輸出 | OutputManager | encode_mp3() | TC-011 |

---

## 需求 → 測試追蹤

| 需求 ID | 單元測試 | 整合測試 | E2E 測試 | 覆蓋狀態 |
|---------|-----------|-----------|----------|----------|
| REQ-001 | ✅ | ✅ | - | 完整 |
| REQ-002 | ✅ | ✅ | ✅ | 完整 |
| REQ-003 | ✅ | ✅ | - | 完整 |
| REQ-004 | ✅ | - | - | 完整 |
| REQ-005 | ✅ | - | - | 完整 |
| REQ-006 | ✅ | ✅ | - | 完整 |
| REQ-007 | ✅ | ✅ | - | 完整 |
| REQ-008 | ✅ | ✅ | - | 完整 |
| REQ-009 | ✅ | ✅ | ✅ | 完整 |
| REQ-010 | ✅ | ✅ | ✅ | 完整 |
| REQ-011 | ✅ | - | - | 完整 |

---

## 雙文件對照

| 文件 | 用途 | 對照對象 |
|------|------|----------|
| **SPEC_TRACKING.md** | 外部規格對照 | PDF 規格書 |
| **TRACEABILITY_MATRIX.md** | 內部需求追蹤 | 使用者需求清單 |

---

## 覆蓋率統計

| 指標 | 數值 |
|------|------|
| 總需求數 | 11 |
| 有測試覆蓋 | 11 |
| 覆蓋率 | **100%** |

---

## 備註

- TRACEABILITY_MATRIX 與 SPEC_TRACKING 互補使用
- 前者追蹤內部需求，後者對照外部 PDF 規格

---

*TRACEABILITY_MATRIX.md 對應 SKILL.md - Phase 2 Templates*
*最後更新: 2026-03-27*