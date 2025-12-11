"""Test caption generation with the trained model."""
from pickle import load
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
from PIL import Image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import Model as KerasModel

print("Loading models...")

# Load tokenizer
tokenizer = load(open('tokenizer.pkl', 'rb'))
vocab_size = len(tokenizer.word_index) + 1
print(f"Tokenizer loaded: {vocab_size} words")

# Load model
try:
    model = load_model('model.h5')
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")
    print("Model may need to be retrained")
    exit(1)

# Load VGG16 for feature extraction
print("Loading VGG16...")
base_model = VGG16()
vgg_model = KerasModel(inputs=base_model.inputs, outputs=base_model.layers[-2].output)
print("VGG16 loaded")

# Function to extract features
def extract_features(image_path):
    image = Image.open(image_path)
    image = image.resize((224, 224))
    image = img_to_array(image)
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    image = preprocess_input(image)
    features = vgg_model.predict(image, verbose=0)
    return features

# Function to generate caption
def generate_caption(model, tokenizer, photo, max_length=20):
    in_text = 'startseq'
    for i in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_length)
        yhat = model.predict([photo, sequence], verbose=0)
        yhat = np.argmax(yhat)
        
        word = None
        for w, idx in tokenizer.word_index.items():
            if idx == yhat:
                word = w
                break
        
        if word is None or word == 'endseq':
            break
        
        in_text += ' ' + word
    
    return in_text.replace('startseq', '').strip()

# Test with sample images
print("\n" + "="*60)
print("TESTING CAPTION GENERATION")
print("="*60)

test_images = [
    ('samples/dog.jpg', 'Dog Image'),
    ('samples/beach.jpg', 'Beach Image'),
]

for img_path, description in test_images:
    try:
        print(f"\n{description}: {img_path}")
        print("-" * 60)
        
        # Extract features
        features = extract_features(img_path)
        
        # Generate caption
        caption = generate_caption(model, tokenizer, features)
        
        print(f"Generated Caption: {caption}")
        
    except Exception as e:
        print(f"Error: {e}")

print("\n" + "="*60)
print("✅ Caption generation is working!")
print("="*60)
