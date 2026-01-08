# Updated System: 4 Uploads Per Day 🚀

## New Configuration

✅ **4 uploads per day** at:
- 9:00 AM
- 12:00 PM (Noon)
- 6:00 PM
- 11:00 PM

✅ **Organ 1.mov uploads EVERY DAY** (always at 9am)

✅ **Other videos rotate** throughout the week

## Today's Schedule (Thursday)
```
09:00 AM - Organ 1.mov
12:00 PM - Charlie Brown.mov
06:00 PM - Chihiro.mov
11:00 PM - Clair De Lune.MP4
```

## Full Weekly Schedule

### Monday
- 09:00 - Organ 1.mov
- 12:00 - Addio.MOV
- 18:00 - Charlie Brown.mov
- 23:00 - Chihiro.mov

### Tuesday
- 09:00 - Organ 1.mov
- 12:00 - Clair De Lune.MP4
- 18:00 - Fantasy.MP4
- 23:00 - Howls Moving Castle.MP4

### Wednesday
- 09:00 - Organ 1.mov
- 12:00 - Pixies.MOV
- 18:00 - Succession.mov
- 23:00 - Addio.MOV

### Thursday
- 09:00 - Organ 1.mov
- 12:00 - Charlie Brown.mov
- 18:00 - Chihiro.mov
- 23:00 - Clair De Lune.MP4

### Friday
- 09:00 - Organ 1.mov
- 12:00 - Fantasy.MP4
- 18:00 - Howls Moving Castle.MP4
- 23:00 - Pixies.MOV

### Saturday
- 09:00 - Organ 1.mov
- 12:00 - Succession.mov
- 18:00 - Addio.MOV
- 23:00 - Charlie Brown.mov

### Sunday
- 09:00 - Organ 1.mov
- 12:00 - Chihiro.mov
- 18:00 - Clair De Lune.MP4
- 23:00 - Fantasy.MP4

## Commands

### Start Automatic Scheduler
Runs in background and uploads 4 videos per day automatically:
```bash
.venv/bin/python main.py schedule
```

### Upload All 4 Videos for Today Now
```bash
.venv/bin/python main.py upload
```

### Upload Specific Time Slot
```bash
# Upload 9am video
.venv/bin/python main.py upload --slot 0

# Upload 12pm video
.venv/bin/python main.py upload --slot 1

# Upload 6pm video
.venv/bin/python main.py upload --slot 2

# Upload 11pm video
.venv/bin/python main.py upload --slot 3
```

### Upload Any Specific Video
```bash
.venv/bin/python main.py upload --video "Organ 1.mov"
```

### Check Status
```bash
.venv/bin/python main.py status
```

## Before Running

1. **Enable Instagram** in [config.yaml](config.yaml):
```yaml
instagram:
  enabled: true
  username: "your_username"
  password: "your_password"
```

2. **Test the schedule**:
```bash
.venv/bin/python main.py status
```

3. **Start the scheduler**:
```bash
.venv/bin/python main.py schedule
```

## Caption Rotation

Each video still has 3 unique captions that rotate:
- 1st upload: Caption #1
- 2nd upload: Caption #2
- 3rd upload: Caption #3
- 4th upload: Back to Caption #1

Since you're uploading 4x/day, **Organ 1.mov will cycle through its 3 captions every 3 days**.

## Customization

Edit [video_config.py](video_config.py):

```python
# Change upload times
UPLOAD_TIMES = ["09:00", "12:00", "18:00", "23:00"]

# Change schedule for any day
DAILY_SCHEDULE = {
    0: ["Organ 1.mov", "Video2", "Video3", "Video4"],  # Monday
    # etc...
}

# Add more captions
VIDEO_CONFIG = {
    "Organ 1.mov": {
        "captions": [
            "Caption 1",
            "Caption 2",
            "Caption 3",
            "Caption 4",  # Add more!
        ]
    }
}
```

## What Changed

- ❌ Single daily upload
- ✅ **4 uploads per day** at different times
- ✅ **Organ 1.mov guaranteed every day** (9am)
- ✅ All other videos rotate throughout the week

Perfect for maximum engagement! 🎵
