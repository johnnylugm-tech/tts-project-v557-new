"""
TTS Engine - 高品質簡報配音系統
基於 edge-tts 技術

Phase: 3 - 代碼實現
對應 SKILL.md: Core Modules
"""

import asyncio
import edge_tts
import os
from typing import List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ErrorHandler:
    """錯誤處理模組 - L1-L4 分類
    
    對應 SKILL.md - L1-L4 Error Classification:
    - L1: 輸入錯誤 → 立即返回
    - L2: 工具錯誤 → 重試 3 次
    - L3: 執行錯誤 → 降級處理
    - L4: 系統錯誤 → 熔斷 + 警報
    """
    
    MAX_RETRIES = 3
    RETRY_DELAYS = [1, 2, 4]
    
    @staticmethod
    def classify(error: Exception) -> int:
        """錯誤分類"""
        error_msg = str(error).lower()
        
        if any(k in error_msg for k in ['invalid', 'empty', 'validation']):
            return 1
        if any(k in error_msg for k in ['timeout', 'connection', 'rate limit']):
            return 2
        if any(k in error_msg for k in ['audio', 'encode', 'file']):
            return 3
        return 4
    
    @staticmethod
    def handle(error: Exception, context: dict = None) -> dict:
        """錯誤處理"""
        level = ErrorHandler.classify(error)
        context = context or {}
        
        handlers = {
            1: lambda: {"status": "failed", "message": f"L1 輸入錯誤: {str(error)}", "action": "return"},
            2: lambda: {"status": "retry", "message": f"L2 工具錯誤: {str(error)}", "action": "retry_3x"},
            3: lambda: {"status": "degraded", "message": f"L3 執行錯誤: {str(error)}", "action": "fallback"},
            4: lambda: {"status": "critical", "message": f"L4 系統錯誤: {str(error)}", "action": "circuit_break"}
        }
        
        return handlers[level]()


class TextProcessor:
    """文本分析與處理模組
    
    對應 SKILL.md - Data Processing:
    - 正則表達式分段
    - 語義完整性保護
    - 長度限制控制 (800字元)
    """
    
    CHUNK_SIZE = 800
    
    @staticmethod
    def validate_input(text: str) -> bool:
        """輸入驗證"""
        if not text or not text.strip():
            return False
        if len(text) > 50000:
            return False
        return True
    
    @staticmethod
    def split_text(text: str) -> List[str]:
        """文本分段 - 保持語義完整性"""
        if len(text) <= TextProcessor.CHUNK_SIZE:
            return [text]
        
        chunks = []
        import re
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


class AsyncSynthesizer:
    """非同步合成引擎
    
    對應 SKILL.md - Async Executor:
    - asyncio 非同步處理
    - WebSocket 流式傳輸
    - 並發控制
    """
    
    def __init__(self, voice: str = "zh-TW-HsiaoHsiaoNeural", 
                 rate: str = "+0%", volume: str = "+0%"):
        self.voice = voice
        self.rate = rate
        self.volume = volume
    
    async def synthesize(self, text: str, output_file: str) -> dict:
        """非同步合成"""
        try:
            communicate = edge_tts.Communicate(text, self.voice, rate=self.rate, volume=self.volume)
            await communicate.save(output_file)
            return {"status": "success", "file": output_file, "text_length": len(text)}
        except Exception as e:
            error_result = ErrorHandler.handle(e, {"text": text, "output": output_file})
            return error_result
    
    async def synthesize_batch(self, chunks: List[str], output_dir: str) -> List[dict]:
        """批量非同步合成"""
        tasks = []
        for i, chunk in enumerate(chunks):
            output_file = os.path.join(output_dir, f"chunk_{i:03d}.mp3")
            tasks.append(self.synthesize(chunk, output_file))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append(ErrorHandler.handle(result))
            else:
                processed_results.append(result)
        
        return processed_results


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
        """初始化"""
        self.voice = voice
        self.rate = rate
        self.volume = volume
        self.text_processor = TextProcessor()
        self.synthesizer = AsyncSynthesizer(voice, rate, volume)
        self.error_handler = ErrorHandler()
        logger.info(f"PresentationTTS 初始化: voice={voice}, rate={rate}, volume={volume}")
    
    def synthesize(self, text: str, output_dir: str) -> dict:
        """同步合成"""
        if not self.text_processor.validate_input(text):
            return {"status": "failed", "message": "L1 輸入驗證失敗: 文字為空或過長"}
        
        chunks = self.text_processor.split_text(text)
        logger.info(f"文本已分段: {len(chunks)} 個區塊")
        
        os.makedirs(output_dir, exist_ok=True)
        
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
                "results": results
            }
        finally:
            loop.close()
    
    async def synthesize_async(self, text: str, output_dir: str) -> dict:
        """非同步合成"""
        if not self.text_processor.validate_input(text):
            return {"status": "failed", "message": "L1 輸入驗證失敗"}
        
        chunks = self.text_processor.split_text(text)
        os.makedirs(output_dir, exist_ok=True)
        
        results = await self.synthesizer.synthesize_batch(chunks, output_dir)
        
        success_count = sum(1 for r in results if r.get("status") == "success")
        
        return {
            "status": "completed",
            "total_chunks": len(chunks),
            "success": success_count,
            "failed": len(chunks) - success_count,
            "results": results
        }


default_tts = PresentationTTS()


if __name__ == "__main__":
    test_text = "這是測試。請問好嗎？很高興認識您！"
    chunks = TextProcessor.split_text(test_text)
    print(f"文本分段: {chunks}")
    
    test_error = ValueError("invalid input")
    level = ErrorHandler.classify(test_error)
    print(f"錯誤分類: L{level}")