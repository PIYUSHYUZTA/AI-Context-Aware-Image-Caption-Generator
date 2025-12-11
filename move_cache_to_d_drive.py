"""Move Hugging Face cache from C drive to D drive."""
import os
import shutil
from pathlib import Path

print("=" * 70)
print("MOVING HUGGING FACE CACHE FROM C: TO D:")
print("=" * 70)
print()

# Source (C drive)
c_cache = Path.home() / '.cache' / 'huggingface'
print(f"📂 Source: {c_cache}")

# Destination (D drive)
d_cache = Path('D:/huggingface_cache')
print(f"📂 Destination: {d_cache}")
print()

# Check if source exists
if not c_cache.exists():
    print("ℹ️  No cache found on C drive")
    print("   This is fine - cache will be created on D drive when needed")
    print()
else:
    # Get size
    total_size = sum(f.stat().st_size for f in c_cache.rglob('*') if f.is_file())
    size_gb = total_size / (1024**3)
    
    print(f"📊 Cache size: {size_gb:.2f} GB")
    print()
    
    # Ask user
    response = input("Move cache to D drive? (y/n): ").strip().lower()
    
    if response == 'y':
        print()
        print("🚀 Moving cache...")
        print("   This may take a few minutes...")
        print()
        
        try:
            # Create destination
            d_cache.mkdir(parents=True, exist_ok=True)
            
            # Copy files
            if (c_cache / 'hub').exists():
                print("   Copying models...")
                shutil.copytree(c_cache / 'hub', d_cache / 'hub', dirs_exist_ok=True)
                print("   ✅ Models copied")
            
            if (c_cache / 'transformers').exists():
                print("   Copying transformers...")
                shutil.copytree(c_cache / 'transformers', d_cache / 'transformers', dirs_exist_ok=True)
                print("   ✅ Transformers copied")
            
            print()
            print("✅ Cache moved successfully!")
            print()
            
            # Ask to delete old cache
            delete = input("Delete old cache from C drive? (y/n): ").strip().lower()
            if delete == 'y':
                print("   Deleting old cache...")
                shutil.rmtree(c_cache)
                print("   ✅ Old cache deleted")
                print()
        
        except Exception as e:
            print(f"❌ Error: {e}")
            print()
    else:
        print("   Skipped")
        print()

print("=" * 70)
print("CONFIGURATION")
print("=" * 70)
print()
print("Environment variables set in:")
print("  - app_enhanced.py")
print("  - utils/external_captioner.py")
print()
print("Cache location: D:/huggingface_cache")
print()
print("Next time you run the app, models will be:")
print("  - Loaded from D:/huggingface_cache (if already there)")
print("  - Downloaded to D:/huggingface_cache (if not there)")
print()
print("=" * 70)
print("✅ SETUP COMPLETE")
print("=" * 70)
print()
print("Restart the app to use D drive:")
print("  python -m streamlit run app_enhanced.py")
print()
