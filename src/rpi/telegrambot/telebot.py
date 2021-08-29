import os
import sys
import telepot
from dotenv import load_dotenv


fname = "users.txt"
dirPath = os.path.dirname(os.path.realpath(__file__))
filePath = os.path.join(dirPath, fname)
dotenv_path = os.path.join(dirPath, ".env")

welcome_msg = "Hi %s, Welcome to Resyringe!!!"
joined_msg = "Hi %s, you have already subscribed to Resyringe"
goodbye_msg = "Goodbye %s, it is sad to see you leave :("
not_join_msg = "Hi %s, you have not subscribe to Resyringe"
notification_msg = "%s have completed"

exitAPP = False


class teleNotification:
    def __init__(self):
        def handle(msg):
            global chat_id

            chat_id = msg['chat']['id']
            command = msg['text']
            name = msg['chat']['first_name']

            print('Message received from ' + str(chat_id))

            if command == '/join':
                returnMsg = self.addUser(chat_id)
                bot.sendMessage(chat_id, returnMsg % name)

            elif command == '/leave':
                returnMsg = self.removeUser(chat_id)
                bot.sendMessage(chat_id, returnMsg % name)

            else:
                bot.sendMessage(chat_id, 'Invalid command.')
                self.sendNotification()

        load_dotenv(dotenv_path=dotenv_path)
        try:
            global bot
            global exitAPP
            bot = telepot.Bot(os.getenv('ACCESS_TOKEN'))
            bot.message_loop(handle)
            while True:
                if exitAPP:
                    break
        except KeyboardInterrupt:
            sys.exit()
    
    
    def addUser(self, chatID):
        isExist = False
        lines = []
        
        if os.path.exists(filePath):
            with open(filePath, "r") as f:
                lines = f.readlines()

        with open(filePath, "a") as f:
            for line in lines:
                if line.strip("\n") == str(chatID):
                    isExist = True
                    break
            if not isExist:
                f.write(str(chatID))

            f.close()
        return joined_msg if isExist else welcome_msg


    def removeUser(self, chatID):
        isExist = False
        lines = []

        if os.path.exists(filePath):
            with open(filePath, "r") as f:
                lines = f.readlines()

            with open(filePath, "w") as f:
                for line in lines:
                    if line.strip("\n") != str(chatID):
                        f.write(line)
                    else:
                        isExist = True
            print (isExist)
            f.close()

        return goodbye_msg if isExist else not_join_msg
                
    def stopTelebot(self):
        global exitAPP
        exitAPP = True
        
    def sendNotification(self, jobType):
        msg = notification_msg % jobType
        
        if os.path.exists(filePath):
            with open(filePath, "r") as f:
                lines = f.readlines()
                for line in lines:
                    bot.sendMessage(line.strip("\n"), msg)


if __name__ == "__main__":
    teleBot = teleNotification()
