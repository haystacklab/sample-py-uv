from fastapi import FastAPI, HTTPException
import requests
import os

app = FastAPI(
    title="API Gateway Service",
    description="FastAPI service with uvicorn to call external APIs",
    version="1.0.0"
)


def basic_get_request():
    api_url = os.getenv('API_URL', 'https://jsonplaceholder.typicode.com/posts/1')
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        
        return {
            'success': True,
            'status_code': response.status_code,
            'data': response.json()
        }
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=408, detail="Request timed out")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


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
    try:
        return {
            'message': 'Hello, World!'
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        'status': 'healthy',
        'message': 'API is running',
        'server': 'uvicorn'
    }


@app.get("/api/get-data")
async def get_data_endpoint():
    result = basic_get_request()
    return result


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