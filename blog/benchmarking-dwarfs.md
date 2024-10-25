# Benchmarking and comparing DwarFS

DwarFS is a filesystem developed by the user mhx on GitHub [1], which is self-described as "A fast high compression read-only file system for Linux, Windows, and macOS." One of my ideas for blendOS was to layer different packages, and combined with its compression and option to be mounted as a FUSE-based filesystem, it's an appealing option for this use case - blendOS is immutable, so it might as well have some compression.

## Methodology

The datasets being used for this test will be the following:

- 25 GB of null data (just `000000000000` in binary)
- 25 GB of random data[^1]
- Data for a 100 million-sided regular polygon; ~29 GB[^2]
- The current Linux longterm release source ([6.6.58](https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.6.58.tar.xz) [2]); ~1.5 GB
- For some rough latency testing:
  - 1000 4 kilobyte files filled with null data (again, just `0000000` in binary)
  - 1000 4 kilobyte files filled with random data

All this data should cover both latency and read speed testing for data that compresses differently - extremely compressible files with null data, decently compressible files, and random data which can't be compressed well.

## Sources

1. <https://github.com/mhx/dwarfs>
2. <https://www.kernel.org/>

## Footnotes

[^1]: This data is from a very early version of a math demonstration program made by a friend. The example below shows what the data looks like for a 3-sided regular polygon.
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
[^2]: My code can generate up to 25 GB/s. However, it does random writes to my drive, which is *much* slower. So on one hand, you could say my code is so amazingly fast that current day technologies simply can't keep up. Or you could say that I have no idea how to code for real world scenarios.
