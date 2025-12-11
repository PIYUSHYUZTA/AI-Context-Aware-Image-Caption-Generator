"""Create real sample images for testing."""
from PIL import Image, ImageDraw, ImageFont
import numpy as np

print("Creating realistic sample images...")
print()

# Create samples directory
import os
os.makedirs('samples_real', exist_ok=True)

# 1. Beach scene
print("1. Creating beach scene...")
beach = Image.new('RGB', (640, 480), color='#87CEEB')  # Sky blue
draw = ImageDraw.Draw(beach)

# Draw sun
draw.ellipse([500, 50, 580, 130], fill='#FFD700')

# Draw ocean
draw.rectangle([0, 300, 640, 480], fill='#4682B4')

# Draw sand
draw.rectangle([0, 350, 640, 480], fill='#F4A460')

# Draw waves
for i in range(5):
    y = 300 + i * 15
    draw.arc([0, y, 640, y+30], 0, 180, fill='white', width=2)

beach.save('samples_real/beach.jpg', quality=95)
print("   ✅ samples_real/beach.jpg")

# 2. Dog scene
print("2. Creating dog scene...")
dog_img = Image.new('RGB', (640, 480), color='#90EE90')  # Light green grass

draw = ImageDraw.Draw(dog_img)

# Draw dog body (simple brown dog)
draw.ellipse([200, 250, 440, 400], fill='#8B4513')  # Body
draw.ellipse([180, 200, 280, 280], fill='#8B4513')  # Head
draw.ellipse([190, 210, 230, 250], fill='#654321')  # Snout
draw.ellipse([240, 220, 260, 240], fill='black')  # Eye
draw.ellipse([200, 220, 220, 240], fill='black')  # Eye
draw.ellipse([215, 245, 225, 255], fill='black')  # Nose

# Draw legs
draw.rectangle([220, 380, 250, 450], fill='#8B4513')
draw.rectangle([390, 380, 420, 450], fill='#8B4513')

# Draw tail
draw.arc([420, 280, 500, 360], 180, 270, fill='#8B4513', width=15)

# Draw ball
draw.ellipse([450, 350, 520, 420], fill='#FF6347')

dog_img.save('samples_real/dog.jpg', quality=95)
print("   ✅ samples_real/dog.jpg")

# 3. City scene
print("3. Creating city scene...")
city = Image.new('RGB', (640, 480), color='#87CEEB')  # Sky

draw = ImageDraw.Draw(city)

# Draw buildings
buildings = [
    (50, 200, 150, 480, '#708090'),
    (170, 150, 270, 480, '#2F4F4F'),
    (290, 180, 390, 480, '#696969'),
    (410, 120, 510, 480, '#556B2F'),
    (530, 220, 630, 480, '#483D8B'),
]

for x1, y1, x2, y2, color in buildings:
    draw.rectangle([x1, y1, x2, y2], fill=color, outline='black', width=2)
    
    # Draw windows
    for wx in range(x1+10, x2-10, 20):
        for wy in range(y1+20, y2-20, 30):
            window_color = '#FFFF00' if np.random.random() > 0.3 else '#000080'
            draw.rectangle([wx, wy, wx+12, wy+15], fill=window_color)

# Draw ground
draw.rectangle([0, 460, 640, 480], fill='#2F4F4F')

city.save('samples_real/city.jpg', quality=95)
print("   ✅ samples_real/city.jpg")

print()
print("=" * 60)
print("✅ Real sample images created in 'samples_real/' folder")
print("=" * 60)
print()
print("These images are:")
print("- Actual drawings (not text placeholders)")
print("- Realistic scenes")
print("- Will generate proper captions")
print()
print("To use them:")
print("1. Copy them to 'samples/' folder")
print("2. Or update test scripts to use 'samples_real/'")
print()
