"""Rebuild tokenizer with proper word-level tokenization and startseq/endseq tokens."""
from tensorflow.keras.preprocessing.text import Tokenizer
from pickle import dump

def load_descriptions(filename):
    """Load descriptions from file."""
    descriptions = {}
    with open(filename, 'r') as f:
        for line in f:
            tokens = line.strip().split()
            if len(tokens) < 2:
                continue
            image_id = tokens[0]
            caption = ' '.join(tokens[1:])
            
            if image_id not in descriptions:
                descriptions[image_id] = []
            descriptions[image_id].append(caption)
    
    return descriptions

def create_tokenizer(descriptions):
    """Create tokenizer from descriptions with startseq and endseq."""
    # Flatten all descriptions into a single list
    all_captions = []
    for desc_list in descriptions.values():
        for desc in desc_list:
            # Add startseq and endseq to each caption
            all_captions.append(f'startseq {desc} endseq')
    
    print(f'Total captions: {len(all_captions)}')
    print(f'Sample caption: {all_captions[0]}')
    
    # Create and fit tokenizer
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(all_captions)
    
    return tokenizer

if __name__ == "__main__":
    print('Loading descriptions...')
    descriptions = load_descriptions('descriptions.txt')
    print(f'Loaded {len(descriptions)} images with descriptions')
    
    print('\nCreating tokenizer...')
    tokenizer = create_tokenizer(descriptions)
    
    vocab_size = len(tokenizer.word_index) + 1
    print(f'\nVocabulary size: {vocab_size}')
    print(f'Has startseq: {"startseq" in tokenizer.word_index}')
    print(f'Has endseq: {"endseq" in tokenizer.word_index}')
    
    if 'startseq' in tokenizer.word_index:
        print(f'startseq index: {tokenizer.word_index["startseq"]}')
    if 'endseq' in tokenizer.word_index:
        print(f'endseq index: {tokenizer.word_index["endseq"]}')
    
    # Show some sample words
    print('\nSample words from vocabulary:')
    for word, idx in list(tokenizer.word_index.items())[:20]:
        print(f'  {idx}: {word}')
    
    # Save tokenizer
    print('\nSaving tokenizer...')
    dump(tokenizer, open('tokenizer.pkl', 'wb'))
    print('Tokenizer saved successfully!')
