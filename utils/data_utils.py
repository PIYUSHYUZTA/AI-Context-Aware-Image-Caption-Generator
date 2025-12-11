"""Data loading and processing utilities."""
from typing import Dict, List, Set
from pathlib import Path


def load_doc(filename: str) -> str:
    """Load document from file.
    
    Args:
        filename: Path to file
        
    Returns:
        File contents as string
    """
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()


def load_set(filename: str) -> Set[str]:
    """Load set of image IDs from file.
    
    Args:
        filename: Path to file with image IDs
        
    Returns:
        Set of image IDs
    """
    doc = load_doc(filename)
    dataset = set()
    
    for line in doc.split('\n'):
        if len(line) < 1:
            continue
        identifier = line.split('.')[0]
        dataset.add(identifier)
    
    return dataset


def load_clean_descriptions(filename: str, dataset: Set[str]) -> Dict[str, List[str]]:
    """Load cleaned descriptions for specific dataset.
    
    Args:
        filename: Path to descriptions file
        dataset: Set of image IDs to load
        
    Returns:
        Dictionary mapping image IDs to list of descriptions
    """
    doc = load_doc(filename)
    descriptions = {}
    
    for line in doc.split('\n'):
        tokens = line.split()
        if len(tokens) < 2:
            continue
            
        image_id = tokens[0]
        image_desc = tokens[1:]
        
        if image_id in dataset:
            if image_id not in descriptions:
                descriptions[image_id] = []
            
            desc = 'startseq ' + ' '.join(image_desc) + ' endseq'
            descriptions[image_id].append(desc)
    
    return descriptions


def to_lines(descriptions: Dict[str, List[str]]) -> List[str]:
    """Convert descriptions dictionary to list of strings.
    
    Args:
        descriptions: Dictionary of descriptions
        
    Returns:
        List of all description strings
    """
    all_desc = []
    for desc_list in descriptions.values():
        all_desc.extend(desc_list)
    return all_desc


def save_descriptions(descriptions: Dict[str, List[str]], filename: str) -> None:
    """Save descriptions to file.
    
    Args:
        descriptions: Dictionary of descriptions
        filename: Output file path
    """
    lines = []
    for key, desc_list in descriptions.items():
        for desc in desc_list:
            lines.append(f"{key} {desc}")
    
    data = '\n'.join(lines)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(data)


def create_train_test_split(
    image_ids: List[str],
    train_ratio: float = 0.8,
    val_ratio: float = 0.1,
    output_dir: str = 'data'
) -> None:
    """Create train/val/test split files.
    
    Args:
        image_ids: List of all image IDs
        train_ratio: Ratio for training set
        val_ratio: Ratio for validation set
        output_dir: Output directory
    """
    import random
    
    # Shuffle
    random.shuffle(image_ids)
    
    # Calculate split points
    n = len(image_ids)
    train_end = int(n * train_ratio)
    val_end = train_end + int(n * val_ratio)
    
    # Split
    train_ids = image_ids[:train_end]
    val_ids = image_ids[train_end:val_end]
    test_ids = image_ids[val_end:]
    
    # Save
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    with open(output_path / 'train.txt', 'w') as f:
        f.write('\n'.join([f"{id}.jpg" for id in train_ids]))
    
    with open(output_path / 'val.txt', 'w') as f:
        f.write('\n'.join([f"{id}.jpg" for id in val_ids]))
    
    with open(output_path / 'test.txt', 'w') as f:
        f.write('\n'.join([f"{id}.jpg" for id in test_ids]))
    
    print(f"Created splits: Train={len(train_ids)}, Val={len(val_ids)}, Test={len(test_ids)}")
