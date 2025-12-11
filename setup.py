"""Setup script for Image Caption Generator."""
from setuptools import setup, find_packages

with open("README_PROFESSIONAL.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="image-caption-generator",
    version="2.0.0",
    author="AI Team",
    description="Enterprise-grade image captioning system powered by deep learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/image-caption-generator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Recognition",
    ],
    python_requires=">=3.8",
    install_requires=[
        "tensorflow>=2.16.0",
        "pillow>=10.0.0",
        "numpy>=1.26.0",
        "tqdm>=4.66.0",
        "matplotlib>=3.8.0",
        "nltk>=3.8.0",
        "streamlit>=1.28.0",
        "fastapi>=0.109.0",
        "uvicorn[standard]>=0.27.0",
        "python-multipart>=0.0.6",
        "pydantic>=2.5.0",
        "pyyaml>=6.0.0",
        "opencv-python>=4.9.0",
        "pandas>=2.2.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "flake8>=7.0.0",
            "black>=24.0.0",
        ],
        "viz": [
            "wordcloud>=1.9.0",
        ],
        "cache": [
            "redis>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "caption-api=api:main",
            "caption-train=train_improved:main",
        ],
    },
)
