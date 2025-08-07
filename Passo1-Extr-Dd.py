import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

CONFIG = {
    'base_url': "https://www.icarros.com.br/comprar/usados-e-seminovos",
    'headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    },
    'selectors': {
        'card_anuncio': "li.small-offer-card",
        'titulo_link': "a.small-offer-card__title-container",
        'infos_carro': ".info-container__car-info p",
        'localizacao': ".info-container__location-info p",
        'preco': "h2.preco",
        'cambio': "//li[@title='Câmbio']",
        'cookie_banner_id': "onetrust-accept-btn-handler"
    },
    'timeouts': {
        'request': 20,
        'selenium_wait': 10
    }
}

def coletar_links_base(max_paginas):
    print(f"FASE 1: Coletando links base de {max_paginas} páginas...")
    lista_dados_base = []
    
    for pagina_atual in range(1, max_paginas + 1):
        url = f"{CONFIG['base_url']}?anunciante=2&ano_min=2015&pag={pagina_atual}"
        try:
            response = requests.get(url, headers=CONFIG['headers'], timeout=CONFIG['timeouts']['request'])
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            anuncios = soup.select(CONFIG['selectors']['card_anuncio'])
            if not anuncios:
                print(f"  > Nenhum anúncio na página {pagina_atual}. Finalizando busca de links.")
                break
            
            for anuncio in anuncios:
                titulo_tag = anuncio.select_one(CONFIG['selectors']['titulo_link'])
                if not titulo_tag or not titulo_tag.has_attr('href'): continue

                link = "https://www.icarros.com.br" + titulo_tag['href']
                titulo_completo = titulo_tag.get('title', 'N/A')
                infos = [info.text.strip() for info in anuncio.select(CONFIG['selectors']['infos_carro'])]
                localizacao_tag = anuncio.select_one(CONFIG['selectors']['localizacao'])
                cidade, estado = (localizacao_tag.text.strip().split(',') + ['N/A'])[:2] if localizacao_tag else ('N/A', 'N/A')
                
                lista_dados_base.append({
                    'link': link, 'estado': estado.strip(), 'cidade': cidade.strip(),
                    'marca': titulo_completo.split(' ')[0], 'modelo': ' '.join(titulo_completo.split(' ')[1:]),
                    'ano': infos[0] if len(infos) > 0 else 'N/A', 'km': infos[1] if len(infos) > 1 else 'N/A'
                })
        except requests.exceptions.RequestException as e:
            print(f"  > Erro de rede na página {pagina_atual}: {e}. Continuando...")
            continue
    
    print(f"FASE 1 concluída. {len(lista_dados_base)} anúncios básicos coletados.")
    return lista_dados_base

def buscar_preco_e_detalhes(carro):
    """
    Esta função é executada em paralelo para cada anúncio.
    Ela abre um navegador, extrai os dados e fecha.
    """
    options = uc.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--blink-settings=imagesEnabled=false')
    
    driver = None
    try:
        driver = uc.Chrome(options=options, use_subprocess=True)
        wait = WebDriverWait(driver, CONFIG['timeouts']['selenium_wait'])
        driver.get(carro['link'])
        
        try:
            wait.until(EC.element_to_be_clickable((By.ID, CONFIG['selectors']['cookie_banner_id']))).click()
            time.sleep(0.5)
        except TimeoutException:
            pass

        preco_elemento = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, CONFIG['selectors']['preco'])))
        carro['preco'] = preco_elemento.text.strip()
        
        try:
            carro['cambio'] = driver.find_element(By.XPATH, CONFIG['selectors']['cambio']).text.strip()
        except NoSuchElementException:
            carro['cambio'] = "Não informado"
            
    except Exception:
        carro['preco'] = "ERRO"
        carro['cambio'] = "ERRO"
    finally:
        if driver:
            driver.quit()
    return carro

def extrair_dados_icarros_otimizado(max_paginas=50):
    
    lista_dados_base = coletar_links_base(max_paginas)
    if not lista_dados_base:
        print("Nenhum dado coletado na Fase 1. Encerrando.")
        return

    print(f"\nFASE 2: Iniciando busca detalhada em paralelo para {len(lista_dados_base)} anúncios...")
    lista_final_carros = []
    
    num_workers = os.cpu_count()
    print(f"Usando {num_workers} workers paralelos.")

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(buscar_preco_e_detalhes, carro) for carro in lista_dados_base]
        
        for i, future in enumerate(as_completed(futures)):
            resultado = future.result()
            lista_final_carros.append(resultado)
            print(f"\rProgresso: {i + 1}/{len(lista_dados_base)} anúncios processados...", end="")

    print("\nFASE 2 concluída.")

    print("\nMontando o arquivo final...")
    df = pd.DataFrame(lista_final_carros)
    colunas_ordenadas = ['estado', 'cidade', 'marca', 'modelo', 'cambio', 'ano', 'km', 'preco', 'link']
    df = df.reindex(columns=colunas_ordenadas)
    
    nome_arquivo = "dados_icarros_completos_50_paginas.csv"
    df.to_csv(nome_arquivo, index=False, sep=';', encoding='utf-8-sig')
    
    print(f"\nSUCESSO! Arquivo '{nome_arquivo}' salvo com {len(df)} registros.")
    print("\nAmostra dos dados finais:")
    print(df.head())

if __name__ == '__main__':
    extrair_dados_icarros_otimizado(max_paginas=50)