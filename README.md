# Image Caption Speed Test using Visual Language Models

#### Test the speed of captioning an image using the latest Visual Language Models (VLMs): OpenAI [GPT-V](https://platform.openai.com/docs/guides/vision), and open-source models like BLIP-2, LLaVA-13B, BakLLaVA, InstructBLIP, CogVLM, etc. available on [Replicate](https://www.replicate.com/explore).

## Installation

```bash
pip install -r requirements.txt
```

Create a `.env` file based on the example `.env.example` file.

## Usage

### For OpenAI

```bash
python openai_caption.py ["IMAGE_URL"] ["PROMPT"]
```

```IMAGE_URL``` is the URL of the image you want to caption. [(Default image)](https://replicate.delivery/pbxt/IqiPBXiSDTHbjN61b809YMPWCB4OBkxXPGmqEiKA7K1pyErB/yud.png)

Default ```PROMPT``` is ```"describe this image"```. But you can add an alternative prompt here if you want it to guide the captioning.

### For pen-source models

```bash
python main.py ["MODEL_ID"] ["IMAGE_URL"] ["PROMPT"]
```

Default ```MODEL_ID``` is [```andreasjansson/blip-2```](https://replicate.com/andreasjansson/blip-2). You can use here any other visual language model available on Replicate. Each model takes in its own unique set of inputs, so the code will recognize the model and correctly construct the right inputs for it.

Right now, the code recognizes how to construct the inputs the following models:
* [```andreasjansson/blip-2```](https://replicate.com/andreasjansson/blip-2)
* [```yorickvp/llava-13b```](https://replicate.com/yorickvp/llava-13b)
* [```gfodor/instructblip```](https://replicate.com/gfodor/instructblip)
* [```lucataco/bakllava```](https://replicate.com/lucataco/bakllava)
* [```naklecha/cogvlm```](https://replicate.com/naklecha/cogvlm)
* [```cjwbw/cogvlm```](https://replicate.com/cjwbw/cogvlm)

## Contributing

Pull requests are welcome! Made with ❤️ by the folks at [Camcorder AI](https://www.github.com/camcorderai).
