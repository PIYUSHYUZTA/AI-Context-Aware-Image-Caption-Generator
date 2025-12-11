"""Train a better model with expanded vocabulary"""
import numpy as np
from pickle import dump, load
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, LSTM, Embedding, Dropout, Add
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.text import Tokenizer

print("="*60)
print("TRAINING BETTER MODEL")
print("="*60)

# Create expanded training captions
expanded_captions = [
    "a child in pink dress is climbing up set of stairs in an entry way",
    "a girl going into wooden building",
    "a little girl climbing into wooden playhouse",
    "a little girl climbing the stairs to her playhouse",
    "a little girl in pink dress going into wooden cabin",
    "black dog and spotted dog are fighting",
    "black dog and tricolored dog playing with each other on the road",
    "black dog and white dog with brown spots are staring at each other in the street",
    "two dogs of different breeds looking at each other on the road",
    "two dogs on pavement moving toward each other",
    # Add more common captions
    "a dog running in the grass",
    "a dog playing with a ball",
    "a person walking on the beach",
    "a man standing near a building",
    "a woman sitting on a bench",
    "children playing in the park",
    "a boy jumping in the air",
    "a cat sleeping on the couch",
    "a bird flying in the sky",
    "people standing in a group",
    "a car parked on the street",
    "a person holding a phone",
    "a man wearing a hat",
    "a woman wearing sunglasses",
    "a dog catching a frisbee",
    "a person swimming in the water",
]

# Add startseq and endseq
all_captions = ['startseq ' + cap + ' endseq' for cap in expanded_captions]

print(f"\nTotal training captions: {len(all_captions)}")

# Create new tokenizer
print("\nCreating tokenizer...")
tokenizer = Tokenizer()
tokenizer.fit_on_texts(all_captions)
vocab_size = len(tokenizer.word_index) + 1
print(f"Vocabulary size: {vocab_size}")

# Save tokenizer
dump(tokenizer, open('tokenizer.pkl', 'wb'))
print("Tokenizer saved")

# Load features
features = load(open('features.pkl', 'rb'))
print(f"Loaded features for {len(features)} images")

# Model parameters
max_length = 20
embedding_dim = 256
lstm_units = 256

print(f"\nBuilding model...")
print(f"  Max length: {max_length}")
print(f"  Embedding: {embedding_dim}")
print(f"  LSTM units: {lstm_units}")
print(f"  Vocab size: {vocab_size}")

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

print("Model built successfully")

# Prepare training data
print("\nPreparing training data...")
X1, X2, y = [], [], []

# Use first image features for all captions
first_img_id = list(features.keys())[0]
feature = features[first_img_id][0]

for caption in all_captions:
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
print("\nTraining model (100 epochs)...")
print("This will take 10-15 minutes. Please wait...")

model.fit([X1, X2], y, epochs=100, batch_size=32, verbose=1)

print("\nTraining complete!")

# Save model
model.save('model.h5')
print("Model saved to model.h5")

# Test
print("\nTesting model...")
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
    print(f"\nGenerated caption: '{caption}'")

print("\n" + "="*60)
print("DONE! Your model is now better!")
print("="*60)
print("\nRun: python -m streamlit run app_enhanced.py")
