
# Documentation

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-3776ab?logo=python&logoColor=white)](https://www.python.org/)
[![discord.py](https://img.shields.io/badge/library-discord.py-5865f2?logo=discord&logoColor=white)](https://github.com/Rapptz/discord.py)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This is a Discord bot that lurks in a channel and periodically sends AI-generated messages using a **Markov chain** text model. It learns from a dataset of messages you provide and generates new sentences that mimic the style of that data. It can also randomly send images from a list.

---

## How It Works

### Startup
When the bot launches, it reads two environment variables:
- `DISCORD_TOKEN` — your bot's secret token from the Discord Developer Portal
- `TARGET_CHANNEL_ID` — the ID of the channel the bot will monitor and speak in

It also randomly picks a **trigger threshold** between 20 and 30. This is how many messages the bot will wait before it decides to speak.

### Listening for Messages
The bot watches the target channel. Every time a user sends a message, an internal counter increments. Once that counter hits the trigger threshold, the bot calls `speak()`, resets the counter, and picks a new random threshold between 20 and 30. This keeps the bot feeling unpredictable and natural.

The bot will also immediately call `speak()` any time it is **directly mentioned** (@ mentioned) in the channel.

### The `speak()` Function
When the bot decides to talk, it does the following:

1. **50% chance** — attempts to send a random image URL from `channel_images.txt`
2. **If that's skipped or fails** — generates a sentence using a Markov chain model built from `channel_messages.txt` and sends it

### Data Files
| File | Purpose |
|---|---|
| `channel_messages.txt` | One message per line. Used to train the Markov chain. |
| `channel_images.txt` | One image URL per line. Randomly picked and sent as-is. |

---

## Setup

1. Install dependencies:
   ```
   pip install discord.py markovify
   ```
2. Create a bot in the [Discord Developer Portal](https://discord.com/developers/applications) and enable the **Message Content Intent**
3. Set your environment variables:
   ```
   DISCORD_TOKEN=your_token_here
   TARGET_CHANNEL_ID=123456789012345678
   ```
4. Populate `channel_messages.txt` with messages (one per line) and optionally `channel_images.txt` with image URLs. The bot will consistently track messages and populate the .txt files. You can optionally create a "scraper" of some sorts to automatically populate the messages.txt.
5. Run the bot:
   ```
   python main.py
   ```

---

## Things to consider / change

### Change How Often the Bot Speaks
The trigger threshold is currently random between 20–30 messages. You can tighten or widen this range:
```python
# Speak more often (every 5–10 messages)
trigger_count = random.randint(5, 10)

# Speak less often (every 50–100 messages)
trigger_count = random.randint(50, 100)
```

### Change the Image Send Chance
The image chance is currently 50%. Adjust the float between `0.0` (never) and `1.0` (always):
```python
# 25% chance of sending an image
if random.random() < 0.25:

# 75% chance of sending an image
if random.random() < 0.75:
```

### Monitor Multiple Channels
Replace the single channel ID check with a list:
```python
ALLOWED_CHANNELS = [123456789, 987654321]

if message.channel.id in ALLOWED_CHANNELS:
```

### Add a Cooldown So the Bot Can't Spam on Mention
Import `time` and track the last time the bot spoke:
```python
import time
last_spoke = 0
COOLDOWN_SECONDS = 60

# Inside on_message, before calling speak() on mention:
if time.time() - last_spoke > COOLDOWN_SECONDS:
    await speak(message.channel)
    last_spoke = time.time()
```

### Reply Instead of Sending a New Message
Change `await channel.send(...)` to reply to the triggering message:
```python
# In on_message, pass the message object to speak()
await message.reply(generated_sentence)
```

### Use a Larger Markov State Size for More Coherent Text
By default `markovify` uses a state size of 2. Increasing it makes output more coherent but requires more training data:
```python
text_model = markovify.NewlineText(text, state_size=3)
```

### Automatically Collect Messages Into the Dataset
Add a logging block inside `on_message` to grow your dataset over time:
```python
if message.channel.id == TARGET_CHANNEL_ID and message.author != client.user:
    if message.content and not message.content.startswith('!'):
        with open(DATA_FILE, 'a', encoding='utf-8') as f:
            f.write(message.content + '\n')
```

---

## Further info
- The more data in `channel_messages.txt`, the better and more varied the generated sentences will be. A few hundred lines is a minimum; thousands is ideal.
- If the Markov model can't generate a sentence (too little data), it silently fails and logs a message to the console.
- The bot ignores its own messages to prevent feedback loops.
