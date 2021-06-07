class Container:
    def __init__(self, container_name, user, container_password, assigned_ip):
        self.container_name = container_name
        self.user = user
        self.container_password = container_password
        self.assigned_ip = assigned_ip

    def info(self):
        info = f"Container name: {self.container_name}; Used user: {self.user}; Assigned IP: {self.assigned_ip}"
        return info
