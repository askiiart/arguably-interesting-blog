labels = ['Null 25 GiB file', 'Random 25 GiB file', '100 million-sided polygon data', 'Linux LTS kernel', '1024 null files (avg)', '1024 random files (avg)']
data = [
        {
        label: 'DwarFS',
        data: [12.8049, 40.71916, 19.11096, 0.16075466, 0.000945113, 3.6729e-05],
        backgroundColor: 'rgb(255, 99, 132)',
        },
        
        {
        label: 'fuse-archive (tar)',
        data: [24.88932, 24.84052, 26.63768, 0.121502, 4.131799999999999e-05, 1.6571e-05],
        backgroundColor: 'rgb(75, 192, 192)',
        },
        
        {
        label: 'Btrfs',
        data: [25.5482, 16.91976, 17.98264, 0.08859571, 6.873e-06, 6.432e-06],
        backgroundColor: 'rgb(54, 162, 235)',
        },
        
]

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
            text: 'Sequential Read Times - in s'
            },
        },
        responsive: true,
        interaction: {
            intersect: false,
        },
        }
    };
    
Chart.defaults.borderColor = "#eee"
Chart.defaults.color = "#eee";
ctx = document.getElementById("seq_read_chart");
new Chart(ctx, config);
