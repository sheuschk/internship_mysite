from django.http import HttpResponseRedirect


def redirect(request):
    """Redirects everyone to the polls app index after starting this django app with the localhost.
    It does not fit perfectly in the mysite directory --> find better solution"""
    return HttpResponseRedirect("/polls")
