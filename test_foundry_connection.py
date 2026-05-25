"""
Test script to verify Foundry connection.

Run this first to make sure your Foundry deployment is reachable
and credentials are correctly configured.

Usage: python test_foundry_connection.py
"""

import asyncio
from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity.aio import AzureCliCredential

from contract_pilot.utils.config import load_config


async def test_connection():
    """Send a simple message to the Foundry agent and verify response."""
    
    print("📋 Loading configuration...")
    config = load_config()
    print(f"   Endpoint: {config.foundry_endpoint}")
    print(f"   Model: {config.foundry_model}")
    
    print("\n🔐 Authenticating with Azure...")
    async with AzureCliCredential() as credential:
        print("✓ Azure CLI credentials acquired")
        
        print("\n🤖 Creating chat client...")
        client = FoundryChatClient(credential=credential)
        
        print("✓ Client created")
        
        print("\n💬 Creating test agent...")
        async with Agent(
            client=client,
            name="TestAgent",
            instructions="You are a helpful assistant. Respond concisely.",
        ) as agent:
            print("✓ Agent created")
            
            print("\n🚀 Sending test message...")
            query = "What is 2 + 2? Answer in one short sentence."
            print(f"   User: {query}")
            
            result = await agent.run(query)
            
            print(f"\n   Agent: {result.text}")
            print("\n✅ Connection test successful!")


if __name__ == "__main__":
    asyncio.run(test_connection())