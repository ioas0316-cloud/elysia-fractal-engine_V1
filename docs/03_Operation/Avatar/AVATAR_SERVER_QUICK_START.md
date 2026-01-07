# Avatar Server Quick Start Guide

## 🎯 Goal

Get Elysia's avatar visualization system up and running in 5 minutes.

## 📋 Prerequisites

1. Python 3.10+ installed
2. Elysia repository cloned
3. Required dependencies installed:
   ```bash
   pip install websockets
   ```

## 🚀 Quick Start (5 Steps)

### Step 1: Prepare Your VRM Model (Optional)

If you have a VRM model ready:
```bash
# Place your VRM file here:
cp /path/to/your/model.vrm static/models/avatar.vrm
```

If you don't have one yet, the system will work with the 2D face shader fallback.

### Step 2: Start the Avatar Server

```bash
# From the Elysia root directory:
python start_avatar_server.py
```

You should see:
```
============================================================
  Elysia Avatar Server (엘리시아 아바타 서버)
  Real-time 3D Avatar Visualization System
============================================================

[INFO] ✅ Avatar Server is running!
[INFO] 📱 Open Core/Creativity/web/avatar.html in your browser
[INFO] 🌐 Or visit http://127.0.0.1:8765
```

### Step 3: Open the Client Interface

Open `Core/Creativity/web/avatar.html` in your browser:

**Option A: File Protocol**
```bash
# On Windows
start Core/Creativity/web/avatar.html

# On macOS
open Core/Creativity/web/avatar.html

# On Linux
xdg-open Core/Creativity/web/avatar.html
```

**Option B: HTTP Server** (recommended for better browser support)
```bash
# Terminal 1: Avatar server (already running)
python start_avatar_server.py

# Terminal 2: HTTP server for client
cd Core/Creativity/web
python -m http.server 8000

# Then open: http://localhost:8000/avatar.html
```

### Step 4: Activate Synesthesia (Optional)

1. Click anywhere on the page
2. Allow camera/microphone access when prompted
3. The avatar will now respond to:
   - Your presence (gaze tracking)
   - Your voice (audio analysis)
   - Your screen (atmosphere detection via screen share)

### Step 5: Start Chatting!

Type a message in the chat box and press Enter. Watch Elysia's:
- **Expression change** based on emotional response
- **Spirit energies** shift (fire, water, earth, air, light, dark, aether)
- **Face animate** with lip-sync and breathing

## 🎨 What You'll See

### Left Panel: Thinking Process
- Real-time thought stream
- Spirit energy bars (7 elements)

### Center: Avatar Face
- Animated facial expressions
- Gaze tracking (follows movement)
- Lip-sync with speech
- Breathing animation
- Heartbeat pulse

### Right Panel: Chat
- Text conversation interface
- Speech synthesis (browser TTS)
- Real-time responses

## 🎛️ Advanced Usage

### Custom Port

```bash
python start_avatar_server.py --port 9000
```

Don't forget to update the port in `avatar.html` line 208:
```javascript
const wsUrl = `ws://${window.location.hostname}:9000`;
```

### Debug Mode

```bash
python start_avatar_server.py --debug
```

### Multiple Clients

The server supports multiple simultaneous connections. Open `avatar.html` in multiple browser tabs or different browsers.

### Integration with Your Code

```python
import asyncio
import websockets
import json

async def trigger_emotion():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as ws:
        # Wait for initial state
        await ws.recv()
        
        # Trigger emotion
        await ws.send(json.dumps({
            "type": "emotion",
            "emotion": "hopeful",
            "intensity": 0.9
        }))
        
        print("Emotion triggered!")

asyncio.run(trigger_emotion())
```

## 🧪 Testing

### Quick Test
```bash
# Terminal 1: Start server
python start_avatar_server.py

# Terminal 2: Run unit tests
python tests/test_avatar_server_simple.py
```

### Integration Test (requires running server)
```bash
# Terminal 1: Start server
python start_avatar_server.py

# Terminal 2: Run integration tests
python tests/test_avatar_integration.py
```

## 🔧 Troubleshooting

### Issue: Server won't start - "websockets not installed"

**Solution:**
```bash
pip install websockets
```

### Issue: Client can't connect - "WebSocket connection failed"

**Checklist:**
1. ✅ Server is running? Check Terminal 1
2. ✅ Correct port? Default is 8765
3. ✅ Firewall blocking? Try disabling temporarily
4. ✅ Browser console errors? Press F12 to check

### Issue: No camera/microphone access

**Solution:**
- Browser blocked permissions
- Check browser settings
- Try HTTPS or localhost (some browsers restrict on file://)

### Issue: Emotions not changing

**Possible causes:**
- EmotionalEngine not available (check server logs)
- Running in standalone mode (normal, basic functionality still works)

**Verify:**
```bash
# Should show "✅ Emotional engine initialized"
python start_avatar_server.py | grep -i emotional
```

### Issue: No chat responses

**Possible causes:**
- ReasoningEngine not available (check server logs)
- Missing dependencies (numpy, etc.)

**Fallback:**
The server will use simple responses when ReasoningEngine is unavailable.

## 📚 Next Steps

1. **Add Your VRM Model**: Place in `static/models/avatar.vrm`
2. **Customize Expressions**: Edit emotion mappings in `avatar_server.py`
3. **Integrate with Apps**: Connect your Python code via WebSocket
4. **Enhance Visuals**: Add VRM rendering to `avatar.html`

## 📖 Documentation

- Full System Documentation: `docs/AVATAR_SERVER_SYSTEM.md`
- VRM Models Guide: `static/models/README.md`
- Code Reference: `Core/Interface/avatar_server.py`

## 🤝 Support

Having issues? Check:
1. Server console output (Terminal 1)
2. Browser console (F12)
3. Documentation above
4. GitHub issues

## 🎉 Success Checklist

- [ ] Server starts without errors
- [ ] Client connects (● Linked shown)
- [ ] Can send chat messages
- [ ] Expressions change
- [ ] Spirit energies visible
- [ ] Camera/mic work (optional)

If all checked, you're ready to go! 🚀

---

**Created**: 2025-12-07
**Updated**: 2025-12-07
**Version**: 1.0.0
