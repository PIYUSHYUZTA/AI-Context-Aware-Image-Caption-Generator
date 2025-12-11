"""Check model architecture and compatibility"""
from tensorflow.keras.models import load_model
from pickle import load

print("=" * 60)
print("CHECKING MODEL ARCHITECTURE")
print("=" * 60)

# Load tokenizer
tokenizer = load(open('tokenizer.pkl', 'rb'))
vocab_size = len(tokenizer.word_index) + 1
print(f"\nTokenizer vocabulary size: {vocab_size}")

# Load model
model = load_model('model.h5')
print(f"\nModel loaded successfully")

# Check model architecture
print("\nModel Summary:")
print("-" * 60)
model.summary()

# Check output layer
print("\n" + "=" * 60)
print("CHECKING OUTPUT LAYER")
print("=" * 60)

output_shape = model.output_shape
print(f"Model output shape: {output_shape}")

if isinstance(output_shape, tuple) and len(output_shape) > 1:
    model_vocab_size = output_shape[-1]
    print(f"Model vocabulary size: {model_vocab_size}")
    
    if model_vocab_size != vocab_size:
        print(f"\n❌ MISMATCH!")
        print(f"   Tokenizer vocab: {vocab_size}")
        print(f"   Model vocab: {model_vocab_size}")
        print(f"\n   The model was trained with a different tokenizer!")
        print(f"   You need to either:")
        print(f"   1. Use the original tokenizer that matches the model")
        print(f"   2. Retrain the model with the current tokenizer")
    else:
        print(f"\n✅ Vocabulary sizes match!")
else:
    print(f"\n⚠️  Could not determine model vocabulary size")

print("\n" + "=" * 60)
