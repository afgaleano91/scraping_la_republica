import requests
import lxml.html as html
import os
import datetime

HOME_URL = 'https://www.larepublica.co/'

XPATH_LINK_TO_ARTICLE = '//a[contains(@class, "kicker")]/@href'
XPATH_TITLE = '//h2[not(@class)]/a/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH__BODY = '//div[@class="html-content"]/p/text()'


def parse_new(link, today):
    try:
        response = requests.get(link)

        if response.status_code == 200:
            news = response.content.decode('utf-8')
            parsed = html.fromstring(news)
            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                
                title = title.replace('\"', '')
                title = title.replace('#','')
                title = title.replace('|','')
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH__BODY)
            except IndexError:
                return
            #manejador contextual de python
            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')

                for p in body:
                    f.write(p)
                    f.write('\n')

        else:
            raise ValueError(f'Error: {response.status_code}')

    except ValueError as ve:
        print(ve)


def parse_home():
    # Para capturar errores y por buena practica se usa un bloque try
    try:
        #usamos response para hacer una peticion get a nuestra url
        response = requests.get(HOME_URL)
        # Solo con code 200 procedemos a ejecutar
        if response.status_code == 200:
            # se debe tomar el contenido y decodificar en un formato legible utf-8 en este caso
            home = response.content.decode('utf-8')
            #Parseamos o convertimos nuestra inforamcion para manipularla
            # print(home)
            parsed = html.fromstring(home)
            #Pasamos nuestros xpath de links para extraerlos de la url
            #print(parsed)
            links_to_news = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            #print(links_to_news)

            today = datetime.date.today().strftime('%d-%m-%Y')

            if not os.path.isdir(today):
                os.mkdir(today)
            
            for link in links_to_news:
                print(link)
                parse_new(link, today)
      
        else:
            #captura de posible error mostrando code de respuesta
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()

if __name__ == "__main__":
    run()