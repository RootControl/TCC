# -*- coding: utf-8 -*-
from google.cloud import translate
import src.database.DatabaseConnection as dc
from src.preprocessing.PreprocessingTokens import removeStopwords
import csv
import time


def translate_text(text, target='en'):
    translate_client = translate.Client.from_service_account_json('apikey.json')
    result = translate_client.translate(text, target_language=target)
    tmp = []
    for row in result:
        tmp.append(row['translatedText'])
    return tmp


def makingTranslateData(game):
    listResult = []
    result = dc.getAllTweets(game)

    with open(f'../files/{game}2.csv', 'w+', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'create_at', 'text', 'user_name', 'user_location']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        count = 0
        writer.writeheader()
        for item in result:
            id_tw, created_at, text, user_name, user_location = item
            removeEnters = text.replace('\n', ' ')
            test = removeStopwords(removeEnters)
            item_list = [e for e in test if e not in '']

            if len(item_list) != 0:
                writer.writerow({'id': f'{id_tw}', 'create_at': f'{created_at}', 'text': f'{translate_text(item_list)}',
                                 'user_name': f'{user_name}', 'user_location': f'{user_location}'})
                print(id_tw)
                count += 1

                if count == 300:
                    time.sleep(20)
                    count = 0

        print('ok')


makingTranslateData('BRACRC')
