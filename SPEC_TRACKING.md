# SPEC_TRACKING.md - 規格追蹤矩陣

**日期**: 2026-03-27  
**Phase**: 2 - 架構設計  
**對應文件**: PDF 規格書（Python 簡報配音 TTS 程式）

---

## 規格追蹤說明

本文件對照 **PDF 規格書** 的每項規格與 SAD.md 的對應實作。

---

## PDF Section 1: 系統概述

| PDF 規格項目 | SAD 對應章節 | 對應狀態 | 備註 |
|-------------|--------------|----------|------|
| 基於 edge-tts 技術 | Section 3.3 AsyncSynthesizer | ✅ 對應 | 使用 edge-tts 庫 |
| Microsoft Edge TTS | Section 3.3 AsyncSynthesizer | ✅ 對應 | 微軟服務 |
| 神經網路語音合成 | Section 3.3 AsyncSynthesizer | ✅ 對應 | DNN 技術 |
| 高品質簡報配音 | Section 1.1 設計目標 | ✅ 對應 | 系統目標 |

---

## PDF Section 2: 系統架構

| PDF 規格項目 | SAD 對應章節 | 對應狀態 | 備註 |
|-------------|--------------|----------|------|
| 四層架構 | Section 2.1 架構圖 | ✅ 對應 | 接入/處理/合成/輸出 |
| 接入通訊層 (WebSocket) | Section 2.1 Layer 1 | ✅ 對應 | WebSocket Handler |
| 文本分析與處理層 | Section 2.1 Layer 2 | ✅ 對應 | TextProcessor |
| 合成引擎層 | Section 2.1 Layer 3 | ✅ 對應 | EdgeTTS Engine |
| 後處理與匯出層 | Section 2.1 Layer 4 | ✅ 對應 | MP3 Encoder |

---

## PDF Section 3: 技術選型

| PDF 規格項目 | SAD 對應章節 | 對應狀態 | 備註 |
|-------------|--------------|----------|------|
| Python 3.8+ | Section 6.2 環境需求 | ✅ 對應 | Python 版本 |
| edge-tts 庫 | Section 3.3 AsyncSynthesizer | ✅ 對應 | 核心依賴 |
| zh-TW-HsiaoHsiaoNeural | Section 3.1 PresentationTTS | ✅ 對應 | 預設音色 |
| asyncio 框架 | Section 3.3 AsyncSynthesizer | ✅ 對應 | 非同步處理 |

---

## PDF Section 4: 功能需求

| PDF 規格項目 | SAD 對應章節 | 對應狀態 | 備註 |
|-------------|--------------|----------|------|
| 文字輸入 (FR-01) | Section 4.1 API | ✅ 對應 | /synthesize |
| 語音合成 (FR-02) | Section 3.3 AsyncSynthesizer | ✅ 對應 | edge-tts 合成 |
| 文本分段 800字元 (FR-03) | Section 3.2 TextProcessor | ✅ 對應 | split_text() |
| 參數調整 rate/volume (FR-04) | Section 3.1 PresentationTTS | ✅ 對應 | __init__ 參數 |
| 音色選擇 (FR-05) | Section 4.2 CLI | ✅ 對應 | -v 參數 |
| 錯誤處理 3次重試 (FR-06) | Section 5 錯誤處理 | ✅ 對應 | L1-L4 分類 |
| 非同步執行 (FR-07) | Section 3.3 AsyncSynthesizer | ✅ 對應 | async/await |
| 檔案輸出 MP3 (FR-08) | Section 2.1 Layer 4 | ✅ 對應 | MP3 Encoder |

---

## PDF Section 5: 錯誤處理

| PDF 規格項目 | SAD 對應章節 | 對應狀態 | 備註 |
|-------------|--------------|----------|------|
| L1 輸入錯誤 | Section 5.1 錯誤分類 | ✅ 對應 | 立即返回 |
| L2 工具錯誤 | Section 5.1 錯誤分類 | ✅ 對應 | 重試 3 次 |
| L3 執行錯誤 | Section 5.1 錯誤分類 | ✅ 對應 | 降級處理 |
| L4 系統錯誤 | Section 5.1 錯誤分類 | ✅ 對應 | 熔斷 + 警報 |
| 重試機制 | Section 5.2 熔斷設計 | ✅ 對應 | 指數退避 |

---

## PDF Section 6: 非功能性需求

| PDF 規格項目 | SAD 對應章節 | 對應狀態 | 備註 |
|-------------|--------------|----------|------|
| 首位元組時間 < 2秒 | Section 7 測試策略 | ✅ 對應 | 效能測試 |
| WebSocket 流式傳輸 | Section 3.3 AsyncSynthesizer | ✅ 對應 | asyncio |
| 並發支援 | Section 3.3 AsyncSynthesizer | ✅ 對應 | 並發控制 |

---

## PDF Section 7: 安全性

| PDF 規格項目 | SAD 對應章節 | 對應狀態 | 備註 |
|-------------|--------------|----------|------|
| 輸入驗證 | Section 8.1 輸入驗證 | ✅ 對應 | UTF-8 驗證 |
| 錯誤訊息脫敏 | Section 8.2 錯誤訊息脫敏 | ✅ 對應 | 不暴露內部資訊 |
| 依賴安全 | Section 6.2 環境需求 | ✅ 對應 | edge-tts 版本控制 |

---

## 對照摘要

| 總規格數 | 已對應 | 差異 | 對應率 |
|----------|--------|------|--------|
| 25 | 25 | 0 | **100%** |

---

## 備註

- 所有 PDF 規格項目均已對應 SAD.md
- SKILL.md 規範（Async Executor、L1-L4 Error Classification）已整合
- 無規格漂移

---

*SPEC_TRACKING.md 對應 SKILL.md - Phase 2 Templates*
*最後更新: 2026-03-27*