# YouTube Setup Guide 📺

Your system is now configured to upload to **both Instagram and YouTube** automatically!

## Current Configuration

✅ **Platforms**: Instagram + YouTube  
✅ **4 uploads per day**: 9am, 12pm, 6pm, 11pm  
✅ **Total uploads per day**: 4 videos × 2 platforms = **8 uploads**

## YouTube Setup Required

To enable YouTube uploads, you need to set up YouTube API access:

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable the **YouTube Data API v3**:
   - Go to "APIs & Services" > "Library"
   - Search for "YouTube Data API v3"
   - Click "Enable"

### Step 2: Create OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Choose "Desktop app" as application type
4. Name it (e.g., "Social Media Agent")
5. Download the JSON file
6. **Save it as `client_secrets.json`** in your project folder

### Step 3: Enable YouTube in Config

Edit [config.yaml](config.yaml):

```yaml
youtube:
  enabled: true  # Change to true
  client_secrets_file: "client_secrets.json"
  credentials_file: "youtube_credentials.json"
```

### Step 4: First-Time Authentication

The first time you run an upload, it will:
1. Open your browser automatically
2. Ask you to sign in to your YouTube account
3. Request permission to upload videos
4. Save credentials to `youtube_credentials.json`

After first authentication, future uploads will be automatic!

## Instagram Setup

Edit [config.yaml](config.yaml):

```yaml
instagram:
  enabled: true
  username: "your_instagram_username"
  password: "your_instagram_password"
```

## Test Your Setup

### Check Status
```bash
.venv/bin/python main.py status
```

### Test Upload Single Video
```bash
.venv/bin/python main.py upload --video "Organ 1.mov"
```
This will upload to **both Instagram and YouTube**!

### Upload Today's Time Slot
```bash
# Upload 9am video to both platforms
.venv/bin/python main.py upload --slot 0
```

### Start Automatic Scheduler
```bash
.venv/bin/python main.py schedule
```

## What Happens When You Run

For each scheduled time (9am, 12pm, 6pm, 11pm):

1. ✅ Uploads video to **Instagram** with caption
2. ✅ Uploads same video to **YouTube** with same caption
3. ✅ Captions rotate automatically
4. ✅ History tracked for both platforms

## Example: 9am Upload Today (Thursday)

**Video**: Organ 1.mov  
**Platforms**: Instagram + YouTube  
**Caption**: "Church organ vibes 🎹\n\n\n\n\n#organ #organmusic #church #classical"  

The system will:
- Upload to Instagram first
- Then upload to YouTube
- Log success/failure for each
- Update upload history

## Upload History

The system tracks uploads across all platforms. Each video's caption rotates independently:

- Upload 1 (Both platforms): Caption #1
- Upload 2 (Both platforms): Caption #2  
- Upload 3 (Both platforms): Caption #3
- Upload 4 (Both platforms): Back to Caption #1

## Troubleshooting

### Instagram Not Working
- Check username/password in config.yaml
- May need to verify login from your device first

### YouTube Not Working
- Make sure `client_secrets.json` is in project folder
- Check that YouTube Data API v3 is enabled
- Run manual upload first to complete OAuth

### Both Platforms Must Work
If one platform fails, the system will:
- Log the error
- Continue with the other platform
- Mark upload as partial success

## Files You Need

✅ `config.yaml` - Platform credentials  
✅ `client_secrets.json` - YouTube OAuth (download from Google)  
⚙️ `youtube_credentials.json` - Auto-created after first auth  
⚙️ `upload_history.json` - Auto-created, tracks uploads  

## Commands Reference

```bash
# Check configuration and status
.venv/bin/python main.py status

# Upload single video to all platforms
.venv/bin/python main.py upload --video "Organ 1.mov"

# Upload specific time slot to all platforms
.venv/bin/python main.py upload --slot 0  # 9am
.venv/bin/python main.py upload --slot 1  # 12pm
.venv/bin/python main.py upload --slot 2  # 6pm
.venv/bin/python main.py upload --slot 3  # 11pm

# Upload all 4 videos for today to all platforms
.venv/bin/python main.py upload

# Start automatic scheduler (8 uploads/day)
.venv/bin/python main.py schedule
```

## Daily Uploads

With both platforms enabled:
- **9:00 AM**: Organ 1.mov → Instagram + YouTube
- **12:00 PM**: Video 2 → Instagram + YouTube
- **6:00 PM**: Video 3 → Instagram + YouTube
- **11:00 PM**: Video 4 → Instagram + YouTube

**Total: 8 uploads per day across 2 platforms! 🚀**
