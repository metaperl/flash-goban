import json
from operator import inv
import urllib.request
from loguru import logger
import pathlib
import sys

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response

def create_deck(deck_name):
    try:
        invoke('createDeck', deck=deck_name)
        result = invoke('deckNames')
        print('got list of decks: {}'.format(result))
    except urllib.error.URLError:
        logger.error("Anki is not started... or Anki-connect is not installed.")
        sys.exit(255)

def make_card(deck_name, front_text, back_text, front_image, back_image):
    parms = {
        "note": {
            "deckName": deck_name,
            "modelName": "Basic",
            "fields": {
                "Front": f"{front_text}\n\n",
                "Back": f"{back_text}\n\n"
            },
            "options": {
                "allowDuplicate": False,
                "duplicateScope": "deck",
                "duplicateScopeOptions": {
                    "deckName": "Default",
                    "checkChildren": False,
                    "checkAllModels": False
                }
            },
            "tags": [
                "flash-goban-tag"
            ],
            "picture": [
                {
                "path": str(front_image.resolve()),
                "filename": front_image.name,
                "fields": [
                    "Front"
                ]
                },
                {
                "path": str(back_image.resolve()),
                "filename": back_image.name,
                "fields": [
                    "Back"
                ]
                }
            ]
        }
    }

    logger.debug(f"{parms=}")
    result = invoke('addNote', **parms)
    logger.debug(f"Result of addNote: {result=}")
    
    
def test_1():
    parms = {
        "note": {
            "deckName": "ogs-buddy",
            "modelName": "Basic",
            "fields": {
                "Front": "front content",
                "Back": "back content"
            },
            "options": {
                "allowDuplicate": False,
                "duplicateScope": "deck",
                "duplicateScopeOptions": {
                    "deckName": "Default",
                    "checkChildren": False,
                    "checkAllModels": False
                }
            },
            "tags": [
                "ogs-buddy-tag"
            ],
            "picture": [{
                "url": "https://en.wikipedia.org/wiki/Go_(game)#/media/File:FloorGoban.JPG",
                "filename": "floor-goban.jpg",
                "fields": [
                    "Front"
                ]
            }],
            "picture": [{
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/A_black_cat_named_Tilly.jpg/220px-A_black_cat_named_Tilly.jpg",
                "filename": "black_cat.jpg",
                "fields": [
                    "Back"
                ]
            }]
        }
    }

    result = invoke('addNote', **parms)
    logger.debug(f"{result=}")


if __name__ == '__main__':
    print('main')
    test_1()
