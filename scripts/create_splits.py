"""Create train/val/test splits for the dataset."""
import os
import random
from pathlib import Path


def create_splits(
    images_dir: str = 'data/Images',
    output_dir: str = 'data',
    train_ratio: float = 0.8,
    val_ratio: float = 0.1,
    seed: int = 42
):
    """Create train/validation/test splits.
    
    Args:
        images_dir: Directory containing images
        output_dir: Output directory for split files
        train_ratio: Ratio for training set
        val_ratio: Ratio for validation set
        seed: Random seed for reproducibility
    """
    random.seed(seed)
    
    # Get all image files
    images_path = Path(images_dir)
    if not images_path.exists():
        print(f"❌ Images directory not found: {images_dir}")
        print("Please run download_dataset.py first")
        return
    
    image_files = list(images_path.glob('*.jpg'))
    print(f"Found {len(image_files)} images")
    
    # Shuffle
    random.shuffle(image_files)
    
    # Calculate split points
    n = len(image_files)
    train_end = int(n * train_ratio)
    val_end = train_end + int(n * val_ratio)
    
    # Split
    train_files = image_files[:train_end]
    val_files = image_files[train_end:val_end]
    test_files = image_files[val_end:]
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Save splits
    with open(output_path / 'train.txt', 'w') as f:
        f.write('\n'.join([img.name for img in train_files]))
    
    with open(output_path / 'val.txt', 'w') as f:
        f.write('\n'.join([img.name for img in val_files]))
    
    with open(output_path / 'test.txt', 'w') as f:
        f.write('\n'.join([img.name for img in test_files]))
    
    print(f"\n✅ Splits created successfully!")
    print(f"   Training:   {len(train_files)} images ({train_ratio*100:.0f}%)")
    print(f"   Validation: {len(val_files)} images ({val_ratio*100:.0f}%)")
    print(f"   Test:       {len(test_files)} images ({(1-train_ratio-val_ratio)*100:.0f}%)")
    print(f"\nFiles saved to:")
    print(f"   {output_path / 'train.txt'}")
    print(f"   {output_path / 'val.txt'}")
    print(f"   {output_path / 'test.txt'}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Create dataset splits')
    parser.add_argument('--images-dir', default='data/Images', help='Images directory')
    parser.add_argument('--output-dir', default='data', help='Output directory')
    parser.add_argument('--train-ratio', type=float, default=0.8, help='Training ratio')
    parser.add_argument('--val-ratio', type=float, default=0.1, help='Validation ratio')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    
    args = parser.parse_args()
    
    create_splits(
        images_dir=args.images_dir,
        output_dir=args.output_dir,
        train_ratio=args.train_ratio,
        val_ratio=args.val_ratio,
        seed=args.seed
    )
