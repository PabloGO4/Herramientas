import glob
import os
import time


class VideoOBS:

    @staticmethod
    def startRecordingVideo():
        oldFolder = os.getcwd()
        os.chdir(r'C:\Program Files\obs-studio\bin\64bit')
        command = "start {}".format('obs64.exe --startrecording')
        os.system(command)
        time.sleep(5)
        os.chdir(oldFolder)

    @staticmethod
    def stopRecordingVideo():
        commandKillTask = "taskkill /F /im {}".format('obs64.exe')
        os.system(commandKillTask)

        time.sleep(3)

        username = os.getenv('username')
        listFiles = glob.glob(os.path.join(r'C:\Users', username, r'Videos\*mkv')) # * means all if need specific format then *.csv
        latestFile = max(listFiles, key=os.path.getctime)
        print(latestFile)

        return latestFile






