# Dedicated Minecraft Server Upgrade Linux
Under normal circumstances, keeping the Minecraft Server up to date is a manual task which requires knowledge on when the later release are pushed by Minecraft. Typically Bedrock clients (Android/IOS/PS4/XBox etc) update themselves when a release is available which can cause issues when connecting to a public server.
<hr>
<b>Pre-Requisites:</b><br>
Python3 (tested using Python3.10)<br>
BeautifulSoup - <a href=https://beautiful-soup-4.readthedocs.io/en/latest/>https://beautiful-soup-4.readthedocs.io/en/latest/</a><br>
Ubuntu 20.04 + Script has been tested on both Ubuntu Server 20.04 and 22.04<br>
Screen - <a href=https://help.ubuntu.com/community/Screen>https://help.ubuntu.com/community/Screen</a><br>
<hr>
<b>Usage</b><br>
In "my" environment, I have a dedicated "Minecraft" user with the minecraft installation in its home directory. The Python script doesn't need root privileges to run, however it does need read/write permissions for the directory which Minecraft is located. The directory is defined as a variable within the script called "minecraft_dir". Edit this to the relevant directory.<br>
Upon completion of the script, the "bedrock_server" will be started in a screen created by the user who initiated the script:<br>
<code>screen -S Bedrock_Server</code>
