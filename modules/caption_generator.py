"""
Caption and Hashtag Generator Module
Uses AI (OpenAI or local Ollama) to generate engaging captions and relevant hashtags
"""

import yaml
import os
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class CaptionGenerator:
    def __init__(self, config_path: str = "config.yaml", 
                 style_path: str = "caption_style.yaml",
                 video_descriptions_path: str = "videos/video_descriptions.yaml"):
        """Initialize the caption generator with config"""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.ai_config = self.config['ai']
        self.hashtag_config = self.config['hashtags']
        
        # Load caption style training
        self.style_config = None
        if os.path.exists(style_path):
            try:
                with open(style_path, 'r') as f:
                    self.style_config = yaml.safe_load(f)
                logger.info("Loaded custom caption style training")
            except Exception as e:
                logger.warning(f"Could not load caption style: {e}")
                self.style_config = None
        
        # Load video descriptions
        self.video_descriptions = {}
        if os.path.exists(video_descriptions_path):
            try:
                with open(video_descriptions_path, 'r') as f:
                    desc_data = yaml.safe_load(f)
                    self.video_descriptions = desc_data.get('videos', {})
                logger.info(f"Loaded descriptions for {len(self.video_descriptions)} videos")
            except Exception as e:
                logger.warning(f"Could not load video descriptions: {e}")
                self.video_descriptions = {}
        
        # Initialize AI client
        if self.ai_config['use_local_ai']:
            try:
                import ollama
                self.client = ollama
                self.use_ollama = True
                logger.info("Using Ollama for local AI generation")
            except ImportError:
                logger.error("Ollama not installed. Run: pip install ollama")
                raise
        else:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.ai_config['openai_api_key'])
                self.use_ollama = False
                logger.info("Using OpenAI API for generation")
            except ImportError:
                logger.error("OpenAI not installed. Run: pip install openai")
                raise
    
    def generate_caption(self, video_path: str, tone: str = "casual", 
                        max_length: int = 2200) -> str:
        """
        Generate a caption for the video
        
        Args:
            video_path: Path to the video file
            tone: Tone of the caption (casual, professional, funny, inspirational)
            max_length: Maximum character length
            
        Returns:
            Generated caption
        """
        video_name = os.path.basename(video_path)
        
        # Get video description if available
        video_description = self.video_descriptions.get(video_name, "")
        
        # Build prompt with custom style if available
        if self.style_config:
            prompt = self._build_custom_prompt(video_name, video_description, tone, max_length)
        else:
            # Build context with video description if available
            video_context = f"Video file: {video_name}"
            if video_description:
                video_context += f"\nVideo content: {video_description}"
            
            prompt = f"""Generate an engaging social media caption for this video.

{video_context}

Tone: {tone}
Max length: {max_length} characters
Include emojis: {self.config.get('caption', {}).get('include_emojis', True)}
Include call-to-action: {self.config.get('caption', {}).get('call_to_action', True)}

Make it engaging, authentic, and optimized for social media engagement.
The caption should be relevant to the actual video content.
Do not include hashtags in the caption (they will be added separately).
"""
        
        try:
            if self.use_ollama:
                response = self.client.chat(
                    model=self.ai_config['model'],
                    messages=[
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ]
                )
                caption = response['message']['content'].strip()
            else:
                response = self.client.chat.completions.create(
                    model=self.ai_config['model'],
                    messages=[
                        {"role": "system", "content": "You are a social media expert who creates engaging captions."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500
                )
                caption = response.choices[0].message.content.strip()
            
            # Ensure it's within length
            if len(caption) > max_length:
                caption = caption[:max_length-3] + "..."
            
            logger.info(f"Generated caption: {caption[:50]}...")
            return caption
            
        except Exception as e:
            logger.error(f"Error generating caption: {e}")
            return f"Check out this amazing video! 🎬✨ {video_name}"
    
    def generate_hashtags(self, video_path: str, caption: str = "") -> List[str]:
        """
        Generate relevant hashtags for the video
        
        Args:
            video_path: Path to the video file
            caption: The generated caption (for context)
            
        Returns:
            List of hashtags (without # symbol)
        """
        video_name = os.path.basename(video_path)
        max_count = self.hashtag_config['max_count']
        custom_tags = self.hashtag_config.get('custom_tags', [])
        
        # Get video description if available
        video_description = self.video_descriptions.get(video_name, "")
        
        # Build context
        video_context = f"Video: {video_name}"
        if video_description:
            video_context += f"\nContent: {video_description}"
        if caption:
            video_context += f"\nCaption: {caption[:200]}"
        
        prompt = f"""Generate {max_count - len(custom_tags)} relevant and trending hashtags for a social media video.

{video_context}

Requirements:
- Highly relevant to the specific video content
- Mix of popular and niche hashtags
- Good for discovery and reach
- Return only the hashtag words (without # symbol)
- One hashtag per line
"""
        
        try:
            if self.use_ollama:
                response = self.client.chat(
                    model=self.ai_config['model'],
                    messages=[
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ]
                )
                hashtags_text = response['message']['content'].strip()
            else:
                response = self.client.chat.completions.create(
                    model=self.ai_config['model'],
                    messages=[
                        {"role": "system", "content": "You are a social media hashtag expert."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=300
                )
                hashtags_text = response.choices[0].message.content.strip()
            
            # Parse hashtags
            hashtags = []
            for line in hashtags_text.split('\n'):
                tag = line.strip().replace('#', '').replace('-', '').strip()
                if tag and len(tag) > 2:
                    hashtags.append(tag)
            
            # Add custom tags
            hashtags.extend(custom_tags)
            
            # Limit to max count
            hashtags = hashtags[:max_count]
            
            logger.info(f"Generated {len(hashtags)} hashtags")
            return hashtags
            
        except Exception as e:
            logger.error(f"Error generating hashtags: {e}")
            # Fallback generic hashtags
            return ["video", "content", "viral", "trending"] + custom_tags
    
    def _build_custom_prompt(self, video_name: str, video_description: str, 
                           tone: str, max_length: int) -> str:
        """
        Build a custom prompt based on the user's caption style training
        
        Args:
            video_name: Name of the video file
            video_description: Description of the video content
            tone: Desired tone
            max_length: Max character length
            
        Returns:
            Custom prompt string
        """
        style = self.style_config.get('style', {})
        examples = self.style_config.get('examples', [])
        common_phrases = self.style_config.get('common_phrases', [])
        avoid_phrases = self.style_config.get('avoid_phrases', [])
        cta_templates = self.style_config.get('cta_templates', [])
        
        # Build video context
        video_context = f"Video file: {video_name}"
        if video_description:
            video_context += f"\nVideo content: {video_description}"
        else:
            video_context += "\n(No description provided - use filename as context)"
        
        prompt = f"""Generate a social media caption for this video.

{video_context}

IMPORTANT: Write in this EXACT style based on these examples:

"""
        
        # Add example captions
        if examples:
            prompt += "=== EXAMPLE CAPTIONS (Match this style exactly) ===\n"
            for i, example in enumerate(examples[:5], 1):
                if example and example.strip():
                    prompt += f"\nExample {i}:\n{example.strip()}\n"
            prompt += "\n"
        
        # Add style description
        if style.get('description'):
            prompt += f"Style Description: {style['description']}\n\n"
        
        # Add structure preferences
        if style.get('structure'):
            prompt += "Structure to follow:\n"
            for item in style['structure']:
                prompt += f"- {item}\n"
            prompt += "\n"
        
        # Add elements preferences
        elements = style.get('elements', {})
        prompt += "Style Elements:\n"
        prompt += f"- Use emojis: {elements.get('use_emojis', True)}\n"
        prompt += f"- Use line breaks: {elements.get('use_line_breaks', True)}\n"
        prompt += f"- Use questions: {elements.get('use_questions', True)}\n"
        prompt += f"- Use storytelling: {elements.get('use_storytelling', False)}\n"
        prompt += f"- Personal pronouns (I, we, you): {elements.get('use_personal_pronouns', True)}\n\n"
        
        # Add common phrases
        if common_phrases:
            prompt += f"Phrases I commonly use: {', '.join(common_phrases)}\n"
        
        # Add phrases to avoid
        if avoid_phrases:
            prompt += f"NEVER use these phrases: {', '.join(avoid_phrases)}\n"
        
        # Add CTA templates
        if cta_templates:
            prompt += f"\nCall-to-action examples: {', '.join(cta_templates[:3])}\n"
        
        prompt += f"\nMax length: {max_length} characters"
        prompt += "\nDo not include hashtags in the caption (they will be added separately)."
        prompt += "\n\nNow write a caption for this video matching MY exact style:"
        
        return prompt
    
    def generate_full_post(self, video_path: str, tone: str = "casual") -> Dict[str, any]:
        """
        Generate complete post with caption and hashtags
        
        Args:
            video_path: Path to the video file
            tone: Tone for the caption
            
        Returns:
            Dictionary with 'caption', 'hashtags', and 'full_text'
        """
        # Generate caption
        caption = self.generate_caption(video_path, tone)
        
        # Generate hashtags
        hashtags = self.generate_hashtags(video_path, caption)
        
        # Combine for full text
        hashtag_string = ' '.join([f'#{tag}' for tag in hashtags])
        full_text = f"{caption}\n\n{hashtag_string}"
        
        return {
            'caption': caption,
            'hashtags': hashtags,
            'hashtag_string': hashtag_string,
            'full_text': full_text,
            'video_path': video_path
        }


if __name__ == "__main__":
    # Test the generator
    logging.basicConfig(level=logging.INFO)
    
    generator = CaptionGenerator()
    
    # Test with a dummy video path
    result = generator.generate_full_post("test_video.mp4", tone="casual")
    
    print("\n=== Generated Post ===")
    print(f"Caption: {result['caption']}")
    print(f"\nHashtags: {result['hashtag_string']}")
    print(f"\n=== Full Post ===\n{result['full_text']}")
