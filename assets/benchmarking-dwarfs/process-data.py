#!/usr/bin/env python3
import csv
import re


# a bunch of horrible code to make the chart.js code


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
        elif filename == 'small-files/random':
            return '1024 random files'
        elif filename == 'small-files/null':
            return '1024 null files'

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

        unit_multiplier = unit_exponents.index(current_unit) - unit_exponents.index(
            unit
        )
        return HelperFunctions.time_num(time) * (1000**unit_multiplier)

    def time_num(time: str):
        time = re.sub('[^0-9\\.]', '', time)
        return float(time)


def get_seq_latency_data() -> tuple:
    # format: { 'labels': ['btrfs'], 'btrfs': [9, 8, 4, 6]}
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

    # NOTE: this will break if the bulk data contains a larger unit than the single file data, but that's unlikely to happen so I'm not gonna deal with it
    largest_time_unit = 'ns'
    for key in datasets.keys():
        if key == 'labels':
            continue
        for item in datasets[key]:
            if item.endswith('ms'):
                largest_time_unit = 'ms'
            elif item.endswith('µs') and largest_time_unit != 'ms':
                largest_time_unit = 'µs'
            elif (
                item.endswith('ns')
                and largest_time_unit != 'ms'
                and largest_time_unit != 'µs'
            ):
                largest_time_unit = 'ns'
            elif re.sub('[0-9]', '', item) == 's':
                largest_time_unit = 's'
                break

    for key in datasets.keys():
        if key == 'labels':
            continue
        for i in range(len(datasets[key])):
            datasets[key][i] = HelperFunctions.convert_time(
                datasets[key][i], largest_time_unit
            )

    with open('assets/benchmarking-dwarfs/data/bulk.csv', 'rt') as f:
        for line in csv.reader(f):
            if line[2] != 'bulk_sequential_read_latency':
                continue
            fs = HelperFunctions.get_fs(line[0])
            label = HelperFunctions.get_label(line[1])
            datasets['labels'].append(label) if label not in datasets[
                'labels'
            ] else False

            for item in line[3:]:
                if item.endswith('ms'):
                    largest_time_unit = 'ms'
                elif item.endswith('µs') and largest_time_unit != 'ms':
                    largest_time_unit = 'µs'
                elif (
                    item.endswith('ns')
                    and largest_time_unit != 'ms'
                    and largest_time_unit != 'µs'
                ):
                    largest_time_unit = 'ns'
                elif re.sub('[0-9]', '', item) == 's':
                    largest_time_unit = 's'
                    break

            for i in range(len(line[3:])):
                line[i + 3] = HelperFunctions.convert_time(item, largest_time_unit)

            datasets[fs].append(sum(line[3:]) / len(line[3:]))

        return (datasets, largest_time_unit)

def seq_latency():
    with open('assets/benchmarking-dwarfs/js/seq_latency.js', 'wt') as f:
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

        #print('Sequential latency:')
        labels_code = 'const labels = $labels$'
        dataset_code = '''
        {
        label: '$label$',
        data: $data$,
        backgroundColor: $color$,
        },
        '''

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

        data, largest_time_unit = get_seq_latency_data()
        labels_code = labels_code.replace('$labels$', format(data['labels']))
        f.write(labels_code)
        data.pop('labels')
        f.write('\nlet data = [')
        for fs in data.keys():
            f.write(
                dataset_code.replace('$label$', fs)
                .replace('$data$', format(data[fs]))
                .replace('$color$', format(chart_colors[list(data.keys()).index(fs)]))
            )
        f.write('\n]\n')

        title = 'Sequential Read Latency'
        f.write(
            config_code.replace('$title$', title).replace('$timeunit$', largest_time_unit)
        )

        f.write('\nChart.defaults.borderColor = "#eee"\n')
        f.write('Chart.defaults.color = "#eee";\n')
        f.write('let ctx = document.getElementById("seq_read_latency_chart");\n')
        f.write('new Chart(ctx, config);\n')


def singles():
    pass


def bulk():
    pass


if __name__ == '__main__':
    seq_latency()