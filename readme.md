# A Discord Bot with some AI related tools

## Prerequisites (not mandatory)

[Automatic1111 SD WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui) OR: [lllyasviel SD WebUI FORGE](https://github.com/lllyasviel/stable-diffusion-webui-forge) for image generation
(TBD) [Koboldcpp](https://github.com/LostRuins/koboldcpp) if you want text generation using GGUF/GGML models (TabbyAPI support for exlv2 is a consideration)

WaifuDiffusion tagger or similar with their csv tag file (see Commands / Features /tagimg)

### Commands / Features

<details>
    <summary>/genimg</summary>

Generates an image using the connected SD WebUI
Options:

- `prompt` (required)
- `neg_prompt`
- `orientation` (Portrait/Landscape)
- `dimensions` (`1152x896 (9:7)` `1216x832 (19:13)` `1344x768 (7:4)` `1536x640 (12:5)`, switches Width/Height depending on selected Orientation)

</details>


<details>
    <summary>/tagimg OR as message command (context menu)</summary>

Tags an image (first image of the message if context menu is used) using a locally stored WaifuDiffusion model by [SmilingWolf](https://huggingface.co/SmilingWolf) (others probably work, untested)
WIP otherwise
The models I personally use are:
- [wd-eva02-large-tagger-v3](https://huggingface.co/SmilingWolf/wd-eva02-large-tagger-v3) (large, slower)
- [wd-convnext-tagger-v3](https://huggingface.co/SmilingWolf/wd-convnext-tagger-v3) (small, faster)

</details>

<details>
    <summary>/reload</summary>

reloads cogs to use updated code if there is any

</details>


#### Instructions: WIP

note: requirements.txt is not finished and bot token and other things will be moved to a config file

- input bot api token at the bottom of main.py
- install required pip packages
```pip install -r requirements.txt```

#### Todo:

- [ ] make requirements.txt actually useful
- [ ] make tagimg command better
- [ ] add more options to genimg
- [ ] add text chat functionality with per channel and message history
- [ ] text chat personal chat mode
- [ ] ephemeral option
