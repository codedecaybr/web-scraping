import requests
from bs4 import BeautifulSoup


## URLS DE BASE ##
URL = "https://www.indeed.com.br/empregos?q=programador&l=S%C3%A3o+Paulo%2C+SP&start=##START_INDEX##"
baseURL = "https://www.indeed.com.br"


def obterPagPesquisa(i):
    """
    Recebe um indice de página i, monta a URL adequada,
    baixa o conteúdo e devolve um objeto do BeautifulSoup
    representando o conteúdo da página de pesquisa do Indeed.
    """

    # monta a URL:
    rURL = URL.replace("##START_INDEX##", str(i*10) )
    print("Baixando página de pesquisa: " + rURL)
    # download da página de pesquisa:
    searchPage = requests.get(rURL)
    # conversão para o objeto do BeautifulSoup:
    searchSoup = BeautifulSoup(searchPage.text, 'html.parser')

    return searchSoup

def obterPagVaga(jobLink):
    """
    Recebe um objeto do BeautifulSoup com o link extraído
    para um anúncio de vaga no Ideed e devolve o objeto
    do BeautifulSoup representando os detalhes da vaga
    anunciada.
    """

    print("\tBaixando página da vaga: %s" %(jobLink.get("title")))
    # download da página da vaga:
    with requests.Session() as s:
        s.max_redirects = 1
        try:
            jobPage = s.get(baseURL + jobLink.get("href"), timeout=2)
        except requests.RequestException:
            print("\t\tMuitos redirecionamentos. Deve ser uma vaga patrocinada.")
            return None
    # verifica se a página baixada pertence
    # ao domínio do indeed.
    # as vagas patrocinadas redirecionam para sites
    # externos, com estruturas desconhecidas
    if "indeed.com.br" not in jobPage.url:
        print("\t\tVaga patrocinada. Ignorando.")
        return None
    # conversão para o objeto do BeautifulSoup:
    jobSoup = BeautifulSoup(jobPage.text, 'html.parser')

    return jobSoup

def main():

    # número de páginas de pesquisa a serem baixadas:
    for i in range(1):

        # obtém página de resultado de pesquisa:
        # obtém página de resultado de pesquisa:
        searchSoup = obterPagPesquisa(i)
        # encontra todos os links de anúncios de vagas
        jobsLinks = searchSoup.find_all(class_="turnstileLink")

        # para cada link encontrado...
        for jobLink in jobsLinks:

            # baixa a página com o detalhe da vaga:
            jobSoup = obterPagVaga(jobLink)
            if jobSoup is None:
                continue

main()
