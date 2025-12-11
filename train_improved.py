"""Improved training script with better data handling and monitoring."""
import os
import numpy as np
from pickle import load, dump
from pathlib import Path
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import load_model as keras_load_model
from tqdm import tqdm

from utils.config import config
from utils.logger import logger
from utils.data_utils import (
    load_set, load_clean_descriptions, load_doc, to_lines
)
from model import define_model, get_callbacks


def load_photo_features(filename: str, dataset: set) -> dict:
    """Load photo features for specific dataset.
    
    Args:
        filename: Path to features file
        dataset: Set of image IDs
        
    Returns:
        Dictionary of features
    """
    all_features = load(open(filename, 'rb'))
    features = {k: all_features[k] for k in dataset if k in all_features}
    logger.info(f"Loaded {len(features)} photo features")
    return features


def data_generator(
    descriptions: dict,
    photos: dict,
    tokenizer,
    max_length: int,
    vocab_size: int,
    batch_size: int = 32
):
    """Generate batches of training data.
    
    Args:
        descriptions: Dictionary of descriptions
        photos: Dictionary of photo features
        tokenizer: Fitted tokenizer
        max_length: Maximum sequence length
        vocab_size: Vocabulary size
        batch_size: Batch size
        
    Yields:
        Tuple of ([image_features, sequences], targets)
    """
    # Create list of all image IDs
    keys = list(descriptions.keys())
    
    while True:
        # Shuffle keys for each epoch
        np.random.shuffle(keys)
        
        for i in range(0, len(keys), batch_size):
            batch_keys = keys[i:i + batch_size]
            
            X1_batch, X2_batch, y_batch = [], [], []
            
            for key in batch_keys:
                if key not in photos:
                    continue
                
                # Get photo features
                photo = photos[key][0]
                
                # Process each description
                for desc in descriptions[key]:
                    seq = tokenizer.texts_to_sequences([desc])[0]
                    
                    # Create input-output pairs
                    for j in range(1, len(seq)):
                        in_seq, out_seq = seq[:j], seq[j]
                        in_seq = pad_sequences([in_seq], maxlen=max_length)[0]
                        out_seq = to_categorical([out_seq], num_classes=vocab_size)[0]
                        
                        X1_batch.append(photo)
                        X2_batch.append(in_seq)
                        y_batch.append(out_seq)
            
            if X1_batch:
                yield (
                    [np.array(X1_batch), np.array(X2_batch)],
                    np.array(y_batch)
                )


def calculate_steps(descriptions: dict, batch_size: int) -> int:
    """Calculate number of steps per epoch.
    
    Args:
        descriptions: Dictionary of descriptions
        batch_size: Batch size
        
    Returns:
        Number of steps
    """
    total_samples = 0
    for desc_list in descriptions.values():
        for desc in desc_list:
            total_samples += len(desc.split()) - 1
    
    steps = total_samples // batch_size
    logger.info(f"Total samples: {total_samples}, Steps per epoch: {steps}")
    return max(steps, 1)


def train_model(
    resume_from: str = None,
    use_validation: bool = True
):
    """Train the caption generation model.
    
    Args:
        resume_from: Path to model checkpoint to resume from
        use_validation: Whether to use validation set
    """
    logger.info("Starting training process...")
    
    # Load tokenizer
    tokenizer_path = config.get('paths.tokenizer_file')
    tokenizer = load(open(tokenizer_path, 'rb'))
    vocab_size = len(tokenizer.word_index) + 1
    logger.info(f"Vocabulary size: {vocab_size}")
    
    # Get configuration
    max_length = config.get('model.max_length', 34)
    epochs = config.get('training.epochs', 20)
    batch_size = config.get('training.batch_size', 32)
    
    # Load training data
    train_file = config.get('data.train_split', 'data/train.txt')
    if not Path(train_file).exists():
        logger.error(f"Training split file not found: {train_file}")
        logger.info("Please create train/test split files first")
        return
    
    train_ids = load_set(train_file)
    logger.info(f"Training images: {len(train_ids)}")
    
    # Load descriptions and features
    descriptions_file = config.get('paths.descriptions_file')
    train_descriptions = load_clean_descriptions(descriptions_file, train_ids)
    logger.info(f"Training descriptions: {len(train_descriptions)}")
    
    features_file = config.get('paths.features_file')
    train_features = load_photo_features(features_file, train_ids)
    logger.info(f"Training features: {len(train_features)}")
    
    # Calculate steps
    steps_per_epoch = calculate_steps(train_descriptions, batch_size)
    
    # Validation data
    validation_data = None
    validation_steps = None
    
    if use_validation:
        val_file = config.get('data.val_split', 'data/val.txt')
        if Path(val_file).exists():
            val_ids = load_set(val_file)
            val_descriptions = load_clean_descriptions(descriptions_file, val_ids)
            val_features = load_photo_features(features_file, val_ids)
            
            validation_steps = calculate_steps(val_descriptions, batch_size)
            validation_data = data_generator(
                val_descriptions,
                val_features,
                tokenizer,
                max_length,
                vocab_size,
                batch_size
            )
            logger.info(f"Validation images: {len(val_ids)}")
    
    # Create or load model
    if resume_from and Path(resume_from).exists():
        logger.info(f"Resuming from checkpoint: {resume_from}")
        model = keras_load_model(resume_from)
    else:
        logger.info("Creating new model...")
        model = define_model(
            vocab_size=vocab_size,
            max_length=max_length,
            embedding_dim=config.get('model.embedding_dim', 256),
            lstm_units=config.get('model.lstm_units', 256),
            dropout_rate=config.get('model.dropout_rate', 0.5),
            learning_rate=config.get('training.learning_rate', 0.001)
        )
    
    # Get callbacks
    callbacks = get_callbacks(config.get('training.checkpoint_dir', 'checkpoints'))
    
    # Create data generator
    train_generator = data_generator(
        train_descriptions,
        train_features,
        tokenizer,
        max_length,
        vocab_size,
        batch_size
    )
    
    # Train model
    logger.info(f"Training for {epochs} epochs...")
    
    try:
        history = model.fit(
            train_generator,
            epochs=epochs,
            steps_per_epoch=steps_per_epoch,
            validation_data=validation_data,
            validation_steps=validation_steps,
            callbacks=callbacks,
            verbose=1
        )
        
        # Save final model
        final_model_path = config.get('paths.model_file', 'model.h5')
        model.save(final_model_path)
        logger.info(f"Training complete! Model saved to {final_model_path}")
        
        # Save training history
        history_path = 'training_history.pkl'
        dump(history.history, open(history_path, 'wb'))
        logger.info(f"Training history saved to {history_path}")
        
    except KeyboardInterrupt:
        logger.info("Training interrupted by user")
        model.save('model_interrupted.h5')
        logger.info("Model saved to model_interrupted.h5")
    
    except Exception as e:
        logger.error(f"Error during training: {e}")
        raise


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Train image caption model')
    parser.add_argument(
        '--resume',
        type=str,
        default=None,
        help='Path to model checkpoint to resume from'
    )
    parser.add_argument(
        '--no-validation',
        action='store_true',
        help='Disable validation during training'
    )
    
    args = parser.parse_args()
    
    train_model(
        resume_from=args.resume,
        use_validation=not args.no_validation
    )
