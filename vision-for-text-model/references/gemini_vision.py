# -*- coding: utf-8 -*-
"""Vision Tool - GLM-4V-Flash with extensible multi-engine fallback"""

import sys, json, base64, urllib.request, pathlib

# ---- API Keys ----
ZHIPU_KEY = "你的-智谱-Key"
ZHIPU_MODEL = "glm-4v-flash"

MIME_MAP = {
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".webp": "image/webp", ".gif": "image/gif", ".bmp": "image/bmp"
}

def _b64(path: pathlib.Path) -> str:
    return base64.b64encode(path.read_bytes()).decode()

def _mime(path: pathlib.Path) -> str:
    return MIME_MAP.get(path.suffix.lower(), "image/png")

# ---- Zhipu GLM-4V-Flash (primary) ----
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

# ---- Engine registry (tried in order) ----
ENGINES = [
    ("Zhipu", _zhipu),
]

# ---- Public ----
def see(image_path: str, prompt: str = "请详细描述这张图片的内容") -> str:
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