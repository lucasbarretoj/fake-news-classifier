import pandas as pd
import pickle
import time
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.utils import resample

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

def carregar_dataset(caminho="dataset.csv"):
    df = pd.read_csv(caminho)
    ok(f"Dataset carregado com {len(df)} amostras")
    print("\nDistribuição original:")
    print(df["Label"].value_counts().to_string())
    return df

def limpar(df):
    antes = len(df)
    df = df.dropna(subset=["Texto", "Label"])
    df = df.drop_duplicates(subset="Texto")
    df = df[df["Texto"].str.split().str.len() >= 5].reset_index(drop=True)

    removidas = antes - len(df)
    ok(f"Limpeza concluída: {len(df)} amostras restantes")
    print(f"  Amostras removidas: {removidas}")
    return df

def balancear(df):
    fake = df[df["Label"] == "Fake"]
    true = df[df["Label"] == "True"]

    menor = min(len(fake), len(true))

    fake_bal = resample(fake, n_samples=menor, random_state=42)
    true_bal = resample(true, n_samples=menor, random_state=42)

    df_bal = pd.concat([fake_bal, true_bal])
    df_bal = df_bal.sample(frac=1, random_state=42).reset_index(drop=True)

    ok("Classes balanceadas com sucesso")
    print(f"  Fake : {len(fake_bal)}")
    print(f"  True : {len(true_bal)}")
    print(f"  Total: {len(df_bal)}")

    return df_bal

def vetorizar(df):
    X = df["Texto"]
    y = df["Label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    ok("Dados divididos em treino e teste")
    print(f"  Treino: {len(X_train)} amostras")
    print(f"  Teste : {len(X_test)} amostras")

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=5000,
        sublinear_tf=True,
        strip_accents="unicode",
        analyzer="word",
        lowercase=True,
        min_df=1,
    )

    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    ok(f"Vetorização TF-IDF concluída com {len(vectorizer.vocabulary_)} termos")

    return vectorizer, X_train_vec, X_test_vec, y_train, y_test

def salvar_dados(vectorizer, X_train_vec, X_test_vec, y_train, y_test):
    with open("vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)

    with open("dados_processados.pkl", "wb") as f:
        pickle.dump({
            "X_train": X_train_vec,
            "X_test": X_test_vec,
            "y_train": y_train,
            "y_test": y_test,
        }, f)

    ok("Arquivos salvos com sucesso")
    print("  vectorizer.pkl        → vetorizador TF-IDF")
    print("  dados_processados.pkl → dados prontos para treino")

def main():
    titulo("Pré-processamento e Vetorização")

    passo(1, "Carregando dataset")
    df = carregar_dataset()

    passo(2, "Limpando dados")
    df = limpar(df)

    passo(3, "Balanceando classes")
    df = balancear(df)

    passo(4, "Vetorizando textos")
    vectorizer, X_train_vec, X_test_vec, y_train, y_test = vetorizar(df)

    passo(5, "Salvando arquivos processados")
    salvar_dados(vectorizer, X_train_vec, X_test_vec, y_train, y_test)

    print(f"\n{VERDE}{NEGRITO}Pré-processamento finalizado com sucesso!{RESET}")
    print(f"{AMARELO}Próximo passo: execute python treinar.py{RESET}\n")

if __name__ == "__main__":
    main()