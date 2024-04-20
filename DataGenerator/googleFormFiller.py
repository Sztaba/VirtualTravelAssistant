from random import randint
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from typing import List, Dict

class GoogleFormFiller:
    def __init__(self, base_url: str, entries: List[str], multi_choice_q:List[str], answers:Dict[str, List[str]], name_entry:str, email_entry:str):
        self.base_url = base_url
        self.entries = entries
        self.multi_choice_q = multi_choice_q
        self.answers = answers
        self.name_entry = name_entry
        self.email_entry = email_entry
    def _random_name_from_file(self, file_path:str) -> str:
        with open(file_path, "r") as file:
            names = file.readlines()
            return names[randint(0, len(names) - 1)].strip()
    def _random_set_from_list(self, lst: list, n: int) -> list:
        return [lst[randint(0, len(lst) - 1)] for i in range(n)]
    def _random_answer(self, entry:str) -> str:
        return self.answers[entry][randint(0, len(self.answers[entry]) - 1)]
    def _append_url(self, entry:str, appendix:str) -> str:
        return f"&entry.{entry}={appendix}"
    def _prepare_email(self, name:str) -> str:
        return f"{name.lower().replace(' ', '.')}@gmail.com"

    def generate_url(self, first_name_file:str, last_name_file:str) -> str: 
        url = self.base_url
        name = self._random_name_from_file(first_name_file) + " " + self._random_name_from_file(last_name_file)
        for entry in self.entries: 
            if entry in self.multi_choice_q:
                set_size = randint(1, len(self.answers[entry]))
                answ = self._random_set_from_list(self.answers[entry],set_size)
                for a in answ:
                    url += self._append_url(entry, a)
            elif entry == self.name_entry:
                url += self._append_url(entry, name)
            elif entry == self.email_entry:
                url += self._append_url(entry, self._prepare_email(name))
            else:
                url += self._append_url(entry, self._random_answer(entry))

        return url.replace(" ", "+")

    def send_filled(self, first_name_file:str, last_name_file:str, xpath:str = "Prześlij", num_of_req:int = 50):
        urls = [self.generate_url(first_name_file, last_name_file) for i in range(num_of_req)]
        driver = webdriver.Firefox()
        for url in urls:
            driver.get(url)
            button = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, f'//div/span/span[text()="{xpath}"]')))
            button.click()
        driver.close()