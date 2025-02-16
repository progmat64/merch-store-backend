from locust import HttpUser, between, task


class MerchStoreUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """Аутентификация пользователя перед тестированием"""
        response = self.client.post(
            "/api/auth/", json={"username": "alena", "password": "BigMoney123"}
        )
        if response.status_code == 200:
            self.token = response.json()["access"]
            self.client.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            self.token = None

    @task(3)
    def get_info(self):
        """Запрос информации о пользователе"""
        if self.token:
            self.client.get("/api/info/")

    @task(2)
    def buy_item(self):
        """Покупка товара"""
        if self.token:
            self.client.get("/api/buy/t-shirt/")

    @task(1)
    def send_coins(self):
        """Перевод монет другому пользователю"""
        if self.token:
            self.client.post(
                "/api/sendCoin/", json={"toUser": "alice", "amount": 10}
            )
