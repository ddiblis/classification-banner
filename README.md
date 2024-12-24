# Classification-Banner

[![Python linting](https://github.com/SecurityCentral/classification-banner/actions/workflows/python-linting.yaml/badge.svg?branch=main)](https://github.com/SecurityCentral/classification-banner/actions/workflows/python-linting.yaml)

Classification Banner is a python script that will display the
classification level banner of a session with a variety of
configuration options on the primary screen.  This script can
help government and possibly private customers display a
notification that sensitive material is being displayed - for
example PII or SECRET Material being processed in a graphical
session. The script has been tested on a variety of graphical
environments such as GNOME2, GNOME3, KDE, twm, icewm, and Cinnamon.

Python script verified working on Red Hat Enterprise Linux and Fedora.

Selecting the classification window and pressing the ESC key
will temporarily hide the window for 15 seconds, it will return
to view after that

# Installation

<!-- ## Fedora
`classification-banner` can be found in the Fedora repositories and installed
via `dnf`:
```sh
dnf -y install classification-banner
```

## RHEL
`classification-banner` can be found in the [EPEL](https://fedoraproject.org/wiki/EPEL) repositories and installed
via `yum`:
```sh
yum -y install classification-banner
``` -->

## Source
To install directly from source, run the following command:
```sh
python setup.py install
```

# Classification Banner Usage

Options should be placed in the `/etc/classification-banner/banner.conf` file.

* `message` - The classification level to display (Default: `UNCLASSIFIED`)
* `fgcolor` - Foreground color of the text to display (Default: `#FFFFFF` "White")
* `bgcolor` - Background color of the banner the text is against (Default: `#007A33` "Green")
* `style` - Syle of banner, choose between Modern and Classic


For your convenience you can set the banner type using the following commands:
(Doing so will automatically set the text and color profile for the banner correctly)

* -u, --unclassified
* -cui, --cui
* -c, --confidential
* -s, --secret
* -ts, --top_secret
* -tssci, --ts_sci
<!-- * `font` - Font face to use for the displayed text (Default: `liberation-sans`)
* `size` - Size of font to use for text (Default: `small`)
* `weight` - Bold or normal (Default: `bold`)
* `show_top` - Show top banner (Default: `True`)
* `show_bottom` - Show bottom banner (Default: `True`)
* `horizontal_resolution` - Manually Set Horiztonal Resolution (OPTIONAL) [if hres is set, vres required]
* `vertical_resolution` - Manually Set Horiztonal Resolution (OPTIONAL) [if vres is set, hres required]
* `sys_info` - Show user and hostname in the top banner (Default: `False`)
* `opacity` - Sets opacity - for composted window managers only (OPTIONAL) [float - range 0 .. 1] (Default: `0.75`)
* `esc` - Enable/Disable the 'ESC to hide' message (Default: `True` (enabled))
* `spanning` - Enable banner(s) to span across screens as a single banner (Default: `False`) -->

Command line options that correspond to the above settings (use `classification-banner --help` for more information):

```
-M, --message
-F, --fgcolor
-B, --bgcolor
-S, --style
-u, --unclassified
-cui, --cui
-c, --confidential
-s, --secret
-ts, --top_secret
-tssci, --ts_sci
```
<!-- --font
--size
--weight
--hide-top
--hide-bottom
-x, --hres
-y, --vres
--system-info
-o, --opacity
--disable-esc
--enable-spanning -->


# Examples

These are examples for the configuration of the Classification Banner
using the `/etc/classification-banner/banner.conf` file for various classifications
based upon generally accepted color guidelines in the DoD/IC.

## Examples from the default `banner.conf`:


### UNCLASSIFIED (Default)

```
    message = UNCLASSIFIED
    foreground = #FFFFFF
    background = #007A33
```

### CONTROLLED UNCLASSIFIED INFORMATION

```
    message = CUI
    foreground = #FFFFFF
    background = #502B85
```

### CONFIDENTIAL

```
    message = CONFIDENTIAL
    foreground = #FFFFFF
    background = #0033A0
```

### SECRET

```
    message = SECRET
    foreground = #FFFFFF
    background = #C8102E
```

### TOP SECRET

```
    message = TOP SECRET
    foreground = #FFFFFF
    background = #FF8C00
```

### TOP SECRET//SCI

```
    message = TOP SECRET//SCI
    foreground = #000000
    background = #FCE83A
```

# Autostart

To auto-start the classification-banner script on the GNOME Desktop,
create the file `/etc/xdg/autostart/classification-banner.desktop`
with the following contents:

```ini
[Desktop Entry]
Name=Classification Banner
Exec=/usr/bin/classification-banner
Comment=User Notification for Security Level of System.
Type=Application
Encoding=UTF-8
Version=1.0
MimeType=application/python;
Categories=Utility;
X-GNOME-Autostart-enabled=true
StartupNotify=false
Terminal=false
```
