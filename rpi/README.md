# Asteroid
Raspberry Pi + python to make an asteroid simulator inside a translucent ball

## Installation
This setup assumes Raspbian Stretch and Rasperry zero W to be connected to internet.

SSH into raspberry as root

```
ssh root@<IP-address>
```

Then let's install basic tools, configure system basics

```
apt-get update && apt-get upgrade && apt-get dist-upgrade
apt-get install -y raspi-config raspi-copies-and-fills locales tzdata nano git bash-completion sudo python3 python3-venv python3-dev build-essential libssl-dev libffi-dev raspberrypi-sys-mods # Some or all can be there already
dpkg-reconfigure locales # Choose appropriate locales and timezone for you, usually en_US.UTF-8 and some local one, for system default I recommend en_US.UTF-8
dpkg-reconfigure tzdata
reboot
```

After reboot, SSH back in

```
ssh root@<IP-address>
```

Create user for running Asteroid, no admin privileges

```
groupadd gpio
useradd -c "Vaasa Hacklab Asteroid" -U -m -d /home/asteroid -s /bin/bash -G dialout,gpio asteroid
passwd asteroid
```

Give gpio-group privileges to access GPIO without root

```
chown root.gpio /dev/gpiomem
chmod g+rw /dev/gpiomem
```

Exit user root SSH-session

```
exit
```

## Login with user asteroid
```
ssh asteroid@<ip-address>
```

Fetch and setup Asteroid

```
git clone https://github.com/vaasahacklab/asteroid.git
cd asteroid
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..
```

Exit user asteroid SSH-session

```
exit
```
## Login again with root

```
ssh root@<IP-address>
```

Copy asteroid systemd service -file into systemd and enable it

```
cp /home/asteroid/asteroid/rpi/asteroid.service.example /lib/systemd/system/asteroid.service
systemctl daemon-reload
systemctl enable asteroid.service
exit
```

Lastly make Rasperry to act as an wireless access point, follow for example this tutorial: https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md


## Optional

Highly recommended is to also add sudo user for maintenance, not for public usage, and disable root login:

SSH into raspberry as root

```
ssh root@<IP-address>
```

Generate new user for admin things:

```
useradd -c "Vaasa Hacklab" -d /home/hacklab -m -s /bin/bash -U -G sudo hacklab
passwd hacklab
exit
```

then ssh with new user:

```
ssh hacklab@<IP-address>
```

then run to disable root login:

```
sudo passwd -l root
exit
```
