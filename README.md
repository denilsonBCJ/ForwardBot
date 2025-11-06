
# ForwardBot 🔁

Um simples **userbot do Telegram** feito em **Python**, que encaminha automaticamente mensagens de um canal de origem para um canal de destino, usando a biblioteca [Telethon](https://github.com/LonamiWebs/Telethon).



## 🚀 Tecnologias utilizadas
- Python 3.10+
- Telethon



## ⚙️ Configuração e uso

1. **Clone o repositório**

   ```bash
   git clone https://github.com/denilsonbcj/ForwardBot.git
   cd ForwardBot
   ```

2. **Instale as dependências**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure suas credenciais**
   Edite o arquivo `main.py` e substitua:

   ```python
   API_ID = SEU_API_ID
   API_HASH = "SEU_API_HASH"
   CANAL_ORIGEM = ID_DO_CANAL_ORIGEM
   CANAL_DESTINO = ID_DO_CANAL_DESTINO
   ```

4. **Execute o bot**

   ```bash
   python main.py
   ```

> Na primeira execução, o Telegram pode pedir o código de autenticação via mensagem ou SMS.
> Após isso, o bot manterá uma sessão salva localmente.



## 📜 Licença

Este projeto está sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.



## 👤 Autor

**Denilson**
Desenvolvedor Python focado em automação e bots para Telegram.

````