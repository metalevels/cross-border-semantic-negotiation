#!/usr/bin/env python3
"""
Example: Italy-Germany Birth Certificate Request
Demonstrates cross-border semantic negotiation for birth certificate requests.
"""

import asyncio
import sys
import os

# Add src to path for local development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from cross_border_implementation import (
        EuropeanDigitalServiceAgent,
        CitizenIdentity,
        CountryCode,
        DocumentType,
        IdentitySystem,
        ItalianANPRSchema
    )
    from datetime import datetime
except ImportError as e:
    print(f"Import error: {e}")
    print("Please install dependencies: pip install -r requirements.txt")
    sys.exit(1)


async def main():
    """Run the Italy-Germany demo."""
    print("🇮🇹 → 🇩🇪 Cross-Border Birth Certificate Demo")
    print("=" * 50)
    
    # Create Italian citizen
    marco = CitizenIdentity(
        citizen_id="RSSMRC85C15H501Z",
        country_of_origin=CountryCode.ITALY,
        identity_system=IdentitySystem.SPID,
        family_name="Rossi",
        given_names=["Marco"],
        date_of_birth=datetime(1985, 3, 15),
        place_of_birth="Roma",
        nationality="Italian",
        gender="M",
        national_id="RSSMRC85C15H501Z",
        eidas_identifier="IT/IT/RSSMRC85C15H501Z"
    )
    
    print(f"👤 Citizen: {marco.given_names[0]} {marco.family_name}")
    print(f"🆔 Identity System: {marco.identity_system.value}")
    print(f"🇮🇹 Source Country: {marco.country_of_origin.value}")
    
    # Create agent
    agent = EuropeanDigitalServiceAgent()
    print("🤖 Semantic negotiation agent initialized")
    
    # Process cross-border request
    print("🔄 Processing cross-border request...")
    request = await agent.process_cross_border_request(
        citizen=marco,
        target_country=CountryCode.GERMANY,
        document_type=DocumentType.BIRTH_CERTIFICATE,
        purpose="employment_verification"
    )
    
    print(f"✅ Request processed: {request.request_id}")
    print(f"📊 Confidence score: {request.confidence_score:.2f}")
    print(f"🎯 Status: {request.status}")
    print(f"🔀 Alignments found: {len(request.alignments)}")
    
    if request.status == "approved":
        print("🎉 Cross-border service provision successful!")
        print("   Marco can now proceed with his German job application.")
    else:
        print("⚠️ Manual review required for this request.")


if __name__ == "__main__":
    asyncio.run(main())
