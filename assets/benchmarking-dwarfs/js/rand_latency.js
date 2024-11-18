labels = ['Null 25 GiB file', 'Random 25 GiB file', '100 million-sided polygon data', 'Linux LTS kernel', '1024 null files (avg)', '1024 random files (avg)']
data = [
        {
        label: 'DwarFS',
        data: [351.30788, 3513.96, 480.97789, 0.882576, 0.000811, 0.000661],
        backgroundColor: 'rgb(255, 99, 132)',
        },
        
        {
        label: 'fuse-archive (tar)',
        data: [0.0, 0.0, 0.0, 0.0, 0.000652, 0.000772],
        backgroundColor: 'rgb(75, 192, 192)',
        },
        
        {
        label: 'Btrfs',
        data: [5.51523, 91.13626, 94.05722, 0.949771, 0.000741, 0.0007509999999999999],
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
            text: 'Random Read Latency - in ms'
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
