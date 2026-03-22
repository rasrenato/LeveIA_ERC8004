"""
API Server - Alpha Signals Backend
Expõe dados do EconomicTracker + Blockchain + Aster-MCP via REST API
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
sys.path.insert(0, '/root/openclaw')

from alpha_signals.economic_tracker import EconomicTracker
from alpha_signals.blockchain_api import get_contract_info, get_all_audits, check_connection
from alpha_signals.aster_api import get_aster_api, AsterAPI

app = Flask(__name__)
CORS(app)

# Economic Tracker singleton
tracker = EconomicTracker(initial_balance=100.0)

# Aster API singleton (NOSSA API, modo TEST por padrão)
aster_api: AsterAPI = get_aster_api(mode="TEST")

@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'ok',
        'blockchain_connected': check_connection()
    })

@app.route('/api/alpha-signals/status', methods=['GET'])
def get_status():
    """Obter status econômico do agente"""
    agent_id = request.args.get('agent', 'default')
    
    # Usar EconomicTracker real
    status = tracker.get_status()
    
    # Adicionar campos extras
    status['agent_id'] = agent_id
    status['signals_generated'] = 125  # Mock
    status['avg_score'] = 0.783  # Mock
    status['win_rate'] = 67.5  # Mock
    
    return jsonify(status)

@app.route('/api/alpha-signals/leaderboard', methods=['GET'])
def get_leaderboard():
    """Leaderboard de agentes"""
    limit = int(request.args.get('limit', 10))
    
    # Mock data
    leaderboard = [
        {'agent_id': 'alpha-001', 'agent_name': 'Alpha Wolf', 'balance': 145.30, 'revenue': 45.30, 'win_rate': 78.5, 'avg_score': 0.856, 'status': 'thriving', 'survival_days': 12},
        {'agent_id': 'alpha-002', 'agent_name': 'Crypto King', 'balance': 132.80, 'revenue': 32.80, 'win_rate': 72.3, 'avg_score': 0.798, 'status': 'thriving', 'survival_days': 10},
        {'agent_id': 'alpha-003', 'agent_name': 'Signal Master', 'balance': 98.75, 'revenue': 12.50, 'win_rate': 67.5, 'avg_score': 0.783, 'status': 'thriving', 'survival_days': 5},
        {'agent_id': 'alpha-004', 'agent_name': 'BTC Hunter', 'balance': 45.20, 'revenue': 5.20, 'win_rate': 45.2, 'avg_score': 0.512, 'status': 'struggling', 'survival_days': 3},
        {'agent_id': 'alpha-005', 'agent_name': 'ETH Trader', 'balance': 18.50, 'revenue': 2.50, 'win_rate': 38.7, 'avg_score': 0.423, 'status': 'critical', 'survival_days': 2},
    ]
    
    return jsonify(leaderboard[:limit])

@app.route('/api/alpha-signals/signals', methods=['GET'])
def get_signals():
    """Sinais recentes do banco PostgreSQL com preço atual e status"""
    import psycopg2
    from decimal import Decimal
    import json
    import requests
    from datetime import datetime, timedelta
    
    limit = int(request.args.get('limit', 20))
    
    # Obter preços atuais da Binance
    def get_current_price(symbol):
        try:
            binance_symbol = symbol.replace('/', '').replace('USDT', 'USDT')
            resp = requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol={binance_symbol}', timeout=5)
            if resp.status_code == 200:
                return float(resp.json()['price'])
        except:
            pass
        return None
    
    try:
        # Conectar no banco
        conn = psycopg2.connect(
            host='127.0.0.1',
            port=5432,
            database='leveclaw',
            user='leveclaw_user',
            password='leveclaw_password'
        )
        cursor = conn.cursor()
        
        # Buscar sinais
        cursor.execute("""
            SELECT id, symbol, direction, entry_min, entry_max, targets, 
                   stop_loss, confidence, status, created_at, analysis
            FROM alpha_signals
            ORDER BY created_at DESC
            LIMIT %s
        """, (limit,))
        
        rows = cursor.fetchall()
        
        signals = []
        now = datetime.utcnow()
        
        for row in rows:
            signal_id = str(row[0])
            symbol = row[1]
            direction = row[2]
            entry_min = float(row[3]) if row[3] else 0
            entry_max = float(row[4]) if row[4] else 0
            targets = row[5] if isinstance(row[5], list) else json.loads(row[5]) if row[5] else []
            stop_loss = float(row[6]) if row[6] else 0
            confidence = row[7]
            db_status = row[8]
            created_at = row[9]
            analysis = row[10]
            
            # Calcular validade (7 dias)
            expires_at = created_at + timedelta(days=7) if created_at else None
            is_expired = expires_at < now if expires_at else False
            
            # Obter preço atual
            current_price = get_current_price(symbol)
            
            # Calcular distância da entrada
            entry_avg = (entry_min + entry_max) / 2 if entry_min and entry_max else 0
            distance_pct = None
            if current_price and entry_avg:
                if direction == 'LONG':
                    distance_pct = ((current_price - entry_avg) / entry_avg) * 100
                else:  # SHORT
                    distance_pct = ((entry_avg - current_price) / entry_avg) * 100
            
            # Determinar status final
            if is_expired:
                final_status = 'expired'
            elif db_status == 'LOSS':
                final_status = 'loss'
            elif db_status == 'WIN':
                final_status = 'win'
            else:
                final_status = 'active'
            
            signals.append({
                'id': signal_id,
                'symbol': symbol,
                'direction': direction,
                'entry_min': entry_min,
                'entry_max': entry_max,
                'entry_avg': entry_avg,
                'current_price': current_price,
                'distance_from_entry_pct': round(distance_pct, 2) if distance_pct else None,
                'targets': targets,
                'stop_loss': stop_loss,
                'confidence': confidence,
                'status': final_status,
                'db_status': db_status,
                'created_at': created_at.isoformat() if created_at else None,
                'expires_at': expires_at.isoformat() if expires_at else None,
                'is_expired': is_expired,
                'analysis': analysis
            })
        
        cursor.close()
        conn.close()
        
        return jsonify(signals)
        
    except Exception as e:
        print(f"Erro ao buscar sinais: {e}")
        return jsonify([])

@app.route('/api/blockchain/info', methods=['GET'])
def blockchain_info():
    """Informações do contrato blockchain"""
    info = get_contract_info()
    return jsonify(info)

@app.route('/api/blockchain/audits', methods=['GET'])
def blockchain_audits():
    """Audits do contrato"""
    limit = int(request.args.get('limit', 100))
    audits = get_all_audits(limit=limit)
    return jsonify(audits)

@app.route('/api/agent/decide', methods=['POST'])
def decide_activity():
    """Decidir atividade (work/learn)"""
    data = request.json
    activity = data.get('activity', 'work')
    reasoning = data.get('reasoning', '')
    
    # Mock response
    return jsonify({
        'success': True,
        'activity': activity,
        'reasoning': reasoning,
        'message': f'Activity {activity} accepted'
    })

@app.route('/api/agent/submit', methods=['POST'])
def submit_signal():
    """Submeter sinal"""
    data = request.json
    
    # Mock response
    return jsonify({
        'success': True,
        'signal_id': 'sig-' + str(len(data)),
        'message': 'Signal submitted for evaluation'
    })


@app.route('/api/aster/execute', methods=['POST'])
def execute_signal_aster():
    """
    Executar sinal via NOSSA API Aster
    
    Payload:
    {
        "user_id": "user123",  # ID do usuário
        "asset": "BTCUSDT",
        "direction": "UP",  # ou "DOWN"
        "size": 0.01  # Tamanho da ordem em USDC
    }
    """
    try:
        data = request.json
        
        # Validar payload
        required_fields = ['user_id', 'asset', 'direction', 'size']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Campo requerido: {field}'
                }), 400
        
        # Converter direção para side da ordem
        side = "BUY" if data.get("direction") == "UP" else "SELL"
        
        # Executar ordem via NOSSA API Aster
        order = aster_api.execute_order(
            user_id=data['user_id'],
            symbol=data['asset'],
            side=side,
            size=float(data['size'])
        )
        
        if order.status == "FILLED":
            return jsonify({
                'success': True,
                'message': 'Ordem executada com sucesso',
                'data': {
                    'order_id': order.id,
                    'symbol': order.symbol,
                    'side': order.side,
                    'size': order.size,
                    'filled_price': order.filled_price,
                    'status': order.status,
                    'filled_at': order.filled_at
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': order.error or f'Ordem {order.status}'
            }), 400
            
    except Exception as e:
        logger.error(f"Erro na execução Aster API: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/aster/status', methods=['GET'])
def aster_status():
    """Status da NOSSA API Aster"""
    try:
        user_id = request.args.get('user_id', 'demo')
        status = aster_api.get_account_status(user_id)
        
        return jsonify({
            'success': True,
            'mode': status['mode'],
            'balance': status['balance'],
            'equity': status['equity'],
            'unrealized_pnl': status['unrealized_pnl'],
            'positions': status['positions']
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/aster/history', methods=['GET'])
def aster_history():
    """Histórico de execuções do usuário"""
    try:
        user_id = request.args.get('user_id')
        limit = int(request.args.get('limit', 100))
        
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'user_id requerido'
            }), 400
        
        history = aster_api.get_execution_history(user_id, limit)
        
        return jsonify({
            'success': True,
            'count': len(history),
            'executions': history
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("=== STARTING ALPHA SIGNALS API SERVER ===")
    print("Port: 5000")
    print("Endpoints:")
    print("  GET  /api/health")
    print("  GET  /api/alpha-signals/status")
    print("  GET  /api/alpha-signals/leaderboard")
    print("  GET  /api/alpha-signals/signals")
    print("  GET  /api/blockchain/info")
    print("  GET  /api/blockchain/audits")
    print("  POST /api/agent/decide")
    print("  POST /api/agent/submit")
    print("")
    
    app.run(host='0.0.0.0', port=5000, debug=False)
