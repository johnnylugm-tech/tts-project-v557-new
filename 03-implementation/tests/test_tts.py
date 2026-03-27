"""
Unit Tests - TTS Engine
Phase: 3 - 代碼實現
對應 SKILL.md: Testing Strategy
"""

import pytest
import tempfile
from tts_engine import PresentationTTS, TextProcessor, ErrorHandler, AsyncSynthesizer


class TestTextProcessor:
    def test_validate_input_valid(self):
        assert TextProcessor.validate_input("Hello") == True
    
    def test_validate_input_empty(self):
        assert TextProcessor.validate_input("") == False
    
    def test_split_text_short(self):
        chunks = TextProcessor.split_text("Hello")
        assert len(chunks) == 1
    
    def test_split_text_long(self):
        chunks = TextProcessor.split_text("測試。" * 200)
        assert len(chunks) > 1


class TestErrorHandler:
    def test_classify_l1(self):
        assert ErrorHandler.classify(ValueError("invalid")) == 1
    
    def test_classify_l2(self):
        assert ErrorHandler.classify(TimeoutError("timeout")) == 2
    
    def test_classify_l3(self):
        assert ErrorHandler.classify(IOError("encode")) == 3
    
    def test_classify_l4(self):
        assert ErrorHandler.classify(Exception("system")) == 4
    
    def test_handle_l1(self):
        result = ErrorHandler.handle(ValueError("invalid"))
        assert result["status"] == "failed"


class TestPresentationTTS:
    def test_init_default(self):
        tts = PresentationTTS()
        assert tts.voice == "zh-TW-HsiaoHsiaoNeural"
    
    def test_init_custom(self):
        tts = PresentationTTS(voice="test", rate="+10%")
        assert tts.voice == "test"
    
    def test_synthesize_empty(self):
        tts = PresentationTTS()
        with tempfile.TemporaryDirectory() as tmpdir:
            result = tts.synthesize("", tmpdir)
            assert result["status"] == "failed"


class TestAsyncSynthesizer:
    def test_init(self):
        synth = AsyncSynthesizer(voice="test")
        assert synth.voice == "test"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
