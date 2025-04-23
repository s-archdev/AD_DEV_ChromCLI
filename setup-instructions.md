# Installing AD_DEV_ChronCLI

Follow these steps to install AD_DEV_ChronCLI on your Mac:

## Prerequisites

- Mac OS X (10.14 Mojave or newer recommended)
- Python 3.6 or higher (comes pre-installed on newer Macs)
- Terminal access

## Step 1: Download the files

Save the following files to a directory on your Mac:

1. `chroncli.py` - The main script
2. `setup.py` - The installation script

## Step 2: Make the scripts executable

Open Terminal and navigate to the directory where you saved the files, then:

```bash
chmod +x chroncli.py
chmod +x setup.py
```

## Step 3: Run the installer

```bash
./setup.py
```

This will:
- Create an installation directory at `~/ad_dev_chroncli/`
- Create a configuration directory at `~/.ad_dev_chroncli/`
- Copy the main script to the installation directory
- Create a symlink in `~/bin/`
- Update your PATH if needed

## Step 4: Start using AD_DEV_ChronCLI

After installation, you can run the application by typing:

```bash
chroncli
```

If you see an error about the command not being found, you may need to update your PATH manually:

```bash
export PATH="$PATH:$HOME/bin"
```

You can add this line to your `~/.bash_profile` or `~/.zshrc` to make it permanent.

## Troubleshooting

### "ModuleNotFoundError: No module named 'curses'"

The curses module should be included with Python on macOS. However, if you're using a custom Python installation or encountering issues, try:

```bash
pip3 install windows-curses
```

### "ImportError: No module named _curses"

This may happen if you're using a Python installation without curses support. Try installing the Python that comes with macOS or use Homebrew:

```bash
brew install python
```

### "chroncli: command not found"

Make sure `~/bin` is in your PATH. You can verify this by running:

```bash
echo $PATH
```

If `~/bin` is not listed, add it to your PATH as described in Step 4.

## Uninstallation

To remove AD_DEV_ChronCLI from your system, run:

```bash
rm -rf ~/ad_dev_chroncli
rm -rf ~/.ad_dev_chroncli
rm ~/bin/chroncli
```

This will remove the application and all its data.
