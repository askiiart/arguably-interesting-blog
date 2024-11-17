#!/usr/bin/env python3
import csv
import re

class HelperFunctions:
    def get_fs(dir):
        if dir.endswith('dwarfs'):
            return 'DwarFS'
        elif dir.endswith('fuse-archive-tar'):
            return 'fuse-archive (tar)'

        return 'Btrfs'

    def get_label(filename):
        if filename == '25G-null.bin':
            return 'Null 25 GiB file'
        elif filename == '25G-random.bin':
            return 'Random 25 GiB file'
        elif filename == '100M-polygon.txt':
            return '100 million-sided polygon data'
        elif filename.startswith('kernel'):
            return 'Linux LTS kernel'

    def convert_time(time: str, unit: str) -> int:
        unit_exponents = ['ns', 'µs', 'ms', 's']

        if time.endswith('ms'):
            current_unit = 'ms'
        elif time.endswith('µs'):
            current_unit = 'µs'
        elif time.endswith('ns'):
            current_unit = 'ns'
        else:
            current_unit = 's'
        
        unit_multiplier = unit_exponents.index(current_unit) - unit_exponents.index(unit)
        return HelperFunctions.time_int(time) * (1000 ** unit_multiplier)
    
    def time_int(time: str):
        time = re.sub("[^0-9\\.]", "", time)
        return float(time)


def sequential_latency():
    datasets = {'labels': []}
    with open('assets/benchmarking-dwarfs/data/benchmark-data.csv', 'rt') as f:
        for line in csv.reader(f):
            fs = HelperFunctions.get_fs(line[0])
            label = HelperFunctions.get_label(line[1])
            datasets['labels'].append(label) if label not in datasets[
                'labels'
            ] else False
            try:
                datasets[fs].append(line[3])
            except KeyError:
                datasets[fs] = []
                datasets[fs].append(line[3])

    return datasets


def singles():
    pass


def bulk():
    pass


if __name__ == '__main__':
    # from https://github.com/chartjs/Chart.js/blob/master/docs/scripts/utils.js (CHART_COLORS)
    # modified so similar color aren't adjacent
    chart_colors = [
        "'rgb(255, 99, 132)'",  # red
        "'rgb(75, 192, 192)'",  # green
        "'rgb(54, 162, 235)'",  # blue
        "'rgb(255, 159, 64)'",  # orange
        "'rgb(153, 102, 255)'",  # purple
        "'rgb(255, 205, 86)'",  # yellow
        "'rgb(201, 203, 207)'",  # grey
    ]

    print('Sequential latency:')
    labels_code = 'const labels = $labels$'
    dataset_code = '''
    {
      label: '$label$',
      data: $data$,
      backgroundColor: $color$,
    },'''

    config_code = '''
let config = {
    type: 'bar',
    data: {
        datasets: data,
        labels
    },
    options: {
      plugins: {
        title: {
          display: true,
          text: '$title$ - in $timeunit$'
        },
      },
      responsive: true,
      interaction: {
        intersect: false,
      },
    }
  };
'''

    data = sequential_latency()
    labels_code = labels_code.replace('$labels$', format(data['labels']))
    print(labels_code)
    data.pop('labels')
    print('let data = [', end='')
    largest_time_unit = 'ns'
    for fs in data.keys():
        for item in data[fs]:
            if item.endswith('ms'):
                largest_time_unit = 'ms'
            elif item.endswith('µs') and largest_time_unit != 'ms':
                largest_time_unit = 'µs'
            elif item.endswith('ns') and largest_time_unit != 'ms' and largest_time_unit != 'µs':
                largest_time_unit = 'ns'
            elif re.sub('[0-9]', '', item) == 's':
                largest_time_unit = 's'
                break

        for i in range(len(data[fs])):
            data[fs][i] = HelperFunctions.convert_time(data[fs][i], largest_time_unit)
        
        print(
            dataset_code.replace('$label$', fs)
            .replace('$data$', format(data[fs]))
            .replace('$color$', format(chart_colors[list(data.keys()).index(fs)])),
            end=''
        )
    print('\n]\n')

    title = 'Sequential Read Latency'
    print(config_code.replace('$title$', title).replace('$timeunit$', largest_time_unit))
    print('\nChart.defaults.borderColor = "#eee"')
    print('Chart.defaults.color = "#eee";')
