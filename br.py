from geminiModel import model
import time

class br:
    def __init__(self) -> None:   
        self.greeting_keywords = ["hello", "hi", "greetings", "hey", "good morning", "good afternoon", "good evening"]
        self.gmodel = model()
        self.getData()

    def getData(self):
        while True:
            text = input("Enter your question (or type 'exit' to quit): ")
            if 'exit' == text.lower():
                break
            response = self.gmodel.process(text)
            print("Response:", response)
            time.sleep(int(len(response.split()) // 2))

if __name__ == "__main__":
    br()
