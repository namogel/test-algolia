from flask import Flask, request, jsonify
from reading import read
from settings import MAX_POPULAR_COUNT

app = Flask(__name__)


@app.route('/1/queries/count/<string:timestamp>', methods=['GET'])
def queries_count(timestamp):
    return jsonify({'count': read(timestamp, 1)['count']})


@app.route('/1/queries/popular/<string:timestamp>', methods=['GET'])
def queries_popular(timestamp):
    try:
        count = int(request.args.get('size', 3))
    except ValueError:
        response = {'detail': 'count is not a number'}
    else:
        if count > MAX_POPULAR_COUNT:
            response = {'detail': 'count max value: {}'.format(MAX_POPULAR_COUNT)}
        else:
            response = {'queries': read(timestamp, count)['queries']}

    return jsonify(response)
