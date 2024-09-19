# OCI Images as a "Filesystem": Vanilla OS

In looking for a layered solution to blendOS's issues, I found that the lead maintainer and creator of blendOS was looking into using OCI images, and has even forked a repo from Vanilla OS. So I'm trying out Vanilla OS's usage of OCI images (which are inherently layered) to see about implementing a similar system in blendOS.

## Installation

Installation is pretty simple, you're again dropped into a simple GNOME session with a GTK installer:

![A basic GNOME session with a white GTK-based installer; it's showing the date and time/time zone selector.](/assets/vanilla-os/1.png)

The process was very similar to blendOS's, though it also detects virtual machines and offers an option to install tools (e.g. clipboard sharing, video drivers) to help with that.

Another notable bit is that it requires more space than blendOS, with a minimum disk size of 50 GB, but given its A/B slot architecture (which I'll get to later), this makes sense.

## First boot

On first boot, there's a very similar setup tool, surely based off the installer. It makes you put in your language, timezone, etc. again, which I was a bit annoyed by, but it's no big deal. Then it has you create your login, select what you want installed (from basic programs like a calendar, office suite, etc.), then restarts and does all that.

![A similar wizard to the installer; it has the Vanilla OS logo and says "Welcome", "Make your choices, this wizard will take care of everything"](/assets/vanilla-os/2.png)

Then you just get a little slideshow detailing automatic updates, its Apx package manager, and other basics, nothing interesting, and nothing I care about.

## Usage and configuration

I tried checking the docs (*Vanilla OS Docs*), which by themselves were difficult to find. They're a bit hidden in "Help" despite being *absolutely essential* to using this distro[^1]. But what I found easily was screenshots of Overwatch. (*Vanilla OS*)

Regardless, once I found the docs, I tried to figure out how it worked, and I was still very confused. After looking over it again, I decided to check Apx's docs, its package manager, and found how to install packages, of course. (*Vanilla OS Docs*) I tried to install GParted; after it not running at first due to Vanilla OS not being configured correctly and not showing a password prompt for it, causing GParted to exit, I ran it in the terminal with `sudo`, just to get a permission denied error. That's because all packages are installed in containers, there is no system package manager... kinda.

### ABRoot

ABRoot is the magic behind Vanilla OS's OCI image backend. As far as I can tell (again, I don't believe there are no relevant for docs for this) it essentially generates a tarball of the relevant data for the new iteration, then symlinks to either that or the current iteration on boot, depending on what the user selects. It provides essentially no advantages over blendOS's approach, and is, in my opinion, massively overcomplicated. (*GitHub: Vanilla-os/abroot*)

It also acts as a package manager of sorts - it's the only way to install packages system-wide on Vanilla OS, and it does this by running `apt` when the new image is built, similar to Akshara.

ABRoot's config file is at `/etc/abroot/abroot.json`, but it doesn't support declarative system-wide packages. Instead, run the following:

```bash
abroot pkg add $PACKAGE_NAME
```

(*Install additional drivers and libraries in Vanilla OS*)

## Conclusion

Vanilla OS wasn't very helpful as to OCI-based layers, but I don't think it was a complete waste of time. Vanilla OS gave me some ideas, and I like its backend's ideas; it will most likely serve as inspiration for when I add layers to blendOS. Plus, my idea would have an advantage: compression.

But I'll get into it later, once it's a bit more fleshed out; plus, that's not the point of this post anyways.

P.S. I can't get it across while keeping this post decent quality and on-topic, but I need to emphasize how confusing the docs were for Vanilla OS. It feels like they try to appeal to users with basic tech literacy while not explaining how it actually works or what anything does. They write how-to guides, not documentation.

## Footnotes

[^1] Below the big download button, there's a link to the installation guide, but this provides nothing helpful, it just guides you through the already extremely simple installation.

## Sources

“Install Additional Drivers and Libraries in Vanilla OS.” *Vanilla OS Docs*, Vanilla OS, [docs.vanillaos.org/handbook/en/install-additional-drivers](https://docs.vanillaos.org/handbook/en/install-additional-drivers). Accessed 19 Sept. 2024.\
“Vanilla OS Docs.” *Vanilla OS*, Vanilla OS, [docs.vanillaos.org/collections/docs](https://docs.vanillaos.org/collections/docs). Accessed 19 Sept. 2024.\
*Vanilla OS*, [vanillaos.org](https://vanillaos.org). Accessed 19 Sept. 2024.\
Vanilla-OS. “GitHub: Vanilla-Os/Abroot.” *GitHub*, [github.com/Vanilla-OS/ABRoot](github.com/Vanilla-OS/ABRoot). Accessed 19 Sept. 2024.
