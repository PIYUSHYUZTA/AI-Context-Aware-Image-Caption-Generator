"""AI-powered image captioning using OpenAI and Google Gemini APIs."""
import base64
from io import BytesIO
import os
from PIL import Image


class OpenAICaptioner:
    """Use OpenAI GPT-4 Vision for image captioning."""
    
    def __init__(self, api_key=None):
        """Initialize OpenAI client.
        
        Args:
            api_key: OpenAI API key (or set OPENAI_API_KEY env variable)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        
        if not self.api_key:
            raise ValueError("OpenAI API key required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
    
    def _encode_image(self, image):
        """Encode PIL image to base64."""
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')
    
    def generate_caption(self, image, style="descriptive"):
        """Generate caption using GPT-4 Vision.
        
        Args:
            image: PIL Image
            style: Caption style - "descriptive", "creative", "technical", "social_media"
            
        Returns:
            Generated caption string
        """
        # Encode image
        base64_image = self._encode_image(image)
        
        # Create prompt based on style
        prompts = {
            "descriptive": "Describe this image in detail. Focus on what you see, including objects, people, actions, colors, and setting.",
            "creative": "Write a creative, engaging caption for this image that would work well on social media.",
            "technical": "Provide a technical, objective description of this image, including composition, lighting, and key elements.",
            "social_media": "Create a catchy social media caption with relevant hashtags for this image."
        }
        
        prompt = prompts.get(style, prompts["descriptive"])
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Using mini for cost efficiency, can use gpt-4o for best quality
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=300
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def generate_multiple_options(self, image, num_options=5):
        """Generate multiple caption options like ChatGPT does.
        
        Args:
            image: PIL Image
            num_options: Number of caption options (default 5)
            
        Returns:
            List of caption options
        """
        base64_image = self._encode_image(image)
        
        prompt = f"""Analyze this image and provide {num_options} different caption options.

Make them varied:
- Option 1: Descriptive and detailed
- Option 2: Short and catchy
- Option 3: Creative/storytelling
- Option 4: Professional/formal
- Option 5: Casual/friendly

Format EXACTLY as:
1. [caption 1]
2. [caption 2]
3. [caption 3]
4. [caption 4]
5. [caption 5]"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500
            )
            
            content = response.choices[0].message.content.strip()
            
            # Parse numbered options
            captions = []
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                    # Remove numbering
                    caption = line.split('.', 1)[-1].strip() if '.' in line else line[1:].strip()
                    if caption:
                        captions.append(caption)
            
            return captions if captions else [content]
            
        except Exception as e:
            return [f"Error: {str(e)}"]


class GeminiCaptioner:
    """Use Google Gemini Vision for image captioning."""
    
    def __init__(self, api_key=None):
        """Initialize Gemini client.
        
        Args:
            api_key: Google API key (or set GOOGLE_API_KEY env variable)
        """
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        
        if not self.api_key:
            raise ValueError("Google API key required. Set GOOGLE_API_KEY environment variable or pass api_key parameter.")
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        except ImportError:
            raise ImportError("Google Generative AI package not installed. Run: pip install google-generativeai")
    
    def generate_caption(self, image, style="descriptive"):
        """Generate caption using Gemini Vision.
        
        Args:
            image: PIL Image
            style: Caption style - "descriptive", "creative", "technical", "social_media"
            
        Returns:
            Generated caption string
        """
        # Create prompt based on style
        prompts = {
            "descriptive": "Describe this image in detail. Focus on what you see, including objects, people, actions, colors, and setting.",
            "creative": "Write a creative, engaging caption for this image that would work well on social media.",
            "technical": "Provide a technical, objective description of this image, including composition, lighting, and key elements.",
            "social_media": "Create a catchy social media caption with relevant hashtags for this image."
        }
        
        prompt = prompts.get(style, prompts["descriptive"])
        
        try:
            response = self.model.generate_content([prompt, image])
            return response.text.strip()
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def generate_multiple_options(self, image, num_options=5):
        """Generate multiple caption options like ChatGPT does.
        
        Args:
            image: PIL Image
            num_options: Number of caption options (default 5)
            
        Returns:
            List of caption options
        """
        prompt = f"""Analyze this image and provide {num_options} different caption options.

Make them varied:
- Option 1: Descriptive and detailed
- Option 2: Short and catchy
- Option 3: Creative/storytelling
- Option 4: Professional/formal
- Option 5: Casual/friendly

Format EXACTLY as:
1. [caption 1]
2. [caption 2]
3. [caption 3]
4. [caption 4]
5. [caption 5]"""
        
        try:
            response = self.model.generate_content([prompt, image])
            content = response.text.strip()
            
            # Parse numbered options
            captions = []
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                    # Remove numbering
                    caption = line.split('.', 1)[-1].strip() if '.' in line else line[1:].strip()
                    if caption:
                        captions.append(caption)
            
            return captions if captions else [content]
            
        except Exception as e:
            return [f"Error: {str(e)}"]


def get_captioner(provider="openai", api_key=None):
    """Get captioner instance based on provider.
    
    Args:
        provider: "openai" or "gemini"
        api_key: API key for the provider
        
    Returns:
        Captioner instance
    """
    if provider.lower() == "openai":
        return OpenAICaptioner(api_key)
    elif provider.lower() == "gemini":
        return GeminiCaptioner(api_key)
    else:
        raise ValueError(f"Unknown provider: {provider}. Use 'openai' or 'gemini'")
