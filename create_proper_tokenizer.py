"""Create a proper tokenizer with realistic vocabulary for image captioning"""
from pickle import dump
from tensorflow.keras.preprocessing.text import Tokenizer

print("Creating proper tokenizer for image captioning...")

# Common image captioning vocabulary (realistic captions)
sample_captions = [
    "startseq a dog is running in the grass endseq",
    "startseq a person is walking on the beach endseq",
    "startseq a child is playing with a ball endseq",
    "startseq a man is riding a bicycle endseq",
    "startseq a woman is sitting on a bench endseq",
    "startseq a cat is sleeping on the couch endseq",
    "startseq a bird is flying in the sky endseq",
    "startseq a car is parked on the street endseq",
    "startseq people are standing in a group endseq",
    "startseq a boy is jumping in the air endseq",
    "startseq a girl is smiling at the camera endseq",
    "startseq a dog is playing with another dog endseq",
    "startseq a person is holding a phone endseq",
    "startseq a man is wearing a hat endseq",
    "startseq a woman is wearing sunglasses endseq",
    "startseq children are playing in the park endseq",
    "startseq a dog is catching a frisbee endseq",
    "startseq a person is swimming in the water endseq",
    "startseq a man is standing near a building endseq",
    "startseq a woman is walking down the street endseq",
    "startseq a child in pink dress is climbing up set of stairs in an entry way endseq",
    "startseq a girl going into a wooden building endseq",
    "startseq a little girl climbing into a wooden playhouse endseq",
    "startseq a little girl climbing the stairs to her playhouse endseq",
    "startseq a little girl in a pink dress going into a wooden cabin endseq",
    "startseq two dogs are playing with each other on the road endseq",
    "startseq two black dogs are looking at each other endseq",
    "startseq a black dog and a white dog with brown spots are staring at each other in the street endseq",
    "startseq two dogs of different breeds looking at each other on the road endseq",
    "startseq two dogs on pavement moving toward each other endseq",
]

# Add more common words for better coverage
additional_words = [
    "the", "a", "an", "is", "are", "in", "on", "at", "with", "and", "or",
    "person", "people", "man", "woman", "child", "boy", "girl", "dog", "cat",
    "running", "walking", "sitting", "standing", "playing", "jumping", "smiling",
    "wearing", "holding", "looking", "moving", "going", "climbing",
    "red", "blue", "green", "yellow", "black", "white", "brown", "pink",
    "big", "small", "little", "large", "young", "old",
    "street", "road", "park", "beach", "building", "house", "water", "grass",
    "near", "next", "front", "behind", "under", "over", "through",
]

# Create comprehensive captions
all_captions = sample_captions.copy()
for word in additional_words:
    all_captions.append(f"startseq {word} endseq")

print(f"Total training captions: {len(all_captions)}")

# Create tokenizer
tokenizer = Tokenizer()
tokenizer.fit_on_texts(all_captions)

vocab_size = len(tokenizer.word_index) + 1
print(f"Vocabulary size: {vocab_size}")

# Save tokenizer
dump(tokenizer, open('tokenizer.pkl', 'wb'))
print("✅ Tokenizer saved to tokenizer.pkl")

# Test it
print("\nTesting tokenizer...")
test_caption = "startseq a dog is running in the grass endseq"
sequence = tokenizer.texts_to_sequences([test_caption])
print(f"Test caption: {test_caption}")
print(f"Sequence: {sequence[0]}")

# Reverse test
words = [tokenizer.index_word.get(i, '') for i in sequence[0]]
print(f"Decoded: {' '.join(words)}")

print("\n✅ Tokenizer created successfully!")
print(f"Vocabulary size: {vocab_size}")
