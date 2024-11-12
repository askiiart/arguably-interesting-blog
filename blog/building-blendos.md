# Building blendOS (and its packages)

This one was pretty simple. First off, I just made [an organization to hold all my blendOS code](https://git.askiiart.net/askiiart-blendos) on my Forgejo instance just to keep it organized. Then I just cloned all the relevant repositories from upstream (*blendOS · GitLab*), added my own code with some minor fixes and stuff, then pushed the updated code to my server.

After that, it was just a matter of adding the actual packaging for the code. For the packages that were required for building the blendOS `iso` file, if I didn't have my own repository for them already, I just made a new branch, updated the packaging, and pushed the packaging to that branch.

Looking at the [package list](https://git.blendos.co/blendOS/image-builder/-/blob/main/packages.x86_64) from `image-builder` (*blendOS / image-builder · GitLab*), it seems the only blendOS-specific packages it uses are:

```txt
filesystem-blend
blend-inst-git
jade-gui
blend-git
blend-settings-git
blend-web-store-git
akshara-git
```

At first, after a bit of minor troubleshooting, I got this all set up and working, pretty simple.

## Oops it didn't work actually

I then realized that my `iso` file worked, but was not using my repo, and I had even forgotten to even add some of the packages.

Turns out I had added my repo to the container's `pacman` configuration, but not to the `pacman` config for `archiso`, the tool used to generate the `iso` file, or the actual resulting `iso` image's `pacman` config either. So while I would have been able to install anything from my repo in the container, the repo was unused by `archiso`.

I just added the missing packages needed to build the `iso` file, plus all the others on blendOS's GitLab, and rebuilt it. After a bit of troubleshooting (nothing interesting, just incompetency, wrong perms, stuff like that), I got it working perfectly.

From the buid log:

```txt
[mkarchiso] INFO: Done!
2.3G /drone/src/image-builder/out/blendOS-2024.10.04-x86_64.iso
0
```

![Screenshot from Drone CI/CD showing the build successfully completed in 6 minutes 48 seconds](/assets/building-blendos/1.png)\
[![Build Status](https://drone.askiiart.net/api/badges/askiiart-blendos/build-blendos-iso/status.svg)](https://drone.askiiart.net/askiiart-blendos/build-blendos-iso)

## Topology of my blendOS repo

```txt
        |-----------------|
        |                 |
        | package builder |
        |                 |
        |-----------------|
                 |
                 |
                 ↓
      |-----------------------------|
      |          ↓                  |
      |    |----------|             |
      |    | packages |             |
      |    |----------|             |
      |                             |
      | Arch/blendOS                |
      | repository                  |
      |                             |
      |           |-----------|     |
      |           | blendOS   |     |
      |           | iso files |←---←|←---←
      |           |-----------|     |    |
      |                             |    |
      |-----------------------------|    |
             |                           |
             |                           |
             |                           |
             ↓                           |
    |-------------------------|          |
    |                         |          |
    | Arch/blendOS            |          |
    | clients                 |          |
    |                         |          |
    |   |--------------|      |          |
    |   | blendOS iso  |-----→|→---------↑
    |   |   builder    |      |
    |   |--------------|      |
    |                         |
    |-------------------------|
```

## Citations

&emsp;- Saraswat, Rudra, et al. “blendOS · GitLab.” *GitLab*, [git.blendos.co/blendOS](https://git.blendos.co/blendOS). Accessed 2 Oct. 2024.\
&emsp;- Saraswat, Rudra, and Asterisk. “blendOS / image-builder · GitLab.” *GitLab*, [git.blendos.co/blendOS/image-builder](https://git.blendos.co/blendOS/image-builder). Accessed 3 Oct. 2024.
