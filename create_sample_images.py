"""Create sample images for testing."""
from PIL import Image, ImageDraw, ImageFont
import os

# Create samples directory
os.makedirs('samples', exist_ok=True)

def create_sample_image(filename, text, bg_color, text_color):
    """Create a sample image with text."""
    img = Image.new('RGB', (400, 300), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a nice font, fallback to default
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    # Calculate text position (center)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    position = ((400 - text_width) // 2, (300 - text_height) // 2)
    
    # Draw text
    draw.text(position, text, fill=text_color, font=font)
    
    # Save
    img.save(f'samples/{filename}')
    print(f"✅ Created: samples/{filename}")

# Create sample images
create_sample_image('beach.jpg', '🏖️ Beach', (135, 206, 235), (255, 255, 255))
create_sample_image('dog.jpg', '🐕 Dog', (144, 238, 144), (0, 0, 0))
create_sample_image('city.jpg', '🌆 City', (70, 130, 180), (255, 255, 255))

print("\n✅ Sample images created in 'samples/' folder")
print("These are placeholder images. For real testing, add actual photos!")
