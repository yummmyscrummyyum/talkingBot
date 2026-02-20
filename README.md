# talkingBot

Discord bot leveraging Markov chain logic to generate non-deterministic text responses and curated media delivery

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-3776ab?logo=python&logoColor=white)](https://www.python.org/)
[![discord.py](https://img.shields.io/badge/library-discord.py-5865f2?logo=discord&logoColor=white)](https://github.com/Rapptz/discord.py)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📝 Overview

**MarkovCord** is an automated engagement tool that simulates human-like conversation patterns by processing historical chat data. It utilizes a state-based probability model to ensure that every interaction is unique yet stylistically consistent with the source corpus.


### Core Capabilities
* **Contextual Text Generation**: Leverages the `markovify` library to synthesize new sentences from a newline-separated text corpus.
* **Media Integration**: Features a probabilistic toggle (default 50%) to serve curated image assets via direct URLs.
* **Priority Interaction**: Responds instantaneously to direct mentions, bypassing the standard message counter.

---

## ⚙️ Technical Architecture

The bot's logic is partitioned into three primary stages:
1.  **Ingestion**: Parses `channel_messages.txt` for text modeling and `channel_images.txt` for media assets.
2.  **Processing**: The `speak` function calculates the response type based on a weighted random distribution.
3.  **Execution**: Dispatches the payload through the Discord Gateway via `discord.py`.

---

## 🚀 Installation & Setup

### 1. System Requirements
Clone the repository and install the necessary dependencies:

```bash
git clone [https://github.com/yummmyscrummyyum/your-repo-name.git](https://github.com/yummmyscrummyyum/your-repo-name.git)
cd your-repo-name
pip install discord.py markovify


