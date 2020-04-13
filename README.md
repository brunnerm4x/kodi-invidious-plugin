# [Invidious](https://invidio.us) plugin for [Kodi](https://kodi.tv)

This plugin provides an [Invidious](https://invidio.us) client for [Kodi](https://kodi.tv). Invidious is a privacy-friendly web frontend to YouTube.


## Installation

To keep track with development, it is recommended to install the plugin with git:

```shell script
# please change the destination if necessary
git clone https://github.com/TheAssassin/kodi-invidious-plugin.git ~/.kodi/addons/plugin.video.invidious

# on an embedded device (e.g., an X96 Mini running CoreELEC, you need to clone to /storage/.kodi/addons/plugin.video.invidious
```

You can also download an archive and extract it in the right place instead of using git:

```shell script
# same here: make sure you change to the right directory
cd ~/.kodi/addons/

# download a zip archive
mkdir plugin.video.invidious
wget https://github.com/TheAssassin/kodi-invidious-plugin/archive/master.tar.gz -O - | tar xz --strip-components=1 -C plugin.video.invidious
```

You may have to restart Kodi before you can enable the plugin. To enable the plugin, please go to the addons settings, switch to *user plugins* and enable the plugin there.


## To Do

- evaluate using youtube-dl to remove dependency on third-party web service (maybe in a second plugin)
- implement adaptive streaming properly
- be able to open YouTube videos from [NewPipe](https://newpipe.net)
