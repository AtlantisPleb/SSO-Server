from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from oidc_provider.models import Client
from oidc_provider.lib.endpoints.authorize import AuthorizeEndpoint
from oidc_provider.lib.endpoints.token import TokenEndpoint
from oidc_provider.lib.endpoints.userinfo import UserInfoEndpoint
from oidc_provider.lib.errors import AuthorizeError, TokenError, UserInfoError
import logging

logger = logging.getLogger(__name__)

@login_required
@require_http_methods(["GET", "POST"])
def authorize(request):
    try:
        authorize = AuthorizeEndpoint(request)
        
        if request.method == 'GET':
            # Check if the user has already given consent
            if request.user.has_consented_to(authorize.client):
                return redirect(authorize.create_response_uri())
            
            # If not, show consent page
            params = authorize.validate_params()
            client = authorize.client
            return render(request, 'oidc/authorize.html', {
                'params': params,
                'client': client,
            })
        
        elif request.method == 'POST':
            # User has submitted the consent form
            if request.POST.get('allow', '') == 'Accept':
                # User gave consent, save it
                request.user.save_consent_for(authorize.client)
                uri = authorize.create_response_uri()
                return redirect(uri)
            else:
                # User denied consent
                raise AuthorizeError('access_denied', 'The user denied access to your application')
    
    except AuthorizeError as error:
        uri = error.create_uri(
            authorize.params.redirect_uri,
            authorize.params.state)
        return redirect(uri)
    except Exception as error:
        logger.exception("An error occurred in the authorize view")
        return JsonResponse({'error': 'server_error', 'error_description': str(error)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def token(request):
    try:
        token = TokenEndpoint(request)
        token_response = token.create_response()
        return JsonResponse(token_response)
    except TokenError as error:
        return JsonResponse(error.create_dict(), status=400)
    except Exception as error:
        logger.exception("An error occurred in the token view")
        return JsonResponse({'error': 'server_error', 'error_description': str(error)}, status=500)

@csrf_exempt
@require_http_methods(["GET", "POST"])
def userinfo(request):
    try:
        userinfo = UserInfoEndpoint(request)
        claims = userinfo.create_response()
        return JsonResponse(claims)
    except UserInfoError as error:
        return JsonResponse(error.create_dict(), status=400)
    except Exception as error:
        logger.exception("An error occurred in the userinfo view")
        return JsonResponse({'error': 'server_error', 'error_description': str(error)}, status=500)