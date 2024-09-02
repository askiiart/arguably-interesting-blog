# Checking out blendOS

blendOS is self-described as "Arch Linux, made declarative, immutable and atomic." And yeah, that's a pretty good description of what it is. But you can never *really* tell what a distro is like without trying it, so...

## Installation

I decided to just run blendOS in a virtual machine; I had a bunch of data I hadn't backed up yet and was actively working on, and didn't feeling like switching yet given I had no experience with blendOS v4 - I've actually tried blendOS v3 before, back when v4 was in alpha, but it had practically zero documentation, not even `man` pages, so I gave up on it very quickly. But with v4, hopefully it's improved since then.

Installation itself was simple: it's got a basic installer, which notably allows for manual partitioning, but does *not* allow for selecting which track to use (which we'll get to later), though to be fair, that's *very* simple to change post-installation.

![blendOS live image boot: a basic GNOME desktop with a vertical white window in the center; it has the blendOS logo and a "Start" button, with the text "Welcome to blendOS", "Press Start to start installing blendOS!"](/assets/blendos/1.png)

## First use

Upon first boot, blendOS drops you into a pretty standard GNOME session with a graphical setup to add a user account, set timezone, and all that.

Here's the default `/system.yaml` file provided:

```yaml
impl: http://github.com/blend-os/tracks/raw/main
repo: https://pkg-repo.blendos.co
track: default-gnome
```

At first I wasn't sure what impl is doing, but according to the [`system.yaml` docs] seems to be combined with the track to get the URL for the raw `yaml` file.[^1]

This is actually a really interesting bit, as it means you can just, say, host your own track(s) for all your computers in a Git repo, and they can each inherit from other configs[^2] or be overridden locally; this actually seems like a very interesting and viable way to centrally manage many computers running Linux, and given I'm constantly switching between several computers; I can just put my config(s) in one repo, and pull from that.

(details on this at [`system.yaml` docs] -> Creating a track repo/webserver)

## Configuration

blendOS's configuration is really simple:

```yaml
impl: http://github.com/blend-os/tracks/raw/main
repo: https://pkg-repo.blendos.co
track: default-gnome

arch-repo: 'https://repo-goes-here.example'

packages:
  - 'fish'

aur-packages:
  - 'EVEN-MORE-FISH'

services:
  - 'service-goes-here'

user-services:
  - 'user-service-goes-here'

package-repos:
  - name: 'repo name'
    repo-url: 'https://repo.url'

commands:
  'echo hiiiiiii > /home/user/helloooooo'
```

(from [`system.yaml` docs])

It's quite basic, but blendOS's design actually works very well for me; I already have a Git repo of [all my configs](https://git.askiiart.net/askiiart/configs), which are intended to be run from a clean installation automatically, so for blendOS I just have to put those scripts into the yaml file and adapt it so the packages are listed in the YAML rather than being installed with `pacman`, `paru` or the like (at least, not directly, via `akshara` instead)

## Problems

*By far*, the biggest of all blendOS's problems is how slow it is to rebuild. It doesn't save "layers" like [`rpm-ostree`][`rpm-ostree` docs] (as used by Fedora atomic); instead, it just completely rebuilds the system every single time. Because of this, it takes a long time to run the updater/rebuilder, even to just install one more package.

Besides that, my only complaints are:

1. The `akshara`'s (the update/rebuild tool) major issue with reinheritance (see [`system.yaml` docs] -> Inheritance).
2. Its community and issue tracking is primarily on Discord, which is then indexed by Answer Overflow so it's searchable with Google and the like; there's no dedicated developer space (only one issue on [their GitLab][blendOS GitLab], where `akshara` is hosted.) However, given you must be pretty competent with Linux to be using blendOS in the first place, and how small the dev team and community is, this isn't much of an issue.
3. There's a lack of documentation for some bits, though the docs are updated and getting new additions constantly.

I've encountered more bugs and missing features since then, but I'll talk about that in my next post, as they'll fit better there.

## Wishlist

This is some other stuff I want, not necessarily problems, but things I'd like added

- I'd like an equivalent of this at the user level specifying packages, repos, and commands for other (containerized) distros.
- I'd like to be able to automatically install blendOS - to be able to script it rather than going through the GUI. Just a tarball of the installed system would be great.

## Sources

Sources are linked as they're used throughout, and also listed separately here.

[blendOS Homepage]: https://blendos.co/
[Introduction to blendOS]: https://blendos.co/install/post-install/intro/
[blendOS reference]: https://blendos.co/reference/
[`system.yaml` docs]: https://blendos.co/reference/configs/system/
[blendOS GitLab]: https://git.blendos.co/blendOS
[`rpm-ostree` docs]: https://coreos.github.io/rpm-ostree/
[blendOS's Git structure]: https://blendos.co/contributing/#git-structure

<!-- Link definition are above, separate (rendered) links below -->

1. [blendOS Homepage]
2. [Introduction to blendOS]
3. [blendOS reference]
4. [`system.yaml` docs]
5. [blendOS GitLab]
6. [`rpm-ostree` docs]
7. [blendOS's Git structure]

Note: As I write this, the docs, particularly the [blendOS reference], are being constantly revised. During the process of writing this, an entire new section has been added, though this post doesn't touch on that and said section is unused here - it'll come into play in the next post.

## Footnotes

[^1]: That is, `http://github.com/blend-os/tracks/raw/main` + `/` + `default-gnome` + `.yaml`; also, I probably should've just... read the documentation from the start, instead of figuring this out on my own and only later checking the docs.

[^2]: For example, in the provided `blend-os/tracks` repo, `default-gnome` actually inherits from the `gnome` track.

<!-- Note if you're viewing the Markdown version: [^1] is for footnotes; that's the formatting used by Pandoc, but VS Code, for example, doesn't support it. -->