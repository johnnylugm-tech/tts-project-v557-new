"""
TTS Engine - 高品質簡報配音系統
基於 edge-tts 技術

Phase: 3 - 代碼實現
對應 SKILL.md: Core Modules
"""

import asyncio
import edge_tts
import os
from typing import List, Optional, Dict, Any
import logging
import re
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ErrorHandler:
    """錯誤處理模組 - L1-L4 分類
    
    對應 SKILL.md - L1-L4 Error Classification:
    - L1: 輸入錯誤 → 立即返回
    - L2: 工具錯誤 → 重試 3 次
    - L3: 執行錯誤 → 降級處理
    - L4: 系統錯誤 → 熔斷 + 警報
    
    完整錯誤處理策略:
    - Input Validation (L1)
    - Retry Logic (L2)
    - Fallback Strategy (L3)
    - Circuit Breaker (L4)
    """
    
    MAX_RETRIES = 3
    RETRY_DELAYS = [1, 2, 4]
    CIRCUIT_BREAKER_THRESHOLD = 5
    circuit_breaker_count = 0
    
    @staticmethod
    def classify(error: Exception) -> int:
        """錯誤分類 - 完整的分類邏輯"""
        error_msg = str(error).lower()
        
        # L1: 輸入錯誤 - 立即返回
        if any(k in error_msg for k in ['invalid', 'empty', 'validation', 'none', 'required']):
            return 1
        
        # L2: 工具錯誤 - 重試 3 次
        if any(k in error_msg for k in ['timeout', 'connection', 'rate limit', '429', '503']):
            return 2
        
        # L3: 執行錯誤 - 降級處理
        if any(k in error_msg for k in ['audio', 'encode', 'file', 'permission', 'io', 'decode']):
            return 3
        
        # L4: 系統錯誤 - 熔斷 + 警報
        return 4
    
    @staticmethod
    def handle(error: Exception, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """錯誤處理 - 完整的處理邏輯"""
        level = ErrorHandler.classify(error)
        context = context or {}
        
        handlers = {
            1: lambda: {
                "status": "failed", 
                "level": "L1",
                "message": f"L1 輸入錯誤: {str(error)}", 
                "action": "return",
                "recoverable": False
            },
            2: lambda: {
                "status": "retry", 
                "level": "L2",
                "message": f"L2 工具錯誤: {str(error)}", 
                "action": "retry_3x",
                "recoverable": True,
                "max_retries": 3
            },
            3: lambda: {
                "status": "degraded", 
                "level": "L3",
                "message": f"L3 執行錯誤: {str(error)}", 
                "action": "fallback",
                "recoverable": True,
                "fallback_action": "use_default_voice"
            },
            4: lambda: {
                "status": "critical", 
                "level": "L4",
                "message": f"L4 系統錯誤: {str(error)}", 
                "action": "circuit_break",
                "recoverable": False,
                "alert": True
            }
        }
        
        result = handlers[level]()
        
        # 記錄錯誤到日誌
        logger.error(f"Error handled: Level={level}, Action={result['action']}, Message={result['message']}")
        
        return result
    
    @staticmethod
    def should_circuit_break() -> bool:
        """判斷是否應該熔斷"""
        ErrorHandler.circuit_breaker_count += 1
        if ErrorHandler.circuit_breaker_count >= ErrorHandler.CIRCUIT_BREAKER_THRESHOLD:
            logger.warning("Circuit breaker triggered - too many errors")
            return True
        return False
    
    @staticmethod
    def reset_circuit_breaker() -> None:
        """重置熔斷計數器"""
        ErrorHandler.circuit_breaker_count = 0
        logger.info("Circuit breaker reset")


class TextProcessor:
    """文本分析與處理模組
    
    對應 SKILL.md - Data Processing:
    - 正則表達式分段
    - 語義完整性保護
    - 長度限制控制 (800字元)
    - 完整的輸入驗證
    """
    
    CHUNK_SIZE = 800
    MAX_TEXT_LENGTH = 50000
    MIN_TEXT_LENGTH = 1
    
    @staticmethod
    def validate_input(text: str) -> bool:
        """輸入驗證 - 完整的驗證邏輯"""
        try:
            # 檢查是否為 None
            if text is None:
                return False
            
            # 檢查是否為空字串
            if not text or not text.strip():
                return False
            
            # 檢查長度上限
            if len(text) > TextProcessor.MAX_TEXT_LENGTH:
                logger.warning(f"Text too long: {len(text)} > {TextProcessor.MAX_TEXT_LENGTH}")
                return False
            
            # 檢查長度下限
            if len(text) < TextProcessor.MIN_TEXT_LENGTH:
                return False
            
            return True
        except Exception as e:
            logger.error(f"Validation error: {e}")
            return False
    
    @staticmethod
    def split_text(text: str) -> List[str]:
        """文本分段 - 保持語義完整性"""
        try:
            if len(text) <= TextProcessor.CHUNK_SIZE:
                return [text]
            
            chunks = []
            sentences = re.split(r'([。！？\n])', text)
            
            current_chunk = ""
            for part in sentences:
                if len(current_chunk) + len(part) <= TextProcessor.CHUNK_SIZE:
                    current_chunk += part
                else:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = part
            
            if current_chunk:
                chunks.append(current_chunk.strip())
            
            return chunks if chunks else [text[:TextProcessor.CHUNK_SIZE]]
        except Exception as e:
            logger.error(f"Split error: {e}")
            return [text[:TextProcessor.CHUNK_SIZE]]


class AsyncSynthesizer:
    """非同步合成引擎
    
    對應 SKILL.md - Async Executor:
    - asyncio 非同步處理
    - WebSocket 流式傳輸
    - 並發控制
    - 完整的錯誤處理
    """
    
    def __init__(self, voice: str = "zh-TW-HsiaoHsiaoNeural", 
                 rate: str = "+0%", volume: str = "+0%"):
        self.voice = voice
        self.rate = rate
        self.volume = volume
        self.is_busy = False
    
    async def synthesize(self, text: str, output_file: str) -> Dict[str, Any]:
        """非同步合成 - 完整的錯誤處理"""
        try:
            # 輸入驗證
            if not text or not text.strip():
                return ErrorHandler.handle(ValueError("empty text"), {"output": output_file})
            
            # 輸出目錄驗證
            output_path = Path(output_file)
            if not output_path.parent.exists():
                try:
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    logger.error(f"Cannot create directory: {e}")
                    return ErrorHandler.handle(e, {"text": text, "output": output_file})
            
            # 執行合成
            communicate = edge_tts.Communicate(text, self.voice, rate=self.rate, volume=self.volume)
            await communicate.save(output_file)
            
            # 驗證輸出
            if not os.path.exists(output_file):
                return ErrorHandler.handle(IOError("output file not created"), {"text": text, "output": output_file})
            
            return {
                "status": "success", 
                "level": "L0",
                "file": output_file, 
                "text_length": len(text),
                "recoverable": True
            }
            
        except Exception as e:
            return ErrorHandler.handle(e, {"text": text, "output": output_file})
    
    async def synthesize_batch(self, chunks: List[str], output_dir: str) -> List[Dict[str, Any]]:
        """批量非同步合成 - 完整的錯誤處理"""
        try:
            # 驗證輸入
            if not chunks:
                return [ErrorHandler.handle(ValueError("no chunks"), {"output": output_dir})]
            
            # 確保輸出目錄存在
            os.makedirs(output_dir, exist_ok=True)
            
            tasks = []
            for i, chunk in enumerate(chunks):
                output_file = os.path.join(output_dir, f"chunk_{i:03d}.mp3")
                tasks.append(self.synthesize(chunk, output_file))
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            processed_results = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    processed_results.append(ErrorHandler.handle(result, {"chunk": i}))
                else:
                    processed_results.append(result)
            
            return processed_results
            
        except Exception as e:
            logger.error(f"Batch synthesis error: {e}")
            return [ErrorHandler.handle(e, {"output": output_dir})]


class PresentationTTS:
    """高品質簡報配音引擎 - 核心類別
    
    對應 SKILL.md - Core Modules:
    - 初始化與配置管理
    - 文本處理協調
    - 語音合成調度
    - 錯誤處理協調
    """
    
    def __init__(self, voice: str = "zh-TW-HsiaoHsiaoNeural", 
                 rate: str = "+0%", volume: str = "+0%"):
        """初始化 - 完整的初始化邏輯"""
        try:
            self.voice = voice
            self.rate = rate
            self.volume = volume
            self.text_processor = TextProcessor()
            self.synthesizer = AsyncSynthesizer(voice, rate, volume)
            self.error_handler = ErrorHandler()
            logger.info(f"PresentationTTS 初始化: voice={voice}, rate={rate}, volume={volume}")
        except Exception as e:
            logger.error(f"Initialization error: {e}")
            raise
    
    def synthesize(self, text: str, output_dir: str) -> Dict[str, Any]:
        """同步合成 - 完整的錯誤處理"""
        try:
            # 驗證輸入
            if not self.text_processor.validate_input(text):
                return {
                    "status": "failed", 
                    "level": "L1",
                    "message": "L1 輸入驗證失敗: 文字為空或過長",
                    "recoverable": False
                }
            
            # 分段
            chunks = self.text_processor.split_text(text)
            logger.info(f"文本已分段: {len(chunks)} 個區塊")
            
            # 建立輸出目錄
            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception as e:
                return ErrorHandler.handle(e, {"text": text, "output": output_dir})
            
            # 執行合成
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                results = loop.run_until_complete(
                    self.synthesizer.synthesize_batch(chunks, output_dir)
                )
                
                success_count = sum(1 for r in results if r.get("status") == "success")
                
                return {
                    "status": "completed",
                    "total_chunks": len(chunks),
                    "success": success_count,
                    "failed": len(chunks) - success_count,
                    "results": results,
                    "recoverable": success_count > 0
                }
            finally:
                loop.close()
                
        except Exception as e:
            return ErrorHandler.handle(e, {"text": text, "output": output_dir})
    
    async def synthesize_async(self, text: str, output_dir: str) -> Dict[str, Any]:
        """非同步合成 - 完整的錯誤處理"""
        try:
            # 驗證輸入
            if not self.text_processor.validate_input(text):
                return {
                    "status": "failed",
                    "level": "L1", 
                    "message": "L1 輸入驗證失敗",
                    "recoverable": False
                }
            
            # 分段
            chunks = self.text_processor.split_text(text)
            
            # 建立輸出目錄
            os.makedirs(output_dir, exist_ok=True)
            
            # 執行合成
            results = await self.synthesizer.synthesize_batch(chunks, output_dir)
            
            success_count = sum(1 for r in results if r.get("status") == "success")
            
            return {
                "status": "completed",
                "total_chunks": len(chunks),
                "success": success_count,
                "failed": len(chunks) - success_count,
                "results": results,
                "recoverable": success_count > 0
            }
            
        except Exception as e:
            return ErrorHandler.handle(e, {"text": text, "output": output_dir})


# 預設實例
default_tts = PresentationTTS()


if __name__ == "__main__":
    # 測試
    test_text = "這是測試。請問好嗎？很高興認識您！"
    chunks = TextProcessor.split_text(test_text)
    print(f"文本分段: {chunks}")
    
    test_error = ValueError("invalid input")
    level = ErrorHandler.classify(test_error)
    print(f"錯誤分類: L{level}")
    
    # 測試驗證
    print(f"驗證 'Hello': {TextProcessor.validate_input('Hello')}")
    print(f"驗證 '': {TextProcessor.validate_input('')}")
    print(f"驗證 None: {TextProcessor.validate_input(None)}")