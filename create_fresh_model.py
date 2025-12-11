"""Create a fresh working model"""
import numpy as np
from pickle import dump, load
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, LSTM, Embedding, Dropout, Add
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical

print("Creating fresh model...")

# Load tokenizer
tokenizer = load(open('tokenizer.pkl', 'rb'))
vocab_size = len(tokenizer.word_index) + 1
print(f"Vocabulary size: {vocab_size}")

# Parameters
max_length = 20
embedding_dim = 256
lstm_units = 256

# Build model
input_img = Input(shape=(4096,))
img_dense = Dropout(0.5)(input_img)
img_dense = Dense(embedding_dim, activation='relu')(img_dense)

input_caption = Input(shape=(max_length,))
caption_embed = Embedding(vocab_size, embedding_dim, mask_zero=False)(input_caption)
caption_embed = Dropout(0.5)(caption_embed)
caption_lstm = LSTM(lstm_units)(caption_embed)

merged = Add()([img_dense, caption_lstm])
merged = Dense(lstm_units, activation='relu')(merged)
output = Dense(vocab_size, activation='softmax')(merged)

model = Model(inputs=[input_img, input_caption], outputs=output)
model.compile(loss='categorical_crossentropy', optimizer=Adam(learning_rate=0.001))

print("Model created")

# Load training data
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

# Prepare training data
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

print(f"Training samples: {len(X1)}")

# Train
print("Training (50 epochs)...")
model.fit([X1, X2], y, epochs=50, batch_size=32, verbose=0)
print("Training complete")

# Save
model.save('model.h5', save_format='h5')
print("Model saved to model.h5")

# Test
print("\nTesting...")
from utils.image_utils import FeatureExtractor
from utils.model_utils import CaptionGenerator
from PIL import Image
import os

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
    print(f"Generated caption: '{caption}'")

print("\nDone! Run: streamlit run app_enhanced.py")
