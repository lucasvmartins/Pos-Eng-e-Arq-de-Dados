# Prática de "webscraping" de trends do X/Twitter

# %%
# Instalando as bibliotecas Tweepy
# ! pip install requests beautifulsoup4 wordcloud matplotlib

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
