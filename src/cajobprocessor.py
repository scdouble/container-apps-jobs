import os
import asyncio
import datetime
from dotenv import load_dotenv
from dotenv import dotenv_values
from azure.storage.queue.aio import QueueClient

# Load environment variables from .env file
if os.path.exists(".env"):
    load_dotenv(override=True)
    config = dotenv_values(".env")

# Read environment variables
fully_qualified_namespace = os.getenv("FULLY_QUALIFIED_NAMESPACE")
input_queue_name = os.getenv("INPUT_QUEUE_NAME")
output_queue_name = os.getenv("OUTPUT_QUEUE_NAME")
max_message_count = int(os.getenv("MAX_MESSAGE_COUNT", 20))
max_wait_time = int(os.getenv("MAX_WAIT_TIME", 5))
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

# Print environment variables
print(f"FULLY_QUALIFIED_NAMESPACE: {fully_qualified_namespace}")
print(f"INPUT_QUEUE_NAME: {input_queue_name}")
print(f"OUTPUT_QUEUE_NAME: {output_queue_name}")
print(f"MAX_MESSAGE_COUNT: {max_message_count}")
print(f"MAX_WAIT_TIME: {max_wait_time}")

async def fibonacci(n):
    if n <= 0:
        raise ValueError("n must be a positive integer")
    elif n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        fib1 = await fibonacci(n - 1)
        fib2 = await fibonacci(n - 2)
        return fib1 + fib2
    
async def send_message(message_text: int, i: int):
    # Check that the message is not empty
    if message_text:
        try:
        # Create a Service Bus client using the credential
            async with QueueClient.from_connection_string(connection_string, queue_name=output_queue_name)as sender:
                # Get a Queue Sender object to send messages to the output queue
                async with sender:
                    # Create a Service Bus message and send it to the queue
                    message = message_text
                    # Send a message to the output queue
                    await sender.send_message(message)
                print(f"[{i}] Sent result message: {message_text}")
        except Exception as e:
            print(f"An error occurred while sending [{i}] message to the {output_queue_name} queue: {e}")
    else:
        print(f"The [{i}] message is empty. Please, enter a valid message.")

async def receive_messages():
    d_today = datetime.datetime.now()
    print(f"Processor running at: {d_today}")
    async with QueueClient.from_connection_string(connection_string, queue_name=input_queue_name)as receiver:
        try:
            received_msgs = receiver.receive_messages(max_messages=max_message_count)

            i = 0
            async for msg in received_msgs:
                i += 1
                try:
                    n = int(str(msg.content))
                    print(f"[{i}] Received Message: {n}")
                    result = await fibonacci(n)
                    print(f"[{i}] The Fibonacci number for {n} is {result}")
                    await send_message(str(result), i)
                except ValueError:
                    print(f"[{i}] Received message {n} is not an integer number")
                    continue
                finally:
                    await receiver.delete_message(msg)
                    print(f"[{i}] Completed message: {n}")

        except Exception as e:
            print(f"An error occurred while receiving messages from the {input_queue_name} queue: {e}")


# Receive messages from the input queue
asyncio.run(receive_messages())