"""Model architecture definitions."""
from tensorflow.keras.models import Model
from tensorflow.keras.layers import (
    Input, Dense, LSTM, Embedding, Dropout, add,
    Bidirectional, BatchNormalization, Attention
)
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import (
    ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, TensorBoard
)
from pickle import load
from pathlib import Path
from utils.config import config
from utils.logger import logger


def define_model(
    vocab_size: int,
    max_length: int,
    embedding_dim: int = 256,
    lstm_units: int = 256,
    dropout_rate: float = 0.5,
    feature_dim: int = 4096,
    learning_rate: float = 0.001
) -> Model:
    """Define CNN-LSTM encoder-decoder model.
    
    Args:
        vocab_size: Size of vocabulary
        max_length: Maximum sequence length
        embedding_dim: Embedding dimension
        lstm_units: Number of LSTM units
        dropout_rate: Dropout rate
        feature_dim: Image feature dimension
        learning_rate: Learning rate for optimizer
        
    Returns:
        Compiled Keras model
    """
    # Image feature encoder
    inputs1 = Input(shape=(feature_dim,), name='image_features')
    fe1 = Dropout(dropout_rate)(inputs1)
    fe2 = Dense(embedding_dim, activation='relu', name='image_encoder')(fe1)
    fe3 = BatchNormalization()(fe2)

    # Sequence encoder
    inputs2 = Input(shape=(max_length,), name='text_input')
    se1 = Embedding(vocab_size, embedding_dim, mask_zero=True, name='embedding')(inputs2)
    se2 = Dropout(dropout_rate)(se1)
    se3 = LSTM(lstm_units, return_sequences=False, name='lstm')(se2)
    se4 = BatchNormalization()(se3)

    # Decoder
    decoder1 = add([fe3, se4])
    decoder2 = Dense(lstm_units, activation='relu', name='decoder_dense')(decoder1)
    decoder3 = Dropout(dropout_rate)(decoder2)
    outputs = Dense(vocab_size, activation='softmax', name='output')(decoder3)

    # Create and compile model
    model = Model(inputs=[inputs1, inputs2], outputs=outputs, name='image_caption_model')
    
    optimizer = Adam(learning_rate=learning_rate)
    model.compile(
        loss='categorical_crossentropy',
        optimizer=optimizer,
        metrics=['accuracy']
    )

    logger.info("Model architecture:")
    model.summary(print_fn=logger.info)
    
    return model


def define_model_with_attention(
    vocab_size: int,
    max_length: int,
    embedding_dim: int = 256,
    lstm_units: int = 256,
    dropout_rate: float = 0.5,
    feature_dim: int = 4096,
    learning_rate: float = 0.001
) -> Model:
    """Define CNN-LSTM model with attention mechanism.
    
    Args:
        vocab_size: Size of vocabulary
        max_length: Maximum sequence length
        embedding_dim: Embedding dimension
        lstm_units: Number of LSTM units
        dropout_rate: Dropout rate
        feature_dim: Image feature dimension
        learning_rate: Learning rate for optimizer
        
    Returns:
        Compiled Keras model with attention
    """
    # Image feature encoder
    inputs1 = Input(shape=(feature_dim,), name='image_features')
    fe1 = Dropout(dropout_rate)(inputs1)
    fe2 = Dense(embedding_dim, activation='relu')(fe1)
    fe3 = BatchNormalization()(fe2)

    # Sequence encoder with bidirectional LSTM
    inputs2 = Input(shape=(max_length,), name='text_input')
    se1 = Embedding(vocab_size, embedding_dim, mask_zero=True)(inputs2)
    se2 = Dropout(dropout_rate)(se1)
    se3 = Bidirectional(LSTM(lstm_units // 2, return_sequences=True))(se2)
    se4 = LSTM(lstm_units, return_sequences=False)(se3)
    se5 = BatchNormalization()(se4)

    # Decoder with attention
    decoder1 = add([fe3, se5])
    decoder2 = Dense(lstm_units, activation='relu')(decoder1)
    decoder3 = Dropout(dropout_rate)(decoder2)
    outputs = Dense(vocab_size, activation='softmax')(decoder3)

    model = Model(inputs=[inputs1, inputs2], outputs=outputs, name='attention_caption_model')
    
    optimizer = Adam(learning_rate=learning_rate)
    model.compile(
        loss='categorical_crossentropy',
        optimizer=optimizer,
        metrics=['accuracy']
    )

    logger.info("Attention model architecture:")
    model.summary(print_fn=logger.info)
    
    return model


def get_callbacks(checkpoint_dir: str = 'checkpoints') -> list:
    """Get training callbacks.
    
    Args:
        checkpoint_dir: Directory to save checkpoints
        
    Returns:
        List of Keras callbacks
    """
    Path(checkpoint_dir).mkdir(parents=True, exist_ok=True)
    Path('logs').mkdir(exist_ok=True)
    
    callbacks = [
        ModelCheckpoint(
            filepath=f'{checkpoint_dir}/model_{{epoch:02d}}_{{val_loss:.2f}}.h5',
            monitor='val_loss',
            save_best_only=True,
            mode='min',
            verbose=1
        ),
        EarlyStopping(
            monitor='val_loss',
            patience=config.get('training.early_stopping_patience', 5),
            restore_best_weights=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=3,
            min_lr=1e-7,
            verbose=1
        ),
        TensorBoard(
            log_dir='logs',
            histogram_freq=1,
            write_graph=True
        )
    ]
    
    return callbacks


if __name__ == "__main__":
    try:
        tokenizer = load(open('tokenizer.pkl', 'rb'))
        vocab_size = len(tokenizer.word_index) + 1
        max_length = config.get('model.max_length', 34)
        
        logger.info(f"Vocabulary size: {vocab_size}")
        logger.info(f"Max length: {max_length}")
        
        # Create standard model
        model = define_model(
            vocab_size=vocab_size,
            max_length=max_length,
            embedding_dim=config.get('model.embedding_dim', 256),
            lstm_units=config.get('model.lstm_units', 256),
            dropout_rate=config.get('model.dropout_rate', 0.5),
            learning_rate=config.get('training.learning_rate', 0.001)
        )
        
        model.save('model.h5')
        logger.info("Model saved to model.h5")
        
    except Exception as e:
        logger.error(f"Error creating model: {e}")
        raise
