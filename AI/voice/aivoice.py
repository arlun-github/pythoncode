from aip import AipSpeech
import pyaudio
import wave
from tqdm import tqdm
import subprocess


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
#RATE = 16000
RATE = 16000
RECORD_SECONDS = 10
VOICE_LEN = 10
FILE_NAME = './output.wav'
FILE_TYPE = FILE_NAME[-3:]

def record_audio(wave_out_path,record_second):
    #CHUNK = 1024
    #FORMAT = pyaudio.paInt16
    #CHANNELS = 2
    #RATE = 44100
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
 
    wf = wave.open(wave_out_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    print("开始录音，请说话.....")
    frames = []
    #for i in tqdm(range(0, int(RATE / CHUNK * record_second))):
    for i in tqdm(range(0, int(RATE / CHUNK * record_second)),\
            desc='录音进度', ncols=100, ascii=' =', bar_format='{l_bar}{bar}|'):
        data = stream.read(CHUNK)
        wf.writeframes(data)
    print("录音结束，请停止说话。")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()
 


def play_audio(wave_path):
 
    CHUNK = 1024
    wf = wave.open(wave_path, 'rb')
    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()
    # open stream (2)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    # read data
    data = wf.readframes(CHUNK)
    # play stream (3)
    datas = []
    while len(data) > 0:
        data = wf.readframes(CHUNK)
        datas.append(data)
    #for d in tqdm(datas):
    for d in datas:
        stream.write(d)
    # stop stream (4)
    stream.stop_stream()
    stream.close()
    # close PyAudio (5)
    p.terminate()
    

def rec(file_name):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    print("开始录音,请说话......")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("录音结束,请结束录音!")
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(file_name, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
def initClient():
    """ 你的 APPID AK SK """
    APP_ID = '23059834'
    API_KEY = 'cgMFxYhfFccAIAbAyRC8akL3'
    SECRET_KEY = 'FnXbkTx4ksepgGS3skltfndbA5zbNIgm'
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    return client

# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def main():
    client = initClient()
    #调用ffmpeg对mp3文件进行转换，转换为百度平台能够识别的wav文件
    #subprocess.call(['ffmpeg', '-i', 'sample1.m4a', 'sample1.wav'])
    try:
        record_audio("output.wav",record_second=VOICE_LEN)
    except Exception as e:
        print(e)
    input("请按任意键播放录音文件......")
    play_audio("output.wav")
    print("开始进行语音识别......")
    #rec('audio.pcm')
    # 识别本地文件
    result = client.asr(get_file_content(FILE_NAME), FILE_TYPE, RATE, {
        'dev_pid': 1537,
    })
    errNo = result.get('err_no')
    if errNo == 0:
        print("语音解析成功，文本为：{}".format(result.get('result')))
    elif errNo == 2000:
        print('语音解析失败')
    else:
        print('出现意外情况，请检查对百度语音平台的调用情况......')
        print("错误吗为：".format(errNo))
        print("错误信息：{}".format(result.get('err_msg')))
         

main()
        
    
