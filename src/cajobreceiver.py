import os
import asyncio
from dotenv import load_dotenv
from dotenv import dotenv_values
import datetime
from azure.storage.queue.aio import QueueClient

if os.path.exists(".env"):
    load_dotenv(override = True)
    config = dotenv_values(".env")


# Read environment variables
fully_qualified_namespace = os.getenv("FULLY_QUALIFIED_NAMESPACE")
output_queue_name = os.getenv("OUTPUT_QUEUE_NAME")
max_message_count = int(os.getenv("MAX_MESSAGE_COUNT", 20))
max_wait_time = int(os.getenv("MAX_WAIT_TIME", 5))
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

# Print environment variable
print(f"FULLY_QUALIFIED_NAMESPACE: {fully_qualified_namespace}")
print(f"OUTPUT_QUEUE_NAME: {output_queue_name}")
print(f"MAX_MESSAGE_COUNT: {max_message_count}")
print(f"MAX_WAIT_TIME: {max_wait_time}")


async def receive_messages():
    
    d_today = datetime.datetime.now()
    print(f"Receiver running at: {d_today}")
    # create a Service Bus client using the connection string
    async with QueueClient.from_connection_string(connection_string, queue_name=output_queue_name)as receiver:
        i = 0
        # Receive a batch of messages until the queue is empty
        while True:
            try:
                properties = await receiver.get_queue_properties()
                count = properties.approximate_message_count
                if count == 0:
                    print(f"{output_queue_name} is empty. Exiting...")
                    break
                received_msgs = receiver.receive_messages(max_messages=5)
                numbers = []
                async for msg in received_msgs:
                # Check if message contains an integer value
                    content = msg.content
                    try:
                        n = int(str(content))
                        i += 1
                        print(f"[{i}] Received Message: {n}")
                        # Complete the message so that the message is removed from the queue
                        numbers.append(n)
                    except ValueError:
                        print(f"[{i}] Received message {str(content)} is not an integer number")
                        continue
                    finally:
                        await receiver.delete_message(msg)
                        # print(f"[{i}] Completed message: {str(content)}")
                if len(numbers) > 0 :
                    print(f"Numbers are :{numbers}")
            except Exception as e:
                print(f"An error occurred while receiving messages from the {output_queue_name} queue: {e}")
                break

# Receive messages from the input queue
asyncio.run(receive_messages())