import requests
import os
import time
from playsound import playsound
import pyaudio
import wave

# 基础URL
base_url = "http://127.0.0.1:9880"

def get_audio_file_path(emotion):
    """获取参考音频的路径"""
    paths = {
        "高兴": "./参考音频/要吸收和消化掉这些对吧？我会努力的！.wav",
        "抑郁": "./参考音频/虽然可惜依旧不能算正式干员的样子.wav",
        "激动": "./参考音频/这下坏人的数量又减少了呢！都是多亏了博士！.wav",
        "平静": "./参考音频/嗯？博士怎么放炮了几个坏人？我去替博士收拾一下吧。.wav",
        "纠结": "./参考音频/不要吧，那我会很困扰啊。.wav"
    }
    return paths.get(emotion)

def change_reference_audio(emotion, prompt_language="zh"):
    """切换参考音频并发送请求"""
    refer_wav_path = get_audio_file_path(emotion)
    filename = os.path.basename(refer_wav_path)
    file_name_without_extension = os.path.splitext(filename)[0]
    prompt_text = file_name_without_extension
    data = {
        "refer_wav_path": refer_wav_path,
        "prompt_text": prompt_text,
        "prompt_language": prompt_language
    }

    response = requests.post(f"{base_url}/change_refer", json=data)
def save_audio_from_response(url, data, output_file):
    """执行推理并保存音频"""
    try:
        response = requests.post(url, json=data)

        if response.status_code == 200:
            with open(output_file, "wb") as f:
                f.write(response.content)
            return output_file
        else:
            print(response.status_code)
    except Exception as e:
        print(e)

def play_wav_file(wav_file):
    # 打开WAV文件
    wf = wave.open(wav_file, 'rb')

    # 创建PyAudio对象
    p = pyaudio.PyAudio()

    # 打开音频流
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # 读取数据并播放
    data = wf.readframes(1024)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(1024)

    # 停止和关闭音频流
    stream.stop_stream()
    stream.close()

    # 关闭PyAudio
    p.terminate()

def gpt_sovits(temp_text="长时间没和我交流，已待机", emotion="高兴", output_file=f"temp_12.wav"):
    t1 = time.time()
    base_url = "http://127.0.0.1:9880"
    url = f"{base_url}/"
    data = {
        "text": f"{temp_text}",
        "text_language": "zh",
        "cut_punc": "，。！？!、：；？.，、—‘’“”《》【】()[]{}「」『』‖｜…‥・﹏﹋﹌·･~－−—―「」『』〝〞",
        # "cut_punc": "。",
        "top_k": 20,
        "top_p": 1.0,
        "temperature": 1,
        "speed": 1.0
    }
    change_reference_audio(emotion, "zh")
    wav_file = save_audio_from_response(url, data, output_file)
    t2 = time.time()
    print(f"TTS耗时： {t2 - t1} seconds")
    # 播放音频
    play_wav_file(wav_file)

"""
$$ http://127.0.0.1:9880?text=晚上好，博士！&refer_wav_path=E:\AI_tools\resperpy\参考音频\虽然可惜依旧不能算正式干员的样子.wav&prompt_text=虽然可惜依旧不能算正式干员的样子&prompt_language=zh&text_language=zh&cut_punc=，。！？!、：；？.，、—‘’“”《》【】()[]{}「」『』‖｜…‥・﹏﹋﹌·･~－−—―「」『』〝〞&top_k=20&top_p=1.0&temperature=1&speed=1.0
"""