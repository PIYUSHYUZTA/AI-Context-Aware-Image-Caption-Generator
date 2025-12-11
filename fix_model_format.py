"""Fix model saving format"""
from tensorflow.keras.models import load_model
import tensorflow as tf

print("Fixing model format...")

# Load model
try:
    model = load_model('model.h5', compile=False)
    print("✅ Model loaded")
    
    # Recompile
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    print("✅ Model recompiled")
    
    # Save in new format
    model.save('model.h5', save_format='h5')
    print("✅ Model saved in compatible format")
    
    # Test loading
    test_model = load_model('model.h5')
    print("✅ Model loads successfully")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nTrying alternative fix...")
    
    # Alternative: save as .keras format
    try:
        model = load_model('model.h5', compile=False)
        model.compile(loss='categorical_crossentropy', optimizer='adam')
        model.save('model_fixed.keras')
        print("✅ Saved as model_fixed.keras")
    except Exception as e2:
        print(f"❌ Alternative also failed: {e2}")

print("\nDone!")
