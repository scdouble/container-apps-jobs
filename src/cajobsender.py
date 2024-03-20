import os
import asyncio
import random
import datetime
from dotenv import load_dotenv
from dotenv import dotenv_values
from azure.storage.queue.aio import QueueClient


if os.path.exists(".env"):
    load_dotenv(override = True)
    config = dotenv_values(".env")


# Read environment variables
account_url = os.getenv("FULLY_QUALIFIED_NAMESPACE")
input_queue_name = os.getenv("INPUT_QUEUE_NAME")
output_queue_name = os.getenv("INPUT_QUEUE_NAME")
min_number = int(os.getenv("MIN_NUMBER", 1))
max_number = int(os.getenv("MAX_NUMBER", 10))
message_count = int(os.getenv("MESSAGE_COUNT", 100))
send_type = os.getenv("SEND_TYPE", "list")
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

# Print environment variables
print(f"ACCOUNT_URL: {account_url}")
print(f"INPUT_QUEUE_NAME: {input_queue_name}")
print(f"MIN_NUMBER: {min_number}")
print(f"MAX_NUMBER: {max_number}")
print(f"MESSAGE_COUNT: {message_count}")
print(f"SEND_TYPE: {send_type}")



async def send_a_list_of_messages(sender):
    try:
        # Create a list of messages and send it to the queue
        tasks = [sender.send_message(random.randint(min_number, max_number)) for _ in range(message_count)]
        await asyncio.gather(*tasks)
        print(f"Sent a list of {message_count} messages to the {input_queue_name} queue")
    except Exception as e:
        print(f"An error occurred while sending a list of message to the {input_queue_name} queue: {e}")

# async def send_batch_message(sender):
#     # Create a batch of messages
#     async with sender:
#         batch_message = await sender.create_message_batch()
#         for _ in range(message_count):
#             try:
#                 # Add a message to the batch
#                 batch_message.add_message(QueueMessage(f"{random.randint(min_number, max_number)}"))
#             except Exception as e:
#                 print(f"An error occurred while creating a batch of messages: {e}")
#                 break
#         # Send the batch of messages to the queue
#         try:
#             await sender.send_message(batch_message)
#             print(f"Sent a batch of {message_count} messages to the {queue_name} queue")
#         except Exception as e:
#             print(f"An error occurred while sending a batch of message to the {queue_name} queue: {e}")

async def run():
    d_today = datetime.datetime.now()
    print(f"Sender running at: {d_today}")
    async with QueueClient.from_connection_string(connection_string, queue_name=input_queue_name)as sender:
        async with sender:
            if send_type == "list":
                await send_a_list_of_messages(sender)
            # elif send_type == "batch":
            #     await send_batch_message(sender)
            else:
                print(f"Invalid send type {send_type}")

asyncio.run(run())
