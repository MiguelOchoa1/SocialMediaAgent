"""
Scheduler Module
Handles scheduling and managing video uploads
"""

import os
import yaml
import schedule
import time
import logging
from datetime import datetime
from typing import List, Dict, Optional
import shutil

logger = logging.getLogger(__name__)


class VideoScheduler:
    def __init__(self, schedule_config_path: str = "schedule_config.yaml"):
        """Initialize scheduler with schedule configuration"""
        with open(schedule_config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.schedule_items = self.config.get('schedule', [])
        self.queue_config = self.config.get('queue', {})
        self.caption_config = self.config.get('caption', {})
        
        self.videos_folder = "videos"
        self.uploaded_folder = "uploaded"
        
        # Ensure folders exist
        os.makedirs(self.videos_folder, exist_ok=True)
        os.makedirs(self.uploaded_folder, exist_ok=True)
        
        self.video_queue = []
        self._load_video_queue()
    
    def _load_video_queue(self):
        """Load available videos from the videos folder"""
        supported_formats = ['.mp4', '.mov', '.avi', '.mkv']
        
        self.video_queue = []
        for file in os.listdir(self.videos_folder):
            file_path = os.path.join(self.videos_folder, file)
            if os.path.isfile(file_path):
                _, ext = os.path.splitext(file)
                if ext.lower() in supported_formats:
                    self.video_queue.append(file_path)
        
        self.video_queue.sort()  # Sort alphabetically
        logger.info(f"Loaded {len(self.video_queue)} videos to queue")
    
    def get_next_video(self) -> Optional[str]:
        """
        Get the next video from the queue
        
        Returns:
            Path to next video or None if queue is empty
        """
        self._load_video_queue()  # Refresh queue
        
        if not self.video_queue:
            logger.warning("No videos in queue")
            return None
        
        if self.queue_config.get('random_selection', False):
            import random
            video_path = random.choice(self.video_queue)
        else:
            video_path = self.video_queue[0]
        
        logger.info(f"Selected video: {os.path.basename(video_path)}")
        return video_path
    
    def mark_video_uploaded(self, video_path: str):
        """
        Mark video as uploaded by moving it to uploaded folder
        
        Args:
            video_path: Path to the uploaded video
        """
        if not self.queue_config.get('mark_uploaded', True):
            return
        
        try:
            filename = os.path.basename(video_path)
            destination = os.path.join(self.uploaded_folder, filename)
            
            # If file exists, add timestamp
            if os.path.exists(destination):
                name, ext = os.path.splitext(filename)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{name}_{timestamp}{ext}"
                destination = os.path.join(self.uploaded_folder, filename)
            
            shutil.move(video_path, destination)
            logger.info(f"Moved uploaded video to: {destination}")
            
        except Exception as e:
            logger.error(f"Error marking video as uploaded: {e}")
    
    def schedule_upload(self, upload_callback, days: List[str], 
                       time_str: str, platform: str):
        """
        Schedule an upload task
        
        Args:
            upload_callback: Function to call for upload (should accept platform, video_path, tone)
            days: List of days (monday, tuesday, etc.)
            time_str: Time in HH:MM format
            platform: Platform to upload to
        """
        day_map = {
            'monday': schedule.every().monday,
            'tuesday': schedule.every().tuesday,
            'wednesday': schedule.every().wednesday,
            'thursday': schedule.every().thursday,
            'friday': schedule.every().friday,
            'saturday': schedule.every().saturday,
            'sunday': schedule.every().sunday,
        }
        
        def upload_task():
            logger.info(f"Scheduled upload triggered for {platform} at {time_str}")
            tone = self.caption_config.get('tone', 'casual')
            
            video_path = self.get_next_video()
            if video_path:
                upload_callback(platform, video_path, tone)
            else:
                logger.warning("No videos available for scheduled upload")
        
        # Schedule for each specified day
        for day in days:
            day = day.lower()
            if day in day_map:
                day_map[day].at(time_str).do(upload_task)
                logger.info(f"Scheduled upload: {day} at {time_str} -> {platform}")
            else:
                logger.warning(f"Unknown day: {day}")
    
    def setup_all_schedules(self, upload_callback):
        """
        Setup all schedules from config
        
        Args:
            upload_callback: Function to call for uploads
        """
        for item in self.schedule_items:
            days = item.get('days', [])
            time_str = item.get('time', '10:00')
            platform = item.get('platform', 'instagram')
            
            self.schedule_upload(upload_callback, days, time_str, platform)
        
        logger.info(f"Setup {len(self.schedule_items)} scheduled uploads")
    
    def run_pending(self):
        """Run all pending scheduled tasks"""
        schedule.run_pending()
    
    def get_schedule_info(self) -> List[Dict]:
        """
        Get information about all scheduled uploads
        
        Returns:
            List of schedule information dictionaries
        """
        info = []
        for job in schedule.jobs:
            info.append({
                'next_run': job.next_run.strftime("%Y-%m-%d %H:%M:%S") if job.next_run else None,
                'job': str(job)
            })
        return info
    
    def clear_schedules(self):
        """Clear all scheduled tasks"""
        schedule.clear()
        logger.info("Cleared all schedules")


if __name__ == "__main__":
    # Test the scheduler
    logging.basicConfig(level=logging.INFO)
    
    def dummy_upload(platform, video_path, tone):
        print(f"Upload: {platform} | {video_path} | tone: {tone}")
    
    scheduler = VideoScheduler()
    scheduler.setup_all_schedules(dummy_upload)
    
    print("\n=== Scheduled Jobs ===")
    for info in scheduler.get_schedule_info():
        print(f"Next run: {info['next_run']} - {info['job']}")
    
    print(f"\nVideos in queue: {len(scheduler.video_queue)}")
