import functools
import traceback

from django.db import transaction
from django.http import JsonResponse
from django.core.mail import send_mail

JSON_DUMPS_PARAMS = {
    'ensure_ascii': False
}


def ret(json_object, status=200):
    return JsonResponse(
        json_object,
        status=status,
        safe=not isinstance(json_object, list),
        json_dumps_params=JSON_DUMPS_PARAMS
    )


def error_response(exception):
    res = {"errorMessage": str(exception),
           "traceback": traceback.format_exc()}
    return ret(res, status=400)


def send_error_mail(exception):
    res = f"{exception}\n{traceback.format_exc()}"
    send_mail('Ошибка', res, 'dima.danilov1928@gmail.com',
              ['megs.dima.da14@gmail.com'], fail_silently=False)
    res = {"errorMessage": str(exception)}
    return ret(res, status=400)


def base_view(fn):
    @functools.wraps(fn)
    def inner(request, *args, **kwargs):
        try:
            with transaction.atomic():
                return fn(request, *args, **kwargs)
        except Exception as e:
            return send_error_mail(e)

    return inner
