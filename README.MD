# FEAR App – Film Experience And Reviews 
ObS: Nome sugerido pelo [ChatGpt](https://https://chatgpt.com)

Esse é um código mini app em python de exemplo de como criar um agente especialista utilizando ChatGpt e LangChain. Foi baseado no estudo de caso do curso [Pós-Graduação em Engenharia de Inteligência Artificial da Data Science Academy](https://www.datascienceacademy.com.br/bundle/pos-graduacao-em-engenharia-de-inteligencia-artificial). 

Esse projeto já roda um servidor web com uma pagina htmml para rodar o teste. 

Primeiro você deve instalar os pacotes necessários que se encontrar no 'requirements.txt'. Sugiro dar uma olhada no [Anaconda](https://www.anaconda.com/download) para instalar um hambiente python em sua máquina. 

No terminal rode 
```python
pip install -r requirements.txt
```
E para rodar o app web execute no terminal

 ```python
 streamlit run FEAR_App.py
 ```
Obs: Para conseguir usar você deve criar e configurar o arquivo *.env* com `OPENAI_API_KEY = "ai_key"` ou configura essa váriavel no seu PATH

![Tela do app](/img/screenshot.png)