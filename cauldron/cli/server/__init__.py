import os
import sys

import flask
from flask import Flask
from flask import request

MY_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
sys.path.append(
    os.path.abspath(os.path.join(MY_DIRECTORY, '..'))
)

from cauldron.cli import commands
from cauldron.environ.response import Response
from cauldron.environ import logger

APPLICATION = Flask('Cauldron')


@APPLICATION.route('/', methods=['GET', 'POST'])
def execute():
    """

    :return:
    """

    r = Response()

    cmd = None
    parts = None
    name = None
    args = None
    request_args = None
    try:
        request_args = request.get_json(silent=True)
        if not request_args:
            request_args = request.values

        cmd = request_args.get('command', '')
        parts = [x.strip() for x in cmd.split(' ', 1)]
        name = parts[0].lower()

        args = request_args.get('args', '')
        if not isinstance(args, str):
            args = ' '.join(args)
        args += ' {}'.format(parts[1] if len(parts) > 1 else '').strip()
    except Exception as err:
        r.fail().notify(
            kind='ERROR',
            code='INVALID_COMMAND',
            message='Unable to parse command'
        ).kernel(
            cmd=cmd if cmd else '',
            parts=parts,
            name=name,
            args=args,
            error=str(err),
            mime_type='{}'.format(request.mimetype),
            request_data='{}'.format(request.data),
            request_args=request_args
        )
        return flask.jsonify(r.serialize())

    try:
        commands.execute(name, args, r)
    except Exception as err:
        r.fail().notify(
            kind='ERROR',
            code='KERNEL_EXECUTION_FAILURE',
            message='Unable to execute command'
        ).kernel(
            cmd=cmd,
            parts=parts,
            name=name,
            args=args,
            error=str(err),
            stack=logger.get_error_stack()
        )

    return flask.jsonify(r.serialize())


def run(port: int = 5010):
    """

    :param port:
    :return:
    """

    APPLICATION.debug = True
    APPLICATION.run(port=port)