"""
CLI Interface - 命令列介面

Phase: 3 - 代碼實現
對應 SKILL.md: Interface Design - CLI
"""

import argparse
import os
import sys
import asyncio
from tts_engine import PresentationTTS, TextProcessor, ErrorHandler


class CLI:
    """命令列介面"""
    
    def __init__(self):
        self.parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(prog="tts-cli", description="高品質簡報配音系統")
        
        subparsers = parser.add_subparsers(dest="command", help="指令")
        
        synthesize_parser = subparsers.add_parser("synthesize", help="文字轉語音")
        synthesize_parser.add_argument("text", help="要轉換的文字")
        synthesize_parser.add_argument("-o", "--output", default="output.mp3", help="輸出檔案")
        synthesize_parser.add_argument("-v", "--voice", default="zh-TW-HsiaoHsiaoNeural", help="音色")
        synthesize_parser.add_argument("-r", "--rate", default="+0%", help="語速")
        synthesize_parser.add_argument("--volume", default="+0%", help="音量")
        
        voices_parser = subparsers.add_parser("voices", help="列出可用音色")
        
        test_parser = subparsers.add_parser("test", help="執行測試")
        test_parser.add_argument("-v", "--verbose", action="store_true", help="詳細輸出")
        
        return parser
    
    def run(self, args: list = None) -> int:
        parsed = self.parser.parse_args(args)
        
        if not parsed.command:
            self.parser.print_help()
            return 1
        
        if parsed.command == "synthesize":
            return self._handle_synthesize(parsed)
        elif parsed.command == "voices":
            return self._handle_voices()
        elif parsed.command == "test":
            return self._handle_test(parsed)
        
        return 0
    
    def _handle_synthesize(self, args) -> int:
        try:
            tts = PresentationTTS(voice=args.voice, rate=args.rate, volume=args.volume)
            output_dir = os.path.dirname(args.output) or "temp"
            os.makedirs(output_dir, exist_ok=True)
            
            result = tts.synthesize(args.text, output_dir)
            
            if result["status"] == "completed":
                print(f"合成完成: {result['success']}/{result['total_chunks']} 區塊")
                return 0
            else:
                print(f"合成失敗: {result.get('message')}")
                return 1
        except Exception as e:
            error_result = ErrorHandler.handle(e)
            print(f"錯誤: {error_result['message']}")
            return 1
    
    def _handle_voices(self) -> int:
        print("可用音色:")
        voices = [
            ("zh-TW-HsiaoHsiaoNeural", "台灣曉曉 (女)"),
            ("zh-TW-HsiaoChenNeural", "台灣曉晨 (男)"),
        ]
        for vid, desc in voices:
            print(f"  {vid:30} - {desc}")
        return 0
    
    def _handle_test(self, args) -> int:
        test_text = "測試。"
        chunks = TextProcessor.split_text(test_text)
        print(f"文本分段: {len(chunks)} 區塊")
        
        test_error = ValueError("invalid")
        level = ErrorHandler.classify(test_error)
        print(f"錯誤分類: L{level}")
        print("測試完成")
        return 0


def main():
    cli = CLI()
    sys.exit(cli.run())


if __name__ == "__main__":
    main()