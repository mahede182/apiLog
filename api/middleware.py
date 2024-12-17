from django.utils import timezone
from drf_api_logger.models import APILogsModel
import json

class CustomAPILoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip admin URLs
        if request.path.startswith('/admin/'):
            return self.get_response(request)

        # Record start time
        start_time = timezone.now()

        # Get the response
        response = self.get_response(request)

        # Calculate execution time
        execution_time = (timezone.now() - start_time).total_seconds()

        # Only log API requests
        if request.path.startswith('/api/'):
            try:
                # Get request body
                if request.body:
                    body = json.loads(request.body)
                else:
                    body = {}

                # Get response body
                if hasattr(response, 'content'):
                    try:
                        response_body = json.loads(response.content)
                    except:
                        response_body = response.content.decode('utf-8')
                else:
                    response_body = {}

                # Create log entry
                APILogsModel.objects.create(
                    api=request.path,
                    headers=json.dumps(dict(request.headers)),
                    body=json.dumps(body),
                    method=request.method,
                    status_code=response.status_code,
                    execution_time=execution_time,
                    response=json.dumps(response_body),
                    added_on=timezone.now()
                )
            except Exception as e:
                print(f"Error logging API request: {str(e)}")

        return response 