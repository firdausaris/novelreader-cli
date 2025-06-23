#!/usr/bin/env python3
"""
NovelReader CLI - AI-powered text-to-speech for novel writing
with Google TTS Integration
"""

import argparse
import re
import pyttsx3
import os
import json
import time
import tempfile
import io
from pathlib import Path
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

class NovelReader:
    def __init__(self, use_google_tts=True):
        self.use_google_tts = use_google_tts
        self.character_voices = {}
        
        if use_google_tts:
            self.setup_google_tts()
        else:
            # Fallback to system TTS
            self.engine = pyttsx3.init()
            self.voices = self.engine.getProperty('voices')
            self.setup_default_voices()
    
    def setup_google_tts(self):
        """Setup Google TTS with different voices for characters"""
        self.gtts_voices = {
            'narrator': {'lang': 'en', 'tld': 'com', 'slow': False},      # US English - authoritative
            'male_1': {'lang': 'en', 'tld': 'com', 'slow': False},        # US English - standard male
            'female_1': {'lang': 'en', 'tld': 'co.uk', 'slow': False},    # British English - elegant
            'male_2': {'lang': 'en', 'tld': 'com.au', 'slow': False},     # Australian English - casual
            'female_2': {'lang': 'en', 'tld': 'ca', 'slow': False},       # Canadian English - friendly
            'child': {'lang': 'en', 'tld': 'co.uk', 'slow': False},       # British - for young characters
            'elderly': {'lang': 'en', 'tld': 'com', 'slow': True},        # US English - slower pace
        }
        self.voice_assignments = {}
        
    def setup_default_voices(self):
        """Setup default voice configurations for pyttsx3 fallback"""
        if hasattr(self, 'voices') and len(self.voices) >= 2:
            self.narrator_voice = self.voices[0].id
            self.default_character_voice = self.voices[1].id if len(self.voices) > 1 else self.voices[0].id
        elif hasattr(self, 'voices'):
            self.narrator_voice = self.voices[0].id
            self.default_character_voice = self.voices[0].id
    
    def assign_google_voice(self, character):
        """Assign Google TTS voice characteristics to characters"""
        if character == 'narrator':
            return self.gtts_voices['narrator']
        
        if character in self.voice_assignments:
            return self.voice_assignments[character]
        
        # Smart voice assignment based on character analysis
        char_lower = character.lower()
        
        # Gender-based assignment (simple heuristics)
        female_names = ['sarah', 'anna', 'emma', 'lisa', 'maria', 'jane', 'kate', 'lucy', 'amy']
        male_names = ['john', 'david', 'mike', 'james', 'robert', 'tom', 'alex', 'sam', 'ben']
        
        if any(name in char_lower for name in female_names):
            voice_key = 'female_1' if len(self.voice_assignments) % 2 == 0 else 'female_2'
        elif any(name in char_lower for name in male_names):
            voice_key = 'male_1' if len(self.voice_assignments) % 2 == 0 else 'male_2'
        else:
            # Alternate between voice types
            voice_keys = ['female_1', 'male_1', 'female_2', 'male_2']
            voice_key = voice_keys[len(self.voice_assignments) % len(voice_keys)]
        
        self.voice_assignments[character] = self.gtts_voices[voice_key]
        return self.voice_assignments[character]
    
    def text_to_speech_google(self, text, character, play_audio=True, save_path=None):
        """Convert text to speech using Google TTS"""
        voice_config = self.assign_google_voice(character)
        
        try:
            # Create TTS object
            tts = gTTS(
                text=text, 
                lang=voice_config['lang'],
                tld=voice_config['tld'],
                slow=voice_config['slow']
            )
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                temp_path = temp_file.name
                tts.save(temp_path)
                
                # Load audio
                audio = AudioSegment.from_mp3(temp_path)
                
                # Apply character-specific audio effects
                audio = self.apply_character_effects(audio, character)
                
                if save_path:
                    audio.export(save_path, format="mp3")
                
                if play_audio:
                    play(audio)
                
                # Clean up temp file
                os.unlink(temp_path)
                
                return audio
                
        except Exception as e:
            print(f"Google TTS error: {e}")
            print("Falling back to system TTS...")
            return self.text_to_speech_fallback(text, character, play_audio)
    
    def apply_character_effects(self, audio, character):
        """Apply audio effects based on character type"""
        # Narrator: Slightly lower pitch, slower
        if character == 'narrator':
            # Slow down slightly for narrative
            audio = audio._spawn(audio.raw_data, overrides={"frame_rate": int(audio.frame_rate * 0.95)})
            audio = audio.set_frame_rate(audio.frame_rate)
        
        # Add subtle volume differences
        elif 'elderly' in character.lower():
            audio = audio - 2  # Slightly quieter
        elif 'child' in character.lower():
            audio = audio + 1  # Slightly louder
        
        return audio
    
    def text_to_speech_fallback(self, text, character, play_audio=True):
        """Fallback to system TTS if Google TTS fails"""
        if not hasattr(self, 'engine'):
            self.engine = pyttsx3.init()
            self.voices = self.engine.getProperty('voices') if not hasattr(self, 'voices') else self.voices
        
        # Set voice properties
        if character == 'narrator':
            if hasattr(self, 'narrator_voice'):
                self.engine.setProperty('voice', self.narrator_voice)
            self.engine.setProperty('rate', 170)
        else:
            if hasattr(self, 'default_character_voice'):
                self.engine.setProperty('voice', self.default_character_voice)
            self.engine.setProperty('rate', 180)
        
        self.engine.setProperty('volume', 0.9)
        
        if play_audio:
            self.engine.say(text)
            self.engine.runAndWait()
    
    def parse_text(self, text):
        """Parse text into dialogue and narrative segments"""
        segments = []
        paragraphs = text.split('\n\n')
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
                
            if self.is_dialogue(para):
                speaker = self.extract_speaker(para)
                dialogue_text = self.extract_dialogue_text(para)
                segments.append({
                    'type': 'dialogue',
                    'speaker': speaker,
                    'text': dialogue_text,
                    'original': para
                })
            else:
                segments.append({
                    'type': 'narrative',
                    'speaker': 'narrator',
                    'text': para,
                    'original': para
                })
        
        return segments
    
    def is_dialogue(self, text):
        """Check if text contains dialogue"""
        return bool(re.search(r'"[^"]*"', text))
    
    def extract_speaker(self, text):
        """Extract speaker name from dialogue paragraph"""
        patterns = [
            r'"[^"]*,"\s*(\w+)\s+said',  # "Hello," John said
            r'(\w+)\s+said,?\s*"',       # John said, "Hello"
            r'"[^"]*"\s*(\w+)\s+replied', # "Hello" John replied
            r'(\w+)\s+replied,?\s*"',     # John replied, "Hello"
            r'"[^"]*,"\s*(\w+)\s+asked',  # "Hello," John asked
            r'(\w+)\s+asked,?\s*"',       # John asked, "Hello"
            r'"[^"]*,"\s*(\w+)\s+whispered', # "Hello," John whispered
            r'(\w+)\s+whispered,?\s*"',   # John whispered, "Hello"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).lower()
        
        return 'unknown'
    
    def extract_dialogue_text(self, text):
        """Extract just the spoken dialogue from the paragraph"""
        dialogue_match = re.search(r'"([^"]*)"', text)
        if dialogue_match:
            return dialogue_match.group(1)
        return text
    
    def list_voice_options(self):
        """List available voice options"""
        print("\nNovelReader Voice Options:")
        print("=" * 50)
        
        if self.use_google_tts:
            print("Using Google Text-to-Speech (High Quality)")
            print("\nAvailable Voice Characteristics:")
            print("Narrator: US English (authoritative)")
            print("Male Characters: US English, Australian English")
            print("Female Characters: British English, Canadian English")
            print("Child Characters: British English (youthful)")
            print("Elderly Characters: US English (slower pace)")
            print("\nCharacters are automatically assigned based on names and context")
        else:
            print("🔧 Using System Text-to-Speech")
            if hasattr(self, 'voices'):
                for i, voice in enumerate(self.voices):
                    gender = "Female" if "female" in voice.name.lower() else "Male"
                    print(f"{i}: {voice.name} ({gender})")
    
    def process_file(self, file_path, output_path=None, preview=False):
        """Process a text file and convert to speech"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return False
        
        print(f"Processing: {file_path}")
        segments = self.parse_text(text)
        
        print(f"Found {len(segments)} segments:")
        dialogue_count = sum(1 for s in segments if s['type'] == 'dialogue')
        narrative_count = len(segments) - dialogue_count
        print(f"  {narrative_count} narrative segments")
        print(f"  {dialogue_count} dialogue segments")
        
        # Show character analysis
        characters = set(s['speaker'] for s in segments if s['speaker'] != 'narrator')
        if characters:
            print(f"  Characters detected: {', '.join(characters)}")
        
        if preview:
            print("\n--- PREVIEW (first 3 segments) ---")
            for i, segment in enumerate(segments[:3]):
                print(f"{i+1}. [{segment['type'].upper()}] {segment['speaker']}: {segment['text'][:100]}...")
            return True
        
        # Generate speech
        if output_path:
            print(f"\n🎵 Generating audio file: {output_path}")
            audio_segments = []
            
            for i, segment in enumerate(segments):
                print(f"  Processing segment {i+1}/{len(segments)}...")
                if self.use_google_tts:
                    audio = self.text_to_speech_google(
                        segment['text'], 
                        segment['speaker'], 
                        play_audio=False
                    )
                    if audio:
                        audio_segments.append(audio)
                        # Add pause between segments
                        audio_segments.append(AudioSegment.silent(duration=800))
            
            if audio_segments:
                # Combine all segments
                final_audio = sum(audio_segments)
                final_audio.export(output_path, format="mp3")
                print(f"Audio saved to: {output_path}")
            
        else:
            # Live playback
            print("\nStarting playback...")
            print("Each character will have a distinct voice and accent")
            print()
            
            for i, segment in enumerate(segments):
                speaker_info = f"[{segment['speaker']}]" if segment['speaker'] != 'narrator' else "[Narrator]"
                print(f"{speaker_info}: {segment['text'][:70]}...")
                
                if self.use_google_tts:
                    self.text_to_speech_google(segment['text'], segment['speaker'])
                else:
                    self.text_to_speech_fallback(segment['text'], segment['speaker'])
                
                time.sleep(0.3)  # Brief pause between segments
        
        return True

def main():
    parser = argparse.ArgumentParser(
        description="NovelReader CLI - AI-powered text-to-speech with Google TTS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --file novel.txt --preview          # Analyze text structure
  %(prog)s --file chapter1.txt                 # Live playback with Google voices
  %(prog)s --file story.txt --output story.mp3 # Generate MP3 audiobook
  %(prog)s --list-voices                       # Show voice information
  %(prog)s --file novel.txt --no-google        # Use system TTS instead
        """
    )
    
    parser.add_argument('--file', '-f', 
                       help='Text file to process')
    parser.add_argument('--output', '-o', 
                       help='Output MP3 file path')
    parser.add_argument('--preview', '-p', action='store_true',
                       help='Preview text analysis without generating audio')
    parser.add_argument('--list-voices', '-lv', action='store_true',
                       help='Show available voice options')
    parser.add_argument('--no-google', action='store_true',
                       help='Use system TTS instead of Google TTS')
    parser.add_argument('--version', action='version', version='NovelReader 2.0 with Google TTS')
    
    args = parser.parse_args()
    
    # Initialize reader
    use_google = not args.no_google
    reader = NovelReader(use_google_tts=use_google)
    
    print("🎭 NovelReader CLI 2.0 - Enhanced Text-to-Speech")
    print("=" * 55)
    
    # Handle voice listing
    if args.list_voices:
        reader.list_voice_options()
        return 0
    
    # Validate that we have a file for other operations
    if not args.file:
        print("Error: --file is required unless using --list-voices")
        parser.print_help()
        return 1
    
    # Validate input file
    if not os.path.exists(args.file):
        print(f"Error: File '{args.file}' not found.")
        return 1
    
    if use_google:
        print("Using Google Text-to-Speech for premium quality")
        print("Characters will automatically get distinct voices and accents")
    else:
        print("Using system Text-to-Speech")
    
    print()
    
    success = reader.process_file(
        file_path=args.file,
        output_path=args.output,
        preview=args.preview
    )
    
    if success:
        print("\nProcessing completed successfully!")
        if not args.preview and use_google:
            print("\nVoice assignments:")
            print("  Narrator: US English (authoritative)")
            for char in reader.voice_assignments:
                voice_info = reader.voice_assignments[char]
                accent = voice_info['tld'].replace('com', 'US').replace('co.uk', 'British').replace('com.au', 'Australian').replace('ca', 'Canadian')
                print(f"  {char}: {accent} English")
            
            print("\nTips:")
            print("  • Use --output filename.mp3 to save as audiobook")
            print("  • Each character automatically gets a unique voice")
            print("  • Narrator uses authoritative US English voice")
    else:
        print("\nProcessing failed.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())