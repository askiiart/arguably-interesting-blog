const labels = ['Null 25 GiB file', 'Random 25 GiB file', '100 million-sided polygon data', 'Linux LTS kernel', '1024 null files', '1024 random files']
let data = [
        {
        label: 'DwarFS',
        data: [0.37114600000000003, 14.15143, 2.95083, 0.001523, 0.014287000000000001, 0.013595000000000001],
        backgroundColor: 'rgb(255, 99, 132)',
        },
        
        {
        label: 'fuse-archive (tar)',
        data: [0.393568, 0.397626, 0.07750499999999999, 0.0012230000000000001, 0.013405, 0.013465],
        backgroundColor: 'rgb(75, 192, 192)',
        },
        
        {
        label: 'Btrfs',
        data: [0.027922000000000002, 0.290906, 0.14088399999999998, 0.0013930000000000001, 0.0032860000000000003, 0.003326],
        backgroundColor: 'rgb(54, 162, 235)',
        },
        
]

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
let ctx = document.getElementById("seq_read_latency_chart");
new Chart(ctx, config);
