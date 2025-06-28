# Universal Sound Separation Baseline

## Introduction

This repository provides a baseline system for **Task 2** of the **CCF 2025 Challenge for Advanced Audio Technology** ([link](https://ccf-aatc.org.cn/)).  
The task focuses on separating individual components from mixed audio signals, specifically mixtures containing **0–2 streams of human speech (from different speakers)** and **2–4 music streams** with various instruments.

The task is divided into two phases:

1. **Simulation Test**  
   - The mixed signal is single-channel, created by combining clean speech and music sources with added reverberation.  
   - SI-SDR is used as the evaluation metric.

2. **Real-world Test**  
   - Uses two-channel recordings of four sources played simultaneously by four loudspeakers.  
   - MOS (Mean Opinion Score) is used for evaluation.

**Note:** This baseline system is designed exclusively for the **simulation test**.  
The code is built on [SpeechBrain](https://speechbrain.github.io/) and uses the **Conv-TasNet** architecture.  
Training data combines AISHELL-1 (speech) and MUSIC (music) datasets with simulated reverberation to match the test conditions.

---

## Environment Setup

```bash
conda create -n sb_sep python=3.11 -y
conda activate sb_sep
pip install -r requirements.txt
```

## Data Preparation

We use **AISHELL-1** as the speech dataset, **MUSIC** as the music dataset, and the **RIRs dataset** to simulate room reverberation.  
All audio files will be converted to `pcm_s16le` format and resampled to **16kHz**.

### Steps

1. Download the datasets: **AISHELL-1**, **MUSIC**, and **RIRs**.
2. Modify the paths in `recipes/Conv-Tasnet/data/data_lists/*.json` to point to the correct data locations.
3. Modify the paths in `recipes/Conv-Tasnet/data/*.csv` to point to the correct data locations.
4. Run the following script to generate the training data:

```bash
   cd recipes/Conv-Tasnet/data
   bash make_data.sh
```

# Training
For Conv-TasNet:
```shell
cd Conv-Tasnet/separation/
python train.py hparams/convtasnet_4mix.yaml
```

# Inference
For Conv-TasNet:
```shell
cd Conv-Tasnet/separation/
python train.py hparams/convtasnet_4mix.yaml --test_only
```


# Pretrained Model

For a quick test, you can download our pretrained model from Hugging Face and place it unde `Conv-Tasnet/separation/results`.

👉 [swc2/Voice-Separation](https://huggingface.co/swc2/Voice-Separation)


<!-- # Results
Below is a summary of the average separation performance for two models in XXX dataset.
Metrics include Scale-Invariant Signal-to-Noise Ratio (SI-SNR) and Signal-to-Distortion Ratio (SDR), along with their respective improvements (i).

| Model       | SI-SNR (dB) | SI-SNRi (dB) | SDR (dB) | SDRi (dB) |
| ----------- | ----------- | ------------ | -------- | --------- |
| SepFormer   |    xxx   |     xxx     |  xxx   |    xxx   |
| Conv-TasNet |    xxx   |     xxx     |  xxx   |    xxx   | -->


# **Citing**
```bibtex
@misc{speechbrain,
  title={{SpeechBrain}: A General-Purpose Speech Toolkit},
  author={Mirco Ravanelli and Titouan Parcollet and Peter Plantinga and Aku Rouhe and Samuele Cornell and Loren Lugosch and Cem Subakan and Nauman Dawalatabad and Abdelwahab Heba and Jianyuan Zhong and Ju-Chieh Chou and Sung-Lin Yeh and Szu-Wei Fu and Chien-Feng Liao and Elena Rastorgueva and François Grondin and William Aris and Hwidong Na and Yan Gao and Renato De Mori and Yoshua Bengio},
  year={2021},
  eprint={2106.04624},
  archivePrefix={arXiv},
  primaryClass={eess.AS},
  note={arXiv:2106.04624}
}


@misc{luo2019convtasnet,
  title={Conv-TasNet: Surpassing ideal time–frequency magnitude masking for speech separation},
  author={Luo, Yi and Mesgarani, Nima},
  journal={IEEE/ACM Transactions on Audio, Speech, and Language Processing},
  volume={27},
  number={8},
  pages={1256--1266},
  year={2019}
}

```
