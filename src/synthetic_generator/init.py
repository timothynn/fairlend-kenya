"""
Synthetic data generation modules using GANs and other generative models
"""

from .fair_gan import FairDataGenerator
from .data_validator import DataValidator

__all__ = ["FairDataGenerator", "DataValidator"]
