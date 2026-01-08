# Hard-Coded Video Uploader Guide

## Overview
This system uploads videos daily with rotating captions. Everything is hard-coded - no AI generation needed!

## How It Works

### 1. Video Configuration (`video_config.py`)
Each video has multiple captions that rotate with each upload:

```python
VIDEO_CONFIG = {
    "Addio.MOV": {
        "captions": [
            "Caption 1 for this video",
            "Caption 2 for this video",
            "Caption 3 for this video"
        ]
    },
    # ... more videos
}
```

### 2. Weekly Schedule
Videos are scheduled by day of the week:

```python
DAILY_SCHEDULE = {
    0: "Addio.MOV",                    # Monday
    1: "Charlie Brown.mov",            # Tuesday
    2: "Chihiro.mov",                  # Wednesday
    3: "Clair De Lune.MP4",           # Thursday
    4: "Fantasy.MP4",                  # Friday
    5: "Howls Moving Castle.MP4",     # Saturday
    6: "Organ 1.mov",                  # Sunday
}
```

### 3. Caption Rotation
- Each time a video is uploaded, it uses the next caption in its list
- After using all captions, it cycles back to the first one
- Upload history is saved in `upload_history.json`

## Usage

### Start the Daily Scheduler
Uploads the scheduled video automatically at the set time (default 6:00 PM):
```bash
python main.py schedule
```

### Upload Today's Video Now
Upload today's scheduled video immediately:
```bash
python main.py upload
```

### Upload a Specific Video
Upload any video with its next caption:
```bash
python main.py upload --video "Addio.MOV"
```

### Check Status
See upload history and which captions were used:
```bash
python main.py status
```

## Configuration

### Change Upload Time
Edit `video_config.py`:
```python
UPLOAD_TIME = "18:00"  # 6:00 PM (24-hour format)
```

### Change Platform
Edit `video_config.py`:
```python
PLATFORM = "instagram"  # or "tiktok", "youtube"
```

### Add New Videos
1. Add video file to `/videos` folder
2. Add to `VIDEO_CONFIG` in `video_config.py`:
```python
"YourVideo.mp4": {
    "captions": [
        "First caption for this video",
        "Second caption for this video",
        "Third caption for this video"
    ]
}
```
3. Add to `DAILY_SCHEDULE` if you want it on a specific day

### Modify Captions
Just edit the captions list in `video_config.py` for any video!

## Upload History

The system tracks:
- Total number of uploads per video
- Which caption was used last
- When it was last uploaded

This is saved in `upload_history.json` and automatically updates after each upload.

## Example Weekly Flow

**Monday 6:00 PM**: Uploads "Addio.MOV" with Caption #1
**Tuesday 6:00 PM**: Uploads "Charlie Brown.mov" with Caption #1  
**Wednesday 6:00 PM**: Uploads "Chihiro.mov" with Caption #1
...

Next week:
**Monday 6:00 PM**: Uploads "Addio.MOV" with Caption #2 (rotation!)
**Tuesday 6:00 PM**: Uploads "Charlie Brown.mov" with Caption #2
...

## Tips

1. **Add more captions**: The more captions per video, the longer before they repeat
2. **Customize schedule**: Change which video uploads on which day in `DAILY_SCHEDULE`
3. **Manual uploads**: Use `python main.py upload --video "filename"` to test
4. **Keep it simple**: Everything is in `video_config.py` - no complex configs!

## Files You Need to Edit

- `video_config.py` - All your videos, captions, and schedule
- That's it! Everything else runs automatically.
