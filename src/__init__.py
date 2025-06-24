"""
Cross-Border Semantic Negotiation Package

AI-driven semantic negotiation for EU digital public services.
Enables seamless cross-border digital service provision through
intelligent ontology alignment and data transformation.
"""

__version__ = "1.0.0"
__author__ = "Cross-Border Semantic Negotiation Team"
__email__ = "contact@semantic-negotiation.eu"

from .cross_border_implementation import (
    EuropeanDigitalServiceAgent,
    CitizenIdentity,
    CountryCode,
    DocumentType,
    IdentitySystem,
    CrossBorderRequest
)

__all__ = [
    "EuropeanDigitalServiceAgent",
    "CitizenIdentity", 
    "CountryCode",
    "DocumentType",
    "IdentitySystem",
    "CrossBorderRequest"
]
