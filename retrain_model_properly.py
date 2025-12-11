"""Script to retrain the model with better parameters."""
import sys
from pathlib import Path

print("=" * 60)
print("IMAGE CAPTION MODEL RETRAINING GUIDE")
print("=" * 60)
print()

# Check if training data exists
data_dir = Path("data")
images_dir = data_dir / "Images"
captions_file = data_dir / "captions.txt"

print("📋 Checking prerequisites...")
print()

# Check data
if not data_dir.exists():
    print("❌ data/ directory not found")
    print()
    print("📥 You need to download training data first:")
    print()
    print("Option 1: Flickr8k Dataset (Recommended for beginners)")
    print("  - Size: ~1GB")
    print("  - Images: 8,000")
    print("  - Download: https://www.kaggle.com/datasets/adityajn105/flickr8k")
    print()
    print("Option 2: COCO Dataset (Advanced)")
    print("  - Size: ~20GB")
    print("  - Images: 120,000+")
    print("  - Download: https://cocodataset.org/")
    print()
    print("After downloading:")
    print("  1. Extract to data/ directory")
    print("  2. Ensure structure:")
    print("     data/")
    print("       Images/")
    print("       captions.txt")
    print()
    sys.exit(1)

if not images_dir.exists():
    print(f"❌ {images_dir} not found")
    print("   Please ensure images are in data/Images/")
    sys.exit(1)

if not captions_file.exists():
    print(f"❌ {captions_file} not found")
    print("   Please ensure captions file exists at data/captions.txt")
    sys.exit(1)

# Count images
image_count = len(list(images_dir.glob("*.jpg"))) + len(list(images_dir.glob("*.png")))
print(f"✅ Found {image_count} images")

# Check captions
with open(captions_file, 'r') as f:
    caption_count = len(f.readlines())
print(f"✅ Found {caption_count} captions")
print()

if image_count < 100:
    print("⚠️  WARNING: Very few images found!")
    print("   Recommended: 5,000+ images for good results")
    print()

# Check if training script exists
if Path("train_improved.py").exists():
    train_script = "train_improved.py"
elif Path("train.py").exists():
    train_script = "train.py"
else:
    print("❌ No training script found (train.py or train_improved.py)")
    sys.exit(1)

print(f"✅ Training script: {train_script}")
print()

# Recommendations
print("=" * 60)
print("📝 RECOMMENDED TRAINING PARAMETERS")
print("=" * 60)
print()
print("For Flickr8k (8,000 images):")
print("  - Epochs: 50-100")
print("  - Batch Size: 64")
print("  - Max Length: 34")
print("  - Vocab Size: 8000")
print("  - Training Time: 2-4 hours (GPU) / 10-20 hours (CPU)")
print()
print("For COCO (120,000+ images):")
print("  - Epochs: 30-50")
print("  - Batch Size: 128")
print("  - Max Length: 40")
print("  - Vocab Size: 10000")
print("  - Training Time: 10-20 hours (GPU) / 100+ hours (CPU)")
print()

# Update config
print("=" * 60)
print("🔧 UPDATING CONFIG")
print("=" * 60)
print()

try:
    import yaml
    
    config_file = Path("config.yaml")
    if config_file.exists():
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        # Update recommended settings
        config['model']['max_length'] = 34
        config['training']['epochs'] = 50
        config['training']['batch_size'] = 64
        config['preprocessing']['max_vocab_size'] = 8000
        
        # Backup old config
        backup_file = Path("config.yaml.backup")
        if not backup_file.exists():
            with open(backup_file, 'w') as f:
                yaml.dump(config, f)
            print("✅ Backed up config to config.yaml.backup")
        
        # Save new config
        with open(config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        
        print("✅ Updated config.yaml with recommended settings")
        print()
    else:
        print("⚠️  config.yaml not found, using defaults")
        print()
        
except Exception as e:
    print(f"⚠️  Could not update config: {e}")
    print()

# Training command
print("=" * 60)
print("🚀 READY TO TRAIN")
print("=" * 60)
print()
print("Run this command to start training:")
print()
print(f"  python {train_script}")
print()
print("Or with custom parameters:")
print()
print(f"  python {train_script} --epochs 50 --batch-size 64")
print()
print("⏱️  Estimated time:")
if image_count < 1000:
    print("  - With GPU: 30-60 minutes")
    print("  - With CPU: 2-4 hours")
elif image_count < 10000:
    print("  - With GPU: 2-4 hours")
    print("  - With CPU: 10-20 hours")
else:
    print("  - With GPU: 10-20 hours")
    print("  - With CPU: 100+ hours (not recommended)")
print()
print("💡 TIP: Use Google Colab for free GPU access!")
print("   https://colab.research.google.com/")
print()

# Ask to proceed
print("=" * 60)
response = input("Start training now? (y/n): ").strip().lower()

if response == 'y':
    print()
    print("🚀 Starting training...")
    print()
    import subprocess
    subprocess.run([sys.executable, train_script])
else:
    print()
    print("👍 No problem! Run the training command when ready.")
    print()
