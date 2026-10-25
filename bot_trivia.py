import discord
from discord.ext import commands
import random
import json
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

RANKING_FILE = "ranking.json"

def carregar_ranking():
    if os.path.exists(RANKING_FILE):
        with open(RANKING_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def guardar_ranking(ranking):
    with open(RANKING_FILE, "w", encoding="utf-8") as f:
        json.dump(ranking, f, indent=4, ensure_ascii=False)

# Banco com mais de 100 perguntas rigorosas
BANCO_PERGUNTAS = [
    # --- GEOGRAFIA & MUNDO ---
    {"categoria": "🌍 Cultura Geral", "pergunta": "Qual é o rio mais longo do mundo?", "opcoes": ["Rio Amazonas", "Rio Nilo", "Rio Mississipi", "Rio Yangtzé"], "resposta": "Rio Nilo"},
    {"categoria": "🌍 Cultura Geral", "pergunta": "Qual é a capital da Austrália?", "opcoes": ["Sydney", "Melbourne", "Canberra", "Brisbane"], "resposta": "Canberra"},
    {"categoria": "🌍 Cultura Geral", "pergunta": "Qual é o país com maior população do mundo?", "opcoes": ["Índia", "China", "Estados Unidos", "Indonésia"], "resposta": "Índia"},
    {"categoria": "🌍 Cultura Geral", "pergunta": "Em que continente se situa o deserto do Saara?", "opcoes": ["Ásia", "África", "América do Sul", "Oceania"], "resposta": "África"},
    {"categoria": "🌍 Cultura Geral", "pergunta": "Qual é o oceano mais pequeno do mundo?", "opcoes": ["Oceano Pacífico", "Oceano Atlântico", "Oceano Índico", "Oceano Ártico"], "resposta": "Oceano Ártico"},
    {"categoria": "🌍 Cultura Geral", "pergunta": "Quantos continentes existem no modelo tradicional de 7 continentes?", "opcoes": ["5", "6", "7", "8"], "resposta": "7"},
    {"categoria": "🌍 Cultura Geral", "pergunta": "Qual é a montanha mais alta do mundo acima do nível do mar?", "opcoes": ["Monte K2", "Monte Everest", "Monte Kilimanjaro", "Monte Elbrus"], "resposta": "Monte Everest"},
    {"categoria": "🌍 Cultura Geral", "pergunta": "Qual é o maior país do mundo em área territorial?", "opcoes": ["Canadá", "China", "Estados Unidos", "Rússia"], "resposta": "Rússia"},
    {"categoria": "🌍 Cultura Geral", "pergunta": "Qual é a moeda oficial do Japão?", "opcoes": ["Yuan", "Won", "Yen", "Dólar"], "resposta": "Yen"},
    {"categoria": "🌍 Cultura Geral", "pergunta": "Em que país se situa a famosa Torre Eiffel?", "opcoes": ["Itália", "França", "Espanha", "Alemanha"], "resposta": "França"},
    {"categoria": "🌍 Cultura Geral", "pergunta": "Qual é a capital de Portugal?", "opcoes": ["Porto", "Coimbra", "Lisboa", "Faro"], "resposta": "Lisboa"},
    {"categoria": "🌍 Cultura Geral", "pergunta": "Qual é o país conhecido como a Terra do Sol Nascente?", "opcoes": ["China", "Japão", "Tailândia", "Coreia do Sul"], "resposta": "Japão"},
    {"categoria": "🌍 Cultura Geral", "pergunta": "Qual é a capital do Canadá?", "opcoes": ["Toronto", "Vancouver", "Ottawa", "Montreal"], "resposta": "Ottawa"},
    {"categoria": "🌍 Cultura Geral", "pergunta": "Qual é o deserto mais árido do planeta Terra?", "opcoes": ["Deserto do Saara", "Deserto do Atacama", "Deserto de Gobi", "Deserto de Mojave"], "resposta": "Deserto do Atacama"},
    {"categoria": "🌍 Cultura Geral", "pergunta": "Em que país fica localizada a cidade de Xangai?", "opcoes": ["Japão", "China", "Coreia do Sul", "Vietname"], "resposta": "China"},
    {"categoria": "🌍 Cultura Geral", "pergunta": "Qual é o mar que separa a Europa da África?", "opcoes": ["Mar Vermelho", "Mar Negro", "Mar Mediterrâneo", "Mar Cáspio"], "resposta": "Mar Mediterrâneo"},
    {"categoria": "🌍 Cultura Geral", "pergunta": "Qual é a capital da Argentina?", "opcoes": ["Buenos Aires", "Santiago", "Montevideu", "Lima"], "resposta": "Buenos Aires"},
    {"categoria": "🌍 Cultura Geral", "pergunta": "Qual é o país com maior linha de costa do mundo?", "opcoes": ["Austrália", "Rússia", "Canadá", "Estados Unidos"], "resposta": "Canadá"},
    {"categoria": "🌍 Cultura Geral", "pergunta": "Em qué país se encontra a antiga cidade de Machu Picchu?", "opcoes": ["México", "Peru", "Colômbia", "Chile"], "resposta": "Peru"},
    {"categoria": "🌍 Cultura Geral", "pergunta": "Qual é a capital da Itália?", "opcoes": ["Milão", "Nápoles", "Roma", "Florença"], "resposta": "Roma"},

    # --- CIÊNCIA & NATUREZA ---
    {"categoria": "🔬 Ciência", "pergunta": "Qual é o planeta mais próximo do Sol?", "opcoes": ["Vénus", "Terra", "Mercúrio", "Marte"], "resposta": "Mercúrio"},
    {"categoria": "🔬 Ciência", "pergunta": "Quantos ossos tem o corpo humano adulto?", "opcoes": ["180", "206", "250", "300"], "resposta": "206"},
    {"categoria": "🔬 Ciência", "pergunta": "Qual o metal cujo símbolo químico é 'Fe'?", "opcoes": ["Ferro", "Flúor", "Fósforo", "Frâncio"], "resposta": "Ferro"},
    {"categoria": "🔬 Ciência", "pergunta": "Qual é o gás predominante na atmosfera da Terra?", "opcoes": ["Oxigénio", "Azoto (Nitrogénio)", "Dióxido de Carbono", "Hidrogénio"], "resposta": "Azoto (Nitrogénio)"},
    {"categoria": "🔬 Ciência", "pergunta": "Qual o animal terrestre mais rápido do mundo?", "opcoes": ["Leão", "Guepardo (Cheetah)", "Cavalo", "Antílope"], "resposta": "Guepardo (Cheetah)"},
    {"categoria": "🔬 Ciência", "pergunta": "Qual é o maior mamífero do planeta Terra?", "opcoes": ["Elefante Africano", "Baleia Azul", "Tubarão Branco", "Girafa"], "resposta": "Baleia Azul"},
    {"categoria": "🔬 Ciência", "pergunta": "Qual é o elemento químico com o símbolo 'O'?", "opcoes": ["Ouro", "Osmónio", "Oxigénio", "Oceano"], "resposta": "Oxigénio"},
    {"categoria": "🔬 Ciência", "pergunta": "Quem formulou a Teoria da Relatividade?", "opcoes": ["Isaac Newton", "Albert Einstein", "Galileu Galilei", "Nikola Tesla"], "resposta": "Albert Einstein"},
    {"categoria": "🔬 Ciência", "pergunta": "Qual é o centro de controlo de uma célula viva?", "opcoes": ["Mitocôndria", "Núcleo", "Ribossoma", "Membrana Celular"], "resposta": "Núcleo"},
    {"categoria": "🔬 Ciência", "pergunta": "Qual é a principal fonte de energia para o sistema solar?", "opcoes": ["A Lua", "O Sol", "Júpiter", "Buraco Negro"], "resposta": "O Sol"},
    {"categoria": "🔬 Ciência", "pergunta": "Qual é o planeta mais quente do sistema solar?", "opcoes": ["Mercúrio", "Vénus", "Marte", "Júpiter"], "resposta": "Vénus"},
    {"categoria": "🔬 Ciência", "pergunta": "Qual é o símbolo químico do ouro?", "opcoes": ["Ag", "Au", "Pb", "Fe"], "resposta": "Au"},
    {"categoria": "🔬 Ciência", "pergunta": "Quantos dentes tem habitualmente um ser humano adulto?", "opcoes": ["28", "30", "32", "34"], "resposta": "32"},
    {"categoria": "🔬 Ciência", "pergunta": "Qual é a vitamina produzida pelo corpo humano através da exposição ao sol?", "opcoes": ["Vitamina A", "Vitamina B12", "Vitamina C", "Vitamina D"], "resposta": "Vitamina D"},
    {"categoria": "🔬 Ciência", "pergunta": "Qual o nome do processo pelo qual as plantas produzem o seu próprio alimento?", "opcoes": ["Fotossíntese", "Respiração", "Digestão", "Fermentação"], "resposta": "Fotossíntese"},
    {"categoria": "🔬 Ciência", "pergunta": "Qual é o osso mais longo do corpo humano?", "opcoes": ["Úmero", "Tíbia", "Fémur", "Costela"], "resposta": "Fémur"},
    {"categoria": "🔬 Ciência", "pergunta": "Qual é o estado físico da água a 100 graus Celsius ao nível do mar?", "opcoes": ["Sólido", "Líquido", "Gasoso (Vapor)", "Plasma"], "resposta": "Gasoso (Vapor)"},
    {"categoria": "🔬 Ciência", "pergunta": "Qual é o planeta conhecido como o Planeta Vermelho?", "opcoes": ["Vénus", "Saturno", "Marte", "Úrano"], "resposta": "Marte"},
    {"categoria": "🔬 Ciência", "pergunta": "Qual é o órgão responsável por bombear o sangue no corpo humano?", "opcoes": ["Pulmão", "Cérebro", "Coração", "Fígado"], "resposta": "Coração"},
    {"categoria": "🔬 Ciência", "pergunta": "Qual o nome da força que atrai os corpos para o centro da Terra?", "opcoes": ["Magnetismo", "Gravidade", "Inércia", "Atrito"], "resposta": "Gravidade"},

    # --- HISTÓRIA & ARTE ---
    {"categoria": "🏛️ História e Arte", "pergunta": "Quem pintou a Mona Lisa?", "opcoes": ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Claude Monet"], "resposta": "Leonardo da Vinci"},
    {"categoria": "🏛️ História e Arte", "pergunta": "Quem escreveu a obra literária 'Os Lusíadas'?", "opcoes": ["Almeida Garrett", "Luís de Camões", "Eça de Queirós", "Fernando Pessoa"], "resposta": "Luís de Camões"},
    {"categoria": "🏛️ História e Arte", "pergunta": "Em que ano terminou a Segunda Guerra Mundial?", "opcoes": ["1939", "1942", "1945", "1950"], "resposta": "1945"},
    {"categoria": "🏛️ História e Arte", "pergunta": "Em que ano começou a Primeira Guerra Mundial?", "opcoes": ["1910", "1914", "1918", "1939"], "resposta": "1914"},
    {"categoria": "🏛️ História e Arte", "pergunta": "Quem foi o primeiro presidente dos Estados Unidos da América?", "opcoes": ["Abraham Lincoln", "Thomas Jefferson", "George Washington", "Benjamin Franklin"], "resposta": "George Washington"},
    {"categoria": "🏛️ História e Arte", "pergunta": "Em que ano ocorreu a Revolução dos Cravos em Portugal?", "opcoes": ["1970", "1974", "1976", "1980"], "resposta": "1974"},
    {"categoria": "🏛️ História e Arte", "pergunta": "Qual civilização antiga construiu as famosas pirâmides de Gizé?", "opcoes": ["Romanos", "Gregos", "Egípcios", "Maias"], "resposta": "Egípcios"},
    {"categoria": "🏛️ História e Arte", "pergunta": "Quem pintou a obra 'A Noite Estrelada'?", "opcoes": ["Salvador Dalí", "Vincent van Gogh", "Claude Monet", "Rembrandt"], "resposta": "Vincent van Gogh"},
    {"categoria": "🏛️ História e Arte", "pergunta": "Em que país nasceu o pintor Pablo Picasso?", "opcoes": ["França", "Itália", "Espanha", "Grécia"], "resposta": "Espanha"},
    {"categoria": "🏛️ História e Arte", "pergunta": "Qual era o nome do império cuja capital era Roma?", "opcoes": ["Império Grego", "Império Romano", "Império Persa", "Império Otomano"], "resposta": "Império Romano"},
    {"categoria": "🏛️ História e Arte", "pergunta": "Quem foi o famoso líder indiano que liderou a independência através da não-violência?", "opcoes": ["Mahatma Gandhi", "Jawaharlal Nehru", "Indira Gandhi", "Subhas Chandra Bose"], "resposta": "Mahatma Gandhi"},
    {"categoria": "🏛️ História e Arte", "pergunta": "Em que século teve início o Renascimento na Europa?", "opcoes": ["Século XIII", "Século XIV", "Século XVI", "Século XVIII"], "resposta": "Século XIV"},
    {"categoria": "🏛️ História e Arte", "pergunta": "Qual foi o navegador português que chegou à Índia em 1498?", "opcoes": ["Cristovão Colombo", "Vasco da Gama", "Fernão de Magalhães", "Pedro Álvares Cabral"], "resposta": "Vasco da Gama"},
    {"categoria": "🏛️ História e Arte", "pergunta": "Qual o monumento emblemático da cidade de Paris conhecido pela sua estrutura de ferro?", "opcoes": ["Coliseu", "Torre Eiffel", "Big Ben", "Estátua da Liberdade"], "resposta": "Torre Eiffel"},
    {"categoria": "🏛️ História e Arte", "pergunta": "Quem esculpiu a estátua de David e pintou o teto da Capela Sistina?", "opcoes": ["Leonardo da Vinci", "Rafael", "Miguel Ângelo", "Donatello"], "resposta": "Miguel Ângelo"},
    {"categoria": "🏛️ História e Arte", "pergunta": "Qual foi o país responsável pela construção do Muro de Berlim durante a Guerra Fria?", "opcoes": ["Alemanha Oriental / União Soviética", "Estados Unidos", "Reino Unido", "França"], "resposta": "Alemanha Oriental / União Soviética"},
    {"categoria": "🏛️ História e Arte", "pergunta": "Em que ano o homem pisou a Lua pela primeira vez?", "opcoes": ["1965", "1969", "1972", "1975"], "resposta": "1969"},
    {"categoria": "🏛️ História e Arte", "pergunta": "Qual foi o império que construiu a cidade de Machu Picchu?", "opcoes": ["Asteca", "Inca", "Maia", "Olmeca"], "resposta": "Inca"},
    {"categoria": "🏛️ História e Arte", "pergunta": "Quem escreveu a famosa peça de teatro 'Romeu e Julieta'?", "opcoes": ["Charles Dickens", "William Shakespeare", "Victor Hugo", "Mark Twain"], "resposta": "William Shakespeare"},
    {"categoria": "🏛️ História e Arte", "pergunta": "Qual é o museu em Paris que abriga a pintura da Mona Lisa?", "opcoes": ["Museu d'Orsay", "Museu do Louvre", "Centro Pompidou", "Museu Rodin"], "resposta": "Museu do Louvre"},

    # --- DESPORTO & FUTEBOL ---
    {"categoria": "⚽ Desporto", "pergunta": "Qual é o país com mais títulos de Campeão do Mundo de Futebol?", "opcoes": ["Alemanha", "Argentina", "Brasil", "Itália"], "resposta": "Brasil"},
    {"categoria": "⚽ Desporto", "pergunta": "Quem ganhou a Bola de Ouro em 2023?", "opcoes": ["Erling Haaland", "Lionel Messi", "Kylian Mbappé", "Kevin De Bruyne"], "resposta": "Lionel Messi"},
    {"categoria": "⚽ Desporto", "pergunta": "Em que clube português é que o Cristiano Ronaldo começou a sua formação profissional?", "opcoes": ["FC Porto", "Benfica", "Sporting CP", "Boavista"], "resposta": "Sporting CP"},
    {"categoria": "⚽ Desporto", "pergunta": "Quantos minutos dura um jogo de futebol oficial (sem prolongamento)?", "opcoes": ["80 minutos", "90 minutos", "100 minutos", "120 minutos"], "resposta": "90 minutos"},
    {"categoria": "⚽ Desporto", "pergunta": "Qual seleção ganhou o Campeonato do Mundo de 2022 no Qatar?", "opcoes": ["França", "Brasil", "Argentina", "Croácia"], "resposta": "Argentina"},
    {"categoria": "⚽ Desporto", "pergunta": "Quem marcou o golo da vitória de Portugal na final do Euro 2016?", "opcoes": ["Cristiano Ronaldo", "Nani", "Éder", "Ricardo Quaresma"], "resposta": "Éder"},
    {"categoria": "⚽ Desporto", "pergunta": "Qual o clube com mais títulos da Liga dos Campeões da UEFA?", "opcoes": ["AC Milan", "Bayern Munique", "Real Madrid", "Barcelona"], "resposta": "Real Madrid"},
    {"categoria": "⚽ Desporto", "pergunta": "Quantos jogadores de campo tem cada equipa numa partida oficial de futebol?", "opcoes": ["9", "10", "11", "8"], "resposta": "10"},
    {"categoria": "⚽ Desporto", "pergunta": "Em que ano se realizou o primeiro Campeonato do Mundo de Futebol?", "opcoes": ["1920", "1930", "1942", "1950"], "resposta": "1930"},
    {"categoria": "⚽ Desporto", "pergunta": "Quem foi o treinador que venceu o Euro 2016 com Portugal?", "opcoes": ["José Mourinho", "Fernando Santos", "Carlos Queiroz", "Leonardo Jardim"], "resposta": "Fernando Santos"},
    {"categoria": "⚽ Desporto", "pergunta": "Qual o país organizador do Mundial de Futebol de 2026?", "opcoes": ["Espanha, Portugal e Marrocos", "EUA, Canadá e México", "China e Japão", "Austrália e Nova Zelândia"], "resposta": "EUA, Canadá e México"},
    {"categoria": "⚽ Desporto", "pergunta": "Qual é o clube com mais títulos de campeão nacional em Portugal?", "opcoes": ["FC Porto", "Benfica", "Sporting CP", "Belenenses"], "resposta": "Benfica"},
    {"categoria": "⚽ Desporto", "pergunta": "Em que país nasceu o futebol moderno e as suas regras oficiais?", "opcoes": ["Brasil", "Inglaterra", "Itália", "França"], "resposta": "Inglaterra"},
    {"categoria": "⚽ Desporto", "pergunta": "Qual foi o único guarda-redes a vencer a Bola de Ouro (no século XX)?", "opcoes": ["Gianluigi Buffon", "Iker Casillas", "Lev Yashin", "Manuel Neuer"], "resposta": "Lev Yashin"},
    {"categoria": "⚽ Desporto", "pergunta": "Que alcunha é dada à seleção nacional de futebol de Itália?", "opcoes": ["La Roja", "A Seleção das Quinas", "La Albiceleste", "Squadra Azzurra"], "resposta": "Squadra Azzurra"},
    {"categoria": "⚽ Desporto", "pergunta": "Qual o jogador conhecido como 'O Rei do Futebol'?", "opcoes": ["Maradona", "Pelé", "Zico", "Ronaldo Nazário"], "resposta": "Pelé"},
    {"categoria": "⚽ Desporto", "pergunta": "Em que continente se realizou o Mundial de 2010?", "opcoes": ["Ásia", "África", "América do Sul", "América do Norte"], "resposta": "África"},
    {"categoria": "⚽ Desporto", "pergunta": "Em que ano Portugal organizou o Campeonato da Europa (Euro 2004)?", "opcoes": ["2000", "2004", "2008", "2012"], "resposta": "2004"},
    {"categoria": "⚽ Desporto", "pergunta": "Quantos pontos vale um ensaio no Rugby Union tradicional?", "opcoes": ["3 pontos", "5 pontos", "7 pontos", "10 pontos"], "resposta": "5 pontos"},
    {"categoria": "⚽ Desporto", "pergunta": "Em que modalidade desportiva se destaca a lenda Michael Jordan?", "opcoes": ["Futebol", "Basquetebol", "Ténis", "Fórmula 1"], "resposta": "Basquetebol"},

    # --- GAMING & TECNOLOGIA ---
    {"categoria": "🎮 Gaming", "pergunta": "Qual foi o jogo mais vendido de todos os tempos?", "opcoes": ["Grand Theft Auto V", "Minecraft", "Tetris", "Cyberpunk 2077"], "resposta": "Minecraft"},
    {"categoria": "🎮 Gaming", "pergunta": "Qual é o nome da protagonista da saga de jogos Tomb Raider?", "opcoes": ["Jill Valentine", "Aloy", "Lara Croft", "Samus Aran"], "resposta": "Lara Croft"},
    {"categoria": "🎮 Gaming", "pergunta": "Em que ano foi lançado o primeiro jogo da consola PlayStation da Sony?", "opcoes": ["1992", "1994", "1998", "2000"], "resposta": "1994"},
    {"categoria": "🎮 Gaming", "pergunta": "Qual é o estúdio responsável pelo jogo Fortnite?", "opcoes": ["EA Sports", "Ubisoft", "Epic Games", "Activision"], "resposta": "Epic Games"},
    {"categoria": "🎮 Gaming", "pergunta": "Qual é o encanador mais famoso do mundo dos videojogos?", "opcoes": ["Luigi", "Sonic", "Mario", "Crash"], "resposta": "Mario"},
    {"categoria": "🎮 Gaming", "pergunta": "Qual destas consolas foi criada pela Microsoft?", "opcoes": ["PlayStation", "Xbox", "Nintendo Switch", "Sega Dreamcast"], "resposta": "Xbox"},
    {"categoria": "🎮 Gaming", "pergunta": "Qual o nome do ouriço azul mascote da SEGA?", "opcoes": ["Knuckles", "Tails", "Sonic", "Shadow"], "resposta": "Sonic"},
    {"categoria": "🎮 Gaming", "pergunta": "Qual o estúdio criador da aclamada saga de jogos Grand Theft Auto (GTA)?", "opcoes": ["Rockstar Games", "Bethesda", "Valve", "Ubisoft"], "resposta": "Rockstar Games"},
    {"categoria": "🎮 Gaming", "pergunta": "Qual o nome do herói da saga The Legend of Zelda?", "opcoes": ["Zelda", "Ganondorf", "Link", "Mario"], "resposta": "Link"},
    {"categoria": "🎮 Gaming", "pergunta": "Em que ano foi lançado o jogo original Minecraft?", "opcoes": ["2005", "2009", "2013", "2015"], "resposta": "2009"},
    {"categoria": "🎮 Gaming", "pergunta": "Qual o nome do protagonista principal da saga God of War?", "opcoes": ["Kratos", "Zeus", "Ares", "Hércules"], "resposta": "Kratos"},
    {"categoria": "🎮 Gaming", "pergunta": "Que jogo popular introduziu o conceito de blocos coloridos e linhas em 1984?", "opcoes": ["Tetris", "Pong", "Pac-Man", "Snake"], "resposta": "Tetris"},
    {"categoria": "💻 Tecnologia", "pergunta": "O que significa a sigla 'URL' na internet?", "opcoes": ["Uniform Resource Locator", "Universal Radio Link", "Unified Read Language", "User Remote Log"], "resposta": "Uniform Resource Locator"},
    {"categoria": "💻 Tecnologia", "pergunta": "Quem é considerado o criador da linguagem de programação Python?", "opcoes": ["Bill Gates", "Guido van Rossum", "Mark Zuckerberg", "Linus Torvalds"], "resposta": "Guido van Rossum"},
    {"categoria": "💻 Tecnologia", "pergunta": "Em qué ano foi fundada a empresa tecnológica Apple?", "opcoes": ["1976", "1984", "1990", "1995"], "resposta": "1976"},
    {"categoria": "💻 Tecnologia", "pergunta": "Qual o significado da sigla 'HTML'?", "opcoes": ["HyperText Markup Language", "High Tech Modern Language", "Hyper Transfer Machine Logic", "Home Tool Multi Language"], "resposta": "HyperText Markup Language"},
    {"categoria": "💻 Tecnologia", "pergunta": "Quem fundou a empresa Microsoft juntamente com Paul Allen?", "opcoes": ["Steve Jobs", "Bill Gates", "Jeff Bezos", "Elon Musk"], "resposta": "Bill Gates"},
    {"categoria": "💻 Tecnologia", "pergunta": "Qual destas redes sociais foi criada por Mark Zuckerberg em 2004?", "opcoes": ["Twitter", "Instagram", "Facebook", "TikTok"], "resposta": "Facebook"},
    {"categoria": "💻 Tecnologia", "pergunta": "Qual o componente principal de um computador responsável pelo processamento de dados?", "opcoes": ["Disco Rígido", "Placa Gráfica", "CPU (Processador)", "Memória RAM"], "resposta": "CPU (Processador)"},
    {"categoria": "💻 Tecnologia", "pergunta": "Qual o sistema operativo móvel criado pela Google?", "opcoes": ["iOS", "Windows Phone", "Android", "Linux"], "resposta": "Android"}
]

class TriviaView(discord.ui.View):
    def __init__(self, opcoes, resposta_certa, jogador):
        super().__init__(timeout=20.0)
        self.opcoes = opcoes
        self.resposta_certa = resposta_certa
        self.jogador = jogador
        self.acertou = None

        letras = ["🇦", "🇧", "🇨", "🇩"]
        for i, opcao in enumerate(opcoes):
            button = discord.ui.Button(
                label=f"{letras[i]} {opcao}", 
                style=discord.ButtonStyle.secondary, 
                custom_id=str(i)
            )
            button.callback = self.button_callback
            self.add_item(button)

    async def button_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.jogador.id:
            await interaction.response.send_message("❌ Este jogo não é teu! Usa o comando `!trivia` para começares a tua própria ronda.", ephemeral=True)
            return

        for child in self.children:
            child.disabled = True

        chosen_index = int(interaction.custom_id)
        escolha_utilizador = self.opcoes[chosen_index]

        embed = interaction.message.embeds[0]

        if escolha_utilizador == self.resposta_certa:
            self.acertou = True
            embed.color = 0x22c55e
            embed.add_field(name="🎉 Certo! (+10 Pontos)", value="A avançar para a próxima pergunta...", inline=False)
        else:
            self.acertou = False
            embed.color = 0xef4444
            embed.add_field(name="❌ Errado!", value=f"A resposta correta era: **{self.resposta_certa}**", inline=False)

        await interaction.response.edit_message(embed=embed, view=self)
        self.stop()

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        self.acertou = False
        self.stop()

@bot.event
async def on_ready():
    print(f'🏆 Bot de Trivia Sequencial ({len(BANCO_PERGUNTAS)} perguntas) está online!')

@bot.command(name='trivia')
async def trivia(ctx):
    """Inicia o modo de sequência contínua: acerta e avança de imediato!"""
    jogador = ctx.author
    pontos = 0
    total_certas = 0

    await ctx.send(f"🎮 **{jogador.mention} iniciou uma ronda de Trivia!** Responde corretamente para avançar automaticamente. O jogo termina se errares ou se o tempo esgotar.")

    while True:
        q = random.choice(BANCO_PERGUNTAS)
        opcoes = list(q["opcoes"])
        random.shuffle(opcoes)

        # Usar string normal sem f-string com quebra de linha mal formatada
        pergunta_texto = q['pergunta']
        desc = f"**{pergunta_texto}**\n\nClica na opção correta! *(Pontos atuais: {pontos})*"

        embed = discord.Embed(
            title=f"🧠 Pergunta #{total_certas + 1} • {q['categoria']}",
            description=f"**{pergunta_texto}**\n\nClica na opção correta! *(Pontos atuais: {pontos})*",
            color=0x3b82f6
        )
        embed.set_footer(text=f"Jogador: {jogador.name} • Tens 20 segundos!")

        view = TriviaView(opcoes, q["resposta"], jogador)
        msg = await ctx.send(embed=embed, view=view)

        await view.wait()

        if view.acertou is True:
            pontos += 10
            total_certas += 1
            await asyncio.sleep(0.8)
        else:
            ranking = carregar_ranking()
            user_id = str(jogador.id)

            if user_id not in ranking:
                ranking[user_id] = {"nome": jogador.name, "pontos": 0}

            ranking[user_id]["pontos"] += pontos
            guardar_ranking(ranking)

            embed_fim = discord.Embed(
                title="💀 Fim de Jogo!",
                description=f"Acertaste em **{total_certas}** perguntas consecutivas.\n🏆 **Total ganho nesta ronda:** `{pontos} pontos`!\n\nOs teus pontos foram guardados no ranking global (`!ranking`).",
                color=0xef4444
            )
            embed_fim.set_footer(text=f"Boa jogada, {jogador.name}!")
            await ctx.send(embed=embed_fim)
            break

@bot.command(name='ranking')
async def ranking(ctx):
    """Mostra a tabela de liderança global do servidor."""
    ranking_data = carregar_ranking()
    
    if not ranking_data:
        await ctx.send("🏆 Ainda ninguém pontuou no Trivia! Usa o comando `!trivia` para começar.")
        return

    ranking_ordenado = sorted(ranking_data.values(), key=lambda x: x["pontos"], reverse=True)

    descricao = ""
    medalhas = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    
    for i, jogador in enumerate(ranking_ordenado[:10]):
        pos = medalhas[i] if i < len(medalhas) else f"**{i+1}.**"
        descricao += f"{pos} **{jogador['nome']}** — `{jogador['pontos']} pontos`\n"

    embed = discord.Embed(
        title="🏆 Tabela de Liderança - Trivia do Servidor",
        description=descricao,
        color=0xf59e0b
    )
    embed.set_footer(text="Usa !trivia para jogares e subires no ranking!")
    await ctx.send(embed=embed)

import os

# O bot vai buscar o token de forma segura às configurações do Render
bot.run(os.getenv("DISCORD_TOKEN"))