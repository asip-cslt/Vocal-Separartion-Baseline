import os
import csv
import json
import fire
import random
import numpy as np
import librosa
import soundfile as sf
from scipy import signal
from tqdm import tqdm

'''
固定4mix,0~2个不同人的语音,其余为不同乐器的声音；
mix完后加混响,模拟安静室内环境。
'''

SAMPLERATE = 16000
CHUNKDUR = 10.0


def mix_audios_with_snr_and_add_reverb(audios, sr, reverb_path, snr_range=[-3.0, 3.0]):
    assert isinstance(audios, list) and len(audios) > 1
    assert isinstance(snr_range, list) and len(snr_range) == 2 and snr_range[1] >= snr_range[0]

    target = audios[0]
    noises = audios[1:]
    target_energy = np.sum(target ** 2)
    mixed = np.copy(target)
    scaled_audios = [target]
    for noise in noises:
        noise_energy = np.sum(noise ** 2)
        snr_db = random.uniform(snr_range[0], snr_range[1])
        snr_linear = 10 ** (snr_db / 10)
        scale = np.sqrt((target_energy / snr_linear) / (noise_energy + 1e-8))
        scaled_noise = noise * scale
        mixed += scaled_noise
        scaled_audios.append(scaled_noise)
    
    if random.random() < 0.5:
        rir_wav = librosa.load(reverb_path, sr=sr)[0]
        rir_wav = rir_wav / np.sqrt(np.sum(rir_wav ** 2))
        wav_len = mixed.shape[0]
        if rir_wav.ndim == mixed.ndim:
            mixed = signal.convolve(mixed, rir_wav, mode='full')[:wav_len]
    
    max_value = np.max(np.abs(mixed))
    if max_value > 1:
        mixed *= 0.9 / max_value
        scaled_audios = [audio * 0.9 / max_value for audio in scaled_audios]
    return mixed, scaled_audios


def generate(speech_dict, music_dict, reverb_dict, save_path, save_csv, num):
    spks = list(speech_dict.keys())
    instrus = list(music_dict.keys())
    rooms = list(reverb_dict.keys())
    writer = csv.writer(open(save_csv, 'w'))
    writer.writerow(['ID', 'duration',
                     'mix_wav', 'mix_wav_format', 'mix_wav_opts',
                     's1_wav', 's1_wav_format', 's1_wav_opts',
                     's2_wav', 's2_wav_format', 's2_wav_opts',
                     's3_wav', 's3_wav_format', 's3_wav_opts',
                     's4_wav', 's4_wav_format', 's4_wav_opts'])
    for i in tqdm(range(num)):
        dest_path = os.path.join(save_path, f"sample-{i:06d}")
        os.makedirs(dest_path)
        speech_num = random.randint(0, 2)
        music_num = 4 - speech_num
        sources = []
        max_len = int(SAMPLERATE * CHUNKDUR)
        if speech_num > 0:
            # 随机选择speech_num名说话人
            chosen_spks = random.sample(spks, k=speech_num)
            for spk in chosen_spks:
                speech = np.zeros((max_len, ), dtype=np.float32)
                lenn = 0
                # AISHELL-1 语音片段较短，因此拼接多条避免长时间的静音段
                while lenn < max_len:
                    chosen_speech = random.choice(speech_dict[spk])
                    wav = librosa.load(chosen_speech, sr=SAMPLERATE)[0]
                    add = min(wav.shape[0], max_len - lenn)
                    speech[lenn:lenn + add] += wav[:add]
                    lenn += add + int(SAMPLERATE * 0.2)
                sources.append(speech)
        # 随机选择music_num个乐器
        chosen_instrus = random.sample(instrus, k=music_num)
        for instru in chosen_instrus:
            music = np.zeros((max_len, ), dtype=np.float32)
            chosen_music = random.choice(music_dict[instru])
            wav = librosa.load(chosen_music, sr=SAMPLERATE)[0]
            start_pos = random.randint(0, max(0, wav.shape[0] - max_len))
            chunk = wav[start_pos:start_pos + max_len]
            music[:chunk.shape[0]] += chunk
            sources.append(music)
        assert len(sources) == 4
        reverb = random.choice(reverb_dict[random.choice(rooms)])
        mixture, sources = mix_audios_with_snr_and_add_reverb(audios=sources,
                                                              sr=SAMPLERATE,
                                                              reverb_path=reverb)
        mixture_path = os.path.join(dest_path, 'mixture.wav')
        sf.write(mixture_path, mixture, samplerate=SAMPLERATE)
        row_meta = [i, CHUNKDUR, mixture_path, 'wav', '']
        for j, audio in enumerate(sources):
            audio_path = os.path.join(dest_path, f'source{j+1}.wav')
            sf.write(audio_path, audio, samplerate=SAMPLERATE)
            row_meta.append(audio_path)
            row_meta.append('wav')
            row_meta.append('')
        assert len(row_meta) == 2 + 3 * 5
        writer.writerow(row_meta)


def main(speech_json_path, music_json_path, reverb_json_path, save_path, save_csv, num, seed):
    random.seed(seed)
    speech_dict = json.load(open(speech_json_path, 'r'))
    music_dict = json.load(open(music_json_path, 'r'))
    reverb_dict = json.load(open(reverb_json_path, 'r'))
    generate(speech_dict, music_dict, reverb_dict, save_path, save_csv, num)


if __name__ == '__main__':
    fire.Fire(main)
