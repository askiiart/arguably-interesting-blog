# Using `clap`

Clap stands for Command Line Argument Parser, and put simply, it's a great library for making command-line stuff with Rust. Even Cargo, Rust's package manager, depends on it (*Cargo/cargo.toml at master*), and it's been downloaded over 300 million times (*Clap - Crates.io: Rust package registry*).

Rather than going over everything clap can do, I'll go over how I've used it in my `disk-read-benchmark` program I'll be using in my next blog post.

## Basics

First off, we need to install `clap`; make sure to enable its `derive` feature as that's what we'll be using.

```sh
cargo add clap --features derive
```

First off, we need to get a bit of code just to start off:

```rust
use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(version, about, long_about = None)]
pub struct Cli {
    #[command(subcommand)]
    pub command: Commands,
}
```

This has the built-in "version" and "about" options, with the long "about" option disabled.

Next, we need to list all out commands we'll have:

```rust
#[derive(Subcommand)]
pub enum Commands {
    ///Run this thing
    Run,
    ///Delete the stuff that thing does
    Delete,
}
```

The documentation comments (`///`) should *not* have a space after the slashes, as otherwise the program will have an extra space where it shouldn't.

Finally, we create the `main()` function. First it parses everything, then checks what command was run and runs the relevant code.

```rust
fn main() {
    let cli = Cli::parse();

    match cli.command {
        Commands::Run {
            run();
        }
        Commands::Delete {
            delete();
        }
    }
}
```

That's all you need to know to use `clap` at a very basic level; for more details, check out the docs (*clap Documentation*). But, you probably don't want to have to type in the entire command automatically, autocomplete would be nice. So I'll also go over how to use `clap_complete` as well.

## `clap_complete`

Searching through the documentation (*Clap_complete Documentation*), you'll notice that the docs don't cover how to use it with clap's derive at all. Instead, after some Googling, I found an example script in *clap*'s repository (*completion-derive.rs at master*), which I then adapted and played around with a bit until I got it figured out.

Anyways, again, we need to install `clap_complete` first:

```sh
cargo add clap_complete
```

Then, add the relevant imports. We'll just being doing it for the fish shell since that's what I use, so we'll only import `Fish`; Bash, Zsh, PowerShell, and Elvish are also supported.

```rust
use clap_complete::aot::{generate, Fish};
```

Then, we need to add a command to generate the completion:

```rust
#[derive(Subcommand)]
pub enum Commands {
    ///Run this thing
    Run,
    ///Delete the stuff that thing does
    Delete,
    ///Generate fish completions
    FishCompletions,
}
```

Next, we actually generate the completion, adding it like it's another command:

```rust
    match cli.command {
        Commands::Run {
            run();
        }
        Commands::Delete {
            delete();
        }
        Commands::GenerateFishCompletions => {
            generate(
                Fish,
                &mut Cli::command(),
                "example-program",
                &mut stdout(),
            );
        }
    }
```

To explain the options for `generate()`:

- `Fish`: The shell we're using.
- `&mut Cli::command()`: I don't actually know what this does, but understanding ths library fully this is beyond my pay grade, especially given the somewhat lacking docs.
- `"example-program"`: The name of our program
- `&mut stdout()`: `stdout`, so that it can print the completions. Why does it do it this way? I don't know, it doesn't make sense to me. Why doesn't it just return it as a String? I don't know. But it works, I suppose.

As an example of all this, here's my `disk-read-benchmark` program, running using all this. The commands have formatting I can't do, so it looks even better than I can even show here.

```txt
~> disk-read-benchmark
Usage: disk-read-benchmark <COMMAND>

Commands:
  generate-bash-completions  Generate bash completions
  generate-zsh-completions   Generate zsh completions
  generate-fish-completions  Generate fish completions
  grab-data                  Grabs the datasets used for benchmarking
  benchmark                  Runs the benchmark
  prep-dirs                  Prepares the directories so other programs can prepare their datasets
  run                        Runs it all
  help                       Print this message or the help of the given subcommand(s)

Options:
  -h, --help     Print help
  -V, --version  Print version
~> disk-read-benchmark generate-fish-completions | source
~> disk-read-benchmark benchmark --help
Runs the benchmark

Usage: disk-read-benchmark benchmark

Options:
  -h, --help  Print help
```

To better see how great it looks, here's a screenshot:

![The same output, but with very nice formatting - underlining and bolding for headers and the tables](/assets/using-clap/1.png)

Pressing tab twice after entering `disk-read-benchmark` displays the completions, which I can select and use like any other program's.

```txt
~> disk-read-benchmark
benchmark                         (Runs the benchmark)  grab-data                               (Grabs the datasets used for benchmarking)
generate-bash-completions  (Generate bash completions)  help                   (Print this message or the help of the given subcommand(s))
generate-fish-completions  (Generate fish completions)  prep-dirs  (Prepares the directories so other programs can prepare their datasets)
generate-zsh-completions    (Generate zsh completions)  run                                                                  (Runs it all)
```

## Sources

&emsp;- clap contributors. “clap Documentation.” Clap - Rust, [docs.rs/clap/latest/clap/](https://docs.rs/clap/latest/clap/). Accessed 12 Nov. 2024.\
&emsp;- clap_complete contributors. “Clap_complete Documentation.” Clap_complete - Rust, [docs.rs/clap_complete/latest/clap_complete](https://docs.rs/clap_complete/latest/clap_complete). Accessed 12 Nov. 2024.\
&emsp;- clap contributors. “clap/clap_complete/examples/completion-derive.rs at master · Clap-Rs/Clap.” GitHub, [github.com/clap-rs/clap/blob/master/clap_complete/examples/completion-derive.rs](https://github.com/clap-rs/clap/blob/master/clap_complete/examples/completion-derive.rs). Accessed 12 Nov. 2024.\
&emsp;- cargo contributors. “cargo/Cargo.Toml at master · rust-lang/cargo.” GitHub, [github.com/rust-lang/cargo/blob/master/Cargo.toml](https://github.com/rust-lang/cargo/blob/master/Cargo.toml). Accessed 12 Nov. 2024.\
&emsp;- “Clap - Crates.io: Rust Package Registry.” crates.io, crates.io/crates/clap. Accessed 12 Nov. 2024.
