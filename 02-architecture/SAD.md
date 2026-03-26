# Software Architecture Description (SAD)

## 基於 edge-tts 之高品質簡報配音系統

**版本**: 1.0.0  
**日期**: 2026-03-27  
**Phase**: 2 - 架構設計  
**對應 SRS**: Phase 1 SRS.md

---

## 1. 系統概述 (System Overview)

### 1.1 設計目標

本系統採用**四層架構**設計，實現高品質簡報配音功能。根據 PDF 規格書 Section 2 和 SKILL.md 的 Core Modules 規範，確保：
- 模組職責清晰
- 錯誤處理分層
- 非同步高效執行

### 1.2 架構原則

| 原則 | 說明 |
|------|------|
| **分層設計** | 四層架構，層層解耦 |
| **非同步優先** | 使用 asyncio 提升效能 |
| **錯誤分類** | L1-L4 錯誤分層處理 |
| **可擴展性** | 支援多音色、多參數 |

---

## 2. 系統架構 (System Architecture)

### 2.1 四層架構圖

```
┌─────────────────────────────────────────────────────────────────┐
│                    接入通訊層 (Layer 1)                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ WebSocket   │  │   API       │  │   CLI       │             │
│  │   Handler   │  │   Gateway   │  │   Interface │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
├─────────────────────────────────────────────────────────────────┤
│                  文本分析與處理層 (Layer 2)                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  Text       │  │  Chunk     │  │  Validation │             │
│  │  Parser     │  │  Splitter  │  │   Module    │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
├─────────────────────────────────────────────────────────────────┤
│                    合成引擎層 (Layer 3)                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Edge-TTS  │  │   Rate/    │  │   Voice     │             │
│  │   Engine    │  │   Volume    │  │   Config    │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
├─────────────────────────────────────────────────────────────────┤
│                  後處理與匯出層 (Layer 4)                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   MP3       │  │   Merge    │  │   Output   │             │
│  │   Encoder   │  │   Engine   │  │   Manager   │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 數據流

```
User Input → Layer 1 (API/CLI) → Layer 2 (Parse & Split) 
         → Layer 3 (TTS Engine) → Layer 4 (Encode & Output)
         → Audio Files (MP3)
```

---

## 3. 核心模組設計 (Core Modules)

### 3.1 PresentationTTS（核心類別）

**職責**: TTS 引擎主控制器  
**對應 SKILL.md**: Core Modules  
**位置**: `src/tts_engine.py`

```python
class PresentationTTS:
    """高品質簡報配音引擎
    
    對應 SKILL.md - Core Modules:
    - 初始化與配置管理
    - 文本處理協調
    - 語音合成調度
    - 錯誤處理協調
    """
    
    def __init__(self, voice, rate, volume):
        # 初始化配置
        pass
    
    def synthesize(self, text, output_dir):
        # 協調各層處理
        pass
```

### 3.2 TextProcessor（文本處理）

**職責**: 文本分析與分段  
**對應 SKILL.md**: Data Processing  
**位置**: `src/text_processor.py`

```python
class TextProcessor:
    """文本分析與處理模組
    
    對應 SKILL.md - Data Processing:
    - 正則表達式分段
    - 語義完整性保護
    - 長度限制控制 (800字元)
    """
    
    def split_text(self, text):
        # 根據句號、問號、感嘆號分段
        pass
```

### 3.3 AsyncSynthesizer（合成引擎）

**職責**: 非同步語音合成  
**對應 SKILL.md**: Async Executor  
**位置**: `src/synthesizer.py`

```python
class AsyncSynthesizer:
    """非同步合成引擎
    
    對應 SKILL.md - Async Executor:
    - asyncio 非同步處理
    - WebSocket 流式傳輸
    - 並發控制
    """
    
    async def synthesize(self, chunk):
        # 非同步合成
        pass
```

### 3.4 ErrorHandler（錯誤處理）

**職責**: 錯誤分類與處理  
**對應 SKILL.md**: Error Handling (L1-L4)  
**位置**: `src/error_handler.py`

```python
class ErrorHandler:
    """錯誤處理模組
    
    對應 SKILL.md - L1-L4 Error Classification:
    - L1: 輸入錯誤 → 立即返回
    - L2: 工具錯誤 → 重試 3 次
    - L3: 執行錯誤 → 降級處理
    - L4: 系統錯誤 → 熔斷 + 警報
    """
    
    def classify(self, error):
        # 錯誤分類
        pass
    
    def handle(self, error):
        # 錯誤處理
        pass
```

---

## 4. 介面設計 (Interface Design)

### 4.1 API 介面

| 方法 | 路徑 | 說明 |
|------|------|------|
| POST | `/synthesize` | 文字轉語音 |
| GET | `/voices` | 取得可用音色 |
| GET | `/status/{task_id}` | 查詢任務狀態 |

### 4.2 CLI 介面

```bash
# 基本用法
python -m tts_cli synthesize "Hello World" -o output.mp3

# 參數調整
python -m tts_cli synthesize "Hello" -v zh-TW-HsiaoHsiaoNeural -r "+10%"
```

---

## 5. 錯誤處理架構 (Error Handling)

### 5.1 錯誤分類

| 等級 | 錯誤類型 | 處理策略 |
|------|----------|----------|
| L1 | 輸入驗證失敗 | 立即返回錯誤訊息 |
| L2 | 網路瞬斷、API 限流 | 重試 3 次，指數退避 |
| L3 | 合成失敗、音效問題 | 降級處理，返回部分結果 |
| L4 | 系統當機、服務不可用 | 熔斷機制，發送警報 |

### 5.2 熔斷設計

```
請求 → 錯誤計數累加 → 閾值達到 → 熔斷觸發
                                    ↓
                              恢復檢查 (30秒)
                                    ↓
                           恢復成功 → 熔斷重置
```

---

## 6. 部署架構 (Deployment)

### 6.1 單機部署

```
┌─────────────────────────────────────────┐
│           Application Server            │
│  ┌───────────────────────────────────┐  │
│  │         Python Runtime            │  │
│  │  ┌─────────┐ ┌─────────┐         │  │
│  │  │  TTS    │ │  API    │         │  │
│  │  │ Engine  │ │ Server  │         │  │
│  │  └─────────┘ └─────────┘         │  │
│  └───────────────────────────────────┘  │
│                    ↓                     │
│           Microsoft Edge TTS (Cloud)   │
└─────────────────────────────────────────┘
```

### 6.2 環境需求

| 項目 | 需求 |
|------|------|
| Python | 3.8+ |
| 依賴 | edge-tts, aiohttp |
| 網路 | 可訪問 Microsoft Edge TTS |

---

## 7. 測試策略 (Testing Strategy)

### 7.1 測試金字塔

```
        ┌─────────────┐
        │   E2E      │  ← 少量
        │  Integration│  ← 適量
        │    Unit    │  ← 大量 (80%)
        └─────────────┘
```

### 7.2 測試範圍

| 類型 | 覆蓋範圍 |
|------|----------|
| 單元測試 | 核心類別每個方法 |
| 整合測試 | API 端點 |
| E2E 測試 | 完整合成流程 |

---

## 8. 安全性設計 (Security Design)

### 8.1 輸入驗證

- 字元編號驗證（UTF-8）
- 長度限制檢查
- 特殊字元過濾

### 8.2 錯誤訊息脫敏

- 不暴露內部路徑
- 不暴露 API 金鑰
- 使用通用錯誤碼

---

## 9. 安全設計 (Security Design)

### 9.1 設計原則

| 安全面向 | 設計內容 | 對應 Constitution |
|----------|----------|-------------------|
| **Authentication** | API 請求驗證機制 | ✅ |
| **Authorization** | 權限控制與訪問管理 | ✅ |
| **Encryption** | SSL/TLS 傳輸加密 | ✅ |
| **Data Protection** | 敏感資訊保護策略 | ✅ |

### 9.1.1 Authentication 設計

```python
class AuthManager:
    """認證管理模組
    
    對應 Constitution - Authentication:
    - API 金鑰驗證
    - Token -based 認證
    """
    def authenticate(self, request):
        # 驗證請求者身份
        pass
```

### 9.1.2 Authorization 設計

```python
class PermissionManager:
    """授權管理模組
    
    對應 Constitution - Authorization:
    - 角色權限映射
    - 資源訪問控制
    """
    def check_permission(self, user, resource):
        # 檢查權限
        pass
```

### 9.1.3 Encryption 設計

- HTTPS/TLS 傳輸加密
- 敏感配置加密存儲
- 日誌脫敏處理

### 9.1.4 Data Protection 設計

- 不記錄用戶敏感文字
- 臨時檔案自動清理
- 記憶體資料保護

---

*本文件對應 Methodology-v2 Phase 2 規範*
*SAD 版本: 1.0.0*
*最後更新: 2026-03-27*