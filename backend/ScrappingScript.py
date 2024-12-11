from django.core.files.base import ContentFile
from bs4 import BeautifulSoup
from datetime import datetime
import requests, string, re, uuid
import pandas as pd

from punchinthehead.models import Atleta, Imagens

alfabeto = list(string.ascii_lowercase)

dictStance = {
  'Orthodox': 1,
  'Southpaw': 2,
  'Switch': 3,
}

for letra in alfabeto:
  url = f"http://www.ufcstats.com/statistics/fighters?char={letra}&page=all"

  headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
  }

  response = requests.get(url, headers=headers)

  if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"class": "b-statistics__table"})
    rows = table.find_all("tr", {"class": "b-statistics__table-row"})

    fighter_data = []
    
    for row in rows[2:]:
      try:
        link = row.find("a").get("href")
        idAtleta = link.split("/")[-1]

        responseAtleta = requests.get(link, headers=headers)

        if responseAtleta.status_code == 200:
          soupAtleta = BeautifulSoup(responseAtleta.text, "html.parser")
          nome = soupAtleta.find("span", {"class":"b-content__title-highlight"}).text.strip()
          apelido = soupAtleta.find("p", {"class":"b-content__Nickname"}).text.strip()
          
          stance = dictStance.get(soupAtleta.find("ul", {"class":"b-list__box-list"}).find_all("li")[-2].text.replace('STANCE:','').replace('--','').strip(), 1)
          dob = soupAtleta.find("ul", {"class":"b-list__box-list"}).find_all("li")[-1].text.replace('DOB:','').replace('--','').strip()
          
          date = datetime.strptime(dob, "%b %d, %Y").date() if dob else None

          linkUFC = f'https://www.ufc.com.br/athletes/all?https%3A%2F%2Fwww.ufc.com.br%2Fathletes%2Fall=&gender=All&search={"%20".join(nome.split(" "))}'
          # print(f'Link UFC: {linkUFC}')

          responseUFC = requests.get(linkUFC, headers=headers)

          if responseUFC.status_code == 200:
            soupUFC = BeautifulSoup(responseUFC.text, "html.parser")
            listaLutadores = soupUFC.find("ul", {"class":"l-flex--4col-1to4"})
            existeLutador = listaLutadores.find(string=re.compile(nome)) if listaLutadores else None

            if not existeLutador:
              print(f'Não encontramos o(a) {nome} {f'"{apelido}"' if apelido else ""} {date}')
              continue

            cardFighter = existeLutador.parent.parent.parent.parent
            endpointPerfil = cardFighter.find("a", {"class":"e-button--black"}).get("href").split("/")[-1]
            print(f'Endpoint: {endpointPerfil}')
            linkPerfilUFC = f'https://www.ufc.com.br/athlete/{endpointPerfil}'

            foto1 = cardFighter.find("img",{"class","image-style-teaser"})
            foto2 = cardFighter.find("img",{"class","image-style-event-fight-card-upper-body-of-standing-athlete"})

            # print(f'Foto {foto1} - {foto2}')
            fotoFrontal = foto1.get("src") if foto1 else None
            fotoCorpo = foto2.get("src") if foto2 else None

            # print(f'\nFighter: {all([foto1,foto2])} {fotoFrontal}\n {fotoCorpo}\n')

            responsePerfil = requests.get(linkPerfilUFC, headers=headers)

            if responsePerfil.status_code == 200 and all([foto1,foto2]):
              soupPerfil = BeautifulSoup(responsePerfil.text, "html.parser")

              fotoMeio = soupPerfil.find("img",{"class","hero-profile__image"}).get("src")

              categoria = soupPerfil.find("p", {"class":"hero-profile__division-title"}).text.replace('Peso-','').replace('Categoria','').strip()
              status = soupPerfil.find("div", {"class":"hero-profile__tags"}).find(string=re.compile("Não está lutando"))
              status = True if status != 'Não está lutando' else False

              bioInfo = soupPerfil.find("div", {"class":"c-bio__info-details"})

              try:
                altura = float(bioInfo.find(string=re.compile("Altura")).parent.parent.find("div",{"class","c-bio__text"}).text) * 0.0254
              except:
                altura = None
              try:
                peso = float(bioInfo.find(string=re.compile("Peso")).parent.parent.find("div",{"class","c-bio__text"}).text) * 0.453592
              except:
                peso = None
              try:
                alcance = float(bioInfo.find(string=re.compile("Envergadura")).parent.parent.find("div",{"class","c-bio__text"}).text) * 0.0254
              except:
                alcance = None

              estreia = datetime.strptime(bioInfo.find(string=re.compile("Estreia no UFC")).parent.parent.find("div",{"class","c-bio__text"}).text, "%d.%m.%y").date()

              # print(f'Categoria: {categoria} - Status: {status} - Altura: {altura:.2f} - Peso: {peso:.2f} - Alcance: {alcance:.2f} - Estreia: {estreia}')

              existeAtleta = Atleta.objects.filter(codigo=idAtleta).exists()

              atleta = Atleta.objects.get(codigo=idAtleta) if existeAtleta else Atleta()
              print(f'Já existe {nome} {f'"{apelido}"' if apelido else ""} {date}') if existeAtleta else None

              atleta.codigo = idAtleta

              atleta.nome, atleta.sobrenome = nome.split(" ", maxsplit=1)
              atleta.apelido = apelido
              
              atleta.altura = float(f'{altura:.2f}') if altura else None
              atleta.peso = float(f'{peso:.2f}') if peso else None
              atleta.alcance = float(f'{alcance:.2f}') if alcance else None

              atleta.posicao = stance

              atleta.data_nascimento = date
              atleta.estreia = estreia

              atleta.save()

              imagemFrontal = Imagens.objects.get(atleta=atleta, tipo=1) if existeAtleta else Imagens()
              imagemCorpo = Imagens.objects.get(atleta=atleta, tipo=2) if existeAtleta else Imagens()
              imagemMeio = Imagens.objects.get(atleta=atleta, tipo=3) if existeAtleta else Imagens()

              imagemFrontal.atleta = atleta
              imagemCorpo.atleta = atleta
              imagemMeio.atleta = atleta

              imagemFrontal.tipo = 1
              imagemCorpo.tipo = 2
              imagemMeio.tipo = 3

              imagemFrontal.arquivo.save(f'{uuid.uuid4()}.jpg', ContentFile(requests.get(fotoFrontal).content))
              imagemCorpo.arquivo.save(f'{uuid.uuid4()}.jpg', ContentFile(requests.get(fotoCorpo).content))
              imagemMeio.arquivo.save(f'{uuid.uuid4()}.jpg', ContentFile(requests.get(fotoMeio).content))
      except Exception as erro:
        print(f'Deu esse Erro: {erro}')
        continue