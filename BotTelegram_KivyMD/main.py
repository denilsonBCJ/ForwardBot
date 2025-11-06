# main.py
import asyncio
from threading import Thread
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import MDList, OneLineIconListItem, IconLeftWidget
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import ScrollView
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.card import MDCard

from bot_forwarder import ForwardBot


class BotAppScreen(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=20, spacing=10, **kwargs)
        self.canais_destino = []
        self.dialog = None
        self.bot = None

        # 🔹 Cabeçalho
        self.add_widget(MDLabel(text="📢 Forward Bot (KivyMD)", halign="center", font_style="H5"))

        # 🔹 Campos de entrada
        self.api_id_field = MDTextField(hint_text="API ID", mode="rectangle")
        self.api_hash_field = MDTextField(hint_text="API HASH", mode="rectangle")
        self.origem_field = MDTextField(hint_text="Canal de Origem (ID)", mode="rectangle")
        self.destino_field = MDTextField(hint_text="Canal de Destino (ID)", mode="rectangle")

        # 🔹 Botões
        self.add_destino_btn = MDFillRoundFlatButton(text="Adicionar Canal de Destino", on_release=self.add_destino)
        self.start_btn = MDFillRoundFlatButton(text="▶ Iniciar Bot", on_release=self.iniciar_bot)

        # 🔹 Lista visual
        self.lista_destinos = MDList()
        scroll = ScrollView(size_hint=(1, 0.4))
        scroll.add_widget(self.lista_destinos)

        # 🔹 Status
        self.status_label = MDLabel(text="Status: Parado", halign="center", theme_text_color="Secondary")

        # 🔹 Layout final
        self.add_widget(self.api_id_field)
        self.add_widget(self.api_hash_field)
        self.add_widget(self.origem_field)
        self.add_widget(self.destino_field)
        self.add_widget(self.add_destino_btn)
        self.add_widget(scroll)
        self.add_widget(self.start_btn)
        self.add_widget(self.status_label)

    def add_destino(self, *args):
        """Adiciona um canal de destino na lista e exibe visualmente"""
        canal = self.destino_field.text.strip()
        if not canal:
            Snackbar(text="⚠️ Informe um ID de canal válido!").open()
            return

        try:
            canal_id = int(canal)
        except ValueError:
            Snackbar(text="❌ O ID do canal precisa ser um número!").open()
            return

        if canal_id in self.canais_destino:
            Snackbar(text="⚠️ Esse canal já foi adicionado!").open()
            return

        self.canais_destino.append(canal_id)
        self.destino_field.text = ""

        item = OneLineIconListItem(text=str(canal_id))
        icon = IconLeftWidget(icon="delete", on_release=lambda x: self.remover_destino(item, canal_id))
        item.add_widget(icon)
        self.lista_destinos.add_widget(item)

    def remover_destino(self, item, canal_id):
        """Remove um canal da lista"""
        if canal_id in self.canais_destino:
            self.canais_destino.remove(canal_id)
        self.lista_destinos.remove_widget(item)
        Snackbar(text=f"Canal {canal_id} removido.").open()

    def iniciar_bot(self, *args):
        """Inicia o bot em uma thread separada"""
        try:
            api_id = int(self.api_id_field.text.strip())
            api_hash = self.api_hash_field.text.strip()
            canal_origem = int(self.origem_field.text.strip())
        except ValueError:
            Snackbar(text="❌ Preencha todos os campos corretamente!").open()
            return

        if not self.canais_destino:
            Snackbar(text="⚠️ Adicione pelo menos um canal de destino!").open()
            return

        self.status_label.text = "Status: Iniciando..."
        self.bot = ForwardBot(api_id, api_hash, canal_origem, self.canais_destino)

        def run_bot():
            asyncio.run(self.bot.iniciar())

        Thread(target=run_bot, daemon=True).start()
        Clock.schedule_once(lambda dt: setattr(self.status_label, "text", "Status: Rodando ✅"), 2)


class ForwardBotApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"
        return BotAppScreen()


if __name__ == "__main__":
    ForwardBotApp().run()
