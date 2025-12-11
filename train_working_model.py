"""Train a working model quickly with available data"""
import numpy as np
from pickle import dump, load
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, LSTM, Embedding, Dropout, Add
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os

print("=" * 60)
print("TRAINING WORKING MODEL")
print("=" * 60)

# Load tokenizer
print("\n1. Loading tokenizer...")
tokenizer = load(open('tokenizer.pkl', 'rb'))
vocab_size = len(tokenizer.word_index) + 1
print(f"   Vocabulary size: {vocab_size}")

# Load features
print("\n2. Loading image features...")
features = load(open('features.pkl', 'rb'))
print(f"   Total images: {len(features)}")

# Load descriptions
print("\n3. Loading descriptions...")
descriptions = {}
with open('descriptions.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = line.split(' ', 1)
        if len(parts) >= 2:
            img_id = parts[0]
            caption = 'startseq ' + parts[1] + ' endseq'
            if img_id not in descriptions:
                descriptions[img_id] = []
            descriptions[img_id].append(caption)

print(f"   Total descriptions: {sum(len(v) for v in descriptions.values())}")

# Parameters
max_length = 20
embedding_dim = 256
lstm_units = 256

print(f"\n4. Model parameters:")
print(f"   Max length: {max_length}")
print(f"   Embedding dim: {embedding_dim}")
print(f"   LSTM units: {lstm_units}")
print(f"   Vocab size: {vocab_size}")

# Create data generator
def data_generator(descriptions, features, tokenizer, max_length, vocab_size):
    """Generate training data"""
    while True:
        for img_id, captions in descriptions.items():
            if img_id not in features:
                continue
            
            feature = features[img_id][0]
            
            for caption in captions:
                # Encode caption
                seq = tokenizer.texts_to_sequences([caption])[0]
                
                # Create input-output pairs
                for i in range(1, len(seq)):
                    in_seq = seq[:i]
                    out_seq = seq[i]
                    
                    # Pad input
                    in_seq = pad_sequences([in_seq], maxlen=max_length)[0]
                    
                    # One-hot encode output
                    out_seq = to_categorical([out_seq], num_classes=vocab_size)[0]
                    
                    yield [feature, in_seq], out_seq

# Build model
print("\n5. Building model...")

# Image feature input
input_img = Input(shape=(4096,))
img_dense = Dropout(0.5)(input_img)
img_dense = Dense(embedding_dim, activation='relu')(img_dense)

# Caption input
input_caption = Input(shape=(max_length,))
caption_embed = Embedding(vocab_size, embedding_dim, mask_zero=True)(input_caption)
caption_embed = Dropout(0.5)(caption_embed)
caption_lstm = LSTM(lstm_units)(caption_embed)

# Merge
merged = Add()([img_dense, caption_lstm])
merged = Dense(lstm_units, activation='relu')(merged)
output = Dense(vocab_size, activation='softmax')(merged)

# Create model
model = Model(inputs=[input_img, input_caption], outputs=output)
model.compile(loss='categorical_crossentropy', optimizer=Adam(learning_rate=0.001))

print("   ✅ Model built")
model.summary()

# Calculate steps
total_samples = sum(len(tokenizer.texts_to_sequences([cap])[0]) - 1 
                   for caps in descriptions.values() 
                   for cap in caps)
steps_per_epoch = max(total_samples // 32, 1)  # batch_size = 32

print(f"\n6. Training configuration:")
print(f"   Total training samples: {total_samples}")
print(f"   Steps per epoch: {steps_per_epoch}")
print(f"   Epochs: 20")

# Train model
print("\n7. Training model...")
print("   This will take 1-2 hours depending on your CPU...")
print("   You can stop anytime with Ctrl+C and the model will still work")

try:
    history = model.fit(
        data_generator(descriptions, features, tokenizer, max_length, vocab_size),
        steps_per_epoch=steps_per_epoch,
        epochs=20,
        verbose=1
    )
    
    print("\n✅ Training complete!")
    
except KeyboardInterrupt:
    print("\n\n⚠️  Training interrupted by user")
    print("   Saving current model state...")

# Save model
print("\n8. Saving model...")
model.save('model.h5')
print("   ✅ Model saved to model.h5")

# Test the model
print("\n9. Testing model...")
from utils.image_utils import FeatureExtractor
from utils.model_utils import CaptionGenerator
from PIL import Image

if os.path.exists('samples/beach.jpg'):
    image = Image.open('samples/beach.jpg')
    feature_extractor = FeatureExtractor()
    features_test = feature_extractor.extract_from_pil(image)
    
    caption_generator = CaptionGenerator(
        model=model,
        tokenizer=tokenizer,
        max_length=max_length,
        beam_width=3,
        use_beam_search=True
    )
    
    caption = caption_generator.generate(features_test)
    print(f"   Test caption: '{caption}'")

print("\n" + "=" * 60)
print("✅ MODEL TRAINING COMPLETE")
print("=" * 60)
print("\nYou can now run: streamlit run app_enhanced.py")
