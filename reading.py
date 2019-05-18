import argparse
import pprint


def read(timestamp, popular_count, folder='data'):
    try:
        date, time = timestamp.split(' ')
    except ValueError:
        date, time = timestamp, None

    year, month, day = date.split('-') +\
        [None for _ in range(2 - date.count('-'))]

    if time:
        hour, minute, _ = time.split(':') +\
            [None for _ in range(2 - time.count(':'))]
    else:
        hour, minute = None, None

    fd_pos = None
    for unit, value, sub_value in [
        ('year', '{}'.format(year), month),
        ('month', '{}-{}'.format(year, month), day),
        ('day', '{}-{}-{}'.format(year, month, day), hour),
        ('hour', '{}-{}-{} {}'.format(year, month, day, hour), minute),
        ('minute', '{}-{}-{} {}:{}'.format(year, month, day, hour, minute), None),
    ]:
        with open(folder + '/{}.dat'.format(unit)) as fd:
            if fd_pos:
                fd.seek(int(fd_pos))
            for line in fd.readlines():
                if line.startswith(value):
                    _, count, fd_pos, populars = line.rstrip('\n').split('\t')
                    if sub_value is None:
                        *populars, _ = populars.split(',', popular_count)
                        populars = (m.split(':') for m in populars)
                        queries = [{'query': value, 'count': int(count)} for count, value in populars]
                        return {'count': int(count), 'queries': queries}
                    break
            else:
                return {'count': 0, 'queries': []}

    return {'count': 0, 'queries': []}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('timestamp')
    parser.add_argument('--count', type=int, default=3)
    args = parser.parse_args()
    pprint.pprint(read(args.timestamp, args.count))
