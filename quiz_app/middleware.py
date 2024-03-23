from django.shortcuts import redirect
from django.urls import resolve

class RequireLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        
        # List of URLs to check for authentication
        auth_required_paths = [
            'quiz_list', 
            'take_quiz', 
            'quiz_score'
        ]
        
        if resolve(request.path_info).url_name in auth_required_paths:
            if not request.user.is_authenticated:
                login_url = '/login/'  # Ensure this matches your actual login URL
                redirect_url = f'{login_url}?next={request.path_info}'
                return redirect(redirect_url)
        
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
