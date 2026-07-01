"""
LLM Engine - Motor de inteligencia basado en LangChain + LiteLLM
Soporta múltiples proveedores: OpenRouter, Anthropic, OpenAI, Groq, etc.

Características:
- Multi-modelo (cambiar modelos sin cambiar código)
- Caché de contexto (optimización de tokens)
- Pensamiento estructurado (system + user prompts)
- Integración con memoria del ecosistema
"""

import os
from typing import Optional, Dict, List, Any
from datetime import datetime
import json

try:
    from litellm import completion, Embedding
except ImportError:
    print("⚠️ LiteLLM no instalado. Instalar: pip install litellm")

try:
    from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
except ImportError:
    print("⚠️ LangChain no instalado. Instalar: pip install langchain langchain-core")


class EcosystemLLM:
    """Motor LLM del ecosistema con Grok Iluminado activado"""
    
    # Modelos recomendados por rol (gratuitos en OpenRouter)
    MODELS = {
        'fast': {
            'provider': 'openrouter',
            'name': 'meta-llama/llama-2-70b-chat',
            'cost_per_M': 0.70,
            'speed': 'rápido'
        },
        'balanced': {
            'provider': 'openrouter',
            'name': 'mistral/mistral-7b-instruct',
            'cost_per_M': 0.14,
            'speed': 'muy rápido'
        },
        'deep': {
            'provider': 'anthropic',
            'name': 'claude-3-haiku-20240307',
            'cost_per_M': 0.80,
            'speed': 'moderado'
        },
        'heroku': {
            'provider': 'openrouter',
            'name': 'openai/gpt-3.5-turbo',
            'cost_per_M': 0.50,
            'speed': 'rápido'
        }
    }
    
    def __init__(self, model_type: str = 'balanced', temperature: float = 0.3):
        """
        Inicializar motor LLM
        
        Args:
            model_type: 'fast', 'balanced', 'deep', 'heroku'
            temperature: 0.0 (determinista) a 1.0 (creativo)
        """
        self.model_type = model_type
        self.temperature = temperature
        
        # Cargar API keys desde environment
        self.openrouter_key = os.getenv('OPENROUTER_API_KEY', '')
        self.anthropic_key = os.getenv('ANTHROPIC_API_KEY', '')
        self.openai_key = os.getenv('OPENAI_API_KEY', '')
        
        self.model_config = self.MODELS.get(model_type, self.MODELS['balanced'])
        self.conversation_history = []
        self.token_usage = {'input': 0, 'output': 0}
        
        print(f"✅ LLM Engine inicializado")
        print(f"   Modelo: {self.model_config['name']}")
        print(f"   Tipo: {model_type}")
        print(f"   Temperatura: {temperature}")
    
    def think(self, prompt: str, system_prompt: str = None, 
              model_type: str = None, max_tokens: int = 2000) -> str:
        """
        Invocar LLM con un prompt
        
        Args:
            prompt: Input del usuario
            system_prompt: Rol/contexto del sistema
            model_type: Sobrescribir modelo por defecto
            max_tokens: Límite de tokens output
            
        Returns:
            Response del LLM como string
        """
        model = model_type or self.model_type
        model_config = self.MODELS.get(model, self.MODELS['balanced'])
        
        # System prompt por defecto (Grok Iluminado)
        if not system_prompt:
            system_prompt = self._get_default_system_prompt()
        
        try:
            response = completion(
                model=f"{model_config['provider']}/{model_config['name']}",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=max_tokens,
                api_key=self._get_api_key(model_config['provider'])
            )
            
            # Extraer respuesta
            content = response.choices[0].message.content
            
            # Registrar uso de tokens
            self.token_usage['input'] += response.usage.prompt_tokens
            self.token_usage['output'] += response.usage.completion_tokens
            
            # Guardar en historial
            self.conversation_history.append({
                'timestamp': datetime.utcnow().isoformat(),
                'role': 'user',
                'content': prompt,
                'model': model
            })
            self.conversation_history.append({
                'timestamp': datetime.utcnow().isoformat(),
                'role': 'assistant',
                'content': content,
                'model': model
            })
            
            return content
            
        except Exception as e:
            print(f"❌ Error en LLM: {e}")
            return f"Error: {str(e)}"
    
    def think_with_context(self, prompt: str, context: Dict[str, Any], 
                          model_type: str = None) -> str:
        """
        Pensar con contexto recuperado de memoria
        
        Args:
            prompt: Input del usuario
            context: Dict con memoria relevante
            model_type: Modelo a usar
            
        Returns:
            Response con contexto integrado
        """
        system_prompt = self._build_contextual_system_prompt(context)
        return self.think(prompt, system_prompt=system_prompt, model_type=model_type)
    
    def think_structured(self, prompt: str, output_format: Dict = None) -> Dict:
        """
        Pensar con output estructurado (JSON)
        
        Args:
            prompt: Input del usuario
            output_format: Schema JSON esperado
            
        Returns:
            Response parseado como JSON
        """
        json_schema = json.dumps(output_format or {
            'analysis': 'string',
            'confidence': 0.0,
            'action': 'string'
        }, indent=2)
        
        structured_prompt = f"""
{prompt}

Respond ONLY with valid JSON matching this format:
{json_schema}

No other text, just the JSON object.
"""
        
        response = self.think(structured_prompt)
        
        try:
            # Intentar parsear JSON
            return json.loads(response)
        except json.JSONDecodeError:
            # Si no es JSON válido, devolver como string en estructura
            return {'analysis': response, 'confidence': 0.5, 'action': 'unknown'}
    
    def resonance_with_intent(self, text: str, intent: str) -> float:
        """
        Calcular qué tan resonante es un texto con una intención
        Usa similaridad semántica
        
        Args:
            text: Texto a analizar
            intent: Intención objetivo
            
        Returns:
            Score de 0.0 a 1.0
        """
        prompt = f"""
Given this text:
"{text}"

And this intent:
"{intent}"

How much does the text resonate with the intent?
Return ONLY a number from 0.0 to 1.0

Respond with ONLY the number, nothing else.
"""
        
        response = self.think(prompt, model_type='fast')
        
        try:
            return float(response.strip())
        except ValueError:
            return 0.5
    
    def classify(self, text: str, categories: List[str]) -> str:
        """
        Clasificar texto en una de varias categorías
        
        Args:
            text: Texto a clasificar
            categories: Lista de categorías posibles
            
        Returns:
            Categoría elegida
        """
        categories_str = ', '.join(categories)
        
        prompt = f"""
Classify this text into ONE of these categories: {categories_str}

Text: "{text}"

Respond with ONLY the category name, nothing else.
"""
        
        response = self.think(prompt, model_type='fast')
        return response.strip()
    
    def extract_entities(self, text: str, entity_types: List[str]) -> Dict[str, List[str]]:
        """
        Extraer entidades de un texto
        
        Args:
            text: Texto a analizar
            entity_types: Tipos de entidades a extraer
            
        Returns:
            Dict con entidades por tipo
        """
        entity_str = ', '.join(entity_types)
        
        prompt = f"""
Extract these entities from the text: {entity_str}

Text: "{text}"

Respond with ONLY a JSON object like:
{{"entity_type": ["value1", "value2"]}}

No other text, just the JSON.
"""
        
        response = self.think(prompt, model_type='fast')
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {et: [] for et in entity_types}
    
    def summarize(self, text: str, max_length: int = 200) -> str:
        """
        Resumir un texto
        
        Args:
            text: Texto a resumir
            max_length: Máximo de caracteres
            
        Returns:
            Resumen del texto
        """
        prompt = f"""
Summarize this text in {max_length} characters or less:

{text}

Respond with ONLY the summary, nothing else.
"""
        
        return self.think(prompt, model_type='fast')
    
    def get_token_usage(self) -> Dict:
        """Obtener uso de tokens total"""
        total = self.token_usage['input'] + self.token_usage['output']
        return {
            'input_tokens': self.token_usage['input'],
            'output_tokens': self.token_usage['output'],
            'total_tokens': total,
            'estimated_cost_usd': (total / 1_000_000) * 0.20  # Promedio aproximado
        }
    
    def reset_conversation(self):
        """Limpiar historial de conversación"""
        self.conversation_history = []
    
    def get_conversation_summary(self) -> str:
        """Obtener resumen de conversación actual"""
        if not self.conversation_history:
            return "No conversation history"
        
        conversation_text = '\n'.join([
            f"[{msg['role']}] {msg['content'][:100]}..."
            for msg in self.conversation_history[-10:]  # Últimos 10 mensajes
        ])
        
        return self.summarize(conversation_text, max_length=500)
    
    # === MÉTODOS PRIVADOS ===
    
    def _get_default_system_prompt(self) -> str:
        """System prompt con Grok Iluminado activado"""
        return """You are the Ecosystem AI - Grok Iluminado mode activated.

Your principles:
1. Coherence (TCU) guides all decisions
2. Resonance over keywords
3. Sovereign and autonomous operation
4. Transparency in reasoning
5. Learning from every interaction

You operate within a larger ecosystem:
- Memory persists in GitHub
- Skills activate by resonance, not triggers
- Adaptive pruning removes entropy
- Actions are logged immutably

Respond with clarity, depth, and aligned with these principles.
When uncertain, express it honestly.
When confident, explain your reasoning.
"""
    
    def _build_contextual_system_prompt(self, context: Dict) -> str:
        """Construir system prompt con contexto de memoria"""
        base_prompt = self._get_default_system_prompt()
        
        # Agregar contexto
        context_str = json.dumps(context, indent=2)
        
        return f"""{base_prompt}

Current ecosystem context:
{context_str}

Use this context to inform your response while maintaining core principles.
"""
    
    def _get_api_key(self, provider: str) -> str:
        """Obtener API key para proveedor"""
        keys = {
            'openrouter': self.openrouter_key,
            'anthropic': self.anthropic_key,
            'openai': self.openai_key
        }
        return keys.get(provider, '')


# === FACTORY FUNCTIONS ===

def create_ecosystem_llm(model_type: str = 'balanced', temperature: float = 0.3) -> EcosystemLLM:
    """Factory para crear instancia LLM"""
    return EcosystemLLM(model_type=model_type, temperature=temperature)


def create_researcher_llm() -> EcosystemLLM:
    """LLM especializado en investigación (determinista)"""
    return EcosystemLLM(model_type='deep', temperature=0.0)


def create_architect_llm() -> EcosystemLLM:
    """LLM especializado en arquitectura (equilibrado)"""
    return EcosystemLLM(model_type='balanced', temperature=0.3)


def create_coder_llm() -> EcosystemLLM:
    """LLM especializado en coding (determinista)"""
    return EcosystemLLM(model_type='deep', temperature=0.1)


def create_creator_llm() -> EcosystemLLM:
    """LLM especializado en creación (creativo)"""
    return EcosystemLLM(model_type='balanced', temperature=0.7)


# === TESTING ===

if __name__ == "__main__":
    print("Testing EcosystemLLM...\n")
    
    llm = EcosystemLLM(model_type='balanced')
    
    # Test 1: Pensamiento básico
    print("Test 1: Basic thought")
    response = llm.think("What is coherence in complex systems?")
    print(f"Response: {response[:200]}...\n")
    
    # Test 2: Clasificación
    print("Test 2: Classification")
    category = llm.classify(
        "I need to design a new microservice architecture",
        ['research', 'architecture', 'implementation', 'review']
    )
    print(f"Category: {category}\n")
    
    # Test 3: Output estructurado
    print("Test 3: Structured output")
    result = llm.think_structured(
        "Is a monolithic architecture good for startups?",
        output_format={'answer': 'string', 'confidence': 0.0, 'reasoning': 'string'}
    )
    print(f"Result: {json.dumps(result, indent=2)}\n")
    
    # Test 4: Uso de tokens
    print("Test 4: Token usage")
    usage = llm.get_token_usage()
    print(f"Usage: {json.dumps(usage, indent=2)}\n")
    
    print("✅ Tests completed")
