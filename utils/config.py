"""Configuration management utilities."""
import yaml
from pathlib import Path
from typing import Any, Dict


class Config:
    """Configuration manager for the application."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize configuration from YAML file.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = Path(config_path)
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot notation key.
        
        Args:
            key: Configuration key (e.g., 'model.vocab_size')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        
        return value if value is not None else default
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value by dot notation key.
        
        Args:
            key: Configuration key (e.g., 'model.vocab_size')
            value: Value to set
        """
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self) -> None:
        """Save configuration to YAML file."""
        with open(self.config_path, 'w') as f:
            yaml.dump(self._config, f, default_flow_style=False)
    
    @property
    def model(self) -> Dict[str, Any]:
        """Get model configuration."""
        return self._config.get('model', {})
    
    @property
    def training(self) -> Dict[str, Any]:
        """Get training configuration."""
        return self._config.get('training', {})
    
    @property
    def data(self) -> Dict[str, Any]:
        """Get data configuration."""
        return self._config.get('data', {})
    
    @property
    def inference(self) -> Dict[str, Any]:
        """Get inference configuration."""
        return self._config.get('inference', {})
    
    @property
    def paths(self) -> Dict[str, Any]:
        """Get paths configuration."""
        return self._config.get('paths', {})


# Global config instance
config = Config()
