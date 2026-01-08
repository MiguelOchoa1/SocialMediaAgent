"""
Social Media Agent - Main Application
Automated video upload scheduler with AI-generated captions and hashtags
"""

import os
import sys
import yaml
import time
import logging
import argparse
from datetime import datetime
from typing import Optional

from modules import CaptionGenerator, VideoUploader, VideoScheduler, VideoProcessor

# Setup logging
def setup_logging(config_path: str = "config.yaml"):
    """Setup logging configuration"""
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        log_config = config.get('logging', {})
        log_level = log_config.get('level', 'INFO')
        log_file = log_config.get('file', 'logs/agent.log')
        
        # Create logs directory
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        return logging.getLogger(__name__)
    except Exception as e:
        # Fallback logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        logger.error(f"Error setting up logging: {e}")
        return logger


logger = setup_logging()


class SocialMediaAgent:
    def __init__(self):
        """Initialize the social media agent"""
        logger.info("=" * 60)
        logger.info("Social Media Agent Starting...")
        logger.info("=" * 60)
        
        try:
            self.caption_generator = CaptionGenerator()
            self.uploader = VideoUploader()
            self.scheduler = VideoScheduler()
            self.video_processor = VideoProcessor()
            
            logger.info("All modules initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing agent: {e}")
            raise
    
    def process_and_upload(self, platform: str, video_path: str, tone: str = "casual"):
        """
        Process video, generate caption/hashtags, and upload
        
        Args:
            platform: Platform to upload to (instagram, tiktok, youtube)
            video_path: Path to video file
            tone: Tone for caption generation
        """
        try:
            logger.info(f"\n{'='*60}")
            logger.info(f"Processing upload: {os.path.basename(video_path)}")
            logger.info(f"Platform: {platform}")
            logger.info(f"{'='*60}\n")
            
            # Step 1: Check and prepare video
            logger.info("Step 1: Preparing video...")
            prepared_video = self.video_processor.prepare_video(video_path)
            video_info = self.video_processor.get_video_info(prepared_video)
            
            if video_info:
                logger.info(f"Video info: {video_info['size_mb']}MB, "
                          f"{video_info.get('duration', 'N/A')}s")
            
            # Step 2: Generate caption and hashtags
            logger.info("Step 2: Generating caption and hashtags...")
            post_data = self.caption_generator.generate_full_post(prepared_video, tone)
            
            logger.info(f"Caption: {post_data['caption'][:100]}...")
            logger.info(f"Hashtags: {len(post_data['hashtags'])} tags generated")
            
            # Step 3: Upload to platform
            logger.info(f"Step 3: Uploading to {platform}...")
            result = self.uploader.upload(
                platform=platform,
                video_path=prepared_video,
                caption=post_data['caption'],
                hashtags=post_data['hashtags']
            )
            
            # Step 4: Mark as uploaded if successful
            if result and result.get('success', False):
                logger.info("✓ Upload successful!")
                self.scheduler.mark_video_uploaded(video_path)
                
                # Clean up compressed file if different from original
                if prepared_video != video_path and os.path.exists(prepared_video):
                    os.remove(prepared_video)
                    logger.info("Cleaned up compressed video")
            else:
                logger.error(f"✗ Upload failed: {result.get('error', 'Unknown error')}")
            
            logger.info(f"\n{'='*60}\n")
            return result
            
        except Exception as e:
            logger.error(f"Error in process_and_upload: {e}", exc_info=True)
            return None
    
    def upload_now(self, platform: str = "instagram", video_path: Optional[str] = None):
        """
        Upload a video immediately (not scheduled)
        
        Args:
            platform: Platform to upload to
            video_path: Specific video to upload (or auto-select from queue)
        """
        if not video_path:
            video_path = self.scheduler.get_next_video()
            if not video_path:
                logger.error("No videos available in queue")
                return False
        
        result = self.process_and_upload(platform, video_path)
        return result is not None and result.get('success', False)
    
    def run_scheduler(self, daemon: bool = False):
        """
        Run the scheduler to handle scheduled uploads
        
        Args:
            daemon: Run in background daemon mode
        """
        # Setup all scheduled uploads
        self.scheduler.setup_all_schedules(
            upload_callback=self.process_and_upload
        )
        
        # Display schedule info
        logger.info("\n" + "="*60)
        logger.info("SCHEDULED UPLOADS")
        logger.info("="*60)
        
        schedule_info = self.scheduler.get_schedule_info()
        if schedule_info:
            for info in schedule_info:
                logger.info(f"Next run: {info['next_run']}")
        else:
            logger.warning("No schedules configured")
        
        logger.info("="*60 + "\n")
        
        # Run scheduler loop
        logger.info("Scheduler is running... Press Ctrl+C to stop")
        
        try:
            while True:
                self.scheduler.run_pending()
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            logger.info("\nScheduler stopped by user")
        except Exception as e:
            logger.error(f"Scheduler error: {e}", exc_info=True)
    
    def test_setup(self):
        """Test the agent setup and configuration"""
        logger.info("\n" + "="*60)
        logger.info("TESTING AGENT SETUP")
        logger.info("="*60 + "\n")
        
        # Test caption generator
        logger.info("Testing Caption Generator...")
        try:
            test_result = self.caption_generator.generate_full_post(
                "test_video.mp4", 
                tone="casual"
            )
            logger.info("✓ Caption Generator working")
            logger.info(f"  Sample caption: {test_result['caption'][:80]}...")
        except Exception as e:
            logger.error(f"✗ Caption Generator error: {e}")
        
        # Test uploader connections
        logger.info("\nTesting Uploader Connections...")
        logger.info(f"  Instagram: {'✓ Enabled' if self.uploader.instagram_client else '✗ Disabled'}")
        logger.info(f"  TikTok: {'✓ Enabled' if self.uploader.tiktok_client else '✗ Disabled'}")
        logger.info(f"  YouTube: {'✓ Enabled' if self.uploader.youtube_client else '✗ Disabled'}")
        
        # Test scheduler
        logger.info("\nTesting Scheduler...")
        logger.info(f"  Videos in queue: {len(self.scheduler.video_queue)}")
        if self.scheduler.video_queue:
            logger.info(f"  Next video: {os.path.basename(self.scheduler.video_queue[0])}")
        
        logger.info("\n" + "="*60 + "\n")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Social Media Agent - Automated video uploads with AI captions'
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='Test the setup and configuration'
    )
    
    parser.add_argument(
        '--upload-now',
        action='store_true',
        help='Upload next video immediately'
    )
    
    parser.add_argument(
        '--video',
        type=str,
        help='Specific video file to upload'
    )
    
    parser.add_argument(
        '--platform',
        type=str,
        default='instagram',
        choices=['instagram', 'tiktok', 'youtube'],
        help='Platform to upload to (default: instagram)'
    )
    
    parser.add_argument(
        '--daemon',
        action='store_true',
        help='Run scheduler in daemon mode'
    )
    
    args = parser.parse_args()
    
    try:
        agent = SocialMediaAgent()
        
        if args.test:
            # Test mode
            agent.test_setup()
            
        elif args.upload_now:
            # Upload now mode
            success = agent.upload_now(
                platform=args.platform,
                video_path=args.video
            )
            sys.exit(0 if success else 1)
            
        else:
            # Scheduler mode (default)
            agent.run_scheduler(daemon=args.daemon)
            
    except KeyboardInterrupt:
        logger.info("\nAgent stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
