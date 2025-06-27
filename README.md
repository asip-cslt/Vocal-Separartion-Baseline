# Universal-Sound-Separation-Baseline

A 4-mix universal sound (speech and instrument) separation baseline based on [SpeechBrain](https://github.com/speechbrain/speechbrain) (using SepFormer & Conv-TasNet).


# Environment Setup
```shell
conda create -n sb_sep python=3.11 -y
conda activate sb_sep
pip install -r requirements.txt
```

# Data Preparation
## Data Usage
To simulate the scenario of competition data, we used three open-source datasets to construct our training and validation sets.

We use [AISHELL-1](https://openslr.org/33/) as the speech dataset, [MUSIC](https://github.com/roudimit/MUSIC_dataset) as the instrument dataset, and [RIRs](https://www.openslr.org/28/) dataset to simulate room reverberation.

All audio data needs to be converted to **pcm_s16le** format and resampled to **16kHz**.

## Data Generation
Firstly, you need to replace the file paths in the data lists with your data path.

Then, execute the data generation script:
```shell
bash data/make_data.sh
```

# Training
For Conv-TasNet:
```shell
cd Conv-Tasnet/separation/
bash example.sh
```

For SepFormer:
```shell
cd Sepformer/separation/
bash example.sh
```

# Pretrain Model

You can download our pretrained model from Hugging Face:

👉 [swc2/Voice-Separation](https://huggingface.co/swc2/Voice-Separation)


<!-- # Results
Below is a summary of the average separation performance for two models in XXX dataset.
Metrics include Scale-Invariant Signal-to-Noise Ratio (SI-SNR) and Signal-to-Distortion Ratio (SDR), along with their respective improvements (i).

| Model       | SI-SNR (dB) | SI-SNRi (dB) | SDR (dB) | SDRi (dB) |
| ----------- | ----------- | ------------ | -------- | --------- |
| SepFormer   |    −20.60   |     5.49     |  −4.60   |    4.62   |
| Conv-TasNet |    −20.22   |     5.88     |  −4.17   |    5.06   | -->


# **Citing**
```bibtex
@misc{luo2019convtasnet,
  title={Conv-TasNet: Surpassing ideal time–frequency magnitude masking for speech separation},
  author={Luo, Yi and Mesgarani, Nima},
  journal={IEEE/ACM Transactions on Audio, Speech, and Language Processing},
  volume={27},
  number={8},
  pages={1256--1266},
  year={2019}
}

@inproceedings{subakan2021attention,
  title={Attention is all you need in speech separation},
  author={Subakan, Cem and Ravanelli, Mirco and Cornell, Samuele and Zanetti, Eleftherios and Collobert, Ronan and Bengio, Yoshua},
  booktitle={ICASSP 2021 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)},
  year={2021},
  pages={31--35}
}
```
