# Benchmarking and comparing DwarFS

DwarFS is a filesystem developed by the user mhx on GitHub [1], which is self-described as "A fast high compression read-only file system for Linux, Windows, and macOS." One of my ideas for blendOS was to layer different packages, and combined with its compression and option to be mounted as a FUSE-based filesystem, it's an appealing option for this use case - blendOS is immutable, so it might as well have some compression.

## Methodology

The datasets being used for this test will be the following:

- 25 GiB of null data (just `00000000` in binary)
- 25 GiB of random data[^1]
- Data for a 100 million-sided regular polygon; ~26.5 GiB[^2]
- The current Linux longterm release source ([6.6.58](https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.6.58.tar.xz) [2]); ~1.5 GB
- For some rough latency testing:
  - 1024 4 KiB files filled with null data (again, just `00000000` in binary)
  - 1024 4 KiB files filled with random data

All this data should cover both latency and read speed testing for data that compresses differently - extremely compressible files with null data, decently compressible files, and random data which can't be compressed well.

### What filesystems?

I'll be benchmarking DwarFS, fuse-archive (with tar files), and btrfs. In some early, basic testing, I found that mounting any *compressed* archives with `fuse-archive`, a tool for mounting archive file formats as read-only filesystems, took far too long. Additionally, being FUSE-based, these would have slightly worse performance than kernel filesystems, so I tried to use a FUSE driver as well for btrfs. Unforunately, I ran into a bug, so I won't be able to quite do an equivalent test; btrfs will only be running in the kernel.

During said early testing, I also ran into the fact that most compressed archives, like Gzip-compressed tar archives, also took far too long to *create*, because Gzip is single-threaded. So all the options with no chance of being used have been marked off, and I'll only be looking into these three.

DwarFS also took far too long to create on its default setting, but on compression level 1, it's much faster - 11m2.738s for the ~80 GiB total, and considering

## Running the benchmark

First installed it by cloning the repository, installing it using Cargo, then added its completions to fish (just for this session):

```sh
git clone https://git.askiiart.net/askiiart/disk-read-benchmark
cd ./disk-read-benchmark
cargo install --path .
disk-read-benchmark generate-fish-completions | source
```

Then I prepared all the data:

```sh
disk-read-benchmark prep-dirs
disk-read-benchmark grab-data
./prepare.sh
```

`disk-read-benchmark` prepares all the directories, generates the data to be used for testing, then `./prepare.sh` uses the data to generate the DwarFS and tar archives.

To run it, I just ran this:

```sh
disk-read-benchmark benchmark
```

Which outputs the data at `data/benchmark-data.csv` and `data/bulk.csv` for the single and bulk files, respectively.

## Results

After processing [the data](/assets/benchmarking-dwarfs/data/) with [this script](/assets/benchmarking-dwarfs/process-data.py) to make it a bit easier, I put the resulting graphs in here ↓

### Sequential read

### Random read

### Sequential read latency

<div>
  <canvas id="seq_read_latency_chart" class="chart"></canvas>
</div>

### Random read latency

The FUSE-based filesystems run into a bit of trouble here - with incompressible data, DwarFS has a hard time keeping up for some reason, despite keeping up just fine with larger random reads on the same data, and so it takes 3 to 4 seconds to run random read latency testing on the 25 GiB random file. Meanwhile, when testing random read latency in `fuse-archive` pretty much just dies, becoming ridiculously slow (even compared to DwarFS), so I didn't test its random read latency at all and just had its results put as 0 milliseconds.

### Summary and notes

## Sources

1. <https://github.com/mhx/dwarfs>
2. <https://www.kernel.org/>
3. <https://git.askiiart.net/askiiart/disk-read-benchmark>
4. <https://git.askiiart.net/confused_ace_noises/maths-demos/src/branch/headless-deterministic>

## Footnotes

[^1]: My code can generate up to 25 GB/s. However, it does random writes to my drive, which is *much* slower. So on one hand, you could say my code is so amazingly fast that current day technologies simply can't keep up. Or you could say that I have no idea how to code for real world scenarios.
[^2]: This data is from a modified version of an abandoned math demonstration program [4] made by a friend; it generates regular polygons and writes their data to a file. I chose this because it was an artificial and reproducible yet fairly compressible dataset (without being extremely compressible like null data).
<details open>
<summary>3-sided regular polygon data</summary>
<br>
<!-- I put it in here just as a `style`, it didn't work. I put it in as a div with that `style`, it didn't work. I put it in as a div of that class which has those properties in style.css, it works -->
<!-- i hate webdev i hate webdev i hate webdev i hate webdev i hate webdev i hate webdev -->
<div class="force-word-wrap">
```
[Vertex { position: Pos([0.5, 0.0, 0.0]), color: Col([0.5310667, 0.7112941, 0.7138775]) }, Vertex { position: Pos([-0.25000003, 0.4330127, 0.0]), color: Col([0.7492257, 0.3142163, 0.49905664]) }, Vertex { position: Pos([0.0, 0.0, 0.0]), color: Col([0.2046682, 0.25598457, 0.72071356]) }, Vertex { position: Pos([-0.25000003, 0.4330127, 0.0]), color: Col([0.6389981, 0.5204368, 0.077735074]) }, Vertex { position: Pos([-0.24999996, -0.43301272, 0.0]), color: Col([0.8869035, 0.30709425, 0.8658899]) }, Vertex { position: Pos([0.0, 0.0, 0.0]), color: Col([0.2046682, 0.25598457, 0.72071356]) }, Vertex { position: Pos([-0.24999996, -0.43301272, 0.0]), color: Col([0.6236294, 0.03584433, 0.7590722]) }, Vertex { position: Pos([0.5, 8.742278e-8, 0.0]), color: Col([0.6105084, 0.3593351, 0.85544324]) }, Vertex { position: Pos([0.0, 0.0, 0.0]), color: Col([0.2046682, 0.25598457, 0.72071356]) }]
```
</div>
</details>

<!-- JavaScript for graphs goes hereeeeeee -->
<!-- EXAMPLE HERE -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
  let ctx = document.getElementById('seq_read_latency_chart');
const labels = ['Null 25 GiB file', 'Random 25 GiB file', '100 million-sided polygon data', 'Linux LTS kernel']
let data = [
    {
      label: 'DwarFS',
      data: [0.37114600000000003, 14.15143, 2.95083, 0.001523],
      backgroundColor: 'rgb(255, 99, 132)',
    },
    {
      label: 'fuse-archive (tar)',
      data: [0.393568, 0.397626, 0.07750499999999999, 0.0012230000000000001],
      backgroundColor: 'rgb(75, 192, 192)',
    },
    {
      label: 'Btrfs',
      data: [0.027922000000000002, 0.290906, 0.14088399999999998, 0.0013930000000000001],
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

  new Chart(ctx, config);
</script>
