"""
Unit Tests - TTS Engine
Phase: 3 - 代碼實現
對應 SKILL.md: Testing Strategy

完整測試策略:
- 單元測試 (Unit Tests)
- 整合測試 (Integration Tests)
- 錯誤處理測試 (Error Handling Tests)
- Regression Tests
- Smoke Tests
"""

import pytest
import tempfile
import os
from pathlib import Path
from tts_engine import (
    PresentationTTS, 
    TextProcessor, 
    ErrorHandler, 
    AsyncSynthesizer
)


class TestTextProcessor:
    """TextProcessor 單元測試"""
    
    def test_validate_input_valid(self):
        """正常輸入"""
        assert TextProcessor.validate_input("Hello") == True
    
    def test_validate_input_empty(self):
        """空字串"""
        assert TextProcessor.validate_input("") == False
    
    def test_validate_input_whitespace(self):
        """空白"""
        assert TextProcessor.validate_input("   ") == False
    
    def test_validate_input_none(self):
        """None 輸入"""
        assert TextProcessor.validate_input(None) == False
    
    def test_validate_input_too_long(self):
        """過長輸入"""
        long_text = "測試" * 20000
        assert TextProcessor.validate_input(long_text) == False
    
    def test_split_text_short(self):
        """短文字不分段"""
        chunks = TextProcessor.split_text("Hello")
        assert len(chunks) == 1
    
    def test_split_text_long(self):
        """長文字分段"""
        chunks = TextProcessor.split_text("測試。" * 200)
        assert len(chunks) > 1
    
    def test_split_text_empty(self):
        """空文字"""
        chunks = TextProcessor.split_text("")
        assert len(chunks) >= 1


class TestErrorHandler:
    """ErrorHandler 錯誤處理測試 - L1-L4"""
    
    def test_classify_l1_invalid(self):
        """L1: 輸入錯誤 - invalid"""
        assert ErrorHandler.classify(ValueError("invalid input")) == 1
    
    def test_classify_l1_empty(self):
        """L1: 輸入錯誤 - empty"""
        assert ErrorHandler.classify(ValueError("empty text")) == 1
    
    def test_classify_l1_validation(self):
        """L1: 輸入錯誤 - validation"""
        assert ErrorHandler.classify(ValueError("validation failed")) == 1
    
    def test_classify_l2_timeout(self):
        """L2: 工具錯誤 - timeout"""
        assert ErrorHandler.classify(TimeoutError("timeout")) == 2
    
    def test_classify_l2_connection(self):
        """L2: 工具錯誤 - connection"""
        assert ErrorHandler.classify(ConnectionError("connection refused")) == 2
    
    def test_classify_l2_rate_limit(self):
        """L2: 工具錯誤 - rate limit"""
        assert ErrorHandler.classify(Exception("429 rate limit")) == 2
    
    def test_classify_l3_audio(self):
        """L3: 執行錯誤 - audio"""
        assert ErrorHandler.classify(IOError("audio file error")) == 3
    
    def test_classify_l3_encode(self):
        """L3: 執行錯誤 - encode"""
        assert ErrorHandler.classify(UnicodeDecodeError("utf-8", b"", 0, 1, "error")) == 3
    
    def test_classify_l4_system(self):
        """L4: 系統錯誤"""
        assert ErrorHandler.classify(Exception("system failure")) == 4
    
    def test_handle_l1(self):
        """L1 處理"""
        result = ErrorHandler.handle(ValueError("invalid"))
        assert result["status"] == "failed"
        assert result["level"] == "L1"
        assert result["recoverable"] == False
    
    def test_handle_l2(self):
        """L2 處理"""
        result = ErrorHandler.handle(TimeoutError("timeout"))
        assert result["status"] == "retry"
        assert result["level"] == "L2"
        assert result["recoverable"] == True
    
    def test_handle_l3(self):
        """L3 處理"""
        result = ErrorHandler.handle(IOError("audio error"))
        assert result["status"] == "degraded"
        assert result["level"] == "L3"
        assert result["recoverable"] == True
    
    def test_handle_l4(self):
        """L4 處理"""
        result = ErrorHandler.handle(Exception("system error"))
        assert result["status"] == "critical"
        assert result["level"] == "L4"
        assert result["recoverable"] == False
    
    def test_circuit_breaker(self):
        """熔斷測試"""
        # Reset first
        ErrorHandler.reset_circuit_breaker()
        
        # Trigger circuit breaker
        for _ in range(6):
            ErrorHandler.should_circuit_break()
        
        # Should trigger
        assert ErrorHandler.should_circuit_breaker() == True


