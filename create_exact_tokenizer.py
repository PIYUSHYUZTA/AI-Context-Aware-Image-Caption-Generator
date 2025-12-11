"""Create tokenizer from descriptions.txt to match model vocab_size=54"""
from pickle import dump
from tensorflow.keras.preprocessing.text import Tokenizer

print("Creating tokenizer from descriptions.txt...")

# Load descriptions
with open('descriptions.txt', 'r') as f:
    lines = f.readlines()

# Parse captions
captions = []
for line in lines:
    line = line.strip()
    if not line:
        continue
    
    # Split image_id and caption
    parts = line.split(' ', 1)
    if len(parts) >= 2:
        caption = parts[1].strip()
        # Add start and end tokens
        caption = 'startseq ' + caption + ' endseq'
        captions.append(caption)

print(f"Total captions: {len(captions)}")
print("\nSample captions:")
for cap in captions[:3]:
    print(f"  - {cap}")

# Create tokenizer
tokenizer = Tokenizer()
tokenizer.fit_on_texts(captions)

vocab_size = len(tokenizer.word_index) + 1
print(f"\nVocabulary size: {vocab_size}")

# Show all words
print("\nComplete vocabulary:")
for word, idx in sorted(tokenizer.word_index.items(), key=lambda x: x[1]):
    print(f"  {idx}: {word}")

# Save tokenizer
dump(tokenizer, open('tokenizer.pkl', 'wb'))
print(f"\n✅ Tokenizer saved to tokenizer.pkl")

# Test
print("\nTesting...")
test_caption = captions[0]
sequence = tokenizer.texts_to_sequences([test_caption])
print(f"Test: {test_caption}")
print(f"Sequence: {sequence[0]}")

print(f"\n✅ Done! Vocabulary size: {vocab_size}")
if vocab_size == 54:
    print("✅ PERFECT MATCH with model!")
else:
    print(f"⚠️  Model expects 54, got {vocab_size}")
