import requests
import time

# Configurações do Injetor de Narrativas - Cabral 🍃
N8N_WEBHOOK_URL = "https://n8n.ialeve.xyz/webhook/market-alert" # Precisaremos criar este nó no seu n8n
CHECK_INTERVAL = 300 # 5 minutos

def get_btc_price():
    try:
        response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
        data = response.json()
        return float(data['price'])
    except Exception as e:
        print(f"Erro ao buscar preço: {e}")
        return None

def monitor_market():
    last_price = get_btc_price()
    print(f"Monitoramento iniciado. Preço base: ${last_price}")
    
    while True:
        current_price = get_btc_price()
        if current_price and last_price:
            change = ((current_price - last_price) / last_price) * 100
            
            # Se o preço oscilar mais de 1.5% em 5 min, disparar alerta
            if abs(change) >= 1.5:
                print(f"ALERTA: Oscilação de {change:.2f}% detectada! Enviando para n8n...")
                # Aqui faremos a chamada para o seu n8n reengajar os leads
                # requests.post(N8N_WEBHOOK_URL, json={"price": current_price, "change": change})
                last_price = current_price
                
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_market()
