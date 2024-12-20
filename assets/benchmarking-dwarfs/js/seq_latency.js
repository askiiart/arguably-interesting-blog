labels = ['Null 25 GiB file', 'Random 25 GiB file', '100 million-sided polygon data', 'Linux LTS kernel', '1024 null files (avg)', '1024 random files (avg)']
data = [
        {
        label: 'DwarFS',
        data: [96.32895, 109.78266, 96.3926, 94.55468, 0.014287000000000001, 0.013595000000000001],
        backgroundColor: 'rgb(255, 99, 132)',
        },
        
        {
        label: 'fuse-archive (tar)',
        data: [98.66828, 94.52984, 96.61561, 93.25915, 0.013405, 0.013465],
        backgroundColor: 'rgb(75, 192, 192)',
        },
        
        {
        label: 'Btrfs',
        data: [96.79632, 97.642, 98.92292, 91.41823, 0.0032860000000000003, 0.003326],
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
            text: 'Sequential Read Latency - in ms'
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
ctx = document.getElementById("seq_read_latency_chart");
new Chart(ctx, config);
