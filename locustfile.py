from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(5, 15)
    
    # def on_start(self):
    #     self.client.post("user/login/", {
    #     "email": "ilayda@ilayda.com",
    #     "password": "1234qwer"
    #     })
    
    @task
    def index(self):
        self.client.get("feed/post/")
