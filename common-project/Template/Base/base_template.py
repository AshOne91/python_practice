class BaseTemplate:
    def __init__(self, name):
        self.name = name
        print(f"{self.name}")

    def DataLoad(self, **kwargs):
        print("Loading data in BaseTemplate")

    def ViewData(self):
        print("View data in BaseTemplate")