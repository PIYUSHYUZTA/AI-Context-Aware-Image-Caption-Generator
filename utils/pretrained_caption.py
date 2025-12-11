"""Fast image captioning using lightweight model."""
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
from PIL import Image
import torch

class PretrainedCaptioner:
    """Use lightweight ViT-GPT2 model for fast, accurate image captioning."""
    
    _instance = None
    _processor = None
    _model = None
    _tokenizer = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize lightweight ViT-GPT2 model."""
        if self._model is None:
            print("Loading lightweight caption model...")
            try:
                # Use smaller, faster model
                model_name = "nlpconnect/vit-gpt2-image-captioning"
                
                self._processor = ViTImageProcessor.from_pretrained(model_name)
                self._tokenizer = AutoTokenizer.from_pretrained(model_name)
                self._model = VisionEncoderDecoderModel.from_pretrained(model_name)
                
                # Move to GPU if available
                if torch.cuda.is_available():
                    self._model = self._model.to("cuda")
                
                print("Model loaded successfully!")
            except Exception as e:
                print(f"Error loading model: {e}")
                raise
    
    def generate_caption(self, image, max_length=50, num_beams=3):
        """Generate caption for an image.
        
        Args:
            image: PIL Image
            max_length: Maximum caption length
            num_beams: Number of beams for beam search
            
        Returns:
            Generated caption string
        """
        try:
            # Prepare image
            pixel_values = self._processor(images=image, return_tensors="pt").pixel_values
            
            # Move to GPU if available
            if torch.cuda.is_available():
                pixel_values = pixel_values.to("cuda")
            
            # Generate caption
            with torch.no_grad():
                output_ids = self._model.generate(
                    pixel_values,
                    max_length=max_length,
                    num_beams=num_beams,
                    early_stopping=True
                )
            
            # Decode caption
            caption = self._tokenizer.decode(output_ids[0], skip_special_tokens=True)
            
            return caption
        except Exception as e:
            print(f"Error generating caption: {e}")
            return "Error generating caption"
    
    def generate_multiple_captions(self, image, num_captions=3, max_length=50):
        """Generate multiple diverse captions.
        
        Args:
            image: PIL Image
            num_captions: Number of captions to generate
            max_length: Maximum caption length
            
        Returns:
            List of generated captions
        """
        try:
            # Prepare image
            pixel_values = self._processor(images=image, return_tensors="pt").pixel_values
            
            # Move to GPU if available
            if torch.cuda.is_available():
                pixel_values = pixel_values.to("cuda")
            
            # Generate multiple captions
            with torch.no_grad():
                output_ids = self._model.generate(
                    pixel_values,
                    max_length=max_length,
                    num_beams=num_captions * 2,
                    num_return_sequences=num_captions,
                    early_stopping=True,
                    do_sample=True,
                    temperature=0.7
                )
            
            # Decode captions
            captions = [
                self._tokenizer.decode(output_id, skip_special_tokens=True)
                for output_id in output_ids
            ]
            
            return captions
        except Exception as e:
            print(f"Error generating captions: {e}")
            return ["Error generating caption"]
