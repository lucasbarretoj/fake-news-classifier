# Classificador de Fake News — Naive Bayes

**Disciplina:** Machine Learning

---

## Integrantes do Grupo

| Pessoa | Nome | Responsabilidade |
|--------|------|-----------------|
| 1 | Lucas de Jesus Barreto | Coleta e preparação do dataset |
| 2 | Giovanna Salomão Rodrigues | Pré-processamento e vetorização |
| 3 | Franklin Ferreira dos Santos | Treinamento do modelo |
| 4 | Lucas Silva Oliveira | Avaliação, métricas e classificador |

---

## Como o Dataset Foi Preparado

Os dados foram coletados utilizando a biblioteca [factcheckexplorer](https://github.com/GONZOsint/factcheckexplorer/), que acessa o Google Fact Check Explorer — base de afirmações verificadas por fact-checkers reconhecidos (Agência Lupa, Aos Fatos, Boatos.org, entre outros).

**Palavras-chave utilizadas:**
```
eleição, Bolsonaro, lula, pt, campanha, urna, voto, fraude
```

**Pipeline de coleta:**
1. Para cada palavra-chave, a biblioteca consulta a API com `language=pt` e `num_results=100`
2. Cada afirmação retornada possui um campo Verdict. Exemplo: “Falso”; “Enganoso”; “Distorcido”; “Verdadeiro”
3. Os vereditos foram mapeados para duas classes — **Fake** ou **True**
4. Afirmações com vereditos inconclusivos, textos muito curtos ou duplicados foram descartadas.
5. Durante os testes, observamos que a API retornava uma quantidade muito maior de afirmações classificadas como Fake do que True.
6. Para evitar um dataset extremamente desbalanceado, foi definido um piso mínimo de 50 amostras por classe.
7. Quando a API não retornava exemplos suficientes para determinada classe, o sistema utilizava automaticamente uma base complementar de afirmações eleitorais para balanceamento do dataset.

A coleta principal do projeto continua sendo feita pela API FactCheckExplorer. A base complementar foi utilizada apenas como apoio técnico para balanceamento das classes e melhoria do treinamento do modelo.

O dataset final (`dataset.csv`) contém afirmações eleitorais classificadas entre Fake ou True.

---

## Algoritmo Utilizado

**Naive Bayes Multinomial (MultinomialNB)**

Escolhido por ser um dos algoritmos mais eficazes para classificação de texto:
- Assume independência condicional entre palavras dado a classe
- Trabalha naturalmente com frequências de termos (TF-IDF)
- Rápido para treinar e classificar, mesmo com vocabulários grandes
- Robusto com datasets pequenos

---

## Como Foi Realizado o Treinamento

Pipeline em dois estágios:

**1. Vetorização TF-IDF** (`preprocessamento.py`)
- `ngram_range=(1, 2)` — unigramas e bigramas
- `max_features=5000` — top 5000 termos mais informativos
- `sublinear_tf=True` — aplica `log(tf)` para suavizar termos muito frequentes
- Vetorizador treinado **somente nos dados de treino** para evitar data leakage

**2. Naive Bayes Multinomial** (`treinar.py`)
- `alpha=1.0` — suavização de Laplace
- Divisão **80% treino / 20% teste**, estratificada

---

## Métricas de Avaliação

As métricas abaixo são geradas ao executar `avaliar.py`:

| Métrica | Descrição |
|---------|-----------|
| **Accuracy** | Proporção total de classificações corretas |
| **Precision** | Das classificadas como Fake, quantas realmente eram Fake |
| **Recall** | De todas as Fake reais, quantas o modelo identificou |
| **F1-Score** | Equilíbrio entre Precision e Recall |

A **Matriz de Confusão** é gerada e salva como `matriz_confusao.png`.

---

## Estrutura do Repositório

```
fake-news-classifier/
├── coletar_dados.py      # coleta do dataset
├── preprocessamento.py   # limpeza e vetorização TF-IDF
├── treinar.py            # treinamento do Naive Bayes
├── avaliar.py            # métricas e classificador final
├── dataset.csv           # Dataset com afirmações eleitorais verificadas
└── README.md             # Este arquivo
```

---

## Como Executar (em ordem)

```bash
# 1. Instalar dependências
pip install pandas scikit-learn matplotlib seaborn requests

# 2. Coletar dados
python coletar_dados.py

# 3. Pré-processar e vetorizar
python preprocessamento.py

# 4. Treinar o modelo
python treinar.py

# 5. Avaliar e classificar
python avaliar.py
```

---

## Exemplo de Uso do Classificador

Ao executar `avaliar.py`, após exibir as métricas e os exemplos, o programa entra em modo interativo onde você pode digitar qualquer afirmação e receber a classificação:

```
→ As urnas eletrônicas foram hackeadas por hackers estrangeiros
   Resultado  : 🔴 FAKE  (confiança: 76.6%)

→ O TSE divulgou o resultado oficial das eleições
   Resultado  : 🟢 VERDADEIRA  (confiança: 67.0%)
```

---

## Observação Importante

O modelo não realiza verificação factual em tempo real e não consulta a internet durante a classificação.

Ele apenas identifica padrões estatísticos aprendidos durante o treinamento com base no dataset utilizado.

Por isso, os resultados devem ser interpretados como uma classificação baseada em aprendizado de máquina, e não como uma validação factual definitiva.