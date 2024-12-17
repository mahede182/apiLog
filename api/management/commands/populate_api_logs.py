from django.core.management.base import BaseCommand
from django.utils import timezone
from drf_api_logger.models import APILogsModel
import random
import json
from decimal import Decimal, ROUND_DOWN

class Command(BaseCommand):
    help = 'Populate DRF API Logger with sample data'

    def handle(self, *args, **options):
        # Sample endpoints
        endpoints = [
            '/api/notes/',
            '/api/test-logging/',
            '/api/users/',
            '/api/auth/login/',
            '/api/auth/logout/'
        ]

        # Sample methods
        methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']

        # Sample status codes
        status_codes = [200, 201, 400, 401, 403, 404, 500]

        # Sample response data
        response_data = [
            {'message': 'Success'},
            {'error': 'Not found'},
            {'data': {'id': 1, 'title': 'Test'}},
            {'status': 'completed'},
            {'result': 'Operation successful'}
        ]

        # Sample request bodies
        request_bodies = [
            {'title': 'Test Note', 'content': 'This is a test note'},
            {'username': 'testuser', 'password': 'testpass'},
            {'email': 'test@example.com'},
            {'status': 'active'},
            {'data': {'key': 'value'}}
        ]

        # Create 50 sample log entries
        for i in range(50):
            # Random execution time between 0.1 and 2.0 seconds
            execution_time = Decimal(str(round(random.uniform(0.1, 2.0), 3)))
            
            # Random endpoint and method
            endpoint = random.choice(endpoints)
            method = random.choice(methods)
            
            # Status code based on method
            if method == 'GET':
                status_code = random.choice([200, 404, 401])
            elif method == 'POST':
                status_code = random.choice([201, 400, 401])
            else:
                status_code = random.choice(status_codes)

            try:
                # Create log entry
                APILogsModel.objects.create(
                    api=endpoint,
                    method=method,
                    status_code=status_code,
                    execution_time=execution_time,
                    added_on=timezone.now(),
                    response=json.dumps(random.choice(response_data)),
                    headers=json.dumps({
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer sample-token',
                        'User-Agent': 'Mozilla/5.0'
                    }),
                    body=json.dumps(random.choice(request_bodies))  # Always include a body
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Created log entry {i+1}/50')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating log entry: {str(e)}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully created 50 sample API log entries')
        ) 