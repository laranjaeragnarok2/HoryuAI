import discord
from discord.ext import commands
import google.generativeai as genai
import os
from dotenv import load_dotenv # Para carregar variáveis de ambiente
import json
from discord.ext import tasks

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Configurar a API do Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Definir os intents do bot (permissões)
# É importante ajustar os intents conforme a necessidade do seu bot.
# Para comandos de mensagem e interações básicas:
intents = discord.Intents.default()
intents.message_content = True # Necessário para ler o conteúdo das mensagens para comandos
intents.members = True # Necessário para alguns comandos de servidor como kick/ban (opcional)

# Criar uma instância do bot com um prefixo de comando
# Você pode usar discord.Bot() para focar em slash commands
bot = commands.Bot(command_prefix='!', intents=intents)

NEWS_CHANNEL_ID = 1381497919835865088  # ID do canal news

@tasks.loop(hours=168)  # 168 horas = 7 dias
async def weekly_news():
    channel = bot.get_channel(NEWS_CHANNEL_ID)
    if channel:
        theme = "comédia"  # Atualize a temática conforme desejar
        prompt = (
            f"Liste 5 novos filmes da temática '{theme}'. Para cada filme, forneça:\n"
            "- Título\n"
            "- Ano\n"
            "- Link da Wikipedia\n"
            "- Um resumo curto da sinopse\n"
            "- Uma breve nota de review\n"
            "- URL de uma imagem representativa\n"
            "Formate a resposta em JSON (lista de objetos)."
        )
        try:
            response = genai.generate_text(prompt=prompt)
            # Supondo que a resposta contenha um campo 'text' com a string JSON
            filmes = json.loads(response.get("text", "[]"))
            
            if filmes:
                for filme in filmes:
                    embed = discord.Embed(
                        title=f"{filme.get('titulo', 'Título não disponível')} ({filme.get('ano', 'Ano')})",
                        url=filme.get('wiki', ''),
                        description=filme.get('sinopse', ''),
                        color=0xFF4500
                    )
                    embed.set_thumbnail(url=filme.get('imagem', ''))
                    embed.add_field(name="Review", value=filme.get('review', ''), inline=False)
                    await channel.send(embed=embed)
            else:
                await channel.send("Não foram encontradas recomendações para a temática.")
        except Exception as e:
            await channel.send(f"Erro ao gerar recomendações: {e}")
    else:
        print("Canal de news não encontrado.")

@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} conectado e pronto!')
    print(f'ID do Bot: {bot.user.id}')
    try:
        # Sincronizar comandos de aplicativo (slash commands) globalmente ou para um guild específico
        # Para desenvolvimento, é mais rápido sincronizar para um guild específico:
        # synced = await bot.tree.sync(guild=discord.Object(id=SEU_GUILD_ID_AQUI))
        # Para produção, sincronize globalmente (pode levar até 1 hora para propagar):
        synced = await bot.tree.sync()
        print(f"Sincronizados {len(synced)} comandos de aplicativo.")
    except Exception as e:
        print(f"Erro ao sincronizar comandos: {e}")
    weekly_news.start()

# --- Comandos do Bot Virão Aqui ---

@bot.command(name="imagem")
async def gerar_imagem(ctx, *, prompt: str):
    """Gera uma imagem usando o Gemini a partir de um prompt."""
    try:
        # Exemplo de uso da API Gemini para gerar imagem (ajuste conforme a resposta real da API)
        response = genai.generate_image(prompt=prompt)
        image_url = response.get('image_url', 'Não foi possível gerar a imagem.')
        await ctx.send(image_url)
    except Exception as e:
        await ctx.send(f"Erro ao gerar imagem: {e}")

@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    """Expulsa um membro do servidor."""
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} foi expulso. Motivo: {reason}")

@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    """Bane um membro do servidor."""
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} foi banido. Motivo: {reason}")

@bot.command(name="recom_filmes")
async def recom_filmes(ctx):
    """Envia recomendações de filmes com embeds bonitos."""
    filmes = [
        {
            "titulo": "Blade Runner",
            "ano": "1982",
            "sinopse": "Num futuro distópico, um caçador persegue replicantes fugitivos, questionando o que é ser humano.",
            "review": "Visual impactante com trilha sonora icônica.",
            "imagem": "https://upload.wikimedia.org/wikipedia/en/5/53/Blade_Runner_poster.jpg",
            "wiki": "https://en.wikipedia.org/wiki/Blade_Runner"
        },
        {
            "titulo": "Tron",
            "ano": "1982",
            "sinopse": "Um programador é transportado para dentro de um mundo digital repleto de desafios.",
            "review": "Pioneiro em gráficos digitais, imerso na estética dos anos 80.",
            "imagem": "https://upload.wikimedia.org/wikipedia/en/8/81/Tron_poster.jpg",
            "wiki": "https://en.wikipedia.org/wiki/Tron"
        },
        {
            "titulo": "Akira",
            "ano": "1988",
            "sinopse": "Em uma Tóquio futurista, um jovem com poderes psíquicos desencadeia um caos revolucionário.",
            "review": "Anime revolucionário que inspirou gerações.",
            "imagem": "https://upload.wikimedia.org/wikipedia/en/4/4e/Akira_-_1988.jpg",
            "wiki": "https://en.wikipedia.org/wiki/Akira_(1988_film)"
        },
        {
            "titulo": "Ghost in the Shell",
            "ano": "1995",
            "sinopse": "Uma ciborgue investiga crimes cibernéticos enquanto questiona sua própria identidade.",
            "review": "Clássico que mistura filosofia e ação em um universo tecnológico.",
            "imagem": "https://upload.wikimedia.org/wikipedia/en/2/2d/Ghostintheshellposter.jpg",
            "wiki": "https://en.wikipedia.org/wiki/Ghost_in_the_Shell_(1995_film)"
        },
        {
            "titulo": "Johnny Mnemonic",
            "ano": "1995",
            "sinopse": "Um mensageiro digital carrega informações vitais no cérebro em um futuro caótico.",
            "review": "Uma visão única do cyberpunk dos anos 90.",
            "imagem": "https://upload.wikimedia.org/wikipedia/en/2/2e/Johnny_Mnemonic_poster.jpg",
            "wiki": "https://en.wikipedia.org/wiki/Johnny_Mnemonic"
        }
    ]
    
    for filme in filmes:
        embed = discord.Embed(
            title=f"{filme['titulo']} ({filme['ano']})",
            url=filme['wiki'],
            description=filme['sinopse'],
            color=0x1E90FF
        )
        embed.set_thumbnail(url=filme['imagem'])
        embed.add_field(name="Review", value=filme['review'], inline=False)
        await ctx.send(embed=embed)

    await ctx.send("Recomendações enviadas com sucesso! Continue assim!")

# Rodar o bot
if DISCORD_BOT_TOKEN:
    bot.run(DISCORD_BOT_TOKEN)
else:
    print("Erro: Token do bot do Discord não encontrado. Verifique seu arquivo .env")

