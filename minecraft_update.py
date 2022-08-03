from bs4 import BeautifulSoup
import requests, re, os, urllib.request, shutil, zipfile, glob, time, sys

def ubuntu_server(href):
    return href and re.compile("linux").search(href)

def server_update():
    ''' Update the below variable to your Minecraft Server Home Directory '''
    #minecraft_dir = "/home/minecraft/"
    
    current_time = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    with open("{}minecraft_server_update.log".format(minecraft_dir), "a") as log_file:
        log_file.write("{}      Checking for Minecraft Server Updates\n".format(current_time))
    time.sleep(5)

    url = "https://www.minecraft.net/en-us/download/server/bedrock"
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36 Edge/12.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")


    #This section goes through the html 'a' tag and extracts the URL to in which we will need
    #to download the latest version
    link = soup.find_all(href=ubuntu_server)
    link = str(link)
    link = link.split("=")
    link = link[5]
    link = link.split('"')
    link = link[1]

    #Next we need to extract the version information from the link as there is no point in
    #downloading it if we are already on the latest version
    web_version = link.split("/")
    web_version = web_version[-1]

    if os.path.exists("{}{}".format(minecraft_dir, web_version)) == False:
        #Notify connected users that the server will be restarted shortly
        if sys.platform == "linux":
            os.system("screen -S Bedrock_Server -p 0 -X stuff 'say Minecraft Update has been identified^M'")
            os.system("screen -S Bedrock_Server -p 0 -X stuff 'say Server will be stopped in 10 minutes^M'")
            time.sleep(600)
            os.system("screen -S Bedrock_Server -p 0 -X stuff 'stop^M'")

        #Remove the old zip file
        pattern = "[a-z]*.zip"
        for i in glob.iglob(pattern):
            os.remove(i)

        #Download the new zip file
        file_path = "{}{}".format(minecraft_dir, web_version)
        urllib.request.urlretrieve(link, file_path)
        current_time = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        with open("{}minecraft_server_update.log".format(minecraft_dir), "a") as log_file:
            log_file.write("{}      Downloading the new version\n".format(current_time))
        if os.path.exists("{}TEMP".format(minecraft_dir)) == False:
            os.mkdir("{}TEMP".format(minecraft_dir))
        else:
            os.rmdir("{}TEMP".format(minecraft_dir))
            os.mkdir("{}TEMP".format(minecraft_dir))
        shutil.copy("{}{}".format(minecraft_dir, web_version), "{}TEMP/{}".format(minecraft_dir, web_version))

        #Process the compressed file
        current_time = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        with open("{}minecraft_server_update.log".format(minecraft_dir), "a") as log_file:
            log_file.write("{}      Processing the new files\n".format(current_time))
        zip_file = "{}TEMP/{}".format(minecraft_dir, web_version)
        with zipfile.ZipFile(zip_file) as z:
            z.extractall(path="{}TEMP/".format(minecraft_dir))
        os.remove(zip_file)
        
        #Remove files that could cause problems with the current server instance
        if os.path.exists("{}TEMP/allowlist.json".format(minecraft_dir)):
            os.remove("{}TEMP/allowlist.json".format(minecraft_dir))
        if os.path.exists("{}TEMP/permissions.json".format(minecraft_dir)):
            os.remove("{}TEMP/permissions.json".format(minecraft_dir))
        if os.path.exists("{}TEMP/server.properties".format(minecraft_dir)):
            os.remove("{}TEMP/server.properties".format(minecraft_dir))

        #Move the remaining files to the parent directory
        for f in os.listdir("{}TEMP/".format(minecraft_dir)):
            try:
                shutil.move("{}TEMP/{}".format(minecraft_dir, f), "{}{}".format(minecraft_dir, f))
            except:
                current_time = time.strftime("%Y%m%d-%H%M%S", time.localtime())
                with open("{}minecraft_server_update.log".format(minecraft_dir), "a") as log_file:
                    log_file.write("{}      Error processing {}TEMP/{}\n".format(current_time, minecraft_dir, f))  
        
        current_time = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        with open("{}minecraft_server_update.log".format(minecraft_dir), "a") as log_file:
            log_file.write("{}      File processing complete\n".format(current_time))
        time.sleep(10)
        current_time = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        with open("{}minecraft_server_update.log".format(minecraft_dir), "a") as log_file:
            log_file.write("{}      Starting the cleanup process\n".format(current_time))

        #Clean-up
        try:
            os.rmdir("{}TEMP".format(minecraft_dir))
        except PermissionError:
            current_time = time.strftime("%Y%m%d-%H%M%S", time.localtime())
            with open("{}minecraft_server_update.log".format(minecraft_dir), "a") as log_file:
                log_file.write("{}      Unable to remove TEMP directory due to permission error\n".format(current_time))

        current_time = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        with open("{}minecraft_server_update.log".format(minecraft_dir), "a") as log_file:
            log_file.write("{}      Minecraft server has been updated\n".format(current_time))

        #Restart the Minecraft Server
        if sys.platform == "linux":
            os.system("chmod +x {}bedrock_server".format(minecraft_dir))
            os.system("screen -S Bedrock_Server -d -m {}bedrock_server".format(minecraft_dir))

    else:
        current_time = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        with open("{}minecraft_server_update.log".format(minecraft_dir), "a") as log_file:
            log_file.write("{}      Minecraft server is at the latest version\n".format(current_time))

server_update()
