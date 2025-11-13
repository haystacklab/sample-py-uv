from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from typing import List, Dict, Optional
import os

class AzureOpenAIClient:
    def __init__(self, connection_string: Optional[str] = None):
        self.conn_str = connection_string or os.getenv("AZURE_AI_PROJECT_CONNECTION_STRING")
        if not self.conn_str:
            raise ValueError("Connection string is required")
        
        self.deployment_name = os.getenv("AZURE_AI_DEPLOYMENT_NAME")
        self.api_version="2025-01-01-preview"
        
        print(f"Initialized AIFoundryClient with deployment: {self.deployment_name}")
        print(f"Initialized AIFoundryClient with AZURE_AI_PROJECT_CONNECTION_STRING: {self.conn_str}")
        
        try:
            # Create token provider
            credential = DefaultAzureCredential()
            self.token_provider = get_bearer_token_provider(
                credential,
                "https://cognitiveservices.azure.com/.default"
            )
        except Exception as e:
            print(f"Failed to create token provider: {str(e)}")
        
        # Initialize client once
        try:
            self.client = AzureOpenAI(
                azure_endpoint=self.conn_str,
                azure_ad_token_provider=self.token_provider,
                api_version=self.api_version
            )
        except Exception as e:
            print(f"Failed to initialize AzureOpenAI: {str(e)}")
            
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 800,
        **kwargs
    ) -> str:
        try:
            response = self.client.chat.completions.create(
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=1.0,
                model=self.deployment_name
            )
            print(f"Response from llm api: {response.choices[0].message.content}")
            return response.choices[0].message.content
        except Exception as e:
            print(f"Chat completion failed: {str(e)}")
            raise Exception(f"Chat completion failed: {str(e)}")