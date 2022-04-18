from selenium import webdriver
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
        self.assertIn('To-do', self.browser.title)
        self.fail('Test end!')

        # Ela é convidada a inserir um item de tarefa imediatamente

        # Ela digita "Buy peacock feathers" em uma caixa de texto

        # Quando ela tecla enter, a página é atualizada, e agora lista
        # "1: Buy peacock feathers" como um item em uma lista de tarefas

        # Ainda continua havendo uma caixa de texto convidando-a a acrescentar
        # outro item. Ela insere "Use peacock feathers to make a fly"

        # A página é atualizada novamente e agora mostra os dois itens em sua lista

        # Alexa se pergunta se o site lembrará de sua lista. Então ela nota que o si-
        # te gerou um URL único para ela -- há um pequeno texto explicativo para isso

        # Ela acessa essa URL e sua lista continua lá

        # Satisfeita, ela volta a dormir

if __name__ == '__main__':
    unittest.main(warnings='ignore')