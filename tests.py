from parsing import Parser
from reading import read


def setup():
    parser = Parser(folder='tests')
    logs = '\n'.join([
        '\n'.join('{}\t{}'.format(timestamp, value) for _ in range(number))
        for timestamp, value, number in [
            ('2015-08-01 00:00:00', 'query1', 10),
            # test minutes
            ('2015-08-01 00:00:01', 'query2', 4),
            ('2015-08-01 00:00:02', 'query3', 3),
            ('2015-08-01 00:00:03', 'query4', 2),
            ('2015-08-01 00:00:04', 'query5', 1),
            # test hours
            ('2015-08-01 00:01:00', 'query6', 5),
            ('2015-08-01 00:02:00', 'query7', 3),
            ('2015-08-01 00:03:00', 'query8', 2),
            ('2015-08-01 00:04:00', 'query9', 1),
            # test day
            ('2015-08-01 01:00:00', 'query10', 6),
            ('2015-08-01 02:00:00', 'query11', 3),
            ('2015-08-01 03:00:00', 'query12', 2),
            ('2015-08-01 04:00:00', 'query13', 1),
            # test months
            ('2015-08-02 00:00:00', 'query14', 7),
            ('2015-08-03 00:00:00', 'query15', 3),
            ('2015-08-04 00:00:00', 'query16', 2),
            ('2015-08-05 00:00:00', 'query17', 1),
            # test years
            ('2015-09-01 00:00:00', 'query18', 8),
            ('2015-10-01 00:00:00', 'query19', 3),
            ('2015-11-01 00:00:00', 'query20', 2),
            ('2015-12-01 00:00:00', 'query21', 1),
        ]
    ])
    with open('tests/logs.tsv', 'w+') as fd:
        fd.write(logs)

    parser.parse('tests/logs.tsv')


def test():
    setup()
    for query, count, populars in [
        ('2015-08-01 00:00', 5, {'query1': 10, 'query2': 4, 'query3': 3}),
        ('2015-08-01 00', 9, {'query1': 10, 'query6': 5, 'query2': 4}),
        ('2015-08-01', 13, {'query1': 10, 'query10': 6, 'query6': 5}),
        ('2015-08', 17, {'query1': 10, 'query14': 7, 'query10': 6}),
        ('2015', 21, {'query1': 10, 'query18': 8, 'query14': 7}),

    ]:
        result = read(query, 3, 'tests')
        print(query, result['count'], {r['query']: r['count'] for r in result['queries']})
        assert result['count'] == count
        assert {r['query']: r['count'] for r in result['queries']} == populars

    print('Tests OK')


if __name__ == '__main__':
    test()
