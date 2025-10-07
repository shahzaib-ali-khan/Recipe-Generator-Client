# Recipe Bot

## Introduction

A Telegram bot that generates recipes based on user-selected language models and ingredients. The bot integrates with a FastAPI backend to fetch supported models and generate recipes. The project uses Poetry for dependency management.

## User Flow

The bot follows a simple three-step process to generate a recipe. If a user wants another recipe, they must restart the process from step 1.

1. **/start**: Initiates the conversation. The bot welcomes the user and displays a list of available language models (e.g., "ChatGPT", "Gemini") to choose from.
2. **Select Model**: The user selects a model from the provided options. The bot then prompts for ingredient input.
3. **Enter Ingredients**: The user enters a comma-separated list of ingredients (e.g., "flour, sugar, eggs"). The bot generates and sends a recipe based on the selected model and ingredients, then ends the conversation.

To request another recipe, repeat the process by sending `/start` again.

## Prerequisites

Ensure the following are installed before setting up the project:

1. **Python 3.11+**:
   - Download from [python.org](https://www.python.org/downloads/).
   - Set `PATH` environment variable
   - Verify: `python --version`.

2. **Poetry 2.2.0+**:
   - Install: `pip install poetry==2.2.0`.
   - Set `PATH` environment variable
   - Verify: `poetry --version`.
3. A Telegram bot token (`TELEGRAM_TOKEN`) obtained from [BotFather](https://core.telegram.org/bots#6-botfather)
4. A running [backend](https://github.com/shahzaib-ali-khan/Recipe-Generator) accessible at `http://127.0.0.1:8000/api/v1/` (or adjust `BASE_URL` accordingly in .env file).

## Setup Instructions

Follow these steps to set up the project locally. Use Windows Command Prompt (cmd) for all commands.

1. **Clone the Repository**:
   ```cmd
   git clone <repository-url>
   cd recipe_telegram_bot
   ```
   Replace `<repository-url>` with repository URL.

2. **Install Dependencies**:
   Install all dependencies using Poetry by running below command in root directory:
   ```cmd
   poetry install
   ```
   - This creates a virtual environment in virtualenvs folder of pypoetry. Copy the complete path.

3. **Activate the Virtual Environment**:<br>
   For Windows:
   ```cmd
   <copied path from last point>\Scripts\activate
   ```
   For mac/linux:<br>
   ```cmd
   source <copied path from last point>\bin\activate
   ```
   - This activates the virtual environment. Run all subsequent commands inside this shell.

## Running the Project

From the root directory run:

   ```cmd
   python -m src.main
   ```

**Note**: Make sure you have completed prerequisites step above.

## Deployment with Docker Compose

Follow these steps to deploy the bot using Docker Compose:

### 1. **Set Up Environment Variables**
Create a `.env` file in the project root with the following content:

1. TELEGRAM_TOKEN=your_telegram_bot_token
2. BASE_URL=http://127.0.0.1:8000/api/v1/

- Replace `your_telegram_bot_token` with the token from BotFather.
- Adjust `BASE_URL` to point to your FastAPI backend (e.g., `http://fastapi:8000/api/v1/` if using Docker Compose with a FastAPI service).


### 2. **Configure Docker Compose**
Create a `compose.yml` file in the project root. Here’s an example that includes both the bot and a placeholder for the FastAPI service:

```yaml
services:
  bot:
    build: .
    environment:
      - TELEGRAM_TOKEN=${TELEGRAM_TOKEN}
      - BASE_URL=${BASE_URL}
    depends_on:
      - fastapi
    ports:
      - "8443:8443"

  fastapi:
    build:
      context: ./fastapi-dir  # Adjust to your FastAPI project directory
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=your_openai_key
      - GEMINI_API_KEY=your_google_key
```

Start the services by: `docker compose up -d`
