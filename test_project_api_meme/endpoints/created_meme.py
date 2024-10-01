import requests
import allure
from endpoints.endpoint import Endpoint


@allure.step('Создание мема')
class CreateMeme(Endpoint):
    meme_id = None

    def create_new_meme(self, payload=None):

        # Если не передан payload, генерируем случайные данные.
        if payload is None:
            payload = self.data_body(self.random_type)

        self.response = requests.post(
            self.url,
            json=payload,
            headers=self.headers
        )
        log = f"""
                    REQUEST:
                        URL: {self.response.request.url}
                        METHOD: {self.response.request.method}
                        JSON:   {self.response.request.body}
                        HEADERS: {self.response.request.headers}

                    RESPONSE:    
                        STATUS_CODE: {self.response.status_code}
                        CONTENT: {self.response.content}
                    """
        print(log)

        # Проверяем, что ответ содержит JSON, прежде чем пытаться его декодировать
        try:
            self.json = self.response.json()
        except requests.exceptions.JSONDecodeError:
            print("Ошибка: ответ не содержит корректный JSON.")
            print("Ответ сервера:", self.response.text)
            return None

        self.meme_id = self.json.get('id')

        return self.meme_id
