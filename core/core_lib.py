import inspect
import json
import traceback

import requests
from bson import ObjectId
import logging

from django.conf import settings
from django.http import HttpResponse

from core.settings import IS_PRODUCTION_SERVER

logger = logging.getLogger(__name__)


def generate_unique_object_id():
    return str(ObjectId())


def return_multi_key_json_response(keys, values, http_response=True,
                                   response_status=requests.codes.ok):
    data = dict(zip(keys, values))
    if http_response is True:
        return HttpResponse(json.dumps(data), status=response_status)
    else:
        return data


def handle_exception(exception_object=None, raise_exception=False,
                     print_exception=False, http_response=True, error_data=None):
    errors = dict()
    errors['__all__'] = list()

    if error_data:
        logger.error(error_data)

    logger.error(traceback.format_exc())
    if print_exception is True and IS_PRODUCTION_SERVER is False:
        print(traceback.format_exc())

    try:
        # Print last function argument
        frames = inspect.trace()
        argvalues = inspect.getargvalues(frames[-1][0])
        if 'request' in argvalues.locals:
            _request = argvalues.locals['request']
            logger.info("Request USER:{}, POST:{}, GET:{}, Function Args:{}".format(
                _request.user, _request.POST, _request.GET, inspect.formatargvalues(*argvalues)))
        else:
            logger.error('Function Args: %s', inspect.formatargvalues(*argvalues))
    except Exception as ex:
        logger.exception(ex)

    if raise_exception is True and exception_object is not None:
        raise exception_object
    else:
        errors['__all__'] = "Something Went Wrong"

    # if rest_response is True:
    #     return return_multi_key_json_rest_response(['errors'], [errors], rest_response,
    #                                                response_status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if http_response is True:
        return return_multi_key_json_response(['errors'], [errors], http_response)
    else:
        return errors


def init_response_dict():
    return {'status': False,
            'cv': {},
            'ud': {},
            'errors': {'__all__': list()}}


def pagination_helper(data, default_count=settings.DEFAULT_PAGINATION_COUNT):
    try:
        page = data.get("page", 1)
        page = int(page) if int(page) >= 1 else 1
    except:
        page = 1

    try:
        count = data.get("count", default_count)
        count = int(count) if int(count) >= 1 else default_count
    except:
        count = default_count

    start = (page * count) - count
    limit = (page * count)

    return start, limit, page, count
