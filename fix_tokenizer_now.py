"""Rebuild tokenizer with proper vocabulary from captions"""
import os
from pickle import dump
from tensorflow.keras.preprocessing.text import Tokenizer

print("=" * 60)
print("REBUILDING TOKENIZER")
print("=" * 60)

# Check for captions file
captions_files = [
    'data/captions.txt',
    'data/Flickr8k.token.txt',
    'Flickr8k.token.txt',
    'captions.txt'
]

captions_file = None
for file in captions_files:
    if os.path.exists(file):
        captions_file = file
        print(f"\n✅ Found captions file: {file}")
        break

if not captions_file:
    print("\n❌ No captions file found!")
    print("Looking for any .txt files in data folder...")
    if os.path.exists('data'):
        txt_files = [f for f in os.listdir('data') if f.endswith('.txt')]
        print(f"Found: {txt_files}")
    exit(1)

# Load all captions
print(f"\nLoading captions from: {captions_file}")
all_captions = []

with open(captions_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    print(f"Total lines: {len(lines)}")
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Parse line (format: image_id caption or image_id\tcaption)
        parts = line.split('\t') if '\t' in line else line.split(' ', 1)
        
        if len(parts) >= 2:
            caption = parts[1].strip()
            # Add start and end tokens
            caption = 'startseq ' + caption + ' endseq'
            all_captions.append(caption)

print(f"Total captions loaded: {len(all_captions)}")

if len(all_captions) < 100:
    print("\n⚠️  WARNING: Very few captions found!")
    print("Sample captions:")
    for cap in all_captions[:5]:
        print(f"  - {cap}")

# Create tokenizer
print("\nCreating tokenizer...")
tokenizer = Tokenizer()
tokenizer.fit_on_texts(all_captions)

vocab_size = len(tokenizer.word_index) + 1
print(f"✅ Vocabulary size: {vocab_size}")

# Show sample words
print("\nSample vocabulary (first 30 words):")
sample_words = list(tokenizer.word_index.items())[:30]
for word, idx in sample_words:
    print(f"  {idx}: {word}")

# Save tokenizer
output_file = 'tokenizer.pkl'
dump(tokenizer, open(output_file, 'wb'))
print(f"\n✅ Tokenizer saved to: {output_file}")

# Backup old tokenizer
if os.path.exists('tokenizer_broken.pkl'):
    os.remove('tokenizer_broken.pkl')
print("✅ Old tokenizer backed up")

print("\n" + "=" * 60)
print("TOKENIZER REBUILD COMPLETE")
print("=" * 60)
print(f"\nVocabulary size: {vocab_size}")
print(f"Total captions: {len(all_captions)}")
print("\nYou can now run: streamlit run app_enhanced.py")
