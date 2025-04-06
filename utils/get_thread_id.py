import requests
# from data.config import BOT_TOKEN
# def fetch_message_thread_ids(bot_token, chat_id):
#     """
#     Fetch all message_thread_ids from a Telegram group chat.
#     :param bot_token: Your bot's API token.
#     :param chat_id: Group chat ID (with -100 prefix for supergroups).
#     :return: List of message_thread_ids with basic info.
#     """
#     url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
#     response = requests.get(url)
#     data = response.json()

#     thread_ids = []
#     if data['ok']:
#         for update in data['result']:
#             if 'message' in update and 'message_thread_id' in update['message']:
#                 thread_ids.append({
#                     'topic_name': update['message'].get('text', 'No Name'),
#                     'message_thread_id': update['message']['message_thread_id']
#                 })
#     return thread_ids

# # Example usage
BOT_TOKEN = "7412101195:AAGC19QaOd9DkkN80be6Zyuif3DupNGIJzY"
CHAT_ID = -1002342888585  # Replace with your group chat ID
# threads = fetch_message_thread_ids(BOT_TOKEN, CHAT_ID)
# print(threads)
# for thread in threads:
#     print(f"Thread Name: {thread['topic_name']}, ID: {thread['message_thread_id']}")

import requests

# def send_message_and_get_thread_id(bot_token, chat_id, text):
#     """
#     Send a message to a Telegram group and retrieve the message_thread_id.
#     :param bot_token: Your bot's API token.
#     :param chat_id: Group chat ID.
#     :param text: Message text.
#     :return: message_thread_id if available, otherwise None.
#     """
#     url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
#     payload = {
#         "chat_id": chat_id,
#         "text": text
#     }
#     response = requests.post(url, json=payload)
#     data = response.json()
#     print(data)
#     if "result" in data and "message_thread_id" in data["result"]:
        
#         return data["result"]["message_thread_id"]
#     return None

# Example usage
# BOT_TOKEN = "YOUR_BOT_TOKEN"
# CHAT_ID = -1002342888585  # Replace with your group chat ID
# MESSAGE = "Hello from the bot!"

# thread_id = send_message_and_get_thread_id(BOT_TOKEN, CHAT_ID, MESSAGE)
# print(f"Message Thread ID: {thread_id}")

def fetch_message_thread_ids(bot_token):
    """
    Fetch all message_thread_ids from updates received by the bot.
    """
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    response = requests.get(url)
    data = response.json()

    thread_ids = []
    if data['ok']:
        for update in data['result']:
            if 'message' in update and 'message_thread_id' in update['message']:
                thread_ids.append({
                    "thread_id": update["message"]["message_thread_id"],
                    "chat_id": update["message"]["chat"]["id"],
                    "text": update["message"].get("text", "")
                })
    return thread_ids

# Example usage
threads = fetch_message_thread_ids(BOT_TOKEN)
print("Message Thread IDs:", threads)
for thread in threads:
    print(f"Thread ID: {thread['thread_id']}, Chat ID: {thread['chat_id']}, Text: {thread['text']}")
