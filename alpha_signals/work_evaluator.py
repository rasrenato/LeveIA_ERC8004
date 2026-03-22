"""
WorkEvaluator - Sistema de Avaliação de Sinais Alpha

Inspirado no ClawWork WorkEvaluator (GPT-5.2 evaluation)
Adaptado para LeveCoin Alpha Signals

Critérios de Avaliação:
1. Direção correta (BUY/SELL vs preço real) → 0.5 pontos
2. Timing (quão cedo o sinal foi dado) → 0.3 pontos
3. Qualidade do reasoning → 0.2 pontos

Score final: 0.0 - 1.0
Payment = score × base_price ($0.10 USDC)
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from pathlib import Path


class WorkEvaluator:
    """
    Avalia qualidade de sinais de trading
    
    Métodos de avaliação:
    1. Auto-eval (pós-mercado): Compara sinal com preço real
    2. LLM-eval (tempo real): GPT avalia qualidade do reasoning
    3. Hybrid: Combina ambos
    """

    def __init__(
        self,
        base_payment: float = 0.10,  # $0.10 USDC por sinal
        max_payment: float = 0.15,   # Máximo com bônus de qualidade
        data_path: Optional[str] = None,
        use_llm_evaluation: bool = False,
        openai_api_key: Optional[str] = None
    ):
        """
        Inicializa WorkEvaluator
        
        Args:
            base_payment: Pagamento base por sinal ($0.10)
            max_payment: Pagamento máximo com bônus ($0.15)
            data_path: Path para salvar avaliações
            use_llm_evaluation: Usar GPT para avaliar reasoning
            openai_api_key: API key para LLM evaluation
        """
        self.base_payment = base_payment
        self.max_payment = max_payment
        self.data_path = data_path or "./data/evaluations"
        self.use_llm_evaluation = use_llm_evaluation
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        
        Path(self.data_path).mkdir(parents=True, exist_ok=True)
        
        # Histórico de avaliações
        self.evaluations: List[Dict] = []
        self._load_history()

    def _load_history(self):
        """Carrega histórico de avaliações"""
        history_path = os.path.join(self.data_path, "evaluations.json")
        if os.path.exists(history_path):
            try:
                with open(history_path, 'r') as f:
                    self.evaluations = json.load(f)
            except:
                self.evaluations = []

    def _save_history(self):
        """Salva histórico de avaliações"""
        history_path = os.path.join(self.data_path, "evaluations.json")
        with open(history_path, 'w') as f:
            json.dump(self.evaluations[-1000:], f, indent=2)  # Últimas 1000

    def evaluate_signal(
        self,
        signal_id: str,
        signal_data: Dict,
        actual_outcome: Optional[Dict] = None,
        llm_score: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Avalia sinal de trading
        
        Args:
            signal_id: ID único do sinal
            signal_data: Dados do sinal (direction, entry, stop, target, reasoning)
            actual_outcome: Resultado real (opcional, para pós-mercado)
                - direction: "UP" ou "DOWN"
                - price_change: % de mudança do preço
                - time_to_target: horas até atingir target
            
            llm_score: Score do LLM (0.0-1.0) para qualidade do reasoning
        
        Returns:
            Dict com score detalhado e payment
        """
        # Inicializar score
        score_breakdown = {
            'direction_score': 0.0,      # 0.5 pontos máx
            'timing_score': 0.0,         # 0.3 pontos máx
            'reasoning_score': 0.0,      # 0.2 pontos máx
            'total_score': 0.0           # 1.0 pontos máx
        }
        
        # 1. Avaliar direção (se temos actual_outcome)
        if actual_outcome:
            score_breakdown['direction_score'] = self._evaluate_direction(
                signal_data,
                actual_outcome
            )
        
        # 2. Avaliar timing (se temos actual_outcome)
        if actual_outcome:
            score_breakdown['timing_score'] = self._evaluate_timing(
                signal_data,
                actual_outcome
            )
        
        # 3. Avaliar reasoning (LLM ou heurística)
        if llm_score is not None and self.use_llm_evaluation:
            score_breakdown['reasoning_score'] = llm_score * 0.2
        else:
            score_breakdown['reasoning_score'] = self._evaluate_reasoning_heuristic(
                signal_data.get('reasoning', '')
            )
        
        # Calcular score total
        score_breakdown['total_score'] = sum(score_breakdown.values())
        
        # Calcular payment
        base_payment = self.base_payment
        bonus = (score_breakdown['total_score'] - 0.5) * 0.10  # Bônus por qualidade
        payment = max(0.0, min(self.max_payment, base_payment + bonus))
        
        # Criar avaliação
        evaluation = {
            'signal_id': signal_id,
            'timestamp': datetime.utcnow().isoformat(),
            'score_breakdown': score_breakdown,
            'payment': payment,
            'base_payment': base_payment,
            'bonus': bonus,
            'has_actual_outcome': actual_outcome is not None,
            'used_llm': llm_score is not None and self.use_llm_evaluation
        }
        
        self.evaluations.append(evaluation)
        self._save_history()
        
        return evaluation

    def _evaluate_direction(
        self,
        signal_data: Dict,
        actual_outcome: Dict
    ) -> float:
        """
        Avalia se a direção estava correta
        
        Score:
        - 0.5: Direção 100% correta
        - 0.25: Parcialmente correta (ex: acertou direção mas não atingiu target)
        - 0.0: Direção errada
        """
        signal_direction = signal_data.get('direction', '').upper()  # "UP" ou "DOWN"
        actual_direction = actual_outcome.get('direction', '').upper()
        
        if signal_direction == actual_direction:
            # Acertou direção
            price_change = actual_outcome.get('price_change', 0)
            
            # Verificar se atingiu target
            target = signal_data.get('target', 0)
            if target and abs(price_change) >= abs(target):
                return 0.5  # Acertou direção + atingiu target
            else:
                return 0.35  # Acertou direção mas não atingiu target
        else:
            # Errou direção
            return 0.0

    def _evaluate_timing(
        self,
        signal_data: Dict,
        actual_outcome: Dict
    ) -> float:
        """
        Avalia timing do sinal
        
        Score:
        - 0.3: Sinal dado com >= 24h de antecedência
        - 0.2: Sinal dado com 12-24h de antecedência
        - 0.1: Sinal dado com < 12h de antecedência
        - 0.0: Sinal atrasado
        """
        time_to_target = actual_outcome.get('time_to_target', None)
        
        if time_to_target is None:
            return 0.15  # Score médio se não temos dados
        
        if time_to_target >= 24:
            return 0.3  # Excelente timing
        elif time_to_target >= 12:
            return 0.2  # Bom timing
        elif time_to_target >= 6:
            return 0.15  # Timing ok
        else:
            return 0.1  # Timing curto

    def _evaluate_reasoning_heuristic(self, reasoning: str) -> float:
        """
        Avalia qualidade do reasoning (heurística sem LLM)
        
        Critérios:
        - Length: >= 100 chars → 0.1 pontos
        - Technical terms: menciona indicadores → 0.05 pontos
        - Risk management: menciona stop/target → 0.05 pontos
        """
        score = 0.0
        
        # Length score (0.1 máx)
        if len(reasoning) >= 200:
            score += 0.1
        elif len(reasoning) >= 100:
            score += 0.07
        elif len(reasoning) >= 50:
            score += 0.05
        
        # Technical terms (0.05 máx)
        tech_terms = ['rsi', 'macd', 'support', 'resistance', 'trend', 
                      'volume', 'fibonacci', 'moving average', 'bollinger']
        reasoning_lower = reasoning.lower()
        if any(term in reasoning_lower for term in tech_terms):
            score += 0.05
        
        # Risk management (0.05 máx)
        if 'stop' in reasoning_lower or 'target' in reasoning_lower:
            score += 0.05
        
        return min(0.2, score)  # Máximo 0.2

    def evaluate_with_llm(self, signal_data: Dict) -> float:
        """
        Avalia reasoning com LLM (GPT-4/5)
        
        Returns:
            Score 0.0-1.0
        """
        if not self.openai_api_key:
            return 0.5  # Score neutro se não tem API key
        
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.openai_api_key)
            
            prompt = f"""
            Avalie a qualidade deste sinal de trading de criptomoedas.
            
            Sinal:
            - Ativo: {signal_data.get('asset', 'BTC')}
            - Direção: {signal_data.get('signal_type', 'BUY')}
            - Entry: {signal_data.get('entry', 'N/A')}
            - Stop Loss: {signal_data.get('stop_loss', 'N/A')}
            - Target: {signal_data.get('target', 'N/A')}
            - Confiança: {signal_data.get('confidence', 0.5)}
            - Reasoning: {signal_data.get('reasoning', 'N/A')}
            
            Critérios de avaliação:
            1. Clarity: O raciocínio é claro e bem estruturado?
            2. Technical analysis: Usa indicadores técnicos relevantes?
            3. Risk management: Define stop loss e target adequados?
            4. Confidence justification: A confiança é justificada pelos dados?
            
            Retorne APENAS um número de 0.0 a 1.0 representando a qualidade geral.
            """
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Você é um avaliador especialista em trading de criptomoedas."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=10,
                temperature=0.1
            )
            
            score_text = response.choices[0].message.content.strip()
            score = float(score_text)
            
            return min(1.0, max(0.0, score))
            
        except Exception as e:
            print(f"⚠️ LLM evaluation failed: {e}")
            return 0.5  # Score neutro em caso de erro

    def get_statistics(self) -> Dict[str, Any]:
        """
        Retorna estatísticas de avaliações
        
        Returns:
            Dict com métricas agregadas
        """
        if not self.evaluations:
            return {
                'total_evaluations': 0,
                'average_score': 0.0,
                'average_payment': 0.0,
                'total_paid': 0.0
            }
        
        total = len(self.evaluations)
        avg_score = sum(e['score_breakdown']['total_score'] for e in self.evaluations) / total
        avg_payment = sum(e['payment'] for e in self.evaluations) / total
        total_paid = sum(e['payment'] for e in self.evaluations)
        
        # Avaliações com outcome real vs apenas LLM
        with_outcome = sum(1 for e in self.evaluations if e['has_actual_outcome'])
        with_llm = sum(1 for e in self.evaluations if e['used_llm'])
        
        return {
            'total_evaluations': total,
            'average_score': round(avg_score, 3),
            'average_payment': round(avg_payment, 4),
            'total_paid': round(total_paid, 4),
            'with_actual_outcome': with_outcome,
            'with_llm_evaluation': with_llm
        }

    def print_statistics(self):
        """Imprime estatísticas formatadas"""
        stats = self.get_statistics()
        
        print("\n" + "="*60)
        print("📊 WORK EVALUATOR STATISTICS")
        print("="*60)
        print(f"📝 Total Evaluations:    {stats['total_evaluations']}")
        print(f"⭐ Average Score:        {stats['average_score']:.3f}")
        print(f"💰 Average Payment:      ${stats['average_payment']:.4f}")
        print(f"💵 Total Paid:           ${stats['total_paid']:.4f}")
        print(f"✅ With Actual Outcome:  {stats['with_actual_outcome']}")
        print(f"🤖 With LLM Evaluation:  {stats['with_llm_evaluation']}")
        print("="*60 + "\n")


# Exemplo de uso
if __name__ == "__main__":
    print("🧪 Testando WorkEvaluator\n")
    
    # Criar evaluator
    evaluator = WorkEvaluator(
        base_payment=0.10,
        max_payment=0.15,
        use_llm_evaluation=False
    )
    
    # Test 1: Sinal bom (com outcome)
    print("="*60)
    print("TEST 1: Sinal bom (acertou direção)")
    print("="*60)
    
    signal_1 = {
        'direction': 'UP',
        'entry': 50000,
        'stop_loss': 49000,
        'target': 52000,
        'reasoning': 'Forte suporte em $49k com divergência positiva no RSI. Volume aumentando nos últimos candles. Alvo de $52k baseado em resistência histórica.'
    }
    
    outcome_1 = {
        'direction': 'UP',
        'price_change': 4.5,  # 4.5% de alta
        'time_to_target': 18  # 18 horas
    }
    
    result_1 = evaluator.evaluate_signal(
        signal_id='signal_test_001',
        signal_data=signal_1,
        actual_outcome=outcome_1
    )
    
    print(f"Score: {result_1['score_breakdown']['total_score']:.3f}")
    print(f"Payment: ${result_1['payment']:.4f}")
    print(f"Breakdown: {json.dumps(result_1['score_breakdown'], indent=2)}\n")
    
    # Test 2: Sinal ruim (errou direção)
    print("="*60)
    print("TEST 2: Sinal ruim (errou direção)")
    print("="*60)
    
    signal_2 = {
        'direction': 'DOWN',
        'entry': 50000,
        'stop_loss': 51000,
        'target': 48000,
        'reasoning': 'Resistência forte em $51k.'
    }
    
    outcome_2 = {
        'direction': 'UP',  # Errou!
        'price_change': 3.0,
        'time_to_target': None
    }
    
    result_2 = evaluator.evaluate_signal(
        signal_id='signal_test_002',
        signal_data=signal_2,
        actual_outcome=outcome_2
    )
    
    print(f"Score: {result_2['score_breakdown']['total_score']:.3f}")
    print(f"Payment: ${result_2['payment']:.4f}")
    print(f"Breakdown: {json.dumps(result_2['score_breakdown'], indent=2)}\n")
    
    # Test 3: Sinal sem outcome (apenas reasoning)
    print("="*60)
    print("TEST 3: Sinal sem outcome (apenas reasoning)")
    print("="*60)
    
    signal_3 = {
        'direction': 'UP',
        'entry': 50000,
        'stop_loss': 49500,
        'target': 51000,
        'reasoning': 'Análise técnica mostra padrão de reversão com MACD cruzando para cima. Volume 30% acima da média. Target baseado em Fibonacci 0.618.'
    }
    
    result_3 = evaluator.evaluate_signal(
        signal_id='signal_test_003',
        signal_data=signal_3,
        actual_outcome=None  # Sem outcome ainda
    )
    
    print(f"Score: {result_3['score_breakdown']['total_score']:.3f}")
    print(f"Payment: ${result_3['payment']:.4f}")
    print(f"Breakdown: {json.dumps(result_3['score_breakdown'], indent=2)}\n")
    
    # Estatísticas finais
    print("="*60)
    print("ESTATÍSTICAS FINAIS")
    print("="*60)
    evaluator.print_statistics()
