#!/usr/bin/env python3
"""
Quick test script for NovelReader CLI with Google TTS
Run this to verify everything is working properly
"""

import os
import sys
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import tempfile

def test_google_tts():
    """Test basic Google TTS functionality"""
    print("🔍 Testing Google TTS...")
    
    try:
        # Test basic TTS
        tts = gTTS("Hello! Google Text-to-Speech is working correctly.", lang='en', tld='com')
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            tts.save(temp_file.name)
            audio = AudioSegment.from_mp3(temp_file.name)
            
            print("Google TTS: Working")
            print("🔊 Playing test audio...")
            play(audio)
            
            os.unlink(temp_file.name)
            return True
            
    except Exception as e:
        print(f"Google TTS Error: {e}")
        return False

def test_different_voices():
    """Test different Google TTS voices/accents"""
    print("\n🎭 Testing different accents...")
    
    voices = [
        ("US English", 'en', 'com'),
        ("British English", 'en', 'co.uk'),
        ("Australian English", 'en', 'com.au'),
        ("Canadian English", 'en', 'ca')
    ]
    
    for name, lang, tld in voices:
        try:
            print(f"🔊 Testing {name}...")
            tts = gTTS(f"Hello from {name}!", lang=lang, tld=tld)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                tts.save(temp_file.name)
                audio = AudioSegment.from_mp3(temp_file.name)
                play(audio)
                os.unlink(temp_file.name)
                
            input("Press Enter for next voice...")
            
        except Exception as e:
            print(f"{name} failed: {e}")

def test_novelreader():
    """Test the main NovelReader functionality"""
    print("\nTesting NovelReader CLI...")
    
    # Check if sample file exists
    if not os.path.exists('sample_novel.txt'):
        print("sample_novel.txt not found")
        return False
    
    # Test preview mode
    print("Testing preview mode...")
    result = os.system("python novelreader.py --file sample_novel.txt --preview")
    
    if result == 0:
        print("Preview mode: Working")
    else:
        print("Preview mode: Failed")
        return False
    
    # Test voice listing
    print("\n🎤 Testing voice listing...")
    result = os.system("python novelreader.py --list-voices")
    
    if result == 0:
        print("Voice listing: Working")
    else:
        print("Voice listing: Failed")
        return False
    
    return True

def check_dependencies():
    """Check if all required packages are installed"""
    print("Checking dependencies...")
    
    required_packages = [
        ('gtts', 'Google Text-to-Speech'),
        ('pydub', 'Audio processing'),
        ('pyttsx3', 'Fallback TTS'),
    ]
    
    all_good = True
    
    for package, description in required_packages:
        try:
            __import__(package)
            print(f"{package}: Installed ({description})")
        except ImportError:
            print(f"{package}: Missing ({description})")
            print(f"   Install with: pip install {package}")
            all_good = False
    
    return all_good

def main():
    print("NovelReader CLI - Google TTS Test Suite")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("\nPlease install missing dependencies first:")
        print("pip install -r requirements.txt")
        return 1
    
    print("\nTesting internet connection...")
    try:
        import urllib.request
        urllib.request.urlopen('http://google.com', timeout=5)
        print("Internet connection: Available")
    except:
        print("Internet connection: Required for Google TTS")
        return 1
    
    # Test Google TTS
    if not test_google_tts():
        print("\nGoogle TTS test failed")
        return 1
    
    # Test different voices (optional)
    print("\nWould you like to test different character voices?")
    choice = input("Type 'y' for yes, any other key to skip: ").lower()
    if choice == 'y':
        test_different_voices()
    
    # Test main application
    if not test_novelreader():
        print("\nNovelReader test failed")
        return 1
    
    print("\nAll tests passed! NovelReader CLI is ready to use.")
    print("\nTry these commands:")
    print("• python novelreader.py --file sample_novel.txt --preview")
    print("• python novelreader.py --file sample_novel.txt")
    print("• python novelreader.py --file sample_novel.txt --output audiobook.mp3")
    
    return 0

if __name__ == "__main__":
    exit(main())