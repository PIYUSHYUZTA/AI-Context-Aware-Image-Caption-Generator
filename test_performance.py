"""Quick performance test for caption generation."""
import time
import numpy as np
from pickle import load
from tensorflow.keras.models import load_model
from utils.config import config
from utils.model_utils import CaptionGenerator

print("Loading models...")
start = time.time()
tokenizer = load(open(config.get('paths.tokenizer_file'), 'rb'))
model = load_model(config.get('paths.model_file'))
print(f"Models loaded in {time.time() - start:.2f}s")

# Create dummy features (simulating VGG16 output)
dummy_features = np.random.rand(1, 4096)

# Test greedy search
print("\nTesting Greedy Search...")
generator = CaptionGenerator(
    model=model,
    tokenizer=tokenizer,
    max_length=20,
    use_beam_search=False
)
start = time.time()
caption = generator.generate(dummy_features)
elapsed = time.time() - start
print(f"Caption: {caption}")
print(f"Time: {elapsed:.2f}s")

# Test beam search
print("\nTesting Beam Search (width=3)...")
generator = CaptionGenerator(
    model=model,
    tokenizer=tokenizer,
    max_length=20,
    beam_width=3,
    use_beam_search=True
)
start = time.time()
caption = generator.generate(dummy_features)
elapsed = time.time() - start
print(f"Caption: {caption}")
print(f"Time: {elapsed:.2f}s")

print("\n✅ Performance test complete!")
