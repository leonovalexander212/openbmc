from locust import HttpUser, task, between

class BMCUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def get_sensors(self):
        self.client.get("/redfish/v1/Chassis", verify=False)
