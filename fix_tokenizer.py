"""Fix the tokenizer to work properly with word-level tokens."""
from pickle import dump, load
from tensorflow.keras.preprocessing.text import Tokenizer

# Load the descriptions file if it exists
try:
    with open('descriptions.txt', 'r') as f:
        lines = f.readlines()
    
    # Extract all descriptions
    descriptions = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) > 1:
            desc = ' '.join(parts[1:])  # Skip image ID
            descriptions.append(desc)
    
    print(f"Found {len(descriptions)} descriptions")
    
    # Create proper tokenizer
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(descriptions)
    
    vocab_size = len(tokenizer.word_index) + 1
    print(f"Vocabulary size: {vocab_size}")
    print(f"Sample words: {list(tokenizer.word_index.items())[:20]}")
    
    # Save the fixed tokenizer
    dump(tokenizer, open('tokenizer_fixed.pkl', 'wb'))
    print("\n✅ Fixed tokenizer saved as 'tokenizer_fixed.pkl'")
    print("Rename it to 'tokenizer.pkl' to use it")
    
except FileNotFoundError:
    print("❌ descriptions.txt not found!")
    print("\nCreating a basic working tokenizer with common words...")
    
    # Create a basic tokenizer with common caption words
    sample_captions = [
        'startseq a dog is running in the park endseq',
        'startseq a cat is sitting on the mat endseq',
        'startseq a person is walking on the street endseq',
        'startseq a child is playing with a ball endseq',
        'startseq a bird is flying in the sky endseq',
        'startseq a car is parked on the road endseq',
        'startseq two people are standing near a building endseq',
        'startseq a man is riding a bicycle endseq',
        'startseq a woman is holding an umbrella endseq',
        'startseq a group of people are walking together endseq',
        'startseq a dog is jumping over a fence endseq',
        'startseq a cat is sleeping on a couch endseq',
        'startseq children are playing in a playground endseq',
        'startseq a person is sitting on a bench endseq',
        'startseq a dog is catching a frisbee endseq',
        'startseq people are walking on the beach endseq',
        'startseq a man is standing in front of a building endseq',
        'startseq a woman is walking down the street endseq',
        'startseq a child is running through the grass endseq',
        'startseq a dog is playing with a toy endseq',
    ]
    
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(sample_captions)
    
    vocab_size = len(tokenizer.word_index) + 1
    print(f"Vocabulary size: {vocab_size}")
    print(f"Sample words: {list(tokenizer.word_index.items())[:30]}")
    
    # Save the basic tokenizer
    dump(tokenizer, open('tokenizer_basic.pkl', 'wb'))
    print("\n✅ Basic tokenizer saved as 'tokenizer_basic.pkl'")
    print("Rename it to 'tokenizer.pkl' to use it")
