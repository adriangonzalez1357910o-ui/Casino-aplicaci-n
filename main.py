import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView

class CasinoState:
    def __init__(self):
        self.fichas = 0
        self.banco = 50
        self.deuda = 0

casino = CasinoState()

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        layout.add_widget(Label(text='¡CASINO!', font_size='28sp', bold=True))
        
        self.lbl_fichas = Label(text=f'Fichas: {casino.fichas} | Deuda: {casino.deuda}', font_size='18sp')
        layout.add_widget(self.lbl_fichas)
        
        self.input_fichas = TextInput(hint_text='Cantidad de fichas a comprar', input_filter='int', multiline=False)
        layout.add_widget(self.input_fichas)
        
        btn_comprar = Button(text='Comprar Fichas', size_hint_y=None, height=50)
        btn_comprar.bind(on_press=self.comprar_fichas)
        layout.add_widget(btn_comprar)
        
        btn_bj = Button(text='Jugar Black Jack', size_hint_y=None, height=50)
        btn_bj.bind(on_press=lambda x: self.ir_a_juego('blackjack'))
        layout.add_widget(btn_bj)
        
        btn_ruleta = Button(text='Jugar Ruleta', size_hint_y=None, height=50)
        btn_ruleta.bind(on_press=lambda x: self.ir_a_juego('ruleta'))
        layout.add_widget(btn_ruleta)
        
        btn_tragamonedas = Button(text='Jugar Tragamonedas', size_hint_y=None, height=50)
        btn_tragamonedas.bind(on_press=lambda x: self.ir_a_juego('tragamonedas'))
        layout.add_widget(btn_tragamonedas)
        
        self.add_widget(layout)

    def on_enter(self):
        self.lbl_fichas.text = f'Fichas: {casino.fichas} | Deuda: {casino.deuda}'

    def comprar_fichas(self, instance):
        if self.input_fichas.text:
            casino.fichas += int(self.input_fichas.text)
            self.lbl_fichas.text = f'Fichas: {casino.fichas} | Deuda: {casino.deuda}'
            self.input_fichas.text = ''

    def ir_a_juego(self, nombre_pantalla):
        self.manager.current = nombre_pantalla

class BlackJackScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        layout.add_widget(Label(text='Black Jack', font_size='24sp', bold=True))
        
        self.input_apuesta = TextInput(hint_text='Fichas a apostar', input_filter='int', multiline=False)
        layout.add_widget(self.input_apuesta)
        
        self.lbl_estado = Label(text='Ingresa tu apuesta y presiona Repartir', font_size='16sp')
        layout.add_widget(self.lbl_estado)
        
        btn_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, height=100)
        
        self.btn_repartir = Button(text='Repartir')
        self.btn_repartir.bind(on_press=self.iniciar_juego)
        btn_layout.add_widget(self.btn_repartir)
        
        self.btn_pedir = Button(text='Pedir Carta', disabled=True)
        self.btn_pedir.bind(on_press=self.pedir_carta)
        btn_layout.add_widget(self.btn_pedir)
        
        self.btn_plantarse = Button(text='Plantarse', disabled=True)
        self.btn_plantarse.bind(on_press=self.plantarse)
        btn_layout.add_widget(self.btn_plantarse)
        
        btn_volver = Button(text='Volver al Menú')
        btn_volver.bind(on_press=self.volver)
        btn_layout.add_widget(btn_volver)
        
        layout.add_widget(btn_layout)
        self.add_widget(layout)
        
        self.baraja = (11, 10, 10, 10, 10, 9, 8, 7, 6, 5, 4, 3, 2)

    def iniciar_juego(self, instance):
        if not self.input_apuesta.text or int(self.input_apuesta.text) <= 0:
            self.lbl_estado.text = 'Ingresa una apuesta válida'
            return
        
        self.apuesta = int(self.input_apuesta.text)
        if self.apuesta > casino.fichas:
            self.lbl_estado.text = 'No tienes suficientes fichas'
            return
            
        self.h_dealer = random.choice(self.baraja)
        self.h_jugador = random.choice(self.baraja) + random.choice(self.baraja)
        self.h_bot = random.choice(self.baraja) + random.choice(self.baraja)
        
        self.lbl_estado.text = f'Dealer revela: {self.h_dealer}\nTus cartas suman: {self.h_jugador}'
        self.btn_pedir.disabled = False
        self.btn_plantarse.disabled = False
        self.btn_repartir.disabled = True

    def pedir_carta(self, instance):
        self.h_jugador += random.choice(self.baraja)
        if self.h_jugador > 21:
            self.finalizar_ronda(perdio_auto=True)
        else:
            self.lbl_estado.text = f'Dealer revela: {self.h_dealer}\nTus cartas suman: {self.h_jugador}'

    def plantarse(self, instance):
        while self.h_dealer < 17:
            self.h_dealer += random.choice(self.baraja)
        while self.h_bot < 17:
            self.h_bot += random.choice(self.baraja)
        self.finalizar_ronda()

    def finalizar_ronda(self, perdio_auto=False):
        p1 = self.h_dealer if self.h_dealer <= 21 else 0
        p2 = self.h_bot if self.h_bot <= 21 else 0
        p3 = self.h_jugador if self.h_jugador <= 21 else 0
        
        ganador = max(p1, p2, p3)
        res = f'Dealer: {self.h_dealer} | Bot: {self.h_bot} | Tú: {self.h_jugador}\n'
        
        if p3 == 0 or perdio_auto:
            res += 'Te pasaste de 21. ¡Has perdido!'
            casino.fichas -= self.apuesta
        elif ganador == p3 and p3 > 0:
            res += '¡Has ganado y duplicado tus fichas!'
            casino.fichas += self.apuesta
        elif ganador == p1:
            res += '¡El ganador es el dealer!'
            casino.fichas -= self.apuesta
        else:
            res += '¡Ha ganado la computadora!'
            casino.fichas -= self.apuesta

        self.lbl_estado.text = res
        self.btn_pedir.disabled = True
        self.btn_plantarse.disabled = True
        self.btn_repartir.disabled = False

    def volver(self, instance):
        self.manager.current = 'menu'

class RuletaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        layout.add_widget(Label(text='Ruleta', font_size='24sp', bold=True))
        
        self.input_apuesta = TextInput(hint_text='Fichas a apostar', input_filter='int', multiline=False)
        layout.add_widget(self.input_apuesta)
        
        self.input_numero = TextInput(hint_text='Número entre 0 y 36', input_filter='int', multiline=False)
        layout.add_widget(self.input_numero)
        
        self.lbl_resultado = Label(text='Elige tu número y apuesta', font_size='16sp')
        layout.add_widget(self.lbl_resultado)
        
        btn_girar = Button(text='Girar Ruleta', size_hint_y=None, height=50)
        btn_girar.bind(on_press=self.girar)
        layout.add_widget(btn_girar)
        
        btn_volver = Button(text='Volver al Menú', size_hint_y=None, height=50)
        btn_volver.bind(on_press=lambda x: setattr(self.manager, 'current', 'menu'))
        layout.add_widget(btn_volver)
        
        self.add_widget(layout)

    def girar(self, instance):
        if not self.input_apuesta.text or not self.input_numero.text:
            self.lbl_resultado.text = 'Completa todos los campos'
            return
            
        apuesta = int(self.input_apuesta.text)
        num_elegido = int(self.input_numero.text)
        
        if apuesta > casino.fichas or num_elegido < 0 or num_elegido > 36:
            self.lbl_resultado.text = 'Datos inválidos o fichas insuficientes'
            return
            
        n = random.randint(0, 36)
        res = f'Salió el número {n}.\n'
        
        if num_elegido == n:
            res += '¡HAS GANADO EL GRAN PREMIO! (+50 fichas)'
            casino.fichas += 50
        elif num_elegido % 2 == 0 and n % 2 == 0:
            res += '¡Has ganado un premio menor! (+25 fichas)'
            casino.fichas += 25
        elif num_elegido % 3 == 0 and n % 3 == 0:
            res += '¡Has ganado un premio menor! (+25 fichas)'
            casino.fichas += 25
        else:
            res += 'Has perdido.'
            casino.fichas -= apuesta
            
        self.lbl_resultado.text = res

class TragamonedasScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        layout.add_widget(Label(text='Máquina Tragamonedas', font_size='24sp', bold=True))
        
        self.input_apuesta = TextInput(hint_text='Fichas a apostar', input_filter='int', multiline=False)
        layout.add_widget(self.input_apuesta)
        
        self.lbl_slots = Label(text='[ ? ]  [ ? ]  [ ? ]', font_size='28sp', bold=True)
        layout.add_widget(self.lbl_slots)
        
        self.lbl_resultado = Label(text='Presiona Jugar', font_size='16sp')
        layout.add_widget(self.lbl_resultado)
        
        btn_jugar = Button(text='Jugar', size_hint_y=None, height=50)
        btn_jugar.bind(on_press=self.jugar)
        layout.add_widget(btn_jugar)
        
        btn_volver = Button(text='Volver al Menú', size_hint_y=None, height=50)
        btn_volver.bind(on_press=lambda x: setattr(self.manager, 'current', 'menu'))
        layout.add_widget(btn_volver)
        
        self.add_widget(layout)

    def jugar(self, instance):
        if not self.input_apuesta.text or int(self.input_apuesta.text) <= 0:
            self.lbl_resultado.text = 'Ingresa una apuesta válida'
            return
            
        apuesta = int(self.input_apuesta.text)
        if apuesta > casino.fichas:
            self.lbl_resultado.text = 'Fichas insuficientes'
            return
            
        opciones = ["Cereza", "Limón", "Estrella"]
        r1, r2, r3 = random.choice(opciones), random.choice(opciones), random.choice(opciones)
        
        self.lbl_slots.text = f'[ {r1} ]  [ {r2} ]  [ {r3} ]'
        
        if r1 == r2 == r3:
            self.lbl_resultado.text = '¡JACKPOT! (+60 fichas)'
            casino.fichas += 60
        elif r1 == r2 or r2 == r3 or r1 == r3:
            self.lbl_resultado.text = '¡Premio! (+30 fichas)'
            casino.fichas += 30
        else:
            self.lbl_resultado.text = '¡Has perdido!'
            casino.fichas -= apuesta

class CasinoApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenuScreen(name='menu'))
        sm.add_widget(BlackJackScreen(name='blackjack'))
        sm.add_widget(RuletaScreen(name='ruleta'))
        sm.add_widget(TragamonedasScreen(name='tragamonedas'))
        return sm

if __name__ == '__main__':
    CasinoApp().run()
    
