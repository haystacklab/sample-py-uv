import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from typing import List, Dict, Optional


class AIFoundryClient:
    def __init__(self, connection_string: Optional[str] = None):
        self.conn_str = connection_string or os.getenv("AZURE_AI_PROJECT_CONNECTION_STRING")
        if not self.conn_str:
            raise ValueError("Connection string is required")
        
        self.deployment_name = os.getenv("AZURE_AI_DEPLOYMENT_NAME")
        
        print(f"Initialized AIFoundryClient with deployment: {self.deployment_name}")
        print(f"Initialized AIFoundryClient with AZURE_AI_PROJECT_CONNECTION_STRING: {self.conn_str}")
        
        # Initialize client once
        try:
            self.client = AIProjectClient.from_connection_string(
                conn_str=self.conn_str,
                credential=DefaultAzureCredential()
            )
        except Exception as e:
            print(f"Failed to initialize AIFoundryClient: {str(e)}")
            
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 800,
        **kwargs
    ) -> str:
        """
        Get chat completion response.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            deployment_name: Model deployment name (uses instance default if not provided)
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            **kwargs: Additional parameters for the API
            
        Returns:
            str: The assistant's response text
        """
        try:
            response = self.client.inference.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Chat completion failed: {str(e)}")
    
    def chat_completion_full_response(
        self,
        messages: List[Dict[str, str]],
        deployment_name: Optional[str] = None,
        **kwargs
    ) -> dict:
        """
        Get full chat completion response object (for accessing metadata).
        
        Returns:
            dict: Full response object with choices, usage, etc.
        """
        model = deployment_name or self.deployment_name
        if not model:
            raise ValueError("deployment_name must be provided")
        
        try:
            response = self.client.inference.chat.completions.create(
                model=model,
                messages=messages,
                **kwargs
            )
            return response
            
        except Exception as e:
            print(f"Chat completion failed: {str(e)}")
            raise Exception(f"Chat completion failed: {str(e)}")