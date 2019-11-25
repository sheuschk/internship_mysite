from django.http import HttpResponseRedirect


def redirect(request):
    """Redirects everyone to the polls app index after starting this django app with the localhost."""
    return HttpResponseRedirect("/polls")
