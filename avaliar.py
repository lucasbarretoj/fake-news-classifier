import pickle
import time
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, classification_report,
)

# ── Cores ─────────────────────────────────────────────────────

VERDE = "\033[92m"
VERMELHO = "\033[91m"
AMARELO = "\033[93m"
AZUL = "\033[94m"
NEGRITO = "\033[1m"
RESET = "\033[0m"

# ── Funções visuais ───────────────────────────────────────────

def titulo(texto):
    print(f"\n{NEGRITO}{AZUL}{'═' * 55}")
    print(f"  {texto}")
    print(f"{'═' * 55}{RESET}")

def passo(numero, texto):
    print(f"\n{AMARELO}[{numero}] {texto}...{RESET}")
    time.sleep(0.4)

def ok(texto):
    print(f"{VERDE}✔ {texto}{RESET}")

# ── Carregar arquivos ────────────────────────────────────────

def carregar_modelo(caminho="modelo.pkl"):
    with open(caminho, "rb") as f:
        return pickle.load(f)

def carregar_vectorizer(caminho="vectorizer.pkl"):
    with open(caminho, "rb") as f:
        return pickle.load(f)

def carregar_dados(caminho="dados_processados.pkl"):
    with open(caminho, "rb") as f:
        return pickle.load(f)

# ── Avaliação ─────────────────────────────────────────────────

def avaliar(modelo, dados):
    y_pred = modelo.predict(dados["X_test"])
    y_test = dados["y_test"]

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, pos_label="Fake")
    rec = recall_score(y_test, y_pred, pos_label="Fake")
    f1 = f1_score(y_test, y_pred, pos_label="Fake")

    titulo("Métricas de Avaliação")

    print(f"""
  {NEGRITO}Accuracy  :{RESET} {VERDE}{acc:.4f} ({acc*100:.1f}%){RESET}
  {NEGRITO}Precision :{RESET} {VERDE}{prec:.4f}{RESET}
  {NEGRITO}Recall    :{RESET} {VERDE}{rec:.4f}{RESET}
  {NEGRITO}F1-Score  :{RESET} {VERDE}{f1:.4f}{RESET}
""")

    titulo("Explicação dos Resultados")

    print(f"""
  O modelo acertou {VERDE}{acc*100:.1f}%{RESET} das amostras de teste.

  A precisão foi de {VERDE}{prec*100:.1f}%{RESET}, ou seja, das notícias que o modelo
  classificou como Fake, essa foi a porcentagem que realmente era Fake.

  O recall foi de {VERDE}{rec*100:.1f}%{RESET}, mostrando que o modelo conseguiu
  encontrar essa porcentagem das notícias Fake presentes no teste.

  O F1-Score foi de {VERDE}{f1:.4f}{RESET}, que representa o equilíbrio entre
  Precision e Recall.
""")

    titulo("Relatório Completo por Classe")
    print(classification_report(y_test, y_pred, target_names=["Fake", "True"]))

    return y_pred

def plotar_matriz_confusao(modelo, dados):
    y_pred = modelo.predict(dados["X_test"])
    y_test = dados["y_test"]

    cm = confusion_matrix(y_test, y_pred, labels=["Fake", "True"])

    titulo("Matriz de Confusão")

    print(f"""
  A matriz de confusão mostra os acertos e erros do modelo:

  - Linha Fake: notícias que realmente eram Fake
  - Linha True: notícias que realmente eram verdadeiras
  - Coluna Fake: notícias previstas como Fake
  - Coluna True: notícias previstas como verdadeiras
""")

    plt.figure(figsize=(7, 5))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=["Fake", "True"],
        yticklabels=["Fake", "True"],
    )

    plt.title("Matriz de Confusão — Naive Bayes", fontsize=14, fontweight="bold")
    plt.ylabel("Valor Real", fontsize=12)
    plt.xlabel("Valor Previsto", fontsize=12)
    plt.tight_layout()
    plt.savefig("matriz_confusao.png", dpi=150)

    ok("Matriz de confusão salva como 'matriz_confusao.png'")
    print(f"{AMARELO}→ Feche a janela do gráfico para continuar a execução.{RESET}")

    plt.show()

def classificar(texto, modelo, vectorizer):
    X = vectorizer.transform([texto])
    predicao = modelo.predict(X)[0]
    probabilidades = modelo.predict_proba(X)[0]
    classes = modelo.classes_

    probs = {c: round(float(p), 4) for c, p in zip(classes, probabilidades)}
    confianca = max(probabilidades)

    return {
        "texto": texto,
        "classificacao": predicao,
        "confianca": f"{confianca*100:.1f}%",
        "probabilidades": probs,
    }

def exibir_classificacao(resultado):
    eh_fake = resultado["classificacao"] == "Fake"
    emoji = "🔴 FAKE" if eh_fake else "🟢 TRUE"
    cor = VERMELHO if eh_fake else VERDE

    print(f"\n  📰 \"{resultado['texto']}\"")
    print(f"     Resultado : {cor}{NEGRITO}{emoji}{RESET}")
    print(f"     Confiança : {resultado['confianca']}")
    print(
        f"     Prob. Fake: {resultado['probabilidades'].get('Fake', 0)*100:.1f}% | "
        f"Prob. True: {resultado['probabilidades'].get('True', 0)*100:.1f}%"
    )

def main():
    titulo("Avaliação e Classificador de Fake News")

    passo(1, "Carregando modelo, vetorizador e dados")
    modelo = carregar_modelo()
    vectorizer = carregar_vectorizer()
    dados = carregar_dados()
    ok(f"{dados['X_test'].shape[0]} amostras de teste carregadas")

    passo(2, "Calculando métricas do modelo")
    avaliar(modelo, dados)

    passo(3, "Gerando matriz de confusão")
    plotar_matriz_confusao(modelo, dados)

    passo(4, "Testando exemplos de classificação")
    titulo("Exemplos de Classificação")

    exemplos = [
        "As urnas eletrônicas foram hackeadas por hackers estrangeiros",
        "O TSE divulgou o resultado oficial das eleições",
        "Lula recebeu dinheiro da Venezuela para financiar sua campanha",
        "O voto no Brasil é secreto e obrigatório para maiores de 18 anos",
        "Militares confirmaram fraude nas urnas em relatório secreto",
    ]

    for exemplo in exemplos:
        resultado = classificar(exemplo, modelo, vectorizer)
        exibir_classificacao(resultado)

    titulo("Classificar Nova Afirmação")
    print(f"{AMARELO}Digite uma afirmação para classificar ou escreva 'sair' para encerrar.{RESET}")

    while True:
        entrada = input(f"\n{NEGRITO}→ {RESET}").strip()

        if entrada.lower() == "sair":
            break

        if len(entrada.split()) < 3:
            print(f"{VERMELHO}Digite uma frase mais completa.{RESET}")
            continue

        resultado = classificar(entrada, modelo, vectorizer)
        exibir_classificacao(resultado)

    print(f"\n{VERDE}{NEGRITO}Execução finalizada com sucesso!{RESET}\n")

if __name__ == "__main__":
    main()