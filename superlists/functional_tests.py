from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()
        
    def test_can_start_a_list_and_retrieve_it_later(self):
        # Alexa ouviu falar de uma nova aplicação online interessante para
        # lista de tarefas. Ela decide verificar a sua homepage
        self.browser.get('http://localhost:8000')

        # Ela percebe que o título da página e o cabeçalho mencionam "To-do"
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        # Ela é convidada a inserir um item de tarefa imediatamente
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(
            input.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # Ela digita "Buy peacock feathers" em uma caixa de texto
        inputbox.send_keys('Buy a peacock feathers')

        # Quando ela tecla enter, a página é atualizada, e agora lista
        # "1: Buy peacock feathers" como um item em uma lista de tarefas
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = self.browser.find_elements(By.TAG_NAME, 'tr')
        self.assertTrue(
            any(row.text == '1: Buy peacock feathers' for row in rows)
        )

        # Ainda continua havendo uma caixa de texto convidando-a a acrescentar
        # outro item. Ela insere "Use peacock feathers to make a fly"


        # A página é atualizada novamente e agora mostra os dois itens em sua lista

        # Alexa se pergunta se o site lembrará de sua lista. Então ela nota que o si-
        # te gerou um URL único para ela -- há um pequeno texto explicativo para isso

        # Ela acessa essa URL e sua lista continua lá

        # Satisfeita, ela volta a dormir

        self.fail('finish the test!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')