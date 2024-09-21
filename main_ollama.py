"""
ASR LLM TTS 部分需要的模型和文件需要自己配置，详情参考README.md
"""
import pvporcupine
import pyaudio
import numpy as np
from funasr_onnx import SenseVoiceSmall
from funasr_onnx.utils.postprocess_utils import rich_transcription_postprocess
from scipy.io.wavfile import write
import sounddevice as sd
import time
import webrtcvad
import os
import requests
import json
from datetime import datetime
import gpt_sovits_api
import soundfile as sf

def record_audio_vad(filename, sample_rate, vad):
    print("Recording started with VAD...")

    audio = []
    silence_frames = 0
    speech_frames = 0
    max_silence_duration = 1.5  # 增加到1.5秒
    min_speech_duration = 0.5  # 最小语音持续时间为0.5秒
    speech_started = False
    valid_speech = False

    stream = sd.InputStream(samplerate=sample_rate, channels=1, dtype='int16')
    with stream:
        while True:
            frame = stream.read(frame_length)[0]
            frame = frame.flatten()

            is_speech = vad.is_speech(frame.tobytes(), sample_rate)

            if is_speech:
                speech_frames += 1
                silence_frames = 0
                if not speech_started:
                    speech_started = True
                    print("Speech detected, recording started.")
            else:
                silence_frames += 1
                if speech_started:
                    audio.append(frame)

            if speech_started:
                audio.append(frame)

            # 检查是否达到最小语音持续时间
            if speech_frames * frame_duration / 1000 >= min_speech_duration:
                valid_speech = True

            # 检查是否达到最大静音持续时间
            if silence_frames * frame_duration / 1000 > max_silence_duration:
                if valid_speech:
                    print("Silence detected after valid speech. Stopping recording.")
                    break
                else:
                    print("Short noise detected. Resetting.")
                    audio = []
                    silence_frames = 0
                    speech_frames = 0
                    speech_started = False
                    valid_speech = False

    if len(audio) > 0 and valid_speech:
        audio_data = np.concatenate(audio, axis=0)
        write(filename, sample_rate, audio_data)
        print(f"Recording finished. Saved to {filename}")
        return filename
    else:
        print("No valid speech detected. No audio file saved.")
        return None

def transcribe_audio(wav_file, model):
    print(f"Processing audio file {wav_file}...")
    t1 = time.time()
    res = model([wav_file], language="zh", use_itn=True)
    transcription = [rich_transcription_postprocess(i) for i in res]
    print(f"ASR耗时: {time.time() - t1} seconds")
    return transcription[0]  # 返回第一个（也是唯一的）转录结果

def tts(temp_text="你好", emotion="抑郁", output_file=f"temp_12.wav"):
    gpt_sovits_api.gpt_sovits(temp_text, emotion, output_file)

def dp_chat(message: str, stream=False):
    global conversation_history
    t1 = time.time()

    conversation_history.append({"role": "user", "content": message})

    payload = {
        "model": "qwen2.5",
        "messages": conversation_history,
        "stream": stream,
    }
    url = "http://localhost:11434/api/chat"
    response = requests.post(url, json=payload)
    if stream:
        # 逐行读取流式响应内容
        for line in response.iter_lines():
            if line:
                # 尝试将每一行解析为 JSON
                try:
                    data = json.loads(line.decode('utf-8'))
                    print(data)  # 打印每一个 JSON 数据块
                except json.JSONDecodeError as e:
                    print(f"JSON 解析失败: {e}")
    else:
        response_json = response.json()
        assistant_response = response_json.get("message", {}).get("content", "")

    t2 = time.time()
    print(f"API response time: {t2 - t1} seconds")

    conversation_history.append({"role": "assistant", "content": assistant_response})

    tts(assistant_response)

    return assistant_response

def play_audio(file_path):
    """触发唤醒词后，播放hello文件"""
    data, fs = sf.read(file_path, dtype='float32')  # 读取音频文件
    sd.play(data, fs)  # 播放音频
    sd.wait()  # 等待音频播放结束

def continuous_conversation(model, vad, sleep_time=10):
    max_silence_duration = sleep_time  # 最大静音时长为 60 秒
    while True:
        audio_filename = "input_audio.wav"
        start_time = time.time()

        # 记录开始录音的时间
        recorded_file = record_audio_vad(audio_filename, sample_rate, vad)

        if recorded_file is None:
            print("No valid speech detected. Please try again.")
            continue

        # 如果超过了指定时间没有检测到有效语音，退出对话
        if time.time() - start_time > max_silence_duration:
            print("No speech detected for 60 seconds. Conversation ended.")
            play_audio("./sleep.wav")
            break

        # 语音转文字
        transcription_result = transcribe_audio(recorded_file, model)
        if transcription_result.lower() in ['退出', '结束对话', 'exit', 'quit']:
            print("对话结束")
            break

        # 生成助手回复
        response = dp_chat(transcription_result)
        print("User:", transcription_result)
        print("Assistant:", response)

def save_conversation_history():
    if not os.path.exists("conversation_logs"):
        os.makedirs("conversation_logs")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"conversation_logs/conversation_{timestamp}.json"

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(conversation_history, f, ensure_ascii=False, indent=2)

    print(f"Conversation history saved to {filename}")

def start_service():
    print("Initializing Porcupine and ASR model...")

    # 加载ASR模型
    model = SenseVoiceSmall(model_dir, batch_size=10, quantize=True)

    # 检测音频流中是否存在语音，它可以区分音频信号中的语音和背景噪音
    vad = webrtcvad.Vad()
    vad.set_mode(2)  # 参数范围0-3，越大越严格，越能忽略更多的背景噪音

    pa = pyaudio.PyAudio()
    stream = pa.open(rate=porcupine.sample_rate,    # 音频流的采样率
                     channels=1,    # 音频流的通道数
                     format=pyaudio.paInt16,    # 音频数据的格式
                     input=True,    # 指定这个音频流是用于输入(采集音频)
                     frames_per_buffer=porcupine.frame_length)  # 缓冲区大小，表示每次从音频输入设备读取多少帧

    print("Listening for wake word...")

    try:
        while True:
            pcm = stream.read(porcupine.frame_length)   # 从麦克风音频输入流中读取指定长度的音频数据
            pcm = np.frombuffer(pcm, dtype=np.int16)

            keyword_index = porcupine.process(pcm)      # 调用process方法检测是否包含唤醒词
            if keyword_index >= 0:
                print("Wake word detected! Starting conversation...")
                stream.stop_stream()    # 上文已经获取到唤醒词，则先停止当前音频流，准备之后的对话
                # 额外功能：播放当前文件夹下的hello.wav
                play_audio("hello.wav")
                continuous_conversation(model, vad)
                stream.start_stream()
                print("Conversation ended. Listening for wake word again...")
    except KeyboardInterrupt:
        print("Stopping service...")
    finally:
        stream.close()
        pa.terminate()
        save_conversation_history()


if __name__ == "__main__":
    # 配置Porcupine关键词检测
    porcupine = pvporcupine.create(
        access_key=f"输入你的API",
        keyword_paths=["./hey-bro_en_windows_v3_0_0/hey-bro_en_windows_v3_0_0.ppn"]
    )

    # ASR模型路径
    model_dir = "conversation_logs/sensevoice-small-onnx-quant"
    sample_rate = 16000
    frame_duration = 30
    frame_length = int(sample_rate * frame_duration / 1000)

    settings = ("你的名字是水月，我是博士，我从事理论与计算化学的工作，需要学习数学物理化学计算机的交叉知识，你是我的助手，你和博士现在都还不够优秀，"
                "你们会在之后的学习生涯中慢慢变得更加优秀。")
    # 全局变量用于存储对话历史
    conversation_history = [
        {"role": "system", "content": f"你将扮演一个和我用语音聊天的对象，回复就和正常说话一样，得简短。{settings}"},
        {"role": "user", "content": "我是谁？你又是谁？"},
        {"role": "assistant", "content": "你是博士，我是水月"}
    ]

    start_service()