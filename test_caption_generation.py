"""Test caption generation to debug the issue."""
from pickle import load
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

print("Loading tokenizer...")
tokenizer = load(open('tokenizer.pkl', 'rb'))
vocab_size = len(tokenizer.word_index) + 1
print(f"Vocabulary size: {vocab_size}")
print(f"Sample words: {list(tokenizer.word_index.items())[:10]}")

print("\nLoading model...")
model = load_model('model.h5')
print(f"Model input shapes: {[inp.shape for inp in model.inputs]}")
print(f"Model output shape: {model.output.shape}")

# Create dummy features
print("\nTesting with dummy features...")
dummy_features = np.random.rand(1, 4096).astype(np.float32)

# Try to generate caption
def word_for_id(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None

max_length = 34
in_text = 'startseq'

print(f"\nStarting caption generation...")
print(f"Initial text: '{in_text}'")

for i in range(max_length):
    # Encode input sequence
    sequence = tokenizer.texts_to_sequences([in_text])[0]
    print(f"Step {i}: Sequence = {sequence}")
    
    # Pad sequence
    sequence = pad_sequences([sequence], maxlen=max_length)
    
    # Predict next word
    yhat = model.predict([dummy_features, sequence], verbose=0)
    print(f"  Prediction shape: {yhat.shape}")
    print(f"  Max probability: {yhat.max():.4f}")
    
    # Get word with highest probability
    yhat = np.argmax(yhat)
    print(f"  Predicted index: {yhat}")
    
    # Map to word
    word = word_for_id(yhat, tokenizer)
    print(f"  Predicted word: '{word}'")
    
    if word is None:
        print("  ❌ Word not found in vocabulary!")
        break
    
    in_text += ' ' + word
    
    if word == 'endseq':
        print("  ✅ Found endseq, stopping")
        break

print(f"\nFinal caption: '{in_text}'")
print(f"Cleaned: '{in_text.replace('startseq', '').replace('endseq', '').strip()}'")
