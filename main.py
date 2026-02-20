import discord
import markovify
import random
import os

TOKEN = os.getenv('DISCORD_TOKEN')
TARGET_CHANNEL_ID = int(os.getenv('TARGET_CHANNEL_ID', 0))
# Files containing data
DATA_FILE = 'channel_messages.txt'
IMAGE_FILE = 'channel_images.txt'


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Random Trigger
message_counter = 0
trigger_count = random.randint(20, 30)

async def speak(channel):
    """
    Random Messages
    """
    print("Attempting to speak")
    
    # Image % Chance
    if random.random() < 0.50:
        try:
            if os.path.exists(IMAGE_FILE):
                with open(IMAGE_FILE, 'r', encoding='utf-8') as f:
                    lines = f.read().splitlines()
                if lines:
                    chosen_image = random.choice(lines)
                    print(f"Sending Image: {chosen_image}")
                    await channel.send(chosen_image)
                    return 
        except Exception as e:
            print(f"Error reading image file: {e}")

    # Fallback
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                text = f.read()

            if text.strip():
                text_model = markovify.NewlineText(text)
                generated_sentence = text_model.make_sentence(tries=100)

                if generated_sentence:
                    print(f"Generated text: {generated_sentence}")
                    await channel.send(generated_sentence)
                else:
                    print("Could not generate a sentence (not enough data).")
            else:
                print("Text data file is empty.")
        else:
            print(f"Data file {DATA_FILE} not found.")
            
    except Exception as e:
        print(f"Error generating sentence: {e}")

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    print(f'Monitoring Channel ID: {TARGET_CHANNEL_ID}')
    print(f'Next message trigger after {trigger_count} messages.')

@client.event
async def on_message(message):
    global message_counter, trigger_count
    if message.author == client.user:
        return
    if message.channel.id == TARGET_CHANNEL_ID:
        message_counter += 1
        print(f"Message Count: {message_counter}/{trigger_count}")

        if message_counter >= trigger_count:
            await speak(message.channel)
            message_counter = 0
            trigger_count = random.randint(20, 30)
            print(f"Counter reset. Next target: {trigger_count}")

    if client.user in message.mentions:
        await speak(message.channel)

if __name__ == "__main__":
    if TOKEN:
        client.run(TOKEN)
    else:
        print("Error")
