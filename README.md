# mfa-interspeech2026
Scripts for "Montreal Forced Aligner and the state of speech-to-text alignment in 2026" to be presented at Interspeech 2026

Preprint of paper available on [here](https://arxiv.org/pdf/2606.18466)

## Versions

* MFA: [3.4](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner/releases/tag/v3.4.0)
  * Benchmarks were done with in development version of 3.4 in January 2026
* MAUS: [WebMAUS](https://clarin.phonetik.uni-muenchen.de/BASWebServices/interface/WebMAUSBasic), accessed January 2026
* MAPS: [v0.5.0](https://github.com/MasonPhonLab/MAPS/releases/tag/v0.5.0)
  * Not reported in the paper is the use of variants implemented in 0.5.0, which had similar performance on TIMIT, but much worse performance on Buckeye, so the original numbers were kept as the benchmark
* Korean Forced Aligner: [Web portal](http://210.125.93.241:5010), accessed January 2026
* WhisperX: [3.4.2](https://github.com/m-bain/whisperX/releases/tag/v3.4.2)
* Wav2Vec2: [torchaudio 2.8.0](https://github.com/pytorch/audio/releases/tag/v2.8.0)
* Nemo Forced Aligner: [12251c3](https://github.com/NVIDIA-NeMo/Speech/tree/12251c3d396a3813fd9346a604f16b505a35c7b9)
* Julius: [1604011](https://github.com/julius-speech/julius/tree/1604011abafa2751181767f785e9aa4740743c65)
  * Adapted from [pyJuliusAlign](https://github.com/timmahrt/pyJuliusAlign)
* Bournemouth Forced Aligner: [0.1.7](https://github.com/tabahi/bournemouth-forced-aligner/releases/tag/v0.1.7)


## Timing performance 

Incomplete, but historical notes

### Timing notes

* Korean forced aligner
  * Upload and processing of Seoul Corpus files:
    * Total time: ~6 hours
    * initial s01 time: 11:43
      * Final s20 time: 15:04
    * initial s21 time: 16:15
      * Final s22 time: 16:39
    * initial s23 time: 10:27
      * Final s40 time: 13:33
