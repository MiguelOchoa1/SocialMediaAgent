"""
Video Upload Module
Handles uploading videos to different social media platforms
"""

import os
import yaml
import logging
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class VideoUploader:
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize uploader with config"""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.instagram_config = self.config.get('instagram', {})
        self.tiktok_config = self.config.get('tiktok', {})
        self.youtube_config = self.config.get('youtube', {})
        
        # Initialize clients
        self._init_instagram()
        self._init_tiktok()
        self._init_youtube()
    
    def _init_instagram(self):
        """Initialize Instagram client"""
        if not self.instagram_config.get('enabled', False):
            self.instagram_client = None
            logger.info("Instagram is disabled")
            return
        
        try:
            from instagrapi import Client
            self.instagram_client = Client()
            
            username = self.instagram_config.get('username')
            password = self.instagram_config.get('password')
            
            if username and password:
                # Try to load session
                session_file = "instagram_session.json"
                if os.path.exists(session_file):
                    self.instagram_client.load_settings(session_file)
                    logger.info("Loaded Instagram session")
                else:
                    self.instagram_client.login(username, password)
                    self.instagram_client.dump_settings(session_file)
                    logger.info("Instagram login successful")
            else:
                logger.warning("Instagram credentials not configured")
                self.instagram_client = None
                
        except ImportError:
            logger.error("instagrapi not installed. Run: pip install instagrapi")
            self.instagram_client = None
        except Exception as e:
            logger.error(f"Instagram initialization error: {e}")
            self.instagram_client = None
    
    def _init_tiktok(self):
        """Initialize TikTok client"""
        if not self.tiktok_config.get('enabled', False):
            self.tiktok_client = None
            logger.info("TikTok is disabled")
            return
        
        # TikTok API implementation would go here
        # Note: TikTok's official API for posting is limited
        logger.warning("TikTok upload not fully implemented - requires API approval")
        self.tiktok_client = None
    
    def _init_youtube(self):
        """Initialize YouTube client"""
        if not self.youtube_config.get('enabled', False):
            self.youtube_client = None
            logger.info("YouTube is disabled")
            return
        
        try:
            from googleapiclient.discovery import build
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            
            # YouTube API implementation
            # Note: Requires OAuth2 setup
            logger.warning("YouTube upload not fully implemented - requires OAuth2 setup")
            self.youtube_client = None
            
        except ImportError:
            logger.error("Google API client not installed")
            self.youtube_client = None
    
    def upload_to_instagram(self, video_path: str, caption: str, 
                           hashtags: list) -> Optional[Dict]:
        """
        Upload video to Instagram
        
        Args:
            video_path: Path to video file
            caption: Post caption
            hashtags: List of hashtags
            
        Returns:
            Upload result dictionary or None
        """
        if not self.instagram_client:
            logger.error("Instagram client not initialized")
            return None
        
        try:
            # Combine caption and hashtags
            full_caption = f"{caption}\n\n" + ' '.join([f'#{tag}' for tag in hashtags])
            
            # Upload video as Instagram Reel
            # Note: Instagram's "trial reels" feature may be deprecated or requires specific account settings
            # Using feed_show="0" keeps reel out of main feed (reels tab only)
            logger.info(f"Uploading to Instagram as Reel: {os.path.basename(video_path)}")
            media = self.instagram_client.clip_upload(
                video_path,
                caption=full_caption,
                feed_show="0",  # "0" = reels tab only (no feed preview)
                extra_data={
                    "audience": "besties"  # Try to limit to close friends/trial mode
                }
            )
            
            result = {
                'platform': 'instagram',
                'media_type': 'trial_reel',
                'media_id': media.pk,
                'timestamp': datetime.now().isoformat(),
                'video_path': video_path,
                'caption': full_caption,
                'success': True
            }
            
            logger.info(f"Successfully uploaded Instagram Trial Reel: {media.pk}")
            return result
            
        except Exception as e:
            logger.error(f"Instagram upload error: {e}")
            return {
                'platform': 'instagram',
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def upload_to_tiktok(self, video_path: str, caption: str, 
                        hashtags: list) -> Optional[Dict]:
        """
        Upload video to TikTok
        
        Note: TikTok's API requires approval and has limited access
        """
        logger.warning("TikTok upload not implemented - requires API approval")
        return {
            'platform': 'tiktok',
            'success': False,
            'error': 'Not implemented - requires TikTok API approval',
            'timestamp': datetime.now().isoformat()
        }
    
    def upload_to_youtube(self, video_path: str, title: str, 
                         description: str, tags: list) -> Optional[Dict]:
        """
        Upload video to YouTube
        
        Note: Requires OAuth2 authentication
        """
        logger.warning("YouTube upload not implemented - requires OAuth2 setup")
        return {
            'platform': 'youtube',
            'success': False,
            'error': 'Not implemented - requires OAuth2 setup',
            'timestamp': datetime.now().isoformat()
        }
    
    def upload(self, platform: str, video_path: str, caption: str, 
              hashtags: list) -> Optional[Dict]:
        """
        Upload video to specified platform
        
        Args:
            platform: Platform name (instagram, tiktok, youtube)
            video_path: Path to video file
            caption: Post caption
            hashtags: List of hashtags
            
        Returns:
            Upload result dictionary
        """
        if not os.path.exists(video_path):
            logger.error(f"Video file not found: {video_path}")
            return None
        
        platform = platform.lower()
        
        if platform == 'instagram':
            return self.upload_to_instagram(video_path, caption, hashtags)
        elif platform == 'tiktok':
            return self.upload_to_tiktok(video_path, caption, hashtags)
        elif platform == 'youtube':
            return self.upload_to_youtube(video_path, caption, hashtags)
        else:
            logger.error(f"Unknown platform: {platform}")
            return None


if __name__ == "__main__":
    # Test the uploader
    logging.basicConfig(level=logging.INFO)
    
    uploader = VideoUploader()
    print("Uploader initialized")
    print(f"Instagram enabled: {uploader.instagram_client is not None}")
    print(f"TikTok enabled: {uploader.tiktok_client is not None}")
    print(f"YouTube enabled: {uploader.youtube_client is not None}")
