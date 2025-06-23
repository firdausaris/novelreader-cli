NovelReader CLI
Context-aware text-to-speech with Google TTS for professional audiobook quality


What is it?:
- Google Text-to-Speech Integration: Professional-quality, natural-sounding voices
- Automatic Character Voices: Each character gets a distinct accent (US, British, Australian, Canadian)
- MP3 Audiobook Export: Generate publication-ready audiobooks
- Smart Voice Assignment: AI-powered character voice mapping
- Enhanced Audio Quality: 22kHz high-quality output
- Overview
NovelReader CLI transforms your manuscripts into immersive audio experiences. Using advanced text analysis and Google's premium text-to-speech technology, it automatically assigns distinct voices and accents to different characters, making your novel come alive.

Key Features
- Smart Text Analysis: Automatically detects dialogue vs narrative sections
- Character Voice Mapping: Each character gets a unique voice with appropriate accent
- Multiple English Accents: US, British, Australian, Canadian variants
- Professional CLI: Simple command-line interface with powerful options
- Live Playback: Instant audio preview with character voices
- Text Preview: Analyze story structure before generating audio
- Audiobook Generation: Export to high-quality MP3 files
- Quick Start

Installation
bash
# Clone the repository
git clone https://github.com/firdausaris/novelreader-cli.git
cd novelreader-cli

# Install dependencies
pip install -r requirements.txt

# For Linux users, install audio dependencies
sudo apt-get install ffmpeg pulseaudio

Basic Usage
bash
# Preview your novel's structure
python novelreader.py --file novel.txt --preview

# Listen with professional character voices
python novelreader.py --file chapter1.txt

# Generate professional audiobook
python novelreader.py --file novel.txt --output audiobook.mp3
- Voice System
Automatic Character Assignment
- Narrator: US English (authoritative, deeper tone)

The old library creaked in the wind... → [Deep, authoritative US voice]
- Female Characters: British & Canadian English

"Hello? Anyone here?" Sarah called out... → [Elegant British accent]
- Male Characters: US & Australian English

"You shouldn't be here," the old man said... → [Gruff Australian accent]
Character Recognition
The system intelligently assigns voices based on:

Name patterns: Sarah, Emma, Anna → Female voices
Name patterns: John, David, Mike → Male voices
Context clues: Age descriptors, character roles
Dialogue patterns: Speech attribution analysis

- How It Works
Advanced Text Analysis Engine
Dialogue Detection: Identifies quoted speech using sophisticated pattern matching
Speaker Extraction: Finds character names from dialogue attribution:
"Hello," Sarah said. → Character: Sarah
John replied, "How are you?" → Character: John
Character Profiling: Builds voice profiles based on context clues
Voice Assignment: Maps characters to appropriate Google TTS voices

Example Processing
Input Text:
The rain hammered against the window. Sarah pushed open the door.
"Is anyone home?" she called out.
"We've been waiting for you," replied the mysterious figure.

Output Analysis:
Narrator: "The rain hammered..." → US English (authoritative)
Sarah: "Is anyone home?" → British English (female)  
Mysterious figure: "We've been waiting..." → Australian English (male)

Technical Implementation
Architecture
NovelReader/
├── novelreader.py          # Main CLI with Google TTS integration
├── sample_novel.txt        # Test content with multiple characters
├── requirements.txt        # Enhanced dependencies
├── setup.py               # Package installer
├── .github/workflows/     # CI/CD automation
└── docs/                  # Setup and usage guides

Key Technologies
Python 3.7+: Core programming language
Google Text-to-Speech (gTTS): Premium voice synthesis
pydub: Professional audio processing and MP3 export
Regular Expressions: Advanced dialogue pattern matching
AudioSegment: High-quality audio manipulation
Voice Quality Comparison
Feature	System TTS	Google TTS (v2.0)

Naturalness	**	*****
Character Variety	Limited	5+ Distinct Accents
Audio Quality	16kHz	22kHz Professional
Pronunciation	Basic	Advanced
Export Quality	WAV only	High-quality MP3

Command Reference
bash
python novelreader.py [OPTIONS]

File Processing:
  --file, -f FILE         Text file to process
  --output, -o FILE       Output MP3 audiobook file
  --preview, -p           Analyze text structure only

Voice Options:
  --list-voices, -lv      Show Google TTS voice information
  --no-google            Use system TTS (offline mode)

Information:
  --version              Show version (2.0 with Google TTS)
  --help, -h             Show detailed help

Examples:
  novelreader.py --file novel.txt --preview
  novelreader.py --file chapter1.txt  
  novelreader.py --file book.txt --output audiobook.mp3
  novelreader.py --list-voices

Use Cases
For Authors & Writers
- Draft Review: Listen to your manuscript while commuting
- Character Development: Hear how each character sounds
- Flow Analysis: Identify pacing and rhythm issues
- Dialogue Testing: Ensure conversations sound natural

For Content Creators
- Audiobook Production: Generate professional audiobooks
- Podcast Content: Convert written content to audio
- Accessibility: Make content available to visually impaired
- Educational Material: Create audio study guides

For Readers
- Multitasking: Listen while driving or exercising
- Comprehension: Audio can improve understanding
- Relaxation: Bedtime story reading
- Entertainment: Hands-free novel enjoyment
- Advanced Features

Character Voice Customization
The system automatically handles voice assignment, but you can influence it:

python
# Character name hints for better voice assignment
female_names = ['sarah', 'anna', 'emma', 'lisa']  # → British/Canadian voices
male_names = ['john', 'david', 'mike', 'james']   # → US/Australian voices
Audio Quality Enhancement
Narrator Optimization: Slower pace, authoritative tone
Character Differentiation: Distinct accents per character
Automatic Pacing: Pauses between segments
Volume Balancing: Consistent listening experience

Troubleshooting
Setup Issues
Missing audio dependencies (Linux):

bash
sudo apt-get install ffmpeg pulseaudio pulseaudio-utils
Internet connectivity required:

Google TTS requires internet connection
Use --no-google for offline mode with system TTS
Character detection problems:

Ensure dialogue uses standard quotation marks (")
Use common name patterns for better recognition
Check --preview mode to debug text analysis
Quality Issues
Audio not playing:

bash
# Test audio system
python -c "from pydub.playback import play; from pydub import AudioSegment; play(AudioSegment.silent(1000))"
Voice assignment problems:

Characters are assigned based on name patterns
Use clear, recognizable names for best results
System learns from context clues in your text

Future Enhancements
- OpenAI Integration: Advanced character personality analysis
- Emotion Detection: Voice tone based on scene mood
- Custom Voice Cloning: Upload voice samples for characters
- GUI Interface: Desktop application with visual controls
- Real-time Processing: Live text-to-speech while typing
- Background Music: Ambient soundtracks for scenes

Contributing
- Contributions welcome! This project demonstrates:

API Integration: Google TTS and audio processing
Text Analysis: Advanced NLP pattern matching
Audio Engineering: Professional audio manipulation
User Experience: Intuitive CLI design
Error Handling: Graceful fallbacks and recovery

License
- MIT License - Use freely for learning, development, and production.



Transform your novel into a professional audiobook with distinct character voices!

Created by Firdaus Aris - 2025



