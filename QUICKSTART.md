# Quick Start Guide

## 🚀 Getting Started (Free Setup)

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Setup Free AI (Ollama - 100% Free & Local)

**Option A: Ollama (Recommended - Free & Private)**
1. Download Ollama from https://ollama.ai
2. Install and run:
   ```bash
   ollama run llama2
   ```
3. Keep `use_local_ai: true` in [config.yaml](config.yaml)

**Option B: OpenAI (Free $5 credit for new accounts)**
1. Sign up at https://platform.openai.com
2. Get API key
3. Set `use_local_ai: false` in [config.yaml](config.yaml)
4. Add your API key to [config.yaml](config.yaml)

### Step 3: Configure Instagram (Free)

1. Open [config.yaml](config.yaml)
2. Add your Instagram credentials:
   ```yaml
   instagram:
     enabled: true
     username: "your_username"
     password: "your_password"
   ```

### Step 4: Add Your Videos

Place your video files in the `videos/` folder:
- Supported formats: .mp4, .mov, .avi
- The agent will automatically pick them up

### Step 5: Configure Schedule

Edit [schedule_config.yaml](schedule_config.yaml) to set when videos should be posted:

```yaml
schedule:
  - days: ["monday", "wednesday", "friday"]
    time: "10:00"
    platform: "instagram"
```

### Step 6: Test Your Setup

```bash
python main.py --test
```

This will verify:
- ✓ AI connection (Ollama or OpenAI)
- ✓ Instagram login
- ✓ Videos in queue
- ✓ Caption generation

### Step 7: Run the Agent

**Run with scheduler:**
```bash
python main.py
```

**Upload a video now:**
```bash
python main.py --upload-now
```

**Upload specific video:**
```bash
python main.py --upload-now --video "videos/my_video.mp4"
```

## 📱 Platform Setup (All Free)

### Instagram
- ✓ Free to use
- ✓ No API application needed
- Uses `instagrapi` library
- Just provide username/password

### TikTok (Optional)
- Requires API approval from TikTok
- Not implemented yet (coming soon)

### YouTube (Optional)
- Requires Google Cloud Console setup
- Free API quota: 10,000 units/day
- Requires OAuth2 setup

## 🎯 Usage Examples

### Test caption generation:
```bash
python -c "from modules import CaptionGenerator; g = CaptionGenerator(); print(g.generate_full_post('test.mp4'))"
```

### Check video queue:
```bash
python -c "from modules import VideoScheduler; s = VideoScheduler(); print(f'Videos: {len(s.video_queue)}')"
```

### Manual upload:
```python
from modules import SocialMediaAgent

agent = SocialMediaAgent()
agent.upload_now(platform='instagram', video_path='videos/my_video.mp4')
```

## 🆘 Troubleshooting

### "No module named 'ollama'"
```bash
pip install ollama
# Then run: ollama run llama2
```

### "Instagram login failed"
- Check username/password in [config.yaml](config.yaml)
- Try logging in manually on Instagram website first
- Instagram may require 2FA verification

### "No videos in queue"
- Add video files to `videos/` folder
- Supported formats: .mp4, .mov, .avi

### Video too large
- Agent automatically compresses videos > 100MB
- Adjust `max_size_mb` in [config.yaml](config.yaml)

## 💰 Cost Breakdown (FREE!)

| Service | Cost | Notes |
|---------|------|-------|
| Python | Free | Open source |
| Ollama | Free | Run AI locally |
| Instagram API | Free | No official API needed |
| VS Code | Free | Your IDE |
| **TOTAL** | **$0** | 100% Free! |

## 🎓 Next Steps

1. ✓ Test your setup: `python main.py --test`
2. ✓ Add videos to `videos/` folder
3. ✓ Configure your schedule in [schedule_config.yaml](schedule_config.yaml)
4. ✓ Run the agent: `python main.py`
5. ✓ Sit back and let it post automatically! 🚀

## 📖 Full Documentation

See [README.md](README.md) for complete documentation.
