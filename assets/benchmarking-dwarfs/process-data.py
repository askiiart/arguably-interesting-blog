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
            return '1024 random files (avg)'
        elif filename == 'small-files/null':
            return '1024 null files (avg)'

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

def get_data(single_files_index: int, bulk_test_name: str):
    # format: { 'labels': ['btrfs'], 'btrfs': [9, 8, 4, 6]}
    data = {'labels': []}
    with open('assets/benchmarking-dwarfs/data/benchmark-data.csv', 'rt') as f:
        for line in csv.reader(f):
            fs = HelperFunctions.get_fs(line[0])
            label = HelperFunctions.get_label(line[1])
            data['labels'].append(label) if label not in data[
                'labels'
            ] else False
            try:
                data[fs].append(line[single_files_index])
            except KeyError:
                data[fs] = []
                data[fs].append(line[single_files_index])

    # NOTE: this will break if the bulk data contains a larger unit than the single file data, but that's unlikely to happen so I'm not gonna deal with it
    # and it's a bit broken regardless but whatever
    largest_time_unit = 'ns'
    for key in data.keys():
        if key == 'labels':
            continue
        for item in data[key]:
            if largest_time_unit == 's':
                break
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
            elif re.sub('[0-9\\.]', '', item) == 's':
                largest_time_unit = 's'
                break

    for key in data.keys():
        if key == 'labels':
            continue
        for i in range(len(data[key])):
            data[key][i] = HelperFunctions.convert_time(
                data[key][i], largest_time_unit
            )

    with open('assets/benchmarking-dwarfs/data/bulk.csv', 'rt') as f:
        for line in csv.reader(f):
            if line[2] != bulk_test_name:
                continue
            fs = HelperFunctions.get_fs(line[0])
            label = HelperFunctions.get_label(line[1])
            data['labels'].append(label) if label not in data[
                'labels'
            ] else False

            for item in line[3:]:
                if largest_time_unit == 's':
                    break
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
                elif re.sub('[0-9]\\.', '', item) == 's':
                    largest_time_unit = 's'
                    break

            for i in range(len(line[3:])):
                line[i + 3] = HelperFunctions.convert_time(item, largest_time_unit)

            data[fs].append(sum(line[3:]) / len(line[3:]))

        return (data, largest_time_unit)


def run(single_files_index: int, bulk_test_name: str, filename: str, title: str, chart_canvas_id: str):
    with open(f'assets/benchmarking-dwarfs/js/{filename}', 'wt') as f:
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

        labels_code = 'labels = $labels$'
        dataset_code = '''
        {
        label: '$label$',
        data: $data$,
        backgroundColor: $color$,
        },
        '''

        config_code = '''
    config = {
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

        data, largest_time_unit = get_data(single_files_index, bulk_test_name)
        labels_code = labels_code.replace('$labels$', format(data['labels']))
        f.write(labels_code)
        data.pop('labels')
        f.write('\ndata = [')
        for fs in data.keys():
            f.write(
                dataset_code.replace('$label$', fs)
                .replace('$data$', format(data[fs]))
                .replace('$color$', format(chart_colors[list(data.keys()).index(fs)]))
            )
        f.write('\n]\n')

        f.write(
            config_code.replace('$title$', title).replace(
                '$timeunit$', largest_time_unit
            )
        )

        f.write('\nChart.defaults.borderColor = "#eee"\n')
        f.write('Chart.defaults.color = "#eee";\n')
        f.write(f'ctx = document.getElementById("{chart_canvas_id}");\n')
        f.write('new Chart(ctx, config);\n')

def declare_vars():
    with open('assets/benchmarking-dwarfs/js/declare_vars.js', 'wt') as f:
        f.write('let labels;\n')
        f.write('let config;\n')
        f.write('let data;\n')
        f.write('let ctx;\n')

if __name__ == '__main__':
    # NOTE: this code is absolutely horrible and all these functions (except declare_vars) should be one function that just takes the title, chart canvas id, filename, test name in bulk, and index in singles
    # and what function to get data from, if that's possible
    # i will repent to the DRY gods someday
    declare_vars()
    run(2, 'bulk_sequential_read', 'seq_read.js', 'Sequential Read Times', 'seq_read_chart')
    run(3, 'bulk_random_read', 'rand_read.js', 'Random Read Times', 'rand_read_chart')
    run(4, 'bulk_sequential_read_latency', 'seq_latency.js', 'Sequential Read Latency', 'seq_read_latency_chart')
    run(5, 'bulk_random_read_latency', 'rand_latency.js', 'Random Read Latency', 'rand_read_latency_chart')
