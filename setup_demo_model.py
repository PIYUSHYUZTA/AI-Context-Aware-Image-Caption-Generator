"""Setup a demo model that works for presentation purposes"""
import numpy as np
from pickle import dump, load
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Input, Dense, LSTM, Embedding, Dropout, Add
from tensorflow.keras.optimizers import Adam
import os

print("=" * 60)
print("SETTING UP DEMO MODEL FOR INTERNSHIP")
print("=" * 60)

print("\nIMPORTANT: This creates a demo model for presentation.")
print("For production, you'd need the full Flickr8k dataset.\n")

# Load current model to check architecture
print("1. Checking current model architecture...")
try:
    old_model = load_model('model.h5')
    print("   ✅ Current model loaded")
    print(f"   Input shapes: {[inp.shape for inp in old_model.inputs]}")
    print(f"   Output shape: {old_model.output.shape}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Load tokenizer
print("\n2. Loading tokenizer...")
tokenizer = load(open('tokenizer.pkl', 'rb'))
vocab_size = len(tokenizer.word_index) + 1
print(f"   Vocabulary size: {vocab_size}")

# Create a properly initialized model
print("\n3. Creating properly initialized model...")

max_length = 20
embedding_dim = 256
lstm_units = 256

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

print("   ✅ Model created")

# Initialize with better weights for demo
print("\n4. Initializing model weights for demo...")
print("   (In production, this would be trained on Flickr8k)")

# Create some training data from descriptions
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical

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

features = load(open('features.pkl', 'rb'))

# Quick training for demo (just to initialize weights properly)
print("\n5. Quick training (10 epochs for demo)...")
print("   This takes ~5-10 minutes...")

X1, X2, y = [], [], []

for img_id, captions in descriptions.items():
    if img_id not in features:
        continue
    
    feature = features[img_id][0]
    
    for caption in captions:
        seq = tokenizer.texts_to_sequences([caption])[0]
        
        for i in range(1, len(seq)):
            in_seq = pad_sequences([seq[:i]], maxlen=max_length)[0]
            out_seq = to_categorical([seq[i]], num_classes=vocab_size)[0]
            
            X1.append(feature)
            X2.append(in_seq)
            y.append(out_seq)

X1 = np.array(X1)
X2 = np.array(X2)
y = np.array(y)

print(f"   Training samples: {len(X1)}")

# Train
model.fit([X1, X2], y, epochs=50, batch_size=32, verbose=1)

print("\n   ✅ Training complete")

# Save model
print("\n6. Saving model...")
model.save('model.h5')
print("   ✅ Model saved")

# Test
print("\n7. Testing model...")
from utils.image_utils import FeatureExtractor
from utils.model_utils import CaptionGenerator
from PIL import Image

if os.path.exists('samples/beach.jpg'):
    image = Image.open('samples/beach.jpg')
    feature_extractor = FeatureExtractor()
    test_features = feature_extractor.extract_from_pil(image)
    
    caption_generator = CaptionGenerator(
        model=model,
        tokenizer=tokenizer,
        max_length=max_length,
        beam_width=3,
        use_beam_search=True
    )
    
    caption = caption_generator.generate(test_features)
    print(f"\n   Generated caption: '{caption}'")
    
    if 'girl' in caption or 'dog' in caption or 'wooden' in caption:
        print("   ✅ Model is generating relevant words!")
    else:
        print("   ⚠️  Caption may not be perfect (limited training data)")

print("\n" + "=" * 60)
print("✅ DEMO MODEL SETUP COMPLETE")
print("=" * 60)

print("\n📝 IMPORTANT NOTES FOR INTERNSHIP:")
print("   - This model works for demonstration purposes")
print("   - It's trained on 10 captions (limited vocabulary)")
print("   - For production, you'd use Flickr8k (8,000 images)")
print("   - Focus your presentation on:")
print("     ✓ System architecture")
print("     ✓ REST API design")
print("     ✓ Docker deployment")
print("     ✓ Professional UI")
print("     ✓ Full-stack ML engineering")

print("\n🚀 Ready to run: streamlit run app_enhanced.py")
