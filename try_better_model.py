"""Try different offline models to find the best one."""
from PIL import Image
import torch

print("Testing different offline models...")
print("=" * 60)

image_path = "samples/dog.jpg"
image = Image.open(image_path)

# Try 1: BLIP (smaller, faster)
print("\n1. Testing BLIP (Salesforce)...")
try:
    from transformers import BlipProcessor, BlipForConditionalGeneration
    
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    
    inputs = processor(image, return_tensors="pt")
    out = model.generate(**inputs, max_length=50)
    caption = processor.decode(out[0], skip_special_tokens=True)
    
    print(f"✅ Result: {caption}")
    
except Exception as e:
    print(f"❌ Error: {e}")

# Try 2: GIT (Microsoft)
print("\n2. Testing GIT (Microsoft)...")
try:
    from transformers import AutoProcessor, AutoModelForCausalLM
    
    processor = AutoProcessor.from_pretrained("microsoft/git-base")
    model = AutoModelForCausalLM.from_pretrained("microsoft/git-base")
    
    inputs = processor(images=image, return_tensors="pt")
    generated_ids = model.generate(pixel_values=inputs.pixel_values, max_length=50)
    caption = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    
    print(f"✅ Result: {caption}")
    
except Exception as e:
    print(f"❌ Error: {e}")

# Try 3: Current ViT-GPT2
print("\n3. Testing ViT-GPT2 (Current)...")
try:
    from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
    
    model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    processor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    
    pixel_values = processor(images=image, return_tensors="pt").pixel_values
    output_ids = model.generate(pixel_values, max_length=50, num_beams=3)
    caption = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    
    print(f"✅ Result: {caption}")
    
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 60)
print("Testing complete!")
print("\nWhich model gave the best result?")
