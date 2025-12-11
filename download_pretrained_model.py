"""Download pre-trained image captioning model"""
import os
import urllib.request
import sys

print("=" * 60)
print("DOWNLOADING PRE-TRAINED MODEL")
print("=" * 60)

# Model sources (Flickr8k trained models)
MODEL_SOURCES = [
    {
        'name': 'Flickr8k CNN-LSTM Model',
        'model_url': 'https://github.com/yashk2810/Image-Captioning/raw/master/models/model_19.h5',
        'tokenizer_url': 'https://github.com/yashk2810/Image-Captioning/raw/master/models/tokenizer.pkl',
        'size': '~50MB'
    }
]

def download_file(url, filename):
    """Download file with progress"""
    try:
        print(f"\nDownloading {filename}...")
        print(f"URL: {url}")
        
        def progress(block_num, block_size, total_size):
            downloaded = block_num * block_size
            percent = min(downloaded * 100 / total_size, 100)
            sys.stdout.write(f"\r  Progress: {percent:.1f}% ({downloaded/1024/1024:.1f}MB)")
            sys.stdout.flush()
        
        urllib.request.urlretrieve(url, filename, progress)
        print(f"\n  ✅ Downloaded: {filename}")
        return True
    except Exception as e:
        print(f"\n  ❌ Error: {e}")
        return False

# Backup current files
print("\n1. Backing up current files...")
if os.path.exists('model.h5'):
    os.rename('model.h5', 'model_old.h5')
    print("  ✅ Backed up model.h5 -> model_old.h5")

if os.path.exists('tokenizer.pkl'):
    os.rename('tokenizer.pkl', 'tokenizer_old_backup.pkl')
    print("  ✅ Backed up tokenizer.pkl -> tokenizer_old_backup.pkl")

# Try downloading from GitHub
print("\n2. Attempting to download pre-trained model...")
print("  Note: This may fail due to GitHub LFS. If it fails, I'll provide alternative.")

source = MODEL_SOURCES[0]
print(f"\n  Source: {source['name']}")
print(f"  Size: {source['size']}")

model_success = download_file(source['model_url'], 'model.h5')
tokenizer_success = download_file(source['tokenizer_url'], 'tokenizer.pkl')

if model_success and tokenizer_success:
    print("\n" + "=" * 60)
    print("✅ DOWNLOAD COMPLETE!")
    print("=" * 60)
    print("\nTesting the model...")
    
    # Test the model
    try:
        from tensorflow.keras.models import load_model
        from pickle import load
        
        model = load_model('model.h5')
        print("  ✅ Model loaded successfully")
        
        tokenizer = load(open('tokenizer.pkl', 'rb'))
        vocab_size = len(tokenizer.word_index) + 1
        print(f"  ✅ Tokenizer loaded (vocab size: {vocab_size})")
        
        print("\n✅ Everything is ready!")
        print("Run: streamlit run app_enhanced.py")
        
    except Exception as e:
        print(f"  ❌ Error testing model: {e}")
        print("\n  The downloaded files may be corrupted.")
        print("  Restoring backups...")
        
        if os.path.exists('model_old.h5'):
            os.rename('model_old.h5', 'model.h5')
        if os.path.exists('tokenizer_old_backup.pkl'):
            os.rename('tokenizer_old_backup.pkl', 'tokenizer.pkl')
        
        print("  ✅ Backups restored")
else:
    print("\n" + "=" * 60)
    print("❌ DOWNLOAD FAILED")
    print("=" * 60)
    print("\nGitHub download failed (likely due to LFS).")
    print("\nAlternative options:")
    print("1. I'll create a training script to train a small model (2-3 hours)")
    print("2. You can manually download from Kaggle")
    print("3. Use Google Drive link (if available)")
    
    # Restore backups
    if os.path.exists('model_old.h5'):
        os.rename('model_old.h5', 'model.h5')
        print("\n✅ Restored original model.h5")
    if os.path.exists('tokenizer_old_backup.pkl'):
        os.rename('tokenizer_old_backup.pkl', 'tokenizer.pkl')
        print("✅ Restored original tokenizer.pkl")

print("\n" + "=" * 60)