class TestPresentationTTS:
    """PresentationTTS 整合測試"""
    
    def test_init_default(self):
        """預設初始化 - Smoke Test"""
        tts = PresentationTTS()
        assert tts.voice == "zh-TW-HsiaoHsiaoNeural"
    
    def test_init_custom(self):
        """自訂初始化 - Smoke Test"""
        tts = PresentationTTS(voice="test", rate="+10%")
        assert tts.voice == "test"
        assert tts.rate == "+10%"
    
    def test_init_with_volume(self):
        """音量初始化"""
        tts = PresentationTTS(volume="+50%")
        assert tts.volume == "+50%"
    
    def test_synthesize_empty(self):
        """空文字合成 - Regression Test"""
        tts = PresentationTTS()
        with tempfile.TemporaryDirectory() as tmpdir:
            result = tts.synthesize("", tmpdir)
            assert result["status"] == "failed"
            assert result["level"] == "L1"
    
    def test_synthesize_whitespace(self):
        """空白合成 - Regression Test"""
        tts = PresentationTTS()
        with tempfile.TemporaryDirectory() as tmpdir:
            result = tts.synthesize("   ", tmpdir)
            assert result["status"] == "failed"
            assert result["level"] == "L1"
    
    def test_synthesize_none(self):
        """None 合成 - Regression Test"""
        tts = PresentationTTS()
        with tempfile.TemporaryDirectory() as tmpdir:
            result = tts.synthesize(None, tmpdir)
            assert result["status"] == "failed"


class TestAsyncSynthesizer:
    """AsyncSynthesizer 單元測試"""
    
    def test_init(self):
        """初始化 - Smoke Test"""
        synth = AsyncSynthesizer(voice="test")
        assert synth.voice == "test"
    
    def test_init_default(self):
        """預設初始化"""
        synth = AsyncSynthesizer()
        assert synth.voice == "zh-TW-HsiaoHsiaoNeural"
        assert synth.is_busy == False


class TestCriticalPath:
    """Critical Path 測試 - 關鍵路徑覆蓋"""
    
    def test_critical_path_1_text_validation(self):
        """關鍵路徑 1: 文字驗證"""
        assert TextProcessor.validate_input("test") == True
        assert TextProcessor.validate_input("") == False
    
    def test_critical_path_2_error_handling(self):
        """關鍵路徑 2: 錯誤處理"""
        result = ErrorHandler.handle(ValueError("test"))
        assert "level" in result
        assert "status" in result
    
    def test_critical_path_3_synthesize(self):
        """關鍵路徑 3: 合成引擎"""
        tts = PresentationTTS()
        with tempfile.TemporaryDirectory() as tmpdir:
            result = tts.synthesize("測試", tmpdir)
            assert "status" in result
    
    def test_critical_path_4_async(self):
        """關鍵路徑 4: 非同步處理"""
        synth = AsyncSynthesizer()
        assert hasattr(synth, 'synthesize')


class TestRegression:
    """Regression Tests - 迴歸測試"""
    
    def test_regression_input_validation(self):
        """輸入驗證迴歸"""
        assert TextProcessor.validate_input("Hello World") == True
    
    def test_regression_empty_handling(self):
        """空輸入處理迴歸"""
        result = ErrorHandler.handle(ValueError(""))
        assert result["level"] == "L1"
    
    def_regression_text_splits = [
        ("短", 1),
        ("測試。" * 100, 2),
        ("。" * 500, 2)
    ]
    
    @pytest.mark.parametrize("text,expected_min", test_regression_text_splits)
    def test_regression_text_splitting(self, text, expected_min):
        """文字分段迴歸"""
        chunks = TextProcessor.split_text(text)
        assert len(chunks) >= expected_min


class TestSmoke:
    """Smoke Tests - 快速冒煙測試"""
    
    def test_smoke_tts_init(self):
        """TTS 初始化冒煙測試"""
        tts = PresentationTTS()
        assert tts is not None
    
    def test_smoke_processor(self):
        """Processor 冒煙測試"""
        processor = TextProcessor()
        assert processor is not None
    
    def test_smoke_handler(self):
        """Handler 冒煙測試"""
        handler = ErrorHandler()
        assert handler is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])