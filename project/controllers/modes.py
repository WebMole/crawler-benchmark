# -*- coding: utf-8 -*-
from os import abort

from flask import render_template, request

from project import app, config
from project.controllers.database import get_db
from project.controllers.form import CreateForm
from project.models.Pagination import Pagination
from project.tools.tools import get_specific_item


@app.route('/print', methods=['GET', 'POST'])
def printer():
    form = CreateForm(request.form)
    if request.method == 'POST' and form.validate():
        from project.models.Printer import Printer

        printer = Printer()
        printer.show_string(form.text.data)
        return render_template('printer/index.html')
    return render_template('printer/print.html', form=form)


@app.route("/modes/<string:mode>/", defaults={'page_number': None})
@app.route("/modes/<string:mode>/page/<int:page_number>")
def entries(mode, page_number):
    try:
        mode = get_specific_item(config.modes, "route", mode)
    except ValueError:
        return "invalid page"

    if not mode.get('enabled'):
        return "This mode is disabled"

    pagination = None
    mode_entries = None

    # todo: Chose if ajax_enabled and infinite_scroll_enabled configs are for each separate modes or globals
    ajax_enabled = config.ajax_enabled
    infinite_scroll_enabled = config.infinite_scroll_enabled

    if ajax_enabled and page_number is None:
        no_layout = False
    else:
        if ajax_enabled:
            no_layout = True
        else:  # AJAX is disabled
            no_layout = False
            infinite_scroll_enabled = False
            if page_number is None:
                page_number = 1
        db = get_db()

        cur = db.execute('select count(id) from ' + mode.get("route"))
        count = cur.fetchone()
        count_value = count[0]

        pagination = Pagination(
            page_number,
            config.pagination_entry_per_page,
            count_value
        )

        db = get_db()
        cur = db.execute(
            'select id, title, text from %s order by id desc limit %d offset %d' % (
                mode.get('route'),
                config.pagination_entry_per_page,
                (pagination.page - 1) * config.pagination_entry_per_page
            )
        )
        mode_entries = cur.fetchall()

        if not mode_entries and page_number != 1:
            abort(404)

    return render_template(
        'modes/' + mode.get('route') + '.html',
        pagination=pagination,
        entries=mode_entries,
        title=mode.get('name'),
        mode=mode.get('route'),
        config=config,
        ajaxOn=ajax_enabled,
        infiniteScrollOn=infinite_scroll_enabled,
        noLayout=no_layout
    )


@app.route("/modes/<string:mode>/<int:mode_id>")
def entry(mode, mode_id):
    try:
        mode = get_specific_item(config.modes, "route", mode)
    except ValueError:
        return "invalid page"

    if not mode.get('enabled'):
        return "This mode is disabled"

    db = get_db()
    cur = db.execute('select id, title, text from ' + mode.get('route') + ' where id = ' + str(mode_id))
    mode_entry = cur.fetchall()

    if not mode_entry:
        abort(404)

    return render_template(
        'modes/' + mode.get('route') + '.html',
        entries=mode_entry,
        title=mode.get('name')
    )