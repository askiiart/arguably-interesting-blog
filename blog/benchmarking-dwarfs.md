# Benchmarking and comparing DwarFS

DwarFS is a filesystem developed by the user mhx on GitHub (*mhx/dwarfs*), which is self-described as "A fast high compression read-only file system for Linux, Windows, and macOS." One of my ideas for blendOS was to layer different packages, and combined with its compression and option to be mounted as a FUSE-based filesystem, it's an appealing option for this use case - blendOS is immutable, so it might as well have some compression.

## Methodology

The datasets being used for this test will be the following:

- 25 GiB of null data (just `00000000` in binary)
- 25 GiB of random data[^1]
- Data for a 100 million-sided regular polygon; ~26.5 GiB[^2]
- The current Linux longterm release source ([6.6.58](https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.6.58.tar.xz) (*The Linux Kernel Archives*)); ~1.5 GB
- For some rough latency testing:
  - 1024 4 KiB files filled with null data (again, just `00000000` in binary)
  - 1024 4 KiB files filled with random data

All this data should cover both latency and read speed testing for data that compresses differently - extremely compressible files with null data, decently compressible files, and random data which can't be compressed well.

### What filesystems?

I'll be benchmarking DwarFS (*mhx/dwarfs*), fuse-archive (*Google/Fuse-Archive*) (with tar files), and btrfs. In some early, basic testing, I found that mounting any *compressed* archives with `fuse-archive`, a tool for mounting archive file formats as read-only filesystems, took far too long. Additionally, being FUSE-based, these would have slightly worse performance than kernel filesystems, so I tried to use a FUSE driver as well for btrfs. Unforunately, I ran into a bug, so I won't be able to quite do an equivalent test; btrfs will only be running in the kernel.

During said early testing, I also ran into the fact that most compressed archives, like Gzip-compressed tar archives, also took far too long to *create*, because Gzip is single-threaded. So all the options with no chance of being used have been marked off, and I'll only be looking into these three.

DwarFS also took far too long to create an archive on its default setting, but on compression level 1, it's much faster - 11m2.738s for the ~80 GiB total, and considering my entire system is about 20 GiB, that should be about 2-3 minutes, which is reasonable; With no compression, tar took 3m3.378s. Mounting the DwarFS archive was nearly instant (0.022s), while mounting the tar archive took 1.352s - not bad, but not ideal when mounting many, and will absolutely be taken into consideration.

## Running the benchmark

First off, installed I installed my benchamark (*Disk Read Benchmark*) by cloning the repository, installing it using Cargo, then added its completions to fish (just for this session):

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

These results interest me quite a bit; unsurprisingly, DwarFS has an advantage on the null file, due to its compression, though it's disappointing the difference in time wasn't greater. However, it does far worse on the random file, and I'm not sure why; as discussed further down, DwarFS doesn't try to compress incompressible files as far as I know, but I could be wrong. As for the 100 million-sided polygon, it's somewhere in between, with an advantage due to its compression, but still taking longer than expected.

As for fuse-archive, it handles the null file well, but takes longer on the others; not much to say.

<div>
  <canvas id="seq_read_chart" class="chart"></canvas>
</div>

### Random read

There's nothing much to say here; although DwarFS took significantly longer, it's still pretty fast - a different of about 14 milliseconds worst case, across a 25 GiB file; similar resuls for the 100 million-sided polygon, though to a less extent, given it can be compressed better. With the null file, due to its compression, DwarFS was actually on par with fuse-archive, but it can't compete with btrfs's performance, given it's so heavily optimized, and in the kernel.

<div>
  <canvas id="rand_read_chart" class="chart"></canvas>
</div>

### Sequential read latency

As expected, DwarFS performs a bit worse on the incompressible random data, but otherwise they'll all roughly equal. I wasn't expecting this, given btrfs is in the kernel, while the other two are using FUSE.

<div>
  <canvas id="seq_read_latency_chart" class="chart"></canvas>
</div>

### Random read latency

Both DwarFS and fuse-archive had some trouble with this test. DwarFS doesn't seem to handle random access very well; this is supposedly fixed, as seen in issue 139 (*Issue #139 · mhx/dwarfs*), but the performance issues are obvious regardless; I'm not sure why, given it doesn't compress uncompressible data, not to mention it does just fine on the random read test, where the only difference is that it reads *more* data. But regardless, DwarFS ended up performing far worse than expected on both the incompressible random data, and the highly compressible null data.

