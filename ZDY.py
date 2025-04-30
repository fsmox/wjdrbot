class ZDY:
    def __init__(self, task_manager):
        self.task_manager = task_manager
        self.name = "ZDY"
        self.description = "ZDY is a task that performs a specific function."
        self.version = "1.0"

    def execute(self):
        print(f"Executing {self.name} version {self.version}")

    def Task_ReturnToCity(self):
        print("Returning to city...")
        # Implement the logic to return to the city here