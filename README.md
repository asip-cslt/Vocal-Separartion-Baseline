# Vocal-Separation-Baseline

A 4-mix vocal separation baseline based on [SpeechBrain](https://github.com/speechbrain/speechbrain) (using SepFormer & Conv-TasNet).

# Results
Below is a summary of the average separation performance for two models in XXX dataset.
Metrics include Scale-Invariant Signal-to-Noise Ratio (SI-SNR) and Signal-to-Distortion Ratio (SDR), along with their respective improvements (i).

| Model     | SI-SNR (dB) | SI-SNRi (dB) | SDR (dB) | SDRi (dB) |
| --------- | ----------- | ------------ | -------- | --------- |
| SepFormer |    −20.60   |     5.49     |  −4.60   |    4.62   |
| TasNet    |    −20.22   |     5.88     |  −4.17   |    5.06   |