.PHONY: start dev

start:
	uvicorn storage-bot.main:app

dev:
	uvicorn storage-bot.main:app --reload