from abc import ABC, abstractmethod

class Programmer(ABC):

    @abstractmethod

    def calculate_salary(self):
        pass

class SeniorProgramer(Programmer):

    def calculate_salary(self):
        return 1000