from pathlib import Path
import numpy as np
import paddle
import yaml
from yacs.config import CfgNode
from paddlespeech.t2s.models.fastspeech2 import FastSpeech2
from paddlespeech.t2s.models.fastspeech2 import FastSpeech2Inference
from paddlespeech.t2s.modules.normalizer import ZScore
# examples/fastspeech2/baker/frontend.py
from zh_frontend import Frontend

# load the pretrained model
checkpoint_dir = Path("fastspeech2_nosil_baker_ckpt_0.4")
with open(checkpoint_dir / "phone_id_map.txt", "r") as f:
    phn_id = [line.strip().split() for line in f.readlines()]
vocab_size = len(phn_id)
with open(checkpoint_dir / "default.yaml") as f:
    fastspeech2_config = CfgNode(yaml.safe_load(f))
odim = fastspeech2_config.n_mels
model = FastSpeech2(
    idim=vocab_size, odim=odim, **fastspeech2_config["model"])
model.set_state_dict(
    paddle.load(args.fastspeech2_checkpoint)["main_params"])
model.eval()

# load stats file
stat = np.load(checkpoint_dir / "speech_stats.npy")
mu, std = stat
mu = paddle.to_tensor(mu)
std = paddle.to_tensor(std)
fastspeech2_normalizer = ZScore(mu, std)

# construct a prediction object
fastspeech2_inference = FastSpeech2Inference(fastspeech2_normalizer, model)

# load Chinese Frontend
frontend = Frontend(checkpoint_dir / "phone_id_map.txt")

# text to spectrogram
sentence = "你好吗？"
input_ids = frontend.get_input_ids(sentence, merge_sentences=True)
phone_ids = input_ids["phone_ids"]
flags = 0
# The output of Chinese text frontend is segmented
for part_phone_ids in phone_ids:
    with paddle.no_grad():
        temp_mel = fastspeech2_inference(part_phone_ids)
        if flags == 0:
            mel = temp_mel
            flags = 1
        else:
            mel = paddle.concat([mel, temp_mel])