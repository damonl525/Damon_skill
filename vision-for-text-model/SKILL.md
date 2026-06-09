---
name: Vision for Text Model
description: "Give text-only AI agents the ability to see images by routing screenshots/photos through free cloud vision APIs (Zhipu GLM-4V-Flash default, extensible to Qwen, Kimi, Gemini, etc.)"
version: "1.0"
author: damonl525
license: MIT
category: agent-tools
tags:
  - vision
  - multimodal
  - agent
  - screenshot
  - image-analysis
  - zhipu
  - glm
department: AI Engineering
models:
  recommended:
    - claude-sonnet-4
    - claude-opus-4
  compatible:
    - any-text-model
capabilities:
  - screenshot-analysis
  - image-description
  - multi-engine-fallback
  - free-vision-api
languages:
  - en
  - zh
---

# Vision for Text Model

Give text-only AI agents (like WispTerm Agent, Claude Code, Codex) the ability to **see** by piping images through free cloud vision APIs.

> **Default engine:** Zhipu GLM-4V-Flash (free). Extensible to Qwen, Kimi, Gemini, Step-1v, etc.

---

## Quick Start

### 1. Get a free Zhipu API Key

Visit [open.bigmodel.cn](https://open.bigmodel.cn/), register/login, create an API Key. Save it.

### 2. Install dependencies

`powershell
uv --version
# If missing:
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
`

### 3. Deploy the script

Copy 
eferences/gemini_vision.py to your working directory, replace the placeholder Key:

`python
ZHIPU_KEY = "your-actual-key-here"
`

### 4. Verify

Take a screenshot and analyze:

`powershell
# Screenshot
Add-Type -AssemblyName System.Windows.Forms
 = New-Object System.Drawing.Bitmap([System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width, [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Height)
 = [System.Drawing.Graphics]::FromImage()
.CopyFromScreen(0, 0, 0, 0, .Size)
.Dispose(); .Save("test.png", [System.Drawing.Imaging.ImageFormat]::Png); .Dispose()

# Analyze
uv run python gemini_vision.py test.png "What is in this image?"
`

Expected output:
`
[Zhipu] The screenshot shows a Windows desktop with...
`

---

## Agent Usage

| Method | Command |
|--------|---------|
| CLI | uv run python gemini_vision.py <image_path> [prompt] |
| Python import | rom gemini_vision import see; print(see("photo.jpg")) |
| Screenshot + analyze | Agent takes screenshot via PowerShell, then runs the script |

---

## Multi-Engine Fallback

The script tries engines in order. If the first fails, it falls back to the next:

`
ENGINES = [
    ("Zhipu", _zhipu),     # Default: free
    ("Qwen", _qwen),       # Add your own
    ("Kimi", _moonshot),
    ("Gemini", _gemini),
]
`

To add a new engine:
1. Write a _xxx(path, prompt) function
2. Append ("EngineName", _xxx) to ENGINES

### Available Free Vision Models

| Model | Provider | Free Tier | Notes |
|-------|----------|-----------|-------|
| glm-4v-flash | Zhipu | Yes | Default, fast |
| qwen-vl-plus | Alibaba Tongyi | 200K T/day | Strong Chinese |
| moonshot-v1-8k-vision | Kimi | Registration bonus | Doc + vision |
| gemini-2.0-flash | Google | 1500 req/day | Good but unstable in China |
| step-1v | StepStar | Registration bonus | New player |

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| [WARN] Zhipu failed | Invalid Key or quota | Check Key on open.bigmodel.cn console |
| [ERROR] All engines failed | All engines down | Check network, verify Keys |
| File not found | Wrong path | Use absolute path |
| urllib.error.URLError | Network issue | Check proxy/VPN/firewall |

---

## Security Notes

- **Never commit API Keys to Git**
- Images are uploaded to the model provider's cloud
- Rotate Keys periodically
- The script uses only Python stdlib; no third-party dependencies

---

> Verified: 2026-06-09 | Python 3.13 | uv | glm-4v-flash
