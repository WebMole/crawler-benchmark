from flask import url_for, request

from project import app


def url_for_other_page(page_number):
    """url_for helper function for pagination"""
    args = request.view_args.copy()
    args['page_number'] = page_number
    return url_for(request.endpoint, **args)


app.jinja_env.globals['url_for_other_page'] = url_for_other_page