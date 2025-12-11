"""Restore the tokenizer that matches the model (vocab size 54)"""
from pickle import load, dump
import os

print("=" * 60)
print("RESTORING CORRECT TOKENIZER")
print("=" * 60)

# Check available tokenizer files
tokenizer_files = ['tokenizer.pkl', 'tokenizer_fixed.pkl', 'tokenizer_old.pkl']

print("\nChecking tokenizer files...")
for file in tokenizer_files:
    if os.path.exists(file):
        try:
            tok = load(open(file, 'rb'))
            vocab_size = len(tok.word_index) + 1
            print(f"  {file}: vocab_size = {vocab_size}")
            
            if vocab_size == 54:
                print(f"  ✅ MATCH! This tokenizer matches the model!")
                
                # Use this tokenizer
                if file != 'tokenizer.pkl':
                    # Backup current
                    if os.path.exists('tokenizer.pkl'):
                        os.rename('tokenizer.pkl', 'tokenizer_backup.pkl')
                    # Copy the correct one
                    import shutil
                    shutil.copy(file, 'tokenizer.pkl')
                    print(f"\n✅ Copied {file} to tokenizer.pkl")
                else:
                    print(f"\n✅ tokenizer.pkl already has correct vocab size")
                
                # Test it
                print("\nTesting tokenizer...")
                print(f"Vocabulary size: {vocab_size}")
                print(f"Sample words: {list(tok.word_index.items())[:20]}")
                
                break
        except Exception as e:
            print(f"  {file}: Error - {e}")
else:
    print("\n❌ No tokenizer with vocab_size=54 found!")
    print("You need to use the original tokenizer from training.")

print("\n" + "=" * 60)
