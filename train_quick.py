"""Quick training script to fix the model for caption generation."""
import numpy as np
from pickle import load, dump
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, LSTM, Embedding, Dropout, Add
from tensorflow.keras.optimizers import Adam

print("Loading data...")

# Load tokenizer
tokenizer = load(open('tokenizer.pkl', 'rb'))
vocab_size = len(tokenizer.word_index) + 1
print(f"Vocabulary size: {vocab_size}")

# Load features
all_features = load(open('features.pkl', 'rb'))
print(f"Loaded features for {len(all_features)} images")

# Load descriptions
descriptions = {}
with open('descriptions.txt', 'r') as f:
    for line in f:
        tokens = line.strip().split()
        if len(tokens) < 2:
            continue
        image_id = tokens[0]
        caption = ' '.join(tokens[1:])
        
        if image_id not in descriptions:
            descriptions[image_id] = []
        descriptions[image_id].append(f'startseq {caption} endseq')

print(f"Loaded {len(descriptions)} images with descriptions")

# Prepare training data
max_length = 20  # Maximum caption length

print("Preparing training sequences...")
X1, X2, y = [], [], []

for image_id, desc_list in descriptions.items():
    if image_id not in all_features:
        continue
    
    photo = all_features[image_id][0]
    
    for desc in desc_list:
        seq = tokenizer.texts_to_sequences([desc])[0]
        
        for i in range(1, len(seq)):
            in_seq = seq[:i]
            out_seq = seq[i]
            
            in_seq = pad_sequences([in_seq], maxlen=max_length)[0]
            out_seq = to_categorical([out_seq], num_classes=vocab_size)[0]
            
            X1.append(photo)
            X2.append(in_seq)
            y.append(out_seq)

X1 = np.array(X1)
X2 = np.array(X2)
y = np.array(y)

print(f"Training samples: {len(X1)}")
print(f"X1 shape: {X1.shape}")
print(f"X2 shape: {X2.shape}")
print(f"y shape: {y.shape}")

# Define model
print("\nBuilding model...")

# Image feature input
input1 = Input(shape=(4096,))
fe1 = Dropout(0.5)(input1)
fe2 = Dense(256, activation='relu')(fe1)

# Sequence input
input2 = Input(shape=(max_length,))
se1 = Embedding(vocab_size, 256, mask_zero=False)(input2)
se2 = Dropout(0.5)(se1)
se3 = LSTM(256)(se2)

# Merge
decoder1 = Add()([fe2, se3])
decoder2 = Dense(256, activation='relu')(decoder1)
outputs = Dense(vocab_size, activation='softmax')(decoder2)

# Create model
model = Model(inputs=[input1, input2], outputs=outputs)
model.compile(loss='categorical_crossentropy', optimizer=Adam(learning_rate=0.001))

print(model.summary())

# Train model
print("\nTraining model...")
print("This will take a few minutes...")

history = model.fit(
    [X1, X2],
    y,
    epochs=20,
    batch_size=32,
    verbose=1
)

# Save model
print("\nSaving model...")
model.save('model.h5')
print("Model saved to model.h5")

# Save training history
dump(history.history, open('training_history.pkl', 'wb'))
print("Training history saved")

print("\n✅ Training complete! The model is now ready to generate captions.")
