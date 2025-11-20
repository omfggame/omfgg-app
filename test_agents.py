"""
Quick test of agents to verify API keys and basic functionality
"""

import os
from dotenv import load_dotenv
import asyncio
from agents import CharacterAgent

load_dotenv('.env.local')

async def test_apis():
    """Test both OpenAI and Anthropic APIs"""
    print("Testing API connections...\n")

    # Check keys
    openai_key = os.getenv('OPENAI_API_KEY')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')

    print(f"OpenAI API Key: {'✓ Found' if openai_key else '✗ Missing'}")
    print(f"Anthropic API Key: {'✓ Found' if anthropic_key else '✗ Missing'}\n")

    if not openai_key and not anthropic_key:
        print("No API keys found. Please add them to .env.local")
        return

    agent = CharacterAgent()

    # Test OpenAI if key exists
    if openai_key:
        print("Testing OpenAI (gpt-4o-mini)...")
        try:
            result = await agent.generate(
                subject="happy cloud",
                mode="Relaxing",
                provider="openai"
            )
            print(f"✓ OpenAI Success!")
            print(f"Response preview: {result[:200]}...\n")
        except Exception as e:
            print(f"✗ OpenAI Error: {e}\n")

    # Test Anthropic if key exists
    if anthropic_key:
        print("Testing Anthropic (claude-haiku-4-5)...")
        try:
            result = await agent.generate(
                subject="happy cloud",
                mode="Relaxing",
                provider="anthropic"
            )
            print(f"✓ Anthropic Success!")
            print(f"Response preview: {result[:200]}...\n")
        except Exception as e:
            print(f"✗ Anthropic Error: {e}\n")

    print("API tests complete!")

if __name__ == "__main__":
    asyncio.run(test_apis())