Meanwhile, when testing random read latency in `fuse-archive` pretty much just dies, becoming ridiculously slow (even compared to DwarFS), so I didn't include its single-file results. It succeeds on the bulk files, but given it just shows as 0 seconds anyways, given the massive scale, I opted to not include it in this graph at all.

<div>
  <canvas id="rand_read_latency_chart" class="chart"></canvas>
</div>

## Misc notes

DwarFS can take up a fair amount of memory if mounting it many times (*Issue #219 · mhx/dwarfs*), and this should be kept in mind for use in BlendOS.

---

Ratarmount (*mxmlnkn/ratarmount*) should also be investigated; it's similar to fuse-archive, but with some improvements, and some important notes. From its README file:

> Note that fuse-archive daemonizes instantly but the mount point will not be usable for a long time and everything trying to use it will hang until then when not using --asyncprogress

> Mounting bzip2 and xz archives has actually become faster than archivemount and fuse-archive with ratarmount -P 0 on most modern processors because it actually uses more than one core for decoding those compressions. indexed_bzip2 supports block parallel decoding since version 1.2.0.

Despite being written in Python, Ratarmount seems to have significant performance improvements over fuse-archive.

---

This should also be tested on systems with different specs, like my Chromebook and laptop, and should try getting the btrfs FUSE driver working and benchmarking that.

## Summary

DwarFS, or just the normal filesystem plus overlayfs, seem like they may be the best options - DwarFS's compression and deduplication are great, and the deduplication could probably be used in way I haven't even thought of yet, but it has some niche issues. Overall, I'm leaning towards using DwarFS as an option, with just overlayfs as the default, but further testing is needed.

## Footnotes

[^1]: My code can generate up to 25 GB/s. However, it does random writes to my drive, which is *much* slower. So on one hand, you could say my code is so amazingly fast that current day technologies simply can't keep up. Or you could say that I have no idea how to code for real world scenarios.
[^2]: This data is from a modified version of an abandoned math demonstration program (*confused_ace_noises/maths-demos*) made by a friend; it generates regular polygons and writes their data to a file. I chose this because it was an artificial and reproducible yet fairly compressible dataset (without being extremely compressible like null data).
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

## Sources

&emsp;- “Confused_ace_noises/Maths-Demos - Branch: Headless-Deterministic.” Forgea: Git with a Cup of Jea, git.askiiart.net/confused_ace_noises/maths-demos/src/branch/headless-deterministic.\
&emsp;- “Disk Read Benchmark - A Simple and Performant Read-Only Disk Benchmark, Written in Rust.” Forgea: Git with a Cup of Jea, git.askiiart.net/askiiart/disk-read-benchmark.\
&emsp;- Google. “Google/Fuse-Archive: Fuse File System for Archives and Compressed Files (ZIP, RAR, 7z, ISO, TGZ, Xz...).” GitHub, github.com/google/fuse-archive.\
&emsp;- The Linux Kernel Archives, Linux Kernel Organization, Inc., <www.kernel.org/>.\
&emsp;- Mhx. “Feature Request: Improve Block Management for Uncompressed Blocks to Save Memory and Enhance Deduplication · ISSUE #139 · MHX/Dwarfs.” GitHub, github.com/mhx/dwarfs/issues/139.\
&emsp;- mhx. “mhx/Dwarfs: A Fast High Compression Read-Only File System for Linux, Windows and Macos.” GitHub, github.com/mhx/dwarfs.\
&emsp;- mhx. “[Feature Request] Mounting Multiple Archives to the Same Path · Issue #219 · MHX/Dwarfs.” GitHub, github.com/mhx/dwarfs/issues/219.\
&emsp;- mxmlnkn. “mxmlnkn/ratarmount: Access Large Archives as a Filesystem Efficiently, e.g., Tar, Rar, Zip, Gz, BZ2, XZ, ZSTD Archives.” GitHub, github.com/mxmlnkn/ratarmount.

<!-- JavaScript for graphs goes hereeeeeee -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="/assets/benchmarking-dwarfs/js/declare_vars.js"></script>
<script src="/assets/benchmarking-dwarfs/js/seq_read.js"></script>
<script src="/assets/benchmarking-dwarfs/js/rand_read.js"></script>
<script src="/assets/benchmarking-dwarfs/js/seq_latency.js"></script>
<script src="/assets/benchmarking-dwarfs/js/rand_latency.js"></script>
