from django.conf import settings as django_settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from oidc_provider import settings


def redirect(uri):
    """
    Custom Response object for redirecting to a Non-HTTP url scheme.
    """
    response = HttpResponse('', status=302)
    response['Location'] = uri
    return response


def get_issuer():
    """
    Construct the issuer full url. Basically is the site url with some path
    appended.
    """
    site_url = settings.get('SITE_URL')
    path = reverse('oidc_provider:provider_info') \
        .split('/.well-known/openid-configuration')[0]
    issuer = site_url + path

    return issuer


def get_rsa_key():
    """
    Load the rsa key previously created with `creatersakey` command.
    """
    file_path = settings.get('OIDC_RSA_KEY_FOLDER') + '/OIDC_RSA_KEY.pem'
    try:
        with open(file_path, 'r') as f:
            key = f.read()
    except IOError:
        raise IOError('We could not find your key file on: ' + file_path)

    return key


class DefaultUserInfo(object):
    """
    Default class for setting OIDC_USERINFO.
    """

    @classmethod
    def get_by_user(cls, user):
        return None


def default_sub_generator(user):
    """
    Default function for setting OIDC_IDTOKEN_SUB_GENERATOR.
    """
    return str(user.id)


def default_after_userlogin_hook(request, user, client):
    """
    Default function for setting OIDC_AFTER_USERLOGIN_HOOK.
    """
    return None
