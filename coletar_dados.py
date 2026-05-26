import os
import time
import pandas as pd

VERDE = "\033[92m"
VERMELHO = "\033[91m"
AMARELO = "\033[93m"
AZUL = "\033[94m"
NEGRITO = "\033[1m"
RESET = "\033[0m"

NUM_RESULTADOS_POR_BUSCA = 300
PISO_POR_CLASSE = 50

def titulo(texto):
    print(f"\n{NEGRITO}{AZUL}{'═' * 55}")
    print(f"  {texto}")
    print(f"{'═' * 55}{RESET}")

def passo(numero, texto):
    print(f"\n{AMARELO}[{numero}] {texto}...{RESET}")
    time.sleep(0.4)

def ok(texto):
    print(f"{VERDE}✔ {texto}{RESET}")

def aviso(texto):
    print(f"{AMARELO}⚠ {texto}{RESET}")

def erro(texto):
    print(f"{VERMELHO}✘ {texto}{RESET}")

try:
    from factcheckexplorer.factcheckexplorer import FactCheckLib
except ImportError:
    passo(0, "Instalando biblioteca factcheckexplorer")
    os.system("pip install git+https://github.com/GONZOsint/factcheckexplorer.git -q")
    from factcheckexplorer.factcheckexplorer import FactCheckLib
    ok("Biblioteca instalada com sucesso")

KEYWORDS = [
    "eleição", "eleições", "Bolsonaro", "Lula", "PT",
    "campanha", "campanha eleitoral", "urna", "urna eletrônica",
    "voto", "fraude", "fraude eleitoral", "TSE",
    "Justiça Eleitoral", "presidente", "governo",
]

FALSO = [
    "falso", "false", "fake", "enganoso", "enganador",
    "distorcido", "errado", "incorrect", "wrong", "untrue",
    "misleading", "partially false", "mostly false",
    "não é bem assim", "não_é_bem_assim", "insustentável",
    "sátira", "sem contexto", "fora de contexto",
    "manipulado", "montagem",
]

VERDADEIRO = [
    "verdadeiro", "true", "correto", "correct", "comprovado",
    "accurate", "real", "mostly true", "partially true",
    "é verdade", "procede", "confirmado", "fato", "verídico",
]

BASE_COMPLEMENTAR = [
    ("O TSE é responsável pela organização das eleições brasileiras", "True"),
    ("O voto no Brasil é secreto e obrigatório para maiores de 18 anos", "True"),
    ("As eleições presidenciais acontecem a cada quatro anos no Brasil", "True"),
    ("O presidente da República é eleito pelo voto direto da população", "True"),
    ("O resultado oficial das eleições é divulgado pela Justiça Eleitoral", "True"),
    ("O segundo turno ocorre quando nenhum candidato atinge maioria absoluta dos votos", "True"),
    ("Eleitores maiores de 70 anos têm voto facultativo no Brasil", "True"),
    ("Analfabetos têm voto facultativo no Brasil", "True"),
    ("Jovens de 16 e 17 anos podem votar de forma facultativa no Brasil", "True"),
    ("A urna eletrônica é utilizada no Brasil desde a década de 1990", "True"),
    ("O título de eleitor identifica o cidadão perante a Justiça Eleitoral", "True"),
    ("O eleitor pode justificar ausência caso não consiga votar", "True"),
    ("As pesquisas eleitorais devem ser registradas na Justiça Eleitoral", "True"),
    ("A propaganda eleitoral possui regras definidas pela legislação brasileira", "True"),
    ("O horário eleitoral gratuito é transmitido no rádio e na televisão", "True"),
    ("Os partidos políticos podem lançar candidatos nas eleições", "True"),
    ("O mesário é convocado pela Justiça Eleitoral para trabalhar no dia da votação", "True"),
    ("As eleições municipais elegem prefeitos e vereadores", "True"),
    ("As eleições gerais elegem presidente, governadores, senadores e deputados", "True"),
    ("O voto é obrigatório para brasileiros alfabetizados entre 18 e 70 anos", "True"),
    ("A Justiça Eleitoral fiscaliza o processo eleitoral brasileiro", "True"),
    ("O eleitor precisa estar regular com a Justiça Eleitoral para votar", "True"),
    ("Municípios com menos de 200 mil eleitores não têm segundo turno para prefeito", "True"),
    ("O mandato do presidente da República no Brasil tem duração de quatro anos", "True"),
    ("Governadores são eleitos pelo voto popular nos estados", "True"),
    ("Prefeitos são eleitos pelo voto popular nos municípios", "True"),
    ("Vereadores são eleitos nas eleições municipais", "True"),
    ("Deputados federais representam a população na Câmara dos Deputados", "True"),
    ("Senadores representam os estados no Senado Federal", "True"),
    ("O Brasil utiliza sistema eletrônico de votação nas eleições", "True"),
    ("O boletim de urna é emitido ao final da votação em cada seção eleitoral", "True"),
    ("A biometria é usada para identificar eleitores em muitas cidades brasileiras", "True"),
    ("A compra de votos é crime eleitoral no Brasil", "True"),
    ("A boca de urna é proibida no dia da votação", "True"),
    ("A prestação de contas de campanha deve ser apresentada à Justiça Eleitoral", "True"),
    ("Os candidatos precisam registrar candidatura na Justiça Eleitoral", "True"),
    ("O voto branco é registrado separadamente dos votos válidos", "True"),
    ("O voto nulo não é considerado voto válido para definir o vencedor", "True"),
    ("Votos válidos excluem votos brancos e nulos", "True"),
    ("A maioria absoluta corresponde a mais da metade dos votos válidos", "True"),
    ("O eleitor deve apresentar documento oficial com foto para votar", "True"),
    ("O e-Título pode ser usado para identificação do eleitor quando possui foto", "True"),
    ("A apuração dos votos é realizada após o encerramento da votação", "True"),
    ("A totalização dos votos consolida os resultados das seções eleitorais", "True"),
    ("A Constituição Federal estabelece o voto direto e secreto", "True"),
    ("O TSE é o órgão máximo da Justiça Eleitoral brasileira", "True"),
    ("Os Tribunais Regionais Eleitorais atuam nos estados", "True"),
    ("A Justiça Eleitoral organiza eleições nacionais, estaduais e municipais", "True"),
    ("O sigilo do voto é protegido pela Constituição Federal", "True"),
    ("A eleição presidencial brasileira pode ser decidida em dois turnos", "True"),

    ("As urnas eletrônicas foram hackeadas por criminosos estrangeiros", "Fake"),
    ("O TSE apagou milhões de votos da oposição", "Fake"),
    ("Militares confirmaram fraude secreta nas urnas eletrônicas", "Fake"),
    ("O resultado da eleição foi alterado antes da divulgação oficial", "Fake"),
    ("As urnas eletrônicas enviam votos pela internet durante a votação", "Fake"),
    ("O sistema eleitoral brasileiro conta votos de eleitores mortos automaticamente", "Fake"),
    ("O STF escolhe diretamente quem será o presidente do Brasil", "Fake"),
    ("O Exército cancelou as eleições brasileiras", "Fake"),
    ("Hackers russos mudaram o resultado das urnas no Brasil", "Fake"),
    ("A urna eletrônica permite descobrir em quem cada eleitor votou", "Fake"),
    ("O voto de quem aperta confirma rápido demais é anulado", "Fake"),
    ("A Justiça Eleitoral proibiu todos os eleitores de votar em determinado candidato", "Fake"),
    ("O TSE colocou votos extras nas urnas durante a madrugada", "Fake"),
    ("As eleições brasileiras são decididas por servidores secretos no exterior", "Fake"),
    ("O eleitor perde o voto se usar roupa amarela no dia da eleição", "Fake"),
    ("A urna eletrônica completa sozinha o voto do eleitor", "Fake"),
    ("O voto branco é transferido automaticamente para o candidato vencedor", "Fake"),
    ("O voto nulo pode cancelar uma eleição presidencial se passar de cinquenta por cento", "Fake"),
    ("O TSE proibiu a fiscalização dos partidos durante a eleição", "Fake"),
    ("As urnas eletrônicas brasileiras foram compradas da Venezuela para fraudar eleições", "Fake"),
    ("Lula comprou votos usando dinheiro público nas eleições", "Fake"),
    ("Bolsonaro venceu a eleição mas teve votos removidos pelo TSE", "Fake"),
    ("O resultado das urnas foi decidido antes da votação começar", "Fake"),
    ("O eleitor que votar nulo terá o voto transferido para o candidato líder", "Fake"),
    ("O TSE controla secretamente todos os votos digitados nas urnas", "Fake"),
    ("A urna eletrônica muda o voto quando o eleitor aperta confirma", "Fake"),
    ("Partidos de oposição foram impedidos de fiscalizar as eleições", "Fake"),
    ("Militares encontraram provas definitivas de fraude nas urnas", "Fake"),
    ("O voto impresso já é obrigatório em todas as eleições brasileiras", "Fake"),
    ("O eleitor precisa levar comprovante de vacinação para votar", "Fake"),
    ("O governo pode descobrir em quem cada pessoa votou", "Fake"),
    ("As urnas brasileiras são conectadas à internet durante a eleição", "Fake"),
    ("O TSE anulou votos de uma região inteira para favorecer um candidato", "Fake"),
    ("O sistema eleitoral permite inserir votos depois do encerramento da votação", "Fake"),
    ("O voto de idosos vale mais que o voto dos outros eleitores", "Fake"),
    ("Eleitores que recebem benefício social são proibidos de votar no Brasil", "Fake"),
    ("O presidente do TSE pode escolher o vencedor da eleição", "Fake"),
    ("A apuração das urnas é feita por empresas estrangeiras sem fiscalização", "Fake"),
    ("O eleitor pode votar pelo WhatsApp nas eleições brasileiras", "Fake"),
    ("A urna eletrônica registra voto automaticamente quando o eleitor demora", "Fake"),
    ("O comprovante de comparecimento mostra em quem o eleitor votou", "Fake"),
    ("A Justiça Eleitoral cancela o voto de quem critica o sistema eleitoral", "Fake"),
    ("O voto em branco sempre vai para o candidato mais votado", "Fake"),
    ("As urnas eletrônicas foram programadas para favorecer partidos específicos", "Fake"),
    ("O eleitor que justificar ausência tem seu voto contado automaticamente", "Fake"),
    ("O TSE proibiu candidatos de oposição de aparecerem na televisão", "Fake"),
    ("A eleição presidencial pode ser cancelada por mensagens nas redes sociais", "Fake"),
    ("O Exército realiza uma contagem secreta paralela dos votos", "Fake"),
    ("A biometria permite saber em qual candidato o eleitor votou", "Fake"),
    ("O sistema eleitoral brasileiro soma votos antes do dia da votação", "Fake"),
]

def mapear_label(verdict):
    if not verdict:
        return None

    v = verdict.lower().strip()

    for f in FALSO:
        if f in v:
            return "Fake"

    for t in VERDADEIRO:
        if t in v:
            return "True"

    return None

def coletar_keyword(keyword):
    registros = []

    try:
        lib = FactCheckLib(keyword, language="pt", num_results=NUM_RESULTADOS_POR_BUSCA)
        raw = lib.fetch_data()

        if not raw:
            return []

        data = lib.clean_json(raw)
        claims = lib.extract_info(data)

        for claim in claims:
            texto = (claim.get("Claim") or "").strip()
            verdict = claim.get("Verdict") or ""
            label = mapear_label(verdict)

            if texto and label and len(texto.split()) >= 5:
                registros.append({"Texto": texto, "Label": label})

    except Exception as e:
        erro(f"Erro ao buscar '{keyword}': {e}")

    return registros

def completar_classe(df_api, label):
    df_classe = df_api[df_api["Label"] == label]

    if len(df_classe) >= PISO_POR_CLASSE:
        return df_classe.sample(n=PISO_POR_CLASSE, random_state=42), 0

    faltam = PISO_POR_CLASSE - len(df_classe)

    df_base = pd.DataFrame(BASE_COMPLEMENTAR, columns=["Texto", "Label"])
    df_base = df_base[df_base["Label"] == label]

    textos_api = set(df_api["Texto"].tolist())
    df_base = df_base[~df_base["Texto"].isin(textos_api)]

    df_complemento = df_base.head(faltam)

    df_final_classe = pd.concat([df_classe, df_complemento], ignore_index=True)

    return df_final_classe, len(df_complemento)

def main():
    titulo("Coleta de Dados")

    passo(1, "Coletando dados da API FactCheckExplorer")

    todos = []

    for kw in KEYWORDS:
        print(f"\n  Buscando palavra-chave: {NEGRITO}{kw}{RESET}")
        dados = coletar_keyword(kw)

        fake_qtd = sum(1 for item in dados if item["Label"] == "Fake")
        true_qtd = sum(1 for item in dados if item["Label"] == "True")

        ok(f"{len(dados)} afirmações encontradas")
        print(f"     Fake: {fake_qtd} | True: {true_qtd}")

        todos.extend(dados)
        time.sleep(1)

    passo(2, "Organizando dados coletados")

    df_api = pd.DataFrame(todos)

    if df_api.empty:
        erro("Nenhum dado foi coletado pela API")
        return

    df_api = df_api.drop_duplicates(subset="Texto")
    df_api = df_api[df_api["Texto"].str.split().str.len() >= 5]
    df_api = df_api.reset_index(drop=True)

    ok(f"Coleta concluída com {len(df_api)} afirmações únicas")

    print("\nDistribuição coletada pela API:")
    print(df_api["Label"].value_counts().to_string())

    passo(3, "Aplicando piso mínimo por classe")

    df_fake, comp_fake = completar_classe(df_api, "Fake")
    df_true, comp_true = completar_classe(df_api, "True")

    if len(df_fake) < PISO_POR_CLASSE or len(df_true) < PISO_POR_CLASSE:
        erro("Não foi possível atingir o piso mínimo de 50 amostras por classe")
        return

    df_final = pd.concat([df_fake, df_true], ignore_index=True)
    df_final = df_final.drop_duplicates(subset="Texto")
    df_final = df_final.sample(frac=1, random_state=42).reset_index(drop=True)

    ok(f"Dataset final criado com {len(df_final)} afirmações")

    print("\nDistribuição final:")
    print(df_final["Label"].value_counts().to_string())

    print(f"\n{AMARELO}Complemento utilizado:{RESET}")
    print(f"  Fake complementadas manualmente: {comp_fake}")
    print(f"  True complementadas manualmente: {comp_true}")

    print(f"\n{AMARELO}Observação:{RESET}")
    print("  A coleta principal foi feita pela API FactCheckExplorer.")
    print("  A base complementar só foi usada quando alguma classe ficou abaixo de 50 exemplos.")
    print("  Isso evita um dataset muito desbalanceado e melhora o treinamento do modelo.")

    passo(4, "Salvando dataset")

    df_final.to_csv("dataset.csv", index=False, encoding="utf-8")

    ok("Dataset salvo como 'dataset.csv'")

    print(f"\n{VERDE}{NEGRITO}Coleta de dados finalizada com sucesso!{RESET}")
    print(f"{AMARELO}Próximo passo: execute python preprocessamento.py{RESET}\n")

if __name__ == "__main__":
    main()