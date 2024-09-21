# Intelligent Voice Assistant System

## Project Overview

This is an intelligent voice assistant system based on keyword detection, speech recognition, speech synthesis, and dialogue generation. The system can initiate a voice conversation with users through specific wake words (such as "hey bro") and provide intelligent replies using advanced natural language processing technology.

## Main Features

- **Keyword Detection**: Real-time monitoring of wake words using Porcupine to initiate conversation.
- **Voice Recording and Detection**: Voice activity detection using WebRTC VAD to record valid voice segments.
- **Speech Recognition (ASR)**: Converting recorded voice to text using the SenseVoice Small model.
- **Dialogue Generation**: Generating the assistant's text replies based on context by calling the Ollama API (compatible with OpenAI API).
- **Speech Synthesis (TTS)**: Outputting the assistant's replies through speech synthesis to simulate human voice conversation.
- **Dialogue History Saving**: Regularly saving dialogue content as JSON files for subsequent analysis.

## Technology Stack

- Python
- Porcupine (Keyword Detection)
- WebRTC VAD (Voice Activity Detection)
- SenseVoice Small (Speech Recognition)
- Ollama API (Dialogue Generation)
- GPT-SoVITS (Speech Synthesis)
- PyAudio, NumPy, SciPy (Audio Processing)

## TTS Part

This project is based on the GPT-SoVITS API, and we appreciate the contributions of the open-source community workers!

### GPT-SoVITS TTS Project

This is a Text-to-Speech (TTS) project based on the GPT-SoVITS API. The project allows users to generate and play voice with different emotions, using predefined reference audio to influence the output voice style.

### Features

- Supports voice generation with various emotions (happy, depressed, excited, calm, confused).
- Uses reference audio to control voice style.
- Real-time generation and playback of WAV format audio files.
- Customizable text input and output filenames.
- Provides TTS processing time statistics.
- Can add an emotion recognition model to decide the reference audio, thus controlling the audio synthesis emotion (to do).

## Usage Guide

1.Clone the repository:
- git clone https://github.com/your-username/intelligent-voice-assistant.git
- cd intelligent-voice-assistant

2. Install dependencies:

- pip install -r requirements.txt

3. Prepare necessary API keys and models:
- Obtain Porcupine API key.
- Download SenseVoice Small model files.
- Ensure Ollama API service is running.
- Start GPT-Sovits API service.
        
4. Configure the system:
- Fill in the Porcupine API key in the script.
- Set the ASR model path.
- Configure Ollama API endpoint (default is local).
- Configure GPT-sovits model and reference audio.

5. Run the main script:

- python main_ollama.py

- Wait for the system to prompt "Listening for wake word..."
- Speak the wake word (default is "hey bro") to start the conversation.
- Engage in natural language interaction with the voice assistant.
- If timed out, trigger again.
- The conversation record is automatically saved at the end of the round.

## Main Features

- Real-time voice interaction.
- Intelligent dialogue generation.
- Natural voice synthesis.
- Automatic sleep mode after a long period of no voice.
- Dialogue history recording.
- Custom settings.

## Customization

- Modify the `settings` variable to customize the assistant's role and background.
- Adjust parameters such as `max_silence_duration` and `min_speech_duration` to optimize voice detection.
- Change the wake word and corresponding model files.

## License

This project is licensed under the MIT License

## Contact

Project Maintainer: HaxxorCialtion - cialtion@outlook.com

Bilibili Video Address: [Insert Bilibili Video Link Here]

## Acknowledgements

- [Porcupine](https://github.com/Picovoice/porcupine) 
- [SenseVoice](https://github.com/FunAudioLLM/SenseVoice) 
- [Ollama](https://github.com/ollama/ollama) 
- [LLM](https://github.com/QwenLM/Qwen2.5) 
- [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS) 