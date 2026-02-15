class Conversations():
    def __init__(self):
        self.chat=[{"role":"assistant",
                    "content":"Hi! how can I help you?"}]

    def add(self,role,query):
        self.chat.append({"role":role,
                          "content":query})

chat = Conversations()