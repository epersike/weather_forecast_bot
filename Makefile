# Makefile for the Weather Forecast Bot

.PHONY: help install llm.test bot.start

help:
	@echo "Available commands:"
	@echo "  make install    - Install project dependencies"
	@echo "  make llm.test   - Run the LLM pipeline test"
	@echo "  make bot.start  - Start the Discord bot"

install:
	@echo "Installing dependencies..."
	pip install -r app/requirements/requirements.dev.txt

llm.test:
	@echo "Running pipeline test..."
	python llm/chain.py

bot.start:
	@echo "Starting Discord bot..."
	python bot/discord.py