 # The Pokédex Telegram Bot

This project is a telegram bot that functions as a pokédex.

It is able to return important information (including an image) about a specific pokémon , given in input with the `/pokemon {pokemon}` command.

## PokeAPI

It retrieves information from PokeAPI, a full RESTful API linked to an extensive database detailing everything about the Pokémon main game series.

## Redis

To make able the bot to run faster, it runs along with Redis, a open source data structure store used as a database. So before it starts making the requests to the API, it checks if those requets have been already made and cached into Redis.

## Inline Keyboard
Furthermore, the message with all of the pokemon info comes with a `inline keyboard`, that makes easier to go through all the pokédex. The are three buttons:
- the first one shows you the previous pokémon
- the second one shows you a variant of the pokémon species. It doesn't appear if the aren't any
- the last one shows you the next pokémon

Since this functionality might have easily filled the chat with many unwanted messages, everytime you use the keyboard the last message will be automatically deleted.

## Additional features

In the message might also appear special "tags" next to the pokémon name that indicates if it has any particularity.

Moreover there is a menu button in the chat that's linked to a pokémon wiki.
On the tap, it shows you the page and you're able to do your own research.

# Bot commands


## Help

## Start

## Search a pokémon

# How to run the bot

## Build the docker image

```
docker build -t pokedex-telegram-bot .
```

## Run the docker image
```
docker run pokedex-telegram-bot
```

<br>

# How to run the bot (with Redis)

## Run the docker compose

```
docker compose up
```

## Run and build the docker compose

```
docker compose up --build
```
