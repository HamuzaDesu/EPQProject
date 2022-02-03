from datetime import date

class Homework():
    def __init__(self, title='Title', description='description', dateDue=None, setBy=None):
        self.title = title
        self.description = description
        self.dateDue = dateDue
        self.dateCreated = self.dateCreated()
        self.setBy = setBy

    def __str__(self) -> str:
        return f'Title: {self.title}\nDescription: {self.description}\nDate Due: {self.dateDue}\nDate Created: {self.dateCreated}\nSet By: {self.setBy}'
    
    def dateCreated(self):
        today = date.today().strftime('%d/%m/%y')
        return today