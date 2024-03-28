import logging
import requests
from system_config import GPT_MODEL
from config import GPT_TOKEN, FOLDER_ID

token = GPT_TOKEN
folder_id = FOLDER_ID

# функция подсчёта токенов
def count_tokens(collection) -> int:
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'}

    data = {
        "modelUri": f"gpt://{folder_id}/{GPT_MODEL}/latest",
        "maxTokens": 800,
        "messages": []}

    for row in collection:
        data["messages"].append(
            {
                "role": row["role"],
                "text": row["text"]})

    result = requests.post(
        url='https://llm.api.cloud.yandex.net/foundationModels/v1/tokenizeCompletion',
        headers=headers,
        json=data).json()

    try:
        result = result['tokens']
        logging.error("Токены для промпта успешно подсчитаны.")
        return len(result)
    except KeyError:
        logging.error("Не удалось посчитать токены для промпта, так как токен недействителен.")
