from typing import Tuple

class ContentValidator:
    @staticmethod
    def validate_content(extracted_text: str) -> Tuple[bool, int]:
        """Validate content once and return word count"""
        if not extracted_text:
            print("❌ No text extracted from PDF")
            return (False, 0)
        
        word_count = len(extracted_text.split())
        print(f"✓ Content validated ({word_count} words)")
        return (True, word_count)

    @staticmethod
    def check_platform_requirements(platform: str, word_count: int, config_manager) -> bool:
        """Check if content meets platform-specific requirements"""
        min_length = config_manager.get_platform_requirement(platform)
        if word_count < min_length:
            print(f"❌ Insufficient content for {platform} ({word_count} words, need {min_length})")
            return False
        return True
