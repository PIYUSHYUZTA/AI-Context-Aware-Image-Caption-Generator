"""Check model compatibility with tokenizer."""
from tensorflow.keras.models import load_model
from pickle import load

print('Loading model...')
model = load_model('model.h5')
print('Model loaded successfully')

print('\nModel summary:')
model.summary()

print('\nLoading tokenizer...')
tokenizer = load(open('tokenizer.pkl', 'rb'))
vocab_size = len(tokenizer.word_index) + 1
print(f'Tokenizer vocab size: {vocab_size}')

# Check if model output matches vocab size
output_shape = model.output_shape
print(f'\nModel output shape: {output_shape}')
print(f'Expected vocab size: {vocab_size}')

if output_shape[-1] == vocab_size:
    print('✓ Model and tokenizer are compatible!')
else:
    print(f'✗ MISMATCH: Model expects {output_shape[-1]} but tokenizer has {vocab_size}')
    print('  The model needs to be retrained with the new tokenizer.')
