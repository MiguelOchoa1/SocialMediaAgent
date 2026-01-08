"""
Video Processor Module
Handles video optimization and preprocessing
"""

import os
import yaml
import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


class VideoProcessor:
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize video processor with config"""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.video_config = self.config.get('video', {})
        self.max_size_mb = self.video_config.get('max_size_mb', 100)
        self.auto_compress = self.video_config.get('auto_compress', True)
    
    def get_video_info(self, video_path: str) -> Optional[dict]:
        """
        Get video information (duration, size, format, etc.)
        
        Args:
            video_path: Path to video file
            
        Returns:
            Dictionary with video info or None
        """
        if not os.path.exists(video_path):
            logger.error(f"Video file not found: {video_path}")
            return None
        
        try:
            from moviepy.editor import VideoFileClip
            
            clip = VideoFileClip(video_path)
            size_mb = os.path.getsize(video_path) / (1024 * 1024)
            
            info = {
                'path': video_path,
                'duration': clip.duration,
                'size_mb': round(size_mb, 2),
                'fps': clip.fps,
                'resolution': clip.size,
                'format': os.path.splitext(video_path)[1]
            }
            
            clip.close()
            logger.info(f"Video info: {info}")
            return info
            
        except ImportError:
            logger.error("moviepy not installed. Run: pip install moviepy")
            # Return basic info without moviepy
            size_mb = os.path.getsize(video_path) / (1024 * 1024)
            return {
                'path': video_path,
                'size_mb': round(size_mb, 2),
                'format': os.path.splitext(video_path)[1]
            }
        except Exception as e:
            logger.error(f"Error getting video info: {e}")
            return None
    
    def compress_video(self, video_path: str, output_path: Optional[str] = None,
                      target_size_mb: Optional[float] = None) -> Optional[str]:
        """
        Compress video to reduce file size
        
        Args:
            video_path: Path to input video
            output_path: Path for output video (optional)
            target_size_mb: Target size in MB (optional, uses config default)
            
        Returns:
            Path to compressed video or None
        """
        try:
            from moviepy.editor import VideoFileClip
            
            if not output_path:
                name, ext = os.path.splitext(video_path)
                output_path = f"{name}_compressed{ext}"
            
            if not target_size_mb:
                target_size_mb = self.max_size_mb
            
            logger.info(f"Compressing video to ~{target_size_mb}MB")
            
            clip = VideoFileClip(video_path)
            
            # Calculate target bitrate
            duration = clip.duration
            target_bitrate = int((target_size_mb * 8192) / duration)
            
            clip.write_videofile(
                output_path,
                bitrate=f"{target_bitrate}k",
                codec='libx264',
                audio_codec='aac',
                logger=None  # Suppress moviepy logs
            )
            
            clip.close()
            
            new_size_mb = os.path.getsize(output_path) / (1024 * 1024)
            logger.info(f"Compressed video saved: {output_path} ({new_size_mb:.2f}MB)")
            
            return output_path
            
        except ImportError:
            logger.error("moviepy not installed. Run: pip install moviepy")
            return None
        except Exception as e:
            logger.error(f"Error compressing video: {e}")
            return None
    
    def should_compress(self, video_path: str) -> bool:
        """
        Check if video should be compressed based on size
        
        Args:
            video_path: Path to video file
            
        Returns:
            True if video should be compressed
        """
        if not self.auto_compress:
            return False
        
        info = self.get_video_info(video_path)
        if not info:
            return False
        
        return info['size_mb'] > self.max_size_mb
    
    def prepare_video(self, video_path: str) -> str:
        """
        Prepare video for upload (compress if needed)
        
        Args:
            video_path: Path to video file
            
        Returns:
            Path to prepared video (may be original or compressed)
        """
        if self.should_compress(video_path):
            logger.info(f"Video exceeds size limit, compressing...")
            compressed_path = self.compress_video(video_path)
            if compressed_path:
                return compressed_path
        
        return video_path


if __name__ == "__main__":
    # Test the processor
    logging.basicConfig(level=logging.INFO)
    
    processor = VideoProcessor()
    print(f"Auto compress: {processor.auto_compress}")
    print(f"Max size: {processor.max_size_mb}MB")
