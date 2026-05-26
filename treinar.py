import pickle
import time
from sklearn.naive_bayes import MultinomialNB

VERDE = "\033[92m"
AMARELO = "\033[93m"
AZUL = "\033[94m"
NEGRITO = "\033[1m"
RESET = "\033[0m"

def titulo(texto):
    print(f"\n{NEGRITO}{AZUL}{'═' * 55}")
    print(f"  {texto}")
    print(f"{'═' * 55}{RESET}")

def passo(numero, texto):
    print(f"\n{AMARELO}[{numero}] {texto}...{RESET}")
    time.sleep(0.4)

def ok(texto):
    print(f"{VERDE}✔ {texto}{RESET}")

def carregar_dados(caminho="dados_processados.pkl"):
    with open(caminho, "rb") as f:
        return pickle.load(f)

def salvar_modelo(modelo, caminho="modelo.pkl"):
    with open(caminho, "wb") as f:
        pickle.dump(modelo, f)

def main():
    titulo("Treinamento do Modelo Naive Bayes")

    passo(1, "Carregando dados processados")
    dados = carregar_dados()

    X_train = dados["X_train"]
    y_train = dados["y_train"]

    ok(f"{X_train.shape[0]} amostras de treino carregadas")
    print(f"  Quantidade de termos/vetores: {X_train.shape[1]}")

    print(f"\n{AMARELO}Distribuição das classes no treino:{RESET}")
    print(y_train.value_counts().to_string())

    passo(2, "Criando modelo supervisionado")
    modelo = MultinomialNB()
    ok("Modelo Naive Bayes criado com sucesso")

    print("""
  O Naive Bayes foi escolhido por ser um algoritmo simples,
  rápido e bastante usado em problemas de classificação de texto.
  Ele calcula a probabilidade de uma frase pertencer a cada classe,
  neste caso: Fake ou True.
""")

    passo(3, "Treinando modelo com os dados vetorizados")
    modelo.fit(X_train, y_train)
    ok("Treinamento concluído")

    print("""
  Nesta etapa, o modelo aprendeu padrões presentes nas frases
  do dataset, usando os textos transformados em números pelo TF-IDF.
""")

    passo(4, "Salvando modelo treinado")
    salvar_modelo(modelo)
    ok("Modelo salvo como 'modelo.pkl'")

    print(f"\n{VERDE}{NEGRITO}Treinamento finalizado com sucesso!{RESET}")
    print(f"{AMARELO}Próximo passo: execute python avaliar.py{RESET}\n")

if __name__ == "__main__":
    main()