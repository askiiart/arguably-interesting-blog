labels = ['Null 25 GiB file', 'Random 25 GiB file', '100 million-sided polygon data', 'Linux LTS kernel', '1024 null files (avg)', '1024 random files (avg)']
data = [
        {
        label: 'DwarFS',
        data: [0.35130788, 3.51396, 0.48097789, 0.0008825759999999999, 1.333e-06, 1.242e-06],
        backgroundColor: 'rgb(255, 99, 132)',
        },
        
        {
        label: 'fuse-archive (tar)',
        data: [0.0, 0.0, 0.0, 0.0, 1.4119999999999998e-06, 2.144e-06],
        backgroundColor: 'rgb(75, 192, 192)',
        },
        
        {
        label: 'Btrfs',
        data: [0.00551523, 0.09113626, 0.09405722, 0.0009497709999999999, 9.82e-07, 1.242e-06],
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
            text: 'Random Read Latency - in s'
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
ctx = document.getElementById("rand_read_latency_chart");
new Chart(ctx, config);
