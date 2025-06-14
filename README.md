# HoryuAI

HoryuAI é um bot para Discord com integração à API Gemini para gerar conteúdo dinâmico. Ele foi desenvolvido para trazer recomendações de filmes, gerar imagens a partir de prompts e auxiliar com comandos administrativos como kick e ban, além de enviar notícias semanais (news) de forma automatizada.

## Funcionalidades

- **Notícias Semanais Automatizadas:**  
  - O bot envia, semanalmente, uma "news" com recomendações de filmes, contendo título, sinopse, review e imagem, tudo em embeds organizados.
  
- **Geração de Imagens:**  
  - Com o comando `!imagem`, o bot utiliza a API Gemini para gerar imagens a partir de um prompt fornecido pelo usuário.
  
- **Recomendações de Filmes:**  
  - Utilizando o comando `!recom_filmes`, o bot envia embeds com recomendações de filmes, incluindo informações como título, ano, sinopse e links para a Wikipedia.
  
- **Comandos Administrativos:**  
  - Comandos como `!kick` e `!ban` para moderação do servidor, garantindo uma gestão simplificada do Discord.

## Tecnologias Utilizadas

- **Python 3.x**
- **discord.py:** Biblioteca para interação com a API do Discord.
- **google.generativeai:** Integração com a API Gemini para geração de conteúdo.
- **python-dotenv:** Para carregar variáveis de ambiente (tokens de autenticação).

## Configuração e Instalação

1. **Clone o Repositório:**
   ```bash
   git clone https://github.com/laranjaeragnarok2/HoryuAI.git
   cd HoryuAI
   ```

2. **Instale as Dependências:**
   - Crie um arquivo `requirements.txt` listando as dependências do projeto (por exemplo, `discord.py`, `python-dotenv`, `google-generativeai` etc.).
   - Instale as dependências:
     ```bash
     pip install -r requirements.txt
     ```

3. **Configure as Variáveis de Ambiente:**
   - Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:
     ```env
     DISCORD_BOT_TOKEN=seu_token_do_discord
     GEMINI_API_KEY=sua_chave_api_gemini
     ```
     
4. **Execute o Bot:**
   - Para rodar o bot, execute:
     ```bash
     python horyuai.py
     ```
   - Ou, se preferir, use:
     ```bash
     py horyuai.py
     ```

## Contribuição

Pull requests são bem-vindos! Se você deseja contribuir para o projeto, abra uma issue para discutir as mudanças importantes antes de enviar seu PR.

## Licença

Este projeto está licenciado sob os termos da licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.

## Contato

Para dúvidas ou sugestões, sinta-se à vontade para entrar em contato via [GitHub Issues](https://github.com/laranjaeragnarok2/HoryuAI/issues).

---

Divirta-se utilizando o HoryuAI e continue evoluindo o projeto!
