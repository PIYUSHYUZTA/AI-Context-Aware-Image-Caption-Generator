"""Script to download and prepare Flickr8k dataset."""
import os
import zipfile
import requests
from pathlib import Path
from tqdm import tqdm


def download_file(url: str, destination: str):
    """Download file with progress bar."""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(destination, 'wb') as file, tqdm(
        desc=destination,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as progress_bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            progress_bar.update(size)


def extract_zip(zip_path: str, extract_to: str):
    """Extract zip file."""
    print(f"Extracting {zip_path}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print("Extraction complete!")


def setup_dataset():
    """Setup Flickr8k dataset."""
    # Create data directory
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)
    
    print("=" * 50)
    print("Flickr8k Dataset Setup")
    print("=" * 50)
    
    print("\nNote: You need to manually download Flickr8k dataset from:")
    print("https://www.kaggle.com/datasets/adityajn105/flickr8k")
    print("\nOr from the official source:")
    print("https://github.com/jbrownlee/Datasets/releases")
    
    print("\nAfter downloading:")
    print("1. Place 'Flickr8k_Dataset.zip' in the 'data' folder")
    print("2. Place 'Flickr8k_text.zip' in the 'data' folder")
    print("3. Run this script again to extract")
    
    # Check if files exist
    dataset_zip = data_dir / 'Flickr8k_Dataset.zip'
    text_zip = data_dir / 'Flickr8k_text.zip'
    
    if dataset_zip.exists():
        extract_zip(str(dataset_zip), str(data_dir))
    else:
        print(f"\n❌ {dataset_zip} not found")
    
    if text_zip.exists():
        extract_zip(str(text_zip), str(data_dir))
    else:
        print(f"\n❌ {text_zip} not found")
    
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("1. Run: python preprocess_captions.py")
    print("2. Run: python preprocess_images.py")
    print("3. Run: python train_improved.py")


if __name__ == "__main__":
    setup_dataset()
