class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        
        # Log request information
        print(f"Request path: {request.path}")
        print(f"Request method: {request.method}")
        print(f"Request headers: {request.headers}")

        response = self.get_response(request)
        
        print("\n\n")
        # Log response information
        print(f"Response status code: {response.status_code}")
        print(f"Response content type: {response.headers['Content-Type']}")

        # Code to be executed for each request/response after
        # the view is called.

        return response