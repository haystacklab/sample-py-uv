from fastapi import FastAPI, HTTPException
import os
from Chat import AIFoundryClient

app = FastAPI(
    title="API Gateway Service",
    description="FastAPI service with uvicorn to call external APIs",
    version="1.0.0"
)


@app.get("/")
async def root():
    """Root endpoint with API documentation"""
    return {
        'message': 'FastAPI Server with Uvicorn',
        'endpoints': {
            '/': 'This help message',
            '/docs': 'Interactive API documentation (Swagger UI)',
            '/redoc': 'Alternative API documentation (ReDoc)',
            '/health': 'Health check',
            '/api/get-data': 'Call basic_get_request and return response',
            '/api/get-data-custom': 'Call API with custom URL (query param: url)'
        },
        'example': 'curl http://localhost:8000/api/get-data'
    }
    
@app.post("/chat")
async def chat(request: dict):
    """
    {
        message: message,
        model: settings.model,
        temperature: settings.temperature,
        max_tokens: settings.maxTokens,
      }
    """
    messages = [{"role": "user", "content": request['message']}]
    print(f"Received chat request: {request['message']}")
    try:
        client = AIFoundryClient()
        response = client.chat_completion(
            messages=messages,
            temperature=request['temperature'],
            max_tokens=request['max_tokens']
        )
        if response:
            return {
                'message': response
            }
        else:
            return {
                'message': 'Hello, World1!'
            }
    except Exception as e:
        print(f"Error in /chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        'status': 'healthy',
        'message': 'API is running',
        'server': 'uvicorn'
    }

if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment variables
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 8000))
    
    # Run with uvicorn
    uvicorn.run(
        app,
        host=host,
        port=port
    )