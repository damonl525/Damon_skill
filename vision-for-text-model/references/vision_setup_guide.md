# 👁️ WispTerm Agent 视觉能力安装指南

> **目标**：给 WispTerm Agent 装上"眼睛"，让它能分析你发的截图、照片、图表等。
> **原理**：Python 脚本 + 智谱 GLM-4V-Flash 免费视觉 API（可扩展其他模型）。
> **前提**：本机已安装 Python 3.10+ 和 uv 包管理器。

---

## 1. 检查前置环境

打开终端，确认以下命令都能输出版本号：

```powershell
python --version   # 应 >= 3.10
uv --version       # 应有版本输出
```

如果没有 uv，执行以下命令安装：

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

## 2. 获取智谱 API Key（免费）

1. 打开 https://open.bigmodel.cn/
2. 注册 / 登录
3. 进入 API Keys 页面，点击创建新 Key，复制保存

> `glm-4v-flash` 是智谱提供的免费视觉模型，支持图片理解和描述。

---

## 3. 部署脚本

在 WispTerm 的工作目录下，创建文件 `gemini_vision.py`，内容如下：

```python
# -*- coding: utf-8 -*-
"""Vision Tool - Zhipu GLM-4V-Flash with extensible multi-engine support"""

import sys, json, base64, urllib.request, pathlib

# ---- API Keys (替换成你自己的 Key) ----
ZHIPU_KEY = "你的-智谱-Key"
ZHIPU_MODEL = "glm-4v-flash"

# ==== 如需添加其他模型，见文档末尾"扩展其他模型"章节 ====

MIME_MAP = {
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".webp": "image/webp", ".gif": "image/gif", ".bmp": "image/bmp"
}

def _b64(path: pathlib.Path) -> str:
    return base64.b64encode(path.read_bytes()).decode()

def _mime(path: pathlib.Path) -> str:
    return MIME_MAP.get(path.suffix.lower(), "image/png")

# ---- 智谱 GLM-4V-Flash (默认引擎) ----
def _zhipu(path: pathlib.Path, prompt: str) -> str:
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    body = json.dumps({
        "model": ZHIPU_MODEL,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:{_mime(path)};base64,{_b64(path)}"}},
                {"type": "text", "text": prompt}
            ]
        }]
    }).encode()
    req = urllib.request.Request(url, data=body, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ZHIPU_KEY}"
    })
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read())["choices"][0]["message"]["content"]

# ---- 引擎注册表 (按顺序尝试，可自行增删) ----
ENGINES = [
    ("Zhipu", _zhipu),
    # 添加新引擎时取消注释并补充函数：
    # ("NewEngine", _new_engine_fn),
]

# ---- Public API ----
def see(image_path: str, prompt: str = "请详细描述这张图片的内容") -> str:
    """分析图片，返回文字描述。自动按 ENGINES 顺序尝试，失败则切换下一个。"""
    path = pathlib.Path(image_path)
    if not path.exists():
        return f"[ERROR] File not found: {image_path}"

    for name, fn in ENGINES:
        try:
            result = fn(path, prompt)
            return f"[{name}] {result}"
        except Exception as e:
            err_msg = str(e)[:200]
            print(f"[WARN] {name} failed: {err_msg}", file=sys.stderr)
            continue
    return "[ERROR] All vision engines failed"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python gemini_vision.py <image_path> [prompt]")
    else:
        p = sys.argv[2] if len(sys.argv) > 2 else "请详细描述这张图片的内容"
        print(see(sys.argv[1], p))
```

---

## 4. 验证安装

### 4.1 截一张测试图

```powershell
Add-Type -AssemblyName System.Windows.Forms
$w = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width
$h = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Height
$bmp = New-Object System.Drawing.Bitmap($w, $h)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.CopyFromScreen(0, 0, 0, 0, $bmp.Size)
$g.Dispose()
$bmp.Save("$pwd\test_screenshot.png", [System.Drawing.Imaging.ImageFormat]::Png)
$bmp.Dispose()
Write-Output "test_screenshot.png saved"
```

### 4.2 让 Agent 看图

```powershell
uv run python gemini_vision.py test_screenshot.png "截图里有什么？"
```

预期输出类似：

```
[Zhipu] 截图显示了一个 Windows 桌面，底部有任务栏……
```

---

## 5. Agent 使用方式

安装完成后，Agent 可通过以下方式调用视觉能力：

| 方式 | 命令 |
|------|------|
| CLI 直接调 | `uv run python gemini_vision.py <图片路径> [问题]` |
| 截屏分析 | 先截屏保存，再调 gemini_vision.py |
| Python import | `from gemini_vision import see; print(see("photo.jpg"))` |

---

## 6. 故障排查

| 症状 | 可能原因 | 解决 |
|------|---------|------|
| `[WARN] Zhipu failed` | Key 无效或额度不足 | 登录智谱控制台检查 Key 和余额 |
| `[ERROR] All engines failed` | 所有引擎都不可用 | 检查网络，确认 Key 正确 |
| `File not found` | 图片路径错误 | 使用绝对路径 |
| `urllib.error.URLError` | 网络不通 | 检查代理/VPN/防火墙 |

---

## 7. 🔌 扩展其他视觉模型

脚本的 `ENGINES` 列表支持接入任意数量的视觉 API，按顺序自动 fallback。
以下是一些免费可用的视觉模型，按需添加：

### A. 通义千问 qwen-vl-plus（阿里云）

- 免费额度：200 万 Token/月
- 获取 Key：https://dashscope.console.aliyun.com/

```python
QWEN_KEY = "你的-通义千问-Key"
QWEN_MODEL = "qwen-vl-plus"

def _qwen(path, prompt):
    url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
    body = json.dumps({
        "model": QWEN_MODEL,
        "messages": [{"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": f"data:{_mime(path)};base64,{_b64(path)}"}},
            {"type": "text", "text": prompt}
        ]}]
    }).encode()
    req = urllib.request.Request(url, data=body, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {QWEN_KEY}"
    })
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read())["choices"][0]["message"]["content"]

# 然后在 ENGINES 里加上：
ENGINES = [
    ("Zhipu", _zhipu),
    ("Qwen", _qwen),   # <-- 新增
]
```

### B. 月之暗面 moonshot-v1（Kimi 视觉）

- 免费额度：15 元注册赠送
- 获取 Key：https://platform.moonshot.cn/

```python
MOONSHOT_KEY = "你的-Moonshot-Key"
MOONSHOT_MODEL = "moonshot-v1-8k-vision-preview"

def _moonshot(path, prompt):
    url = "https://api.moonshot.cn/v1/chat/completions"
    body = json.dumps({
        "model": MOONSHOT_MODEL,
        "messages": [{"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": f"data:{_mime(path)};base64,{_b64(path)}"}},
            {"type": "text", "text": prompt}
        ]}]
    }).encode()
    req = urllib.request.Request(url, data=body, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {MOONSHOT_KEY}"
    })
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read())["choices"][0]["message"]["content"]
```

### C. 其他可选

| 模型 | 提供商 | 免费额度 | 说明 |
|------|--------|---------|------|
| `glm-4v-flash` | 智谱 | ✅ 免费 | 当前默认引擎 |
| `qwen-vl-plus` | 阿里通义 | 200万T/月 | 中文理解强 |
| `moonshot-v1-8k-vision` | Kimi | 注册即送 | 长文档+视觉 |
| `gemini-2.0-flash` | Google | 1500次/天 | 网络可能不稳定（国内） |
| `step-1v` | 阶跃星辰 | 注册赠送 | 国产新势力 |

> **添加原则**：写一个 `_xxx(path, prompt)` 函数 → 加入 `ENGINES` 列表 → 完成。顺序即优先级。

---

## 8. 安全提醒

- ⚠️ **不要将 API Key 提交到 Git 或公开分享**
- ⚠️ 图片会上传到对应模型服务商的云端服务器
- 💡 建议定期更换 Key
- 💡 脚本仅依赖 Python 标准库，无第三方依赖

---

> 最后验证时间：2026-06-09
> Python 3.13 / uv / glm-4v-flash