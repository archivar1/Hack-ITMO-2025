import requests
from typing import Optional, Dict, Any, List
from datetime import datetime, date
from app.config import get_settings


class HumanAPIService:
    """
    Сервис для работы с Human API.
    Предоставляет доступ к данным о здоровье пользователей из различных источников.
    """

    BASE_URL = "https://api.humanapi.co"
    AUTH_URL = "https://user.humanapi.co/oauth/authorize"
    TOKEN_URL = "https://user.humanapi.co/oauth/token"

    def __init__(self):
        settings = get_settings()
        self.client_id = settings.HUMAN_API_CLIENT_ID
        self.client_secret = settings.HUMAN_API_CLIENT_SECRET
        self.redirect_uri = settings.HUMAN_API_REDIRECT_URI

    def get_authorization_url(self, user_id: str, state: Optional[str] = None) -> str:
        """
        Генерирует URL для авторизации пользователя в Human API.

        Args:
            user_id: ID пользователя в вашей системе
            state: Опциональный параметр для защиты от CSRF

        Returns:
            URL для перенаправления пользователя
        """
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'state': state or user_id,
        }

        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        return f"{self.AUTH_URL}?{query_string}"

    def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        """
        Обменивает authorization code на session token.

        Args:
            code: Authorization code, полученный после авторизации пользователя

        Returns:
            Словарь с session token и другой информацией
        """
        try:
            response = requests.post(
                self.TOKEN_URL,
                data={
                    'grant_type': 'authorization_code',
                    'code': code,
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                    'redirect_uri': self.redirect_uri,
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_detail = f"{str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_detail += f" | Response: {error_data}"
                except:
                    error_detail += f" | Status: {e.response.status_code} | Text: {e.response.text[:200]}"
            raise Exception(f"Ошибка при получении токена: {error_detail}")

    def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Обновляет истекший session token используя refresh token.

        Args:
            refresh_token: Refresh token для обновления

        Returns:
            Новый session token и refresh token
        """
        try:
            response = requests.post(
                self.TOKEN_URL,
                data={
                    'grant_type': 'refresh_token',
                    'refresh_token': refresh_token,
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_detail = f"{str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_detail += f" | Response: {error_data}"
                except:
                    error_detail += f" | Status: {e.response.status_code} | Text: {e.response.text[:200]}"
            raise Exception(f"Ошибка при обновлении токена: {error_detail}")

    def _make_request(self, session_token: str, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Выполняет запрос к Human API.

        Args:
            session_token: Session token пользователя
            endpoint: Endpoint API (например, '/v1/human/activities/summaries')
            params: Параметры запроса

        Returns:
            Ответ от API
        """
        url = f"{self.BASE_URL}{endpoint}"
        headers = {
            'Authorization': f'Bearer {session_token}',
            'Content-Type': 'application/json',
        }

        try:
            response = requests.get(url, headers=headers, params=params or {})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_detail = f"{str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_detail += f" | Response: {error_data}"
                except:
                    error_detail += f" | Status: {e.response.status_code} | Text: {e.response.text[:200]}"
            raise Exception(f"Ошибка при запросе к Human API: {error_detail}")

    def get_steps(self, session_token: str, date_str: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Получает количество шагов пользователя за указанную дату.

        Args:
            session_token: Session token пользователя
            date_str: Дата в формате YYYY-MM-DD или 'today'. По умолчанию - сегодня

        Returns:
            Данные о шагах или None
        """
        if date_str == 'today' or date_str is None:
            date_str = datetime.now().strftime('%Y-%m-%d')

        params = {'date': date_str}
        try:
            # Human API endpoint для получения шагов
            data = self._make_request(session_token, '/v1/human/activities/summaries', params)

            # Обработка ответа (структура может отличаться в зависимости от версии API)
            if isinstance(data, list) and len(data) > 0:
                return data[0]
            elif isinstance(data, dict):
                return data
            return None
        except Exception:
            return None

    def get_calories(self, session_token: str, date_str: Optional[str] = None) -> Optional[float]:
        """
        Получает количество сожженных калорий за указанную дату.

        Args:
            session_token: Session token пользователя
            date_str: Дата в формате YYYY-MM-DD или 'today'. По умолчанию - сегодня

        Returns:
            Количество калорий или None
        """
        if date_str == 'today' or date_str is None:
            date_str = datetime.now().strftime('%Y-%m-%d')

        params = {'date': date_str}
        try:
            # Human API endpoint для получения калорий
            data = self._make_request(session_token, '/v1/human/activities/summaries', params)

            # Извлекаем калории из ответа
            if isinstance(data, list) and len(data) > 0:
                summary = data[0]
                return summary.get('calories', 0.0)
            elif isinstance(data, dict):
                return data.get('calories', 0.0)
            return None
        except Exception:
            return None

    def get_activities(self, session_token: str, date_str: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Получает список активностей пользователя за указанную дату.

        Args:
            session_token: Session token пользователя
            date_str: Дата в формате YYYY-MM-DD или 'today'. По умолчанию - сегодня

        Returns:
            Список активностей
        """
        if date_str == 'today' or date_str is None:
            date_str = datetime.now().strftime('%Y-%m-%d')

        params = {'date': date_str}
        try:
            data = self._make_request(session_token, '/v1/human/activities', params)

            if isinstance(data, list):
                return data
            elif isinstance(data, dict) and 'activities' in data:
                return data['activities']
            return []
        except Exception:
            return []

    def get_profile(self, session_token: str) -> Optional[Dict[str, Any]]:
        """
        Получает профиль пользователя.

        Args:
            session_token: Session token пользователя

        Returns:
            Профиль пользователя или None
        """
        try:
            return self._make_request(session_token, '/v1/human/profile')
        except Exception:
            return None

