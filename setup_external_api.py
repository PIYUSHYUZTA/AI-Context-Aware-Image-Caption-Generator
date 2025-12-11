"""Automated setup script for external API support."""
import subprocess
import sys
from pathlib import Path

print("╔══════════════════════════════════════════════════════════════╗")
print("║     EXTERNAL API SETUP - Automated Installation Script      ║")
print("╚══════════════════════════════════════════════════════════════╝")
print()

def run_command(cmd, description):
    """Run a command and show progress."""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"✅ {description} - Success!")
            return True
        else:
            print(f"❌ {description} - Failed")
            print(f"   Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - Error: {e}")
        return False

# Step 1: Check Python version
print("Step 1: Checking Python version...")
version = sys.version_info
print(f"   Python {version.major}.{version.minor}.{version.micro}")
if version.major < 3 or (version.major == 3 and version.minor < 8):
    print("❌ Python 3.8+ required")
    sys.exit(1)
print("✅ Python version OK")
print()

# Step 2: Upgrade pip
print("Step 2: Upgrading pip...")
if run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip"):
    print()
else:
    print("⚠️  Pip upgrade failed, continuing anyway...")
    print()

# Step 3: Install packages
print("Step 3: Installing required packages...")
print("   This may take 5-10 minutes...")
print()

packages = [
    ("transformers", "Hugging Face Transformers"),
    ("torch", "PyTorch"),
    ("pillow", "Pillow (Image Processing)")
]

all_success = True
for package, description in packages:
    if not run_command(
        f"{sys.executable} -m pip install {package}",
        f"Installing {description}"
    ):
        all_success = False
    print()

if not all_success:
    print("⚠️  Some packages failed to install")
    print("   Try manual installation:")
    print("   pip install transformers torch pillow")
    print()
    sys.exit(1)

# Step 4: Verify installation
print("Step 4: Verifying installation...")
print()

try:
    import transformers
    print(f"✅ transformers {transformers.__version__}")
except ImportError:
    print("❌ transformers not found")
    all_success = False

try:
    import torch
    print(f"✅ torch {torch.__version__}")
except ImportError:
    print("❌ torch not found")
    all_success = False

try:
    from PIL import Image
    print(f"✅ pillow (PIL) installed")
except ImportError:
    print("❌ pillow not found")
    all_success = False

print()

if not all_success:
    print("❌ Installation verification failed")
    sys.exit(1)

# Step 5: Test external API
print("Step 5: Testing external API...")
print("   This will download the BLIP model (~1-2 GB)")
print()

response = input("   Download and test now? (y/n): ").strip().lower()
if response == 'y':
    print()
    if Path("test_external_api.py").exists():
        print("🚀 Running test...")
        print()
        subprocess.run([sys.executable, "test_external_api.py"])
    else:
        print("⚠️  test_external_api.py not found")
        print("   You can test manually later")
else:
    print("   Skipped. You can test later with:")
    print("   python test_external_api.py")

print()
print("╔══════════════════════════════════════════════════════════════╗")
print("║                    ✅ SETUP COMPLETE!                        ║")
print("╚══════════════════════════════════════════════════════════════╝")
print()
print("🎉 External API support is now installed!")
print()
print("Next steps:")
print("1. Run: streamlit run app_enhanced.py")
print("2. Select 'External API (BLIP)' in sidebar")
print("3. Upload an image and generate captions")
print()
print("📖 For more info, read: EXTERNAL_API_SETUP_GUIDE.md")
print()
