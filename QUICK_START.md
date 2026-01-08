# Quick Start Guide 🚀

## Your System is Ready!

Everything has been converted to a hard-coded, daily upload system with rotating captions.

## Current Configuration

✅ **9 videos** configured with 3 captions each  
✅ **Weekly schedule** set (Monday-Sunday)  
✅ **Upload time**: 6:00 PM daily  
✅ **Platform**: Instagram (currently disabled for safety)

## Commands You Need

### Check Status
See which videos have been uploaded and which caption was used last:
```bash
cd /Users/mocho042/Documents/GitHub/SocialMediaAgent
.venv/bin/python main.py status
```

### Upload Today's Video Now
Uploads today's scheduled video immediately:
```bash
.venv/bin/python main.py upload
```

### Upload Specific Video
Upload any video with its next caption:
```bash
.venv/bin/python main.py upload --video "Addio.MOV"
```

### Start Daily Scheduler
Runs in background and uploads automatically at 6 PM every day:
```bash
.venv/bin/python main.py schedule
```
*(Press Ctrl+C to stop the scheduler)*

## Before You Upload

### Enable Instagram
Edit [config.yaml](config.yaml):
```yaml
instagram:
  enabled: true          # Change to true
  username: "your_username"
  password: "your_password"
```

## Your Schedule

| Day | Video |
|-----|-------|
| Monday | Addio.MOV |
| Tuesday | Charlie Brown.mov |
| Wednesday | Chihiro.mov |
| Thursday | Clair De Lune.MP4 |
| Friday | Fantasy.MP4 |
| Saturday | Howls Moving Castle.MP4 |
| Sunday | Organ 1.mov |

## How Caption Rotation Works

**First Upload of Addio.MOV:**
- Uses Caption #1: "Bro is not in carnegie hall 🥀..."

**Second Upload of Addio.MOV:**
- Uses Caption #2: "Just vibing with Einaudi 🎹..."

**Third Upload of Addio.MOV:**
- Uses Caption #3: "When the organ hits different 😮‍💨..."

**Fourth Upload of Addio.MOV:**
- Cycles back to Caption #1

## Customize Everything

All your settings are in [video_config.py](video_config.py):

```python
# Change upload time
UPLOAD_TIME = "14:00"  # 2 PM instead of 6 PM

# Change schedule
DAILY_SCHEDULE = {
    0: "Pixies.MOV",  # Monday
    # etc...
}

# Edit captions
VIDEO_CONFIG = {
    "Addio.MOV": {
        "captions": [
            "Your custom caption here",
            "Another caption",
            "And another"
        ]
    }
}
```

## Tips

- **Test first**: Use `upload` command to test before enabling scheduler
- **Monitor logs**: Check `logs/agent.log` for upload history
- **Track history**: `upload_history.json` shows what caption was used last
- **Add more captions**: The more captions per video, the more variety!

## Files Reference

- **`video_config.py`** - All videos, captions, schedule, settings
- **`config.yaml`** - Platform credentials (Instagram, TikTok, YouTube)
- **`main.py`** - The uploader script
- **`upload_history.json`** - Auto-generated upload tracking

## Next Steps

1. ✅ System is installed and working
2. [ ] Test: `.venv/bin/python main.py status`
3. [ ] Add Instagram credentials to `config.yaml`
4. [ ] Test upload: `.venv/bin/python main.py upload`
5. [ ] Start scheduler: `.venv/bin/python main.py schedule`

Done! Your automated daily uploads are ready. 🎉
