# Social Media Agent

Automated social media agent for scheduling video uploads with AI-generated captions and hashtags.

## Features

- 📅 Schedule video uploads at specific times
- 🤖 Auto-generate captions and hashtags using AI
- 📱 Support for multiple platforms (Instagram, TikTok, YouTube)
- 🎬 Video preprocessing and optimization
- 🔄 Queue management for multiple videos

## Free Tools & APIs Used

- **Python** - Main programming language
- **OpenAI API** - Free tier for caption/hashtag generation (or use Ollama locally)
- **Platform APIs**:
  - Instagram Graph API (Meta)
  - TikTok API
  - YouTube Data API v3
- **Schedule** - Python scheduling library

## Setup

1. Install Python 3.8+
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your API keys in `config.yaml`:
   - Get Instagram API credentials from Meta Developer Portal
   - Get TikTok API from TikTok Developer Portal
   - Get YouTube API from Google Cloud Console
   - Get OpenAI API key (or use Ollama locally for free)

4. Add your videos to the `videos/` folder

5. Configure your upload schedule in `schedule_config.yaml`

## Usage

Run the agent:
```bash
python main.py
```

Run in background:
```bash
python main.py --daemon
```

## Project Structure

```
social-media-agent/
├── main.py                 # Main application entry
├── config.yaml            # API credentials and settings
├── schedule_config.yaml   # Upload schedule configuration
├── requirements.txt       # Python dependencies
├── modules/
│   ├── caption_generator.py  # AI caption/hashtag generation
│   ├── scheduler.py          # Video scheduling logic
│   ├── uploader.py          # Platform upload handlers
│   └── video_processor.py   # Video optimization
├── videos/                # Place your videos here
├── logs/                  # Application logs
└── .env.example          # Environment variables template
```

## Free API Limits

- **Instagram**: 200 requests/hour
- **TikTok**: Varies by access level
- **YouTube**: 10,000 quota units/day
- **OpenAI**: $5 free credit (or use Ollama locally - unlimited)

## Alternative: Local AI (100% Free)

Instead of OpenAI API, you can use **Ollama** locally:
1. Install Ollama: https://ollama.ai
2. Run: `ollama run llama2`
3. Set `use_local_ai: true` in config.yaml

## License

MIT
# SocialMediaAgent
