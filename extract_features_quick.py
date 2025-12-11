"""Quick script to extract features for available images."""
import numpy as np
from pickle import dump
from pathlib import Path
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import Model

print("Loading VGG16 model...")
base_model = VGG16()
model = Model(inputs=base_model.inputs, outputs=base_model.layers[-2].output)
print("VGG16 loaded successfully")

# Load descriptions to get image IDs
print("\nLoading image IDs from descriptions...")
image_ids = set()
with open('descriptions.txt', 'r') as f:
    for line in f:
        tokens = line.strip().split()
        if len(tokens) >= 2:
            image_ids.add(tokens[0])

print(f"Found {len(image_ids)} unique image IDs")

# Check for images in data/Images directory
images_dir = Path('data/Images')
features = {}

# First check if actual images exist
found_actual_images = False
if images_dir.exists():
    print(f"\nChecking {images_dir}...")
    
    for image_id in image_ids:
        # Try different extensions
        for ext in ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']:
            image_path = images_dir / f"{image_id}{ext}"
            
            if image_path.exists():
                try:
                    print(f"Processing {image_path.name}...")
                    
                    # Load and preprocess image
                    image = load_img(image_path, target_size=(224, 224))
                    image = img_to_array(image)
                    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
                    image = preprocess_input(image)
                    
                    # Extract features
                    feature = model.predict(image, verbose=0)
                    features[image_id] = feature
                    print(f"  ✓ Extracted features for {image_id}")
                    found_actual_images = True
                    break
                    
                except Exception as e:
                    print(f"  ✗ Error processing {image_path.name}: {e}")

if not found_actual_images:
    print(f"\n⚠️  No images found in {images_dir}")
    print("Using sample images instead...")

# Check samples directory
samples_dir = Path('samples')
if samples_dir.exists() and not found_actual_images:
    print(f"\nFound samples directory. Extracting features...")
    
    # Map sample images to description IDs
    image_ids_list = list(image_ids)
    sample_mapping = {
        'dog.jpg': image_ids_list[0] if len(image_ids_list) > 0 else 'sample_dog',
        'beach.jpg': image_ids_list[1] if len(image_ids_list) > 1 else 'sample_beach',
    }
    
    for sample_file, image_id in sample_mapping.items():
        sample_path = samples_dir / sample_file
        
        if sample_path.exists():
            try:
                print(f"Processing {sample_file}...")
                
                # Load and preprocess image
                image = load_img(sample_path, target_size=(224, 224))
                image = img_to_array(image)
                image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
                image = preprocess_input(image)
                
                # Extract features
                feature = model.predict(image, verbose=0)
                features[image_id] = feature
                print(f"  ✓ Extracted features for {image_id}")
                
            except Exception as e:
                print(f"  ✗ Error processing {sample_file}: {e}")

# Save features
if features:
    print(f"\n✅ Extracted features for {len(features)} images")
    dump(features, open('features.pkl', 'wb'))
    print("Features saved to features.pkl")
else:
    print("\n❌ No features extracted. Please ensure images are available.")
    print("\nOptions:")
    print("1. Place images in data/Images/ directory")
    print("2. Ensure sample images exist in samples/ directory")
