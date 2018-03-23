# tinker-dash

A simple Selenium browser launcher which rotates a sequence of browser tabs.

This launcher was developed to display online dashboard pages using the
Chromium browser. The launcher is intended to run on a single board ARM computer,
such as an ASUS Tinker Board or a Raspberry Pi, which is connected to a monitor.

## Getting Started

These instructions will get a copy of the project up and running on your
ARM device for development and testing purposes. These instructions cover
installation on a Debian based operating system such as TinkerOS-Debian or
Raspbian. The project was developed on TinkerOS-Debian running on an ASUS
Tinker Board. It has not been tested on a Raspbian environment.

The list of dashboard pages is maintained in the file the-dashboard-list.txt.

### Prerequisites

The launcher utilises Selenium WebDriver bindings to drive the browser
(http://www.seleniumhq.org/). These bindings require the ChromeDriver
server executable, which can be installed to a local /bin directory
and added to the PATH. An ARM build of the ChromeDriver is available
from the Electron GUI project (https://github.com/electron).

### Installing

This project is installed to the default /home/linaro folder of the
ASUS Tinker Board. To install ChromeDriver and tinker-dash to this folder
use the following steps:
```
sudo apt-get install python-pip

pip install selenium

cd /home/linaro/

git clone https://github.com/anthonyblanchflower/tinker-dash.git

mkdir bin

cd /home/linaro/bin

wget https://github.com/electron/electron/releases/download/v1.8.0/chromedriver-v1.8.0-linux-arm.zip

unzip -a chromedriver-v1.8.0-linux-arm.zip

export PATH="/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games:/home/linaro/bin"
```

An additional step is required to install the gecko driver for Firefox:
```
/bin/bash set-up.sh <OS Type>
```

### Usage

#### Cloud content synchronisation across multiple ARM devices

In production environments I run this launcher on several ARM devices and
host the dashboard list file in an AWS public S3 bucket. This allows me to
synchronise the content displayed across each device. I then use the Requests
HTTP library to populate the dashboard list. This requires me to use
an alternative pull_list function:
```
import requests

def pull_list(list_file):
    found = False

    # Incase the list is being edited retry the request
    while not found:
        request = requests.get(list_file)
        if request.status_code == 200:
            found = True
    return request.content.split()
```
For this version of the pull_list function, the DASHBOARD_LIST global contains
the object key for the dashboard list file:
```
DASHBOARD_LIST = 'http://xxxxx.s3-website-eu-west-1.amazonaws.com/DashboardList/the-dashboard-list.txt'
```
#### Starting the launcher on boot

To launch tinker-dash automatically after a system boot, I create this tinker-dash.sh
file in /home/linaro/tinker-dash:
```
#!/bin/bash
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games:/home/linaro/bin"
python /home/linaro/tinker-dash/tinker-dash.py
```

I then create a tinkerdash.desktop file in /usr/share/applications:
```
[Desktop Entry]
Name=Kiosk Autostart
Exec=/home/linaro/tinker-dash/tinker-dash.sh
Type=Application
Terminal=false
```

This tinkerdash.desktop file should then be copied to /home/linaro/.config/autostart/

## License

This project is licensed under the MIT License - see the LICENSE file for details

## Acknowledgements

http://www.seleniumhq.org/

https://github.com/electron

https://github.com/DanteLore

https://public.tableau.com/en-us/s/gallery
