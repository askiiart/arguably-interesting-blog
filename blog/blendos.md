# Checking out blendOS

---

WARNING: This page is a work-in-progress, and is very incomplete. Read at your own risk.

---

blendOS is self-described as "Arch Linux, made declarative, immutable and atomic." And yeah, that's a pretty good description of what it is. But you can never *really* tell what a distro is like without trying it, so...

## Installation

I decided to just run blendOS in a virtual machine; I had a bunch of data I hadn't backed up yet and was actively working on, and didn't feeling like switching yet given I had no experience with blendOS v4 - I've actually tried blendOS v3 before, back when v4 was in alpha, but it had practically zero documentation, not even `man` pages, so I gave up on it very quickly. But with v4, hopefully it's improved since then.

## First use

Upon first boot, blendOS drops you into a pretty standard GNOME session, on account of the `/system.yaml` file by default:

```yaml
impl: http://github.com/blend-os/tracks/raw/main
repo: https://pkg-repo.blendos.co
track: default-gnome
```

At first I wasn't sure what impl is doing, but it seems to be combined with the track to get the URL for the raw `yaml` file[^1].

This is actually a really interesting bit *which isn't documented*, as it means you can just, say, host your own track(s) for all your computers in a Git repo, and they can each inherit from other configs[^2] or be overridden locally; this actually seems like a very interesting and viable way to centrally manage many computers running Linux, and given I'm constantly switching between several computers; I can just put my config(s) in one repo, and pull from that.

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

It's quite basic, but blendOS actually works very well for me; I already have a Git repo of [all my configs](https://git.askiiart.net/askiiart/configs), which are intended to be run from a clean installation automatically, so for blendOS I just have to put those scripts into the yaml file and adapt it so the packages are listed in the YAML rather than being installed with `pacman` or `yay`.

## Problems

Biggest of all blendOS's problems is how slow it is to rebuild. It doesn't save "layers" of packages like [`rpm-ostree`](https://github.com/coreos/rpm-ostree) (as used by Fedora atomic)

## Wishlist

## Sources

- \[1\] [blendOS homepage](https://blendos.co/)
- \[2\] [blendOS post-install intro](https://blendos.co/install/post-install/intro/)

## Footnotes

[^1]: That is, `http://github.com/blend-os/tracks/raw/main` + `/` + `default-gnome` + `.yaml`
[^2]: In the provided `blend-os/tracks` repo, `default-gnome` actually inherits from the `gnome` track.
