import requests
import json
import os
from urllib.parse import quote

# HTTP Headers for API requests
API_HEADERS = {
    'sec-ch-ua-platform': '"Windows"',
    'Referer': 'https://tracker.gg/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'sec-ch-ua': '"Chromium";v="148", "Brave";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
}


def log_message(message: str, log_viewer=None):
    """Send message to console and/or log viewer"""
    print(message)
    if log_viewer is not None:
        log_viewer.write(message)


def fetch_premier_stats(log_viewer=None) -> int:
    """
    Fetch Premier stats for all players
    Returns the number of players processed successfully
    """
    carpeta = 'stats_premier'
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    
    log_message("[yellow]Obteniendo estadísticas de Premier...[/yellow]", log_viewer)
    
    # Leer archivos de stats para obtener season_id_premier
    try:
        archivos_competitivo = [f for f in os.listdir('stats') if f.endswith('.json')]
    except FileNotFoundError:
        log_message("  [yellow]⚠ No se encontró carpeta stats[/yellow]", log_viewer)
        return 0
    
    count = 0
    for archivo_comp in archivos_competitivo:
        ruta_comp = os.path.join('stats', archivo_comp)
        
        try:
            with open(ruta_comp, 'r') as f:
                datos_comp = json.load(f)
        except Exception as e:
            log_message(f"  [red]✗ Error al leer {archivo_comp}: {e}[/red]", log_viewer)
            continue
        
        jugador = datos_comp.get('Jugador')
        season_id_premier = datos_comp.get('SeasonIdPremier')
        
        if not jugador or not season_id_premier:
            log_message(f"  [yellow]⚠ {jugador} - No tiene seasonId de Premier[/yellow]", log_viewer)
            continue
        
        log_message(f"  → {jugador}...", log_viewer)
        
        # Buscar el nombre completo en nombres.txt
        try:
            with open('nombres.txt', 'r') as f:
                nombres_txt = f.read().strip().split('\n')
            
            nombre_completo = None
            for linea in nombres_txt:
                if linea.strip().startswith(jugador + '#'):
                    nombre_completo = linea.strip()
                    break
            
            if not nombre_completo:
                log_message(f"    [yellow]⚠ No se encontró ID para {jugador} en nombres.txt[/yellow]", log_viewer)
                continue
        except FileNotFoundError:
            log_message(f"    [red]✗ No se encontró nombres.txt[/red]", log_viewer)
            continue
        
        # Hacer petición a /segments/season
        nombre_encoded = quote(nombre_completo)
        url = f'https://api.tracker.gg/api/v2/valorant/standard/profile/riot/{nombre_encoded}/segments/season'
        
        params = {
            'playlist': 'premier',
            'seasonId': season_id_premier,
            'source': 'web',
        }
        
        response = requests.get(url, params=params, headers=API_HEADERS)
        
        if response.status_code == 200:
            try:
                data = response.json()
                
                # data es un array, no un dict
                if 'data' in data and isinstance(data['data'], list) and len(data['data']) > 0:
                    segment = data['data'][0]
                    
                    # Extraer el nombre del season
                    acto_premier = segment.get('metadata', {}).get('name', 'Premier')
                    
                    # Las stats están dentro del objeto del segment
                    if 'stats' in segment:
                        stats_premier = segment['stats']
                    else:
                        log_message(f"    [yellow]⚠ {jugador} - No tiene stats en segment[/yellow]", log_viewer)
                        continue
                    
                    # Extraer las mismas stats que en Competitivo
                    datos_principales = {
                        'Jugador': jugador,
                        'Acto': acto_premier,
                        'Damage/Round': stats_premier.get('damagePerRound', {}).get('displayValue'),
                        'K/D Ratio': stats_premier.get('kDRatio', {}).get('displayValue'),
                        'Headshot %': stats_premier.get('headshotsPercentage', {}).get('displayValue'),
                        'KAST': stats_premier.get('kAST', {}).get('displayValue'),
                        'ACS': stats_premier.get('scorePerRound', {}).get('displayValue'),
                        'KAD Ratio': stats_premier.get('kADRatio', {}).get('displayValue'),
                    }
                    
                    # Guardar JSON
                    archivo_nombre = os.path.join(carpeta, f"{jugador}.json")
                    with open(archivo_nombre, 'w') as f:
                        json.dump(datos_principales, f, indent=4)
                    
                    log_message(f"    [green]✓ {jugador}[/green]", log_viewer)
                    count += 1
            
            except Exception as e:
                log_message(f"    [red]✗ {jugador} - Error: {e}[/red]", log_viewer)
        else:
            log_message(f"    [red]✗ {jugador} - Error {response.status_code}[/red]", log_viewer)
    
    return count


def main():
    """Legacy main function for CLI compatibility"""
    headers = {
        'sec-ch-ua-platform': '"Windows"',
        'Referer': 'https://tracker.gg/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'sec-ch-ua': '"Chromium";v="148", "Brave";v="148", "Not/A)Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
    }
    
    # Crear carpeta para los stats si no existe
    carpeta = 'stats_premier'
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    
    print("Obteniendo estadísticas de Premier...\n")
    
    # Leer archivos de stats para obtener season_id_premier
    try:
        archivos_competitivo = [f for f in os.listdir('stats') if f.endswith('.json')]
    except FileNotFoundError:
        print("  ⚠ No se encontró carpeta stats")
        return
    
    for archivo_comp in archivos_competitivo:
        ruta_comp = os.path.join('stats', archivo_comp)
        
        try:
            with open(ruta_comp, 'r') as f:
                datos_comp = json.load(f)
        except Exception as e:
            print(f"  ✗ Error al leer {archivo_comp}: {e}")
            continue
        
        jugador = datos_comp.get('Jugador')
        season_id_premier = datos_comp.get('SeasonIdPremier')
        
        if not jugador or not season_id_premier:
            print(f"  ⚠ {jugador} - No tiene seasonId de Premier")
            continue
        
        print(f"Obteniendo datos de {jugador}...")
        
        # Buscar el nombre completo en nombres.txt
        try:
            with open('nombres.txt', 'r') as f:
                nombres_txt = f.read().strip().split('\n')
            
            nombre_completo = None
            for linea in nombres_txt:
                if linea.strip().startswith(jugador + '#'):
                    nombre_completo = linea.strip()
                    break
            
            if not nombre_completo:
                print(f"  ✗ No se encontró ID para {jugador} en nombres.txt")
                continue
        except FileNotFoundError:
            print(f"  ✗ No se encontró nombres.txt")
            continue
        
        # Hacer petición a /segments/season
        nombre_encoded = quote(nombre_completo)
        url = f'https://api.tracker.gg/api/v2/valorant/standard/profile/riot/{nombre_encoded}/segments/season'
        
        params = {
            'playlist': 'premier',
            'seasonId': season_id_premier,
            'source': 'web',
        }
        
        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code == 200:
            try:
                data = response.json()
                
                # data es un array, no un dict
                if 'data' in data and isinstance(data['data'], list) and len(data['data']) > 0:
                    segment = data['data'][0]
                    
                    # Extraer el nombre del season
                    acto_premier = segment.get('metadata', {}).get('name', 'Premier')
                    
                    # Las stats están dentro del objeto del segment
                    if 'stats' in segment:
                        stats_premier = segment['stats']
                    else:
                        print(f"  ⚠ {jugador} - No tiene stats en segment")
                        continue
                    
                    # Extraer las mismas stats que en Competitivo
                    datos_principales = {
                        'Jugador': jugador,
                        'Acto': acto_premier,
                        'Damage/Round': stats_premier.get('damagePerRound', {}).get('displayValue'),
                        'K/D Ratio': stats_premier.get('kDRatio', {}).get('displayValue'),
                        'Headshot %': stats_premier.get('headshotsPercentage', {}).get('displayValue'),
                        'KAST': stats_premier.get('kAST', {}).get('displayValue'),
                        'ACS': stats_premier.get('scorePerRound', {}).get('displayValue'),
                        'KAD Ratio': stats_premier.get('kADRatio', {}).get('displayValue'),
                    }
                    
                    # Guardar JSON
                    archivo_nombre = os.path.join(carpeta, f"{jugador}.json")
                    with open(archivo_nombre, 'w') as f:
                        json.dump(datos_principales, f, indent=4)
                    
                    print(f"  ✓ {jugador}")
            
            except Exception as e:
                print(f"  ✗ {jugador} - Error: {e}")
        else:
            print(f"  ✗ {jugador} - Error {response.status_code}")
    headers = {
        'sec-ch-ua-platform': '"Windows"',
        'Referer': 'https://tracker.gg/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'sec-ch-ua': '"Chromium";v="148", "Brave";v="148", "Not/A)Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
    }
    
    # Crear carpeta para los stats si no existe
    carpeta = 'stats_premier'
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    
    print("Obteniendo estadísticas de Premier...\n")
    
    # Leer archivos de stats para obtener season_id_premier
    try:
        archivos_competitivo = [f for f in os.listdir('stats') if f.endswith('.json')]
    except FileNotFoundError:
        print("  ⚠ No se encontró carpeta stats")
        return
    
    for archivo_comp in archivos_competitivo:
        ruta_comp = os.path.join('stats', archivo_comp)
        
        try:
            with open(ruta_comp, 'r') as f:
                datos_comp = json.load(f)
        except Exception as e:
            print(f"  ✗ Error al leer {archivo_comp}: {e}")
            continue
        
        jugador = datos_comp.get('Jugador')
        season_id_premier = datos_comp.get('SeasonIdPremier')
        
        if not jugador or not season_id_premier:
            print(f"  ⚠ {jugador} - No tiene seasonId de Premier")
            continue
        
        print(f"Obteniendo datos de {jugador}...")
        
        # Buscar el nombre completo en nombres.txt
        try:
            with open('nombres.txt', 'r') as f:
                nombres_txt = f.read().strip().split('\n')
            
            nombre_completo = None
            for linea in nombres_txt:
                if linea.strip().startswith(jugador + '#'):
                    nombre_completo = linea.strip()
                    break
            
            if not nombre_completo:
                print(f"  ✗ No se encontró ID para {jugador} en nombres.txt")
                continue
        except FileNotFoundError:
            print(f"  ✗ No se encontró nombres.txt")
            continue
        
        # Hacer petición a /segments/season
        nombre_encoded = quote(nombre_completo)
        url = f'https://api.tracker.gg/api/v2/valorant/standard/profile/riot/{nombre_encoded}/segments/season'
        
        params = {
            'playlist': 'premier',
            'seasonId': season_id_premier,
            'source': 'web',
        }
        
        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code == 200:
            try:
                data = response.json()
                
                # data es un array, no un dict
                if 'data' in data and isinstance(data['data'], list) and len(data['data']) > 0:
                    segment = data['data'][0]
                    
                    # Extraer el nombre del season
                    acto_premier = segment.get('metadata', {}).get('name', 'Premier')
                    
                    # Las stats están dentro del objeto del segment
                    if 'stats' in segment:
                        stats_premier = segment['stats']
                    else:
                        print(f"  ⚠ {jugador} - No tiene stats en segment")
                        continue
                    
                    # Extraer las mismas stats que en Competitivo
                    datos_principales = {
                        'Jugador': jugador,
                        'Acto': acto_premier,
                        'Damage/Round': stats_premier.get('damagePerRound', {}).get('displayValue'),
                        'K/D Ratio': stats_premier.get('kDRatio', {}).get('displayValue'),
                        'Headshot %': stats_premier.get('headshotsPercentage', {}).get('displayValue'),
                        'KAST': stats_premier.get('kAST', {}).get('displayValue'),
                        'ACS': stats_premier.get('scorePerRound', {}).get('displayValue'),
                        'KAD Ratio': stats_premier.get('kADRatio', {}).get('displayValue'),
                    }
                    
                    # Guardar JSON
                    archivo_nombre = os.path.join(carpeta, f"{jugador}.json")
                    with open(archivo_nombre, 'w') as f:
                        json.dump(datos_principales, f, indent=4)
                    
                    print(f"  ✓ {jugador}")
            
            except Exception as e:
                print(f"  ✗ {jugador} - Error: {e}")
        else:
            print(f"  ✗ {jugador} - Error {response.status_code}")


if __name__ == '__main__':
    main()