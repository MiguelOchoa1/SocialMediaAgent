"""
Social Media Agent - Main Application
Automated daily video upload with rotating hard-coded captions
"""

import os
import sys
import time
import logging
import schedule
from datetime import datetime, timedelta
from typing import Optional
import json

from video_config import VIDEO_CONFIG, DAILY_SCHEDULE, UPLOAD_TIME, PLATFORM
from modules import VideoUploader

# Setup logging
def setup_logging():
    """Setup logging configuration"""
    log_file = 'logs/agent.log'
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)


logger = setup_logging()


class SocialMediaAgent:
    def __init__(self):
        """Initialize the social media agent"""
        logger.info("=" * 60)
        logger.info("Social Media Agent Starting (Hard-coded Mode)...")
        logger.info("=" * 60)
        
        try:
            self.uploader = VideoUploader()
            self.upload_history_file = "upload_history.json"
            self.upload_history = self._load_upload_history()
            
            logger.info("Agent initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing agent: {e}")
            raise
    
    def _load_upload_history(self):
        """Load upload history to track which caption was used last"""
        if os.path.exists(self.upload_history_file):
            try:
                with open(self.upload_history_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_upload_history(self):
        """Save upload history"""
        with open(self.upload_history_file, 'w') as f:
            json.dump(self.upload_history, f, indent=2)
    
    def _get_next_caption_index(self, video_filename):
        """Get the next caption index for a video (rotates through available captions)"""
        if video_filename not in self.upload_history:
            self.upload_history[video_filename] = {'last_caption_index': -1, 'upload_count': 0}
        
        video_data = VIDEO_CONFIG.get(video_filename)
        if not video_data:
            return 0
        
        num_captions = len(video_data['captions'])
        last_index = self.upload_history[video_filename]['last_caption_index']
        
        # Get next caption in rotation
        next_index = (last_index + 1) % num_captions
        return next_index
    
    def upload_daily_video(self):
        """
        Upload today's scheduled video with rotating caption
        """
        try:
            # Get today's day of week (0=Monday, 6=Sunday)
            today = datetime.now().weekday()
            
            # Get scheduled video for today
            video_filename = DAILY_SCHEDULE.get(today)
            
            if not video_filename:
                logger.warning(f"No video scheduled for today ({datetime.now().strftime('%A')})")
                return
            
            logger.info(f"\n{'='*60}")
            logger.info(f"Daily Upload: {video_filename}")
            logger.info(f"Day: {datetime.now().strftime('%A')}")
            logger.info(f"Platform: {PLATFORM}")
            logger.info(f"{'='*60}\n")
            
            # Get video path
            video_path = os.path.join("videos", video_filename)
            
            if not os.path.exists(video_path):
                logger.error(f"Video file not found: {video_path}")
                return
            
            # Get video config
            video_data = VIDEO_CONFIG.get(video_filename)
            if not video_data:
                logger.error(f"No caption config found for: {video_filename}")
                return
            
            # Get next caption in rotation
            caption_index = self._get_next_caption_index(video_filename)
            caption = video_data['captions'][caption_index]
            
            logger.info(f"Using caption #{caption_index + 1} of {len(video_data['captions'])}")
            logger.info(f"Caption preview: {caption[:50]}...")
            
            # Upload the video
            logger.info(f"Uploading to {PLATFORM}...")
            result = self.uploader.upload(
                video_path=video_path,
                caption=caption,
                platform=PLATFORM
            )
            
            # Update upload history
            if result and result.get('success', False):
                logger.info("✓ Upload successful!")
                
                # Update caption rotation
                self.upload_history[video_filename]['last_caption_index'] = caption_index
                self.upload_history[video_filename]['upload_count'] += 1
                self.upload_history[video_filename]['last_upload'] = datetime.now().isoformat()
                self._save_upload_history()
                
                logger.info(f"Upload count for this video: {self.upload_history[video_filename]['upload_count']}")
            else:
                logger.error(f"✗ Upload failed: {result.get('error', 'Unknown error')}")
            
            logger.info(f"\n{'='*60}\n")
            return result
            
        except Exception as e:
            logger.error(f"Error in upload_daily_video: {e}", exc_info=True)
            return None
    
    def upload_specific_video(self, video_filename: str):
        """
        Upload a specific video immediately with next caption in rotation
        
        Args:
            video_filename: Name of video file to upload
        """
        try:
            logger.info(f"\n{'='*60}")
            logger.info(f"Manual Upload: {video_filename}")
            logger.info(f"Platform: {PLATFORM}")
            logger.info(f"{'='*60}\n")
            
            video_path = os.path.join("videos", video_filename)
            
            if not os.path.exists(video_path):
                logger.error(f"Video file not found: {video_path}")
                return False
            
            video_data = VIDEO_CONFIG.get(video_filename)
            if not video_data:
                logger.error(f"No caption config found for: {video_filename}")
                return False
            
            # Get next caption in rotation
            caption_index = self._get_next_caption_index(video_filename)
            caption = video_data['captions'][caption_index]
            
            logger.info(f"Using caption #{caption_index + 1} of {len(video_data['captions'])}")
            logger.info(f"Caption: {caption}")
            
            # Upload
            result = self.uploader.upload(
                video_path=video_path,
                caption=caption,
                platform=PLATFORM
            )
            
            # Update history
            if result and result.get('success', False):
                logger.info("✓ Upload successful!")
                self.upload_history[video_filename]['last_caption_index'] = caption_index
                self.upload_history[video_filename]['upload_count'] += 1
                self.upload_history[video_filename]['last_upload'] = datetime.now().isoformat()
                self._save_upload_history()
                return True
            else:
                logger.error(f"✗ Upload failed: {result.get('error', 'Unknown error')}")
                return False
                
        except Exception as e:
            logger.error(f"Error in upload_specific_video: {e}", exc_info=True)
            return False
    
    def run_scheduler(self):
        """
        Run the daily scheduler
        """
        logger.info("\n" + "="*60)
        logger.info("DAILY UPLOAD SCHEDULER")
        logger.info("="*60)
        logger.info(f"Upload Time: {UPLOAD_TIME}")
        logger.info(f"Platform: {PLATFORM}")
        logger.info("\nWeekly Schedule:")
        
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for day_num, video_filename in DAILY_SCHEDULE.items():
            logger.info(f"  {days[day_num]}: {video_filename}")
        
        logger.info("="*60 + "\n")
        
        # Schedule daily upload
        schedule.every().day.at(UPLOAD_TIME).do(self.upload_daily_video)
        
        logger.info(f"Scheduler started. Waiting for {UPLOAD_TIME}...")
        logger.info("Press Ctrl+C to stop\n")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("\nScheduler stopped by user")
    
    def show_status(self):
        """Show current status and upload history"""
        logger.info("\n" + "="*60)
        logger.info("UPLOAD STATUS")
        logger.info("="*60)
        
        for video_filename, video_data in VIDEO_CONFIG.items():
            if video_filename in self.upload_history:
                history = self.upload_history[video_filename]
                logger.info(f"\n{video_filename}:")
                logger.info(f"  Total uploads: {history['upload_count']}")
                logger.info(f"  Last caption used: #{history['last_caption_index'] + 1} of {len(video_data['captions'])}")
                if 'last_upload' in history:
                    logger.info(f"  Last upload: {history['last_upload']}")
            else:
                logger.info(f"\n{video_filename}: Never uploaded")
        
        logger.info("\n" + "="*60 + "\n")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Social Media Agent - Daily Video Uploader')
    parser.add_argument('command', choices=['schedule', 'upload', 'status'], 
                       help='Command to run')
    parser.add_argument('--video', help='Specific video filename to upload (for upload command)')
    
    args = parser.parse_args()
    
    agent = SocialMediaAgent()
    
    if args.command == 'schedule':
        # Run the daily scheduler
        agent.run_scheduler()
    
    elif args.command == 'upload':
        # Upload a specific video now
        if args.video:
            agent.upload_specific_video(args.video)
        else:
            # Upload today's scheduled video
            agent.upload_daily_video()
    
    elif args.command == 'status':
        # Show status
        agent.show_status()


if __name__ == "__main__":
    main()
