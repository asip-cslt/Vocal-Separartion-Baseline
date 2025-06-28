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



SAMPLERATE = 16000
CHUNKDUR = 10.0
import pyloudnorm
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
METER = pyloudnorm.Meter(SAMPLERATE)


def reverberate(audio, reverb_path):

    rirs = librosa.load(reverb_path, sr=SAMPLERATE)[0]
    rirs = rirs / np.sqrt(np.sum(rirs**2))
    if rirs.ndim == audio.ndim:
        audio = signal.convolve(audio, rirs, mode='full')[:audio.shape[0]]

    return audio
def mix_audios_with_snr_and_add_reverb(audios, sr, reverb_path, snr_range=[-3.0, 3.0]):
    assert isinstance(audios, list) and len(audios) > 1
    assert isinstance(snr_range, list) and len(snr_range) == 2 and snr_range[1] >= snr_range[0]

    target = audios[0]
    noises = audios[1:]
    target_energy = np.sum(target ** 2)
    mixed = np.copy(target)
    scaled_audios = [target]
    for noise in noises:
        c_loudness = METER.integrated_loudness(noise)
        if c_loudness == float('-inf'):
            raise ValueError("Detected -inf loudness, skip sample")

        if random.random() < 0.5:
            noise = reverberate(noise, reverb_path)

        noise_energy = np.sum(noise ** 2)
        snr_db = random.uniform(snr_range[0], snr_range[1])
        snr_linear = 10 ** (snr_db / 10)
        scale = np.sqrt((target_energy / snr_linear) / (noise_energy + 1e-8))
        scaled_noise = noise * scale
        mixed += scaled_noise
        scaled_audios.append(scaled_noise)
    
    # if random.random() < 0.5:
    #     rir_wav = librosa.load(reverb_path, sr=sr)[0]
    #     rir_wav = rir_wav / np.sqrt(np.sum(rir_wav ** 2))
    #     wav_len = mixed.shape[0]
    #     if rir_wav.ndim == mixed.ndim:
    #         mixed = signal.convolve(mixed, rir_wav, mode='full')[:wav_len]
    
    max_value = np.max(np.abs(mixed))
    if max_value > 1:
        mixed *= 0.9 / max_value
        scaled_audios = [audio * 0.9 / max_value for audio in scaled_audios]
    return mixed, scaled_audios

def generate(speech_dict, music_dict, reverb_dict, save_path, num):
    os.makedirs(save_path, exist_ok=True)
    spks = list(speech_dict.keys())
    instrus = list(music_dict.keys())
    rooms = list(reverb_dict.keys())
    # with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(open('baseline_valid_data_300.csv', 'w'))
    writer.writerow([
        "ID","duration","mix_wav","mix_wav_format","mix_wav_opts",
        "s1_wav","s1_wav_format","s1_wav_opts",
        "s2_wav","s2_wav_format","s2_wav_opts",
        "s3_wav","s3_wav_format","s3_wav_opts",
        "s4_wav","s4_wav_format","s4_wav_opts"
    ])
    sample_id = 0

    for i in tqdm(range(num), desc="Generating samples"):
        
        speech_num = random.randint(0, 2)
        music_num = 4 - speech_num
        sources = []
        max_len = SAMPLERATE * CHUNKDUR
        if speech_num > 0:
            chosen_spks = random.sample(spks, k=speech_num)
            for spk in chosen_spks:
                speech = np.zeros((max_len, ), dtype=np.float32)
                lenn = 0
                while lenn < max_len:
                    chosen_speech = random.choice(speech_dict[spk])
                    wav = librosa.load(chosen_speech, sr=SAMPLERATE)[0]
                    add = min(wav.shape[0], max_len - lenn)
                    speech[lenn:lenn + add] += wav[:add]
                    lenn += add + int(SAMPLERATE * 0.2)
                sources.append(speech)
        chosen_instrus = random.sample(instrus, k=music_num)
        for instru in chosen_instrus:
            music = np.zeros((max_len, ), dtype=np.float32)
            chosen_music = random.choice(music_dict[instru])
            wav = librosa.load(chosen_music, sr=SAMPLERATE)[0]
            start_pos = random.randint(0, max(0, wav.shape[0] - max_len))
            chunk = wav[start_pos:start_pos + max_len]
            music[:chunk.shape[0]] += chunk
            sources.append(music)
        # import ipdb; ipdb.set_trace()
        assert len(sources) == 4

        
        
        reverb = random.choice(reverb_dict[random.choice(rooms)])
        try:
            mixture, sources = mix_audios_with_snr_and_add_reverb(audios=sources,
                                                                sr=SAMPLERATE,
                                                                reverb_path=reverb)
        except ValueError as e:
            print(f"Skip sample {i+1}: {e}")
            continue
        sample_id += 1
        dest = os.path.join(save_path, f"sample-{sample_id:06d}")
        os.makedirs(dest, exist_ok=True)
        mix_path = os.path.join(dest, "mixture.wav")
        sf.write(mix_path, mixture, SAMPLERATE)

        row = [
            sample_id,
            1,             # duration
            mix_path,
            "wav",         # mix_wav_format
            "",            # mix_wav_opts
        ]

        for idx, src in enumerate(sources, start=1):
            src_path = os.path.join(dest, f"source{idx}.wav")
            sf.write(src_path, src, SAMPLERATE)
            row.extend([
                src_path,
                "wav",       # format
                ""           # opts
            ])

        writer.writerow(row)


def main(speech_json_path, music_json_path, reverb_json_path, save_path, save_csv, num, seed):
    random.seed(seed)
    speech_dict = json.load(open(speech_json_path, 'r'))
    music_dict = json.load(open(music_json_path, 'r'))
    reverb_dict = json.load(open(reverb_json_path, 'r'))
    generate(speech_dict, music_dict, reverb_dict, save_path, save_csv, num)


if __name__ == '__main__':
    fire.Fire(main)
