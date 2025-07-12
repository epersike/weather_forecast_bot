# Weather Forecast Bot

> A simple Discord bot that uses LangChain and OpenAI to answer questions about the weather forecast for any city in the world.

### Technologies Used

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![LangChain](https://img.shields.io/badge/LangChain-4A90E2?style=for-the-badge)
![OpenAI](https://img.shields.io/badge/openai-%23343541.svg?style=for-the-badge&logo=openai&logoColor=white)
![Discord.py](https://img.shields.io/badge/discord.py-5865F2?style=for-the-badge&logo=discord&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)

## Features

- **Natural Language Processing**: Understands questions about the weather forecast.
- **Intelligent Validation**: Uses an LLM to validate if the question is about the weather and to extract the city and country.
- **Dynamic Forecast Fetching**: Queries the Open-Meteo API to get real-time weather data for the extracted location.
- **Contextual Responses**: Provides detailed answers or friendly error messages, depending on the question's validity and data availability.
- **Discord Integration**: Works as a Discord bot, responding to mentions.

## Prerequisites

1.  **OpenAI API Key**: Get yours at [platform.openai.com](https://platform.openai.com/)
2.  **Discord Bot Token**: Get yours at the [Discord Developer Portal](https://discord.com/developers/applications)

## Installation and Setup

Follow the steps below to set up and run the project in your local environment.

**1. Clone repository:**
```sh
git clone https://github.com/epersike/weather_forecast_bot.git
cd weather_forecast_bot
```

**2. Edit .env file:**

Rename .env.sample file to .env and set the environment variables values accordingly.
```sh
OPENAI_API_KEY=YOUR_OPENAI_KEY
DISCORD_TOKEN=YOUR_DISCORD_APP_TOKEN
```

**3. Dependency installation:**

```sh
make install
```

## Launch application

You can use the provided `Makefile` for convenience.

**1. Test the LLM pipeline:**
```sh
make llm.test
```

2 - Launch discord bot app:
```sh
make bot.start
```

## Release History

* 0.0.2
    Refactored the application folder organization.
* 0.0.1
    * Work in progress.

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
