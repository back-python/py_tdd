from socket import send_fds
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:    
                table = self.browser.find_element(By.ID, 'id_list_table')
                rows = table.find_elements(By.TAG_NAME, 'tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
        
    def test_can_start_a_list_for_one_user(self):
        # Alexa ouviu falar de uma nova aplicação online interessante para
        # lista de tarefas. Ela decide verificar a sua homepage
        self.browser.get(self.live_server_url)

        # Ela percebe que o título da página e o cabeçalho mencionam "To-do"
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        # Ela é convidada a inserir um item de tarefa imediatamente
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # Ela digita "Buy peacock feathers" em uma caixa de texto
        inputbox.send_keys('Buy peacock feathers')

        # Quando ela tecla enter, a página é atualizada, e agora lista
        # "1: Buy peacock feathers" como um item em uma lista de tarefas
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # Ainda continua havendo uma caixa de texto convidando-a a acrescentar
        # outro item. Ela insere "Use peacock feathers to make a fly"
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # A página é atualizada novamente e agora mostra os dois itens em sua lista
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # Satisfeita, ela volta a dormir

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Alexa inicia uma nova lista de tarefas
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # Ela percebe que sua lista tem um URL único
        alexa_list_url = self.browser.current_url
        self.assertRegex(alexa_list_url, '/lists/.+')

        # Agora um novo usuário, Jubi, chega ao site

        ## Usaremos uma nova sessão para garantir que nenhuma informação de
        ## Alexa está vindo de cookies etc

        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Jubi acessa a página e não há nenhum sinal da lista de Alexa
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Jubi inicia uma nova lista inserindo um novo item. Ele é 
        # menos interessante que Alexa
        inputbox.send_keys('Buy a milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy a milk')

        # Jubi obtém o próprio URL exclusivo
        jubi_list_url = self.browser.current_url
        self.assertRegex(jubi_list_url, '/lists/.+')
        self.assertNotEqual(alexa_list_url, jubi_list_url)

        # Novamente não há nenhum sinal da lista de Alexa
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfeitos, ambos voltam a dormir

