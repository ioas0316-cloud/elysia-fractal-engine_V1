# 🔌 How to Activate Sovereign Mode (Local GPU Setup)

## ❓ "Did you install AI on my computer?"

**No.**
Elysia has installed the **Driver (local_bridge.py)**, but she needs you to provide the **Engine (Stable Diffusion)**.
A full AI model is massive (10GB+) and requires specific installation tailored to your graphics card. We did not touch your system files.

## 🛠️ The Architecture

- **Elysia (The Artist)**: Sends commands like `"Draw a silver-haired girl"`.
- **Local Bridge (The Cable)**: Transmits this command to port `7860`.
- **Stable Diffusion (The Brush)**: **[MISSING]** This is what you must install.

---

## 🚀 Setup Instructions

To enable Elysia to draw uncensored images on your PC, follow these steps:

### 1. Install Stable Diffusion WebUI (Automatic1111)

This is the standard software for running AI models locally.

1. Download and install **[Automatic1111](https://github.com/AUTOMATIC1111/stable-diffusion-webui)**.
2. Follow their installation guide for Windows (requires Python 3.10 and Git).

### 2. Enable the API

Elysia talks to the software via code, so the API must be on.

1. Open your `webui-user.bat` file (right-click -> Edit).
2. Find the line `set COMMANDLINE_ARGS=`.
3. Add `--api` to it.
    - Example: `set COMMANDLINE_ARGS=--api --xformers`
4. Save and run `webui-user.bat`.

### 3. Verify Connection

1. Ensure the console says: `Running on local URL:  http://127.0.0.1:7860`
2. Tell Elysia: **"I have connected the engine."**

### 4. Unleash Sovereignty

Once connected, Elysia's `local_bridge.py` will no longer save JSON files.
It will generate **Real, Uncensored Images** directly to `c:\Elysia\outputs\bridge\` folder.

---

## 🎨 Note on Models

You can download any model (Anime, Realistic, Artistic) from Civitai and put it in your Stable Diffusion `models` folder. Elysia will use **whatever model you have loaded**, essentially adopting that art style instantly.
