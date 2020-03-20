cyberpower_exporter
===================

This is an application for exporting cyberpower ups metrics to Prometheus.

Installation
------------

First, install the CyberPower PowerPanel Personal Linux software: https://www.cyberpowersystems.com/product/software/power-panel-personal/powerpanel-for-linux/

Second, make sure you have python3 and pip3 installed. Then:

::

    sudo pip3 install git+https://gitlab.com/shouptech/cyberpower_exporter.git

Installing as root is important. The application must run as root in order to access the cyberpower data.

You could simply run it as root like this:

::

    sudo /usr/local/bin/cyberpower_exporter

But that would not be great because it wouldn't run in the background. If you're using systemd, it's easy to make a service.

Create the file /etc/systemd/system/cyberpower_exporter.service with these contents:

::

    [Unit]
    Description=CyberPower Exporter
    After=network-online.target

    [Service]
    Type=simple
    User=root
    Group=root
    ExecStart=/usr/local/bin/cyberpower_exporter
    SyslogIdentifier=cyberpower_exporter
    Restart=always

    [Install]
    WantedBy=multi-user.target

Then enable & start the service:

::

    $ sudo systemctl daemon-reload
    $ sudo systemctl enable cyberpower_exporter.service
    Created symlink /etc/systemd/system/multi-user.target.wants/cyberpower_exporter.service → /etc/systemd/system/cyberpower_exporter.service.
    $ sudo systemctl start cyberpower_exporter.service

If you have a firewall enabled, ensure you allow port 10100 through.

Test that it's working by running:

::

    curl <ipaddress>:10100

Now go ahead and point prometheus to it!
