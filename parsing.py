import argparse
from collections import defaultdict, namedtuple
from datetime import datetime
from settings import MAX_POPULAR_COUNT
from dateutil.relativedelta import relativedelta


Popular = namedtuple('Popular', ('count', 'value'))
Meta = namedtuple('Meta', ('timestamp', 'count', 'populars', 'fd_pos'))
Cursor = namedtuple('Cursor', ('start', 'end'))

UNITS = ['minute', 'hour', 'day', 'month', 'year']


class Parser:
    def __init__(self, folder='data'):
        self.counts = defaultdict(int)
        self.metas = defaultdict(list)
        self.folder = folder

    def compute_meta(self, unit, **kwargs):
        sub_unit_index = UNITS.index(unit) - 1
        sub_unit = UNITS[sub_unit_index] if sub_unit_index >= 0 else None

        if sub_unit is None:
            sorted_items = sorted(self.counts.items(), key=lambda item: item[1], reverse=True)
            sub_fd_pos = 0
            self.counts = defaultdict(int)
        else:
            counts = defaultdict(int)
            for meta in self.metas[sub_unit]:
                for popular in meta.populars:
                    counts[popular.value] += popular.count
            sorted_items = sorted(counts.items(), key=lambda item: item[1], reverse=True)
            sub_fd_pos = self.metas[sub_unit][0].fd_pos if self.metas[sub_unit] else 0
            self.metas[sub_unit] = []

        populars = [Popular(count, value) for value, count in sorted_items]
        meta = Meta(populars=populars, **kwargs)
        self.metas[unit].append(meta)

        return meta, sub_fd_pos

    def dump_meta(self, fd, **kwargs):
        meta, sub_fd_pos = self.compute_meta(fd_pos=fd.tell(), **kwargs)

        # dump only the first n populars to avoid taking too much disk, this will
        # limit the maximum number of populars possible to retrive
        fd.write('{}\t{}\t{}\t{}\n'.format(
            meta.timestamp,
            meta.count,
            sub_fd_pos,
            ','.join('{}:{}'.format(p.count, p.value) for p in meta.populars[:MAX_POPULAR_COUNT])
        ))

    def parse(self, filename):
        with open(filename) as fd_read,\
                open(self.folder + '/minute.dat', 'w+') as fd_write_minutes,\
                open(self.folder + '/hour.dat', 'w+') as fd_write_hours,\
                open(self.folder + '/day.dat', 'w+') as fd_write_days,\
                open(self.folder + '/month.dat', 'w+') as fd_write_months,\
                open(self.folder + '/year.dat', 'w+') as fd_write_years:

            fds = {
                'year': fd_write_years,
                'month': fd_write_months,
                'day': fd_write_days,
                'hour': fd_write_hours,
                'minute': fd_write_minutes,
            }
            cursors = None
            distincts = defaultdict(set)

            def get_cursor(unit, timestamp):
                # returns the time range surrounding timestamp for the given unit
                start = timestamp.replace(second=0, **{
                    k: v for k, v in {'minute': 0, 'hour': 0, 'day': 1, 'month': 1}.items()
                    if UNITS.index(k) < UNITS.index(unit)
                })
                return Cursor(start, start + relativedelta(**{unit + 's': 1}))

            def dump_meta(unit, timestamp):
                self.dump_meta(
                    fds[unit], unit=unit, timestamp=cursors[unit].start, count=len(distincts[unit])
                )
                cursors[unit] = get_cursor(unit, timestamp)
                distincts[unit].clear()

            for line in fd_read.readlines():
                time, value = line.rstrip('\n').split('\t')
                timestamp = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')

                if cursors is None:
                    cursors = {unit: get_cursor(unit, timestamp) for unit in UNITS}

                for unit in UNITS:
                    if timestamp >= cursors[unit].end:
                        dump_meta(unit, timestamp)

                    distincts[unit].add(value)

                self.counts[value] += 1

            for unit in UNITS:
                dump_meta(unit, timestamp)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    Parser().parse(args.filename)
