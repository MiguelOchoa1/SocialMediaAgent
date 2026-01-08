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
            
            # Calculate target bitrate (reserve 128kbps for audio)
            duration = clip.duration
            audio_bitrate = 128  # kbps for audio
            target_video_bitrate = int((target_size_mb * 8192) / duration) - audio_bitrate
            
            clip.write_videofile(
                output_path,
                bitrate=f"{target_video_bitrate}k",
                codec='libx264',
                audio=True,
                audio_codec='aac',
                audio_bitrate=f"{audio_bitrate}k",
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
    
    def convert_to_mp4(self, video_path: str, output_path: Optional[str] = None) -> Optional[str]:
        """
        Convert video to MP4 format for better compatibility
        
        Args:
            video_path: Path to input video
            output_path: Path for output video (optional)
            
        Returns:
            Path to converted video or None
        """
        try:
            from moviepy.editor import VideoFileClip
            
            if not output_path:
                name, _ = os.path.splitext(video_path)
                output_path = f"{name}.mp4"
            
            # Skip if already MP4
            if video_path.lower().endswith('.mp4'):
                return video_path
            
            logger.info(f"Converting {os.path.basename(video_path)} to MP4...")
            
            clip = VideoFileClip(video_path)
            
            clip.write_videofile(
                output_path,
                codec='libx264',
                audio=True,
                audio_codec='aac',
                audio_bitrate='128k',
                logger=None
            )
            
            clip.close()
            logger.info(f"Converted to MP4: {output_path}")
            
            return output_path
            
        except ImportError:
            logger.error("moviepy not installed. Run: pip install moviepy")
            return None
        except Exception as e:
            logger.error(f"Error converting video: {e}")
            return None
    
    def prepare_video(self, video_path: str) -> str:
        """
        Prepare video for upload (convert format and compress if needed)
        
        Args:
            video_path: Path to video file
            
        Returns:
            Path to prepared video (may be original, converted, or compressed)
        """
        current_path = video_path
        
        # Convert MOV and other formats to MP4
        if not video_path.lower().endswith('.mp4'):
            logger.info(f"Converting non-MP4 file to MP4 format...")
            converted_path = self.convert_to_mp4(video_path)
            if converted_path:
                current_path = converted_path
        
        # Compress if needed
        if self.should_compress(current_path):
            logger.info(f"Video exceeds size limit, compressing...")
            compressed_path = self.compress_video(current_path)
            if compressed_path:
                return compressed_path
        
        return current_path


if __name__ == "__main__":
    # Test the processor
    logging.basicConfig(level=logging.INFO)
    
    processor = VideoProcessor()
    print(f"Auto compress: {processor.auto_compress}")
    print(f"Max size: {processor.max_size_mb}MB")
