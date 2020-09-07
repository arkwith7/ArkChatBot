import os
import sys

from DialogManager.tf_chat_bot_response import *


os.environ["TF_CPP_MIN_LOG_LEVEL"]="3"
# import warnings
# warnings.filterwarnings('ignore', '.*do not.*',)
# ???™” ë§ë­‰ì¹˜ì? ???™” ?˜?„ê°? ? •?˜?œ JSON ë¬¸ì„œ ì§‘í•© ?½ê¸?
# input_file_name = '../ArkNLU/DialogIntents/intents.json'
project_path = "C:/Business/Dev/workspace/ATDA/"
input_file_name = project_path + 'ArkChatFramework/ArkNLU/DialogIntents/intents_kr.json'
intents = read_dialog_intents_jsonfile(input_file_name)

for i in range(3):    # Add this for loop.
    sys.stdout.write('\033[F') # Back to previous line.
    sys.stdout.write('\033[K') # Clear line.

print(intents)
