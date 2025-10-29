# Prática de "webscraping" de trends do X/Twitter

# %%
# Instalando as bibliotecas requests beautifulsoup4 wordcloud (caso ainda não tenha)
# ! pip install requests beautifulsoup4 wordcloud

# %%
# Importando bibliotecas
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# %%
# Capturando os trending topics do Brasil via Trends24
url = "https://trends24.in/brazil/"
response = requests.get(url)

# Define a codificação para UTF-8
response.encoding = 'UTF-8'

# Cria o objeto BeautifulSoup usando o texto já decodificado
soup = BeautifulSoup(response.text, 'html.parser')

# %%
# Extraindo os tópicos
trends = [tag.text.strip() for tag in soup.select(".trend-card__list a")]

# %%
# Criando a wordcloud
text = " ".join(trends)
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)

# %%
# Exibindo o resultado
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
