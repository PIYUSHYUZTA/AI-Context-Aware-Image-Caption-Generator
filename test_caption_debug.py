"""Debug script to test caption generation."""
import numpy as np
from pickle import load
from tensorflow.keras.models import load_model
from PIL import Image
import traceback

# Load models
print("Loading tokenizer...")
tokenizer = load(open('tokenizer.pkl', 'rb'))
print(f"Tokenizer loaded. Vocab size: {len(tokenizer.word_index)}")

print("\nLoading model...")
model = load_model('model.h5')
print("Model loaded successfully")
print(f"Model inputs: {[inp.shape for inp in model.inputs]}")
print(f"Model output: {model.output.shape}")

# Check tokenizer
print("\n=== Tokenizer Check ===")
print(f"Has 'startseq': {'startseq' in tokenizer.word_index}")
print(f"Has 'endseq': {'endseq' in tokenizer.word_index}")
if 'startseq' in tokenizer.word_index:
    print(f"startseq index: {tokenizer.word_index['startseq']}")
if 'endseq' in tokenizer.word_index:
    print(f"endseq index: {tokenizer.word_index['endseq']}")

# Test with dummy features
print("\n=== Testing Caption Generation ===")
try:
    # Create dummy image features (VGG16 output is 4096)
    dummy_features = np.random.rand(1, 4096)
    print(f"Dummy features shape: {dummy_features.shape}")
    
    # Try to generate caption
    max_length = 20
    in_text = 'startseq'
    
    print(f"\nStarting caption generation with max_length={max_length}")
    
    for i in range(5):  # Just test first 5 iterations
        print(f"\nIteration {i+1}:")
        print(f"  Current text: '{in_text}'")
        
        # Convert to sequence
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        print(f"  Sequence: {sequence}")
        
        # Pad sequence
        from tensorflow.keras.preprocessing.sequence import pad_sequences
        sequence = pad_sequences([sequence], maxlen=max_length)
        print(f"  Padded sequence shape: {sequence.shape}")
        
        # Predict
        print(f"  Predicting...")
        yhat = model.predict([dummy_features, sequence], verbose=0)
        print(f"  Prediction shape: {yhat.shape}")
        print(f"  Prediction sum: {np.sum(yhat)}")
        print(f"  Prediction max: {np.max(yhat)}")
        
        # Get predicted word
        yhat_idx = np.argmax(yhat)
        print(f"  Predicted index: {yhat_idx}")
        
        # Find word
        word = None
        for w, idx in tokenizer.word_index.items():
            if idx == yhat_idx:
                word = w
                break
        
        print(f"  Predicted word: '{word}'")
        
        if word is None or word == 'endseq':
            print("  Stopping (endseq or None)")
            break
        
        in_text += ' ' + word
    
    final_caption = in_text.replace('startseq', '').strip()
    print(f"\n=== FINAL CAPTION ===")
    print(f"'{final_caption}'")
    
except Exception as e:
    print(f"\n!!! ERROR !!!")
    print(f"Error: {e}")
    traceback.print_exc()
