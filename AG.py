import customtkinter
import random

# Dados do problema
NUM_MAQUINAS = 7
CAPACIDADES = [20, 15, 35, 40, 15, 15, 10]
INTERVALOS_MANUTENCAO = [2, 2, 1, 1, 1, 1, 1]
DEMANDAS = [80, 90, 65, 70]
NUM_INTERVALOS = 4

def calcular_reserva(cromossomo):
    # Calcula Reserva de Potência disponível em cada intervalo
    reservas = []
    for intervalo in range(NUM_INTERVALOS):
        demanda = DEMANDAS[intervalo]
        potencia_disponivel = sum(CAPACIDADES)
        for i in range(NUM_MAQUINAS):
            for k in range(INTERVALOS_MANUTENCAO[i]):
                if cromossomo[i] + k == intervalo:
                    potencia_disponivel -= CAPACIDADES[i]
        reserva = potencia_disponivel - demanda
        reservas.append(reserva)
    return reservas

def calcular_parada(cromossomo):
# Soma a capacidade de cada máquina parada por intervalo
    parada_por_intervalo = [0] * NUM_INTERVALOS
    for i in range(NUM_MAQUINAS):
        for k in range(INTERVALOS_MANUTENCAO[i]):
            intv = cromossomo[i] + k
            if intv < NUM_INTERVALOS:
                parada_por_intervalo[intv] += CAPACIDADES[i]
    return parada_por_intervalo

def penalidade(cromossomo):
# Calcula penalidades caso não haja potência suficiente ou manutenção inválida
    reserva = calcular_reserva(cromossomo)
    penalidade_total = 0
    for r in reserva:
        if r < 0:
            penalidade_total += abs(r) * 10        # Penalidade proporcional ao déficit
    for i in [0, 1]:
        if INTERVALOS_MANUTENCAO[i] == 2:
            if cromossomo[i] > NUM_INTERVALOS - 2:
                penalidade_total += 1000           # Penalidade se manutenção extrapola o intervalo
    return penalidade_total

def aptidao(cromossomo):
# Calcula a aptidão como a média da reserva menos a penalidade
    reserva = calcular_reserva(cromossomo)
    media_reserva = min(reserva) / NUM_INTERVALOS
    pen = penalidade(cromossomo)
    return media_reserva - pen

def crossover(pai1, pai2):
# Cruzamento de dois pais para gerar filhos
    ponto = random.randint(1, NUM_MAQUINAS - 1)
    return pai1[:ponto] + pai2[ponto:], pai2[:ponto] + pai1[ponto:]

def mutacao(cromossomo, taxa_mutacao):
    # Aplica mutações aleatórias no cromossomo
    for i in range(NUM_MAQUINAS):
        if random.random() < taxa_mutacao:
            cromossomo[i] = random.randint(0, NUM_INTERVALOS - INTERVALOS_MANUTENCAO[i])
    return cromossomo

def gerar_cromossomo_valido():
    # Gera um cromossomo válido respeitando o limite de intervalos
    return [random.randint(0, NUM_INTERVALOS - INTERVALOS_MANUTENCAO[i]) for i in range(NUM_MAQUINAS)]

def algoritmo_genetico(tamanho_populacao, taxa_crossover, taxa_mutacao, num_geracoes, callback=None):
    # Executa o algoritmo genético principal
    populacao = [gerar_cromossomo_valido() for _ in range(tamanho_populacao)]
    for geracao in range(num_geracoes):
        aptidoes = [aptidao(c) for c in populacao]
        nova_populacao = []

        # Seleção por torneio: compara dois indivíduos aleatórios
        for _ in range(tamanho_populacao):
            ind1, ind2 = random.sample(range(tamanho_populacao), 2)
            vencedor = populacao[ind1] if aptidoes[ind1] > aptidoes[ind2] else populacao[ind2]
            nova_populacao.append(vencedor[:])

        # Cruzamento dos indivíduos
        for i in range(0, tamanho_populacao - 1, 2):
            if random.random() < taxa_crossover:
                nova_populacao[i], nova_populacao[i + 1] = crossover(nova_populacao[i], nova_populacao[i + 1])

        # Mutação dos indivíduos
        for i in range(tamanho_populacao):
            nova_populacao[i] = mutacao(nova_populacao[i], taxa_mutacao)

        populacao = nova_populacao
        melhor = max(populacao, key=aptidao)

     # Atualiza a interface a cada geração, se fornecido
        if callback:
            callback(melhor, geracao + 1)

    # Retorna o melhor cromossomo da população final
    return max(populacao, key=aptidao)

# ---------------- Interface ----------------
class InterfaceAG:
    def __init__(self, root):
        self.root = root
        self.root.title('Programação de Manutenção de Máquinas')
        self.root.geometry("1300x720")
        self.root.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        self.tamanho_populacao = customtkinter.IntVar(value=100)
        self.taxa_crossover = customtkinter.DoubleVar(value=0.8)
        self.taxa_mutacao = customtkinter.DoubleVar(value=0.01)
        self.num_geracoes = customtkinter.IntVar(value=200)

        self.capacidades_entries = []
        self.intervalos_entries = []

        input_frame = customtkinter.CTkFrame(root)
        input_frame.grid(row=0, column=0, columnspan=NUM_INTERVALOS + 2, pady=10)

        customtkinter.CTkLabel(input_frame, text="Tamanho da População:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        customtkinter.CTkEntry(input_frame, textvariable=self.tamanho_populacao, width=80).grid(row=0, column=1, padx=5)

        customtkinter.CTkLabel(input_frame, text="Taxa de Crossover:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        customtkinter.CTkEntry(input_frame, textvariable=self.taxa_crossover, width=80).grid(row=1, column=1, padx=5)

        customtkinter.CTkLabel(input_frame, text="Taxa de Mutação:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        customtkinter.CTkEntry(input_frame, textvariable=self.taxa_mutacao, width=80).grid(row=2, column=1, padx=5)

        customtkinter.CTkLabel(input_frame, text="Número de Gerações:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        customtkinter.CTkEntry(input_frame, textvariable=self.num_geracoes, width=80).grid(row=3, column=1, padx=5)

        customtkinter.CTkButton(input_frame, text="Executar", command=self.executar_ag, fg_color="#007acc", width=120).grid(row=4, column=0, columnspan=2, pady=10)
        customtkinter.CTkButton(input_frame, text="Resetar", command=self.resetar_interface, fg_color="orange", text_color="black", width=120).grid(row=5, column=0, columnspan=2, pady=5)

        self.intervalo_frames = []
        self.maquina_labels = []
        self.info_labels = []

        for i in range(NUM_INTERVALOS):
            frame = customtkinter.CTkFrame(root, corner_radius=8, width=140)
            frame.grid(row=1, column=i + 1, padx=5, pady=5, sticky="n")

            titulo = customtkinter.CTkLabel(frame, text=f"Intervalo {i + 1}", font=("Arial", 16, "bold"))
            titulo.grid(row=0, column=0, pady=5)

            maquina_col = []
            for j in range(NUM_MAQUINAS):
                label = customtkinter.CTkLabel(frame, text=f"Maq {j+1}", width=80, height=25, corner_radius=5)
                label.grid(row=j + 1, column=0, padx=4, pady=3)
                maquina_col.append(label)
            self.maquina_labels.append(maquina_col)

            info = customtkinter.CTkLabel(frame, text="", font=("Arial", 14), justify="left")
            info.grid(row=NUM_MAQUINAS + 2, column=0, pady=5)
            self.info_labels.append(info)

        lateral_frame = customtkinter.CTkFrame(root, corner_radius=8, width=180)
        lateral_frame.grid(row=1, column=NUM_INTERVALOS + 1, padx=10, pady=5, sticky="n")

        customtkinter.CTkLabel(lateral_frame, text="MÁQUINAS", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=5)
        customtkinter.CTkLabel(lateral_frame, text="POTÊNCIA | INTERVALO", font=("Arial", 12)).grid(row=1, column=1, columnspan=2, sticky="w", padx=5)

        for i in range(NUM_MAQUINAS):
            customtkinter.CTkLabel(lateral_frame, text=f"Maq {i+1}").grid(row=i + 2, column=0, padx=5, pady=2, sticky="e")
            cap_var = customtkinter.IntVar(value=CAPACIDADES[i])
            dur_var = customtkinter.IntVar(value=INTERVALOS_MANUTENCAO[i])
            cap_entry = customtkinter.CTkEntry(lateral_frame, textvariable=cap_var, width=40)
            dur_entry = customtkinter.CTkEntry(lateral_frame, textvariable=dur_var, width=40)
            cap_entry.grid(row=i + 2, column=1, padx=2, pady=2, sticky="w")
            dur_entry.grid(row=i + 2, column=2, padx=2, pady=2, sticky="w")
            self.capacidades_entries.append(cap_var)
            self.intervalos_entries.append(dur_var)

        self.aptidao_label = customtkinter.CTkLabel(root, text="Aptidão: -")
        self.aptidao_label.grid(row=NUM_MAQUINAS + 3, column=1, columnspan=NUM_INTERVALOS, pady=5)

        self.geracao_label = customtkinter.CTkLabel(root, text="Geração: -")
        self.geracao_label.grid(row=NUM_MAQUINAS + 4, column=1, columnspan=NUM_INTERVALOS, pady=5)

    def atualizar_interface(self, cromossomo, geracao):
        global CAPACIDADES, INTERVALOS_MANUTENCAO

        for i in range(NUM_MAQUINAS):
            CAPACIDADES[i] = self.capacidades_entries[i].get()
            INTERVALOS_MANUTENCAO[i] = self.intervalos_entries[i].get()

        for i in range(NUM_INTERVALOS):
            for j in range(NUM_MAQUINAS):
                self.maquina_labels[i][j].configure(text=f"Maq {j+1}", bg_color="green")

        for maquina_idx, intervalo in enumerate(cromossomo):
            duracao = INTERVALOS_MANUTENCAO[maquina_idx]
            for k in range(duracao):
                intv = intervalo + k
                if intv < NUM_INTERVALOS:
                    self.maquina_labels[intv][maquina_idx].configure(text=f"Maq {maquina_idx+1}", bg_color="red")

        reservas = calcular_reserva(cromossomo)
        paradas = calcular_parada(cromossomo)
        potencia_total = sum(CAPACIDADES)

        for i in range(NUM_INTERVALOS):
            Pd = DEMANDAS[i]
            Pp = paradas[i]
            Pt = potencia_total
            Pl = reservas[i]
            self.info_labels[i].configure(
                text=f"Pt: {Pt} MW\nPp: {Pp} MW\nPd: {Pd} MW\nPl: {Pl} MW"
            )

        self.aptidao_label.configure(text=f"Aptidão: {aptidao(cromossomo):.2f}")
        self.geracao_label.configure(text=f"Geração: {geracao}")
        self.root.update()

    def executar_ag(self):
        melhor = algoritmo_genetico(
            self.tamanho_populacao.get(),
            self.taxa_crossover.get(),
            self.taxa_mutacao.get(),
            self.num_geracoes.get(),
            callback=self.atualizar_interface
        )
        print("Melhor programação encontrada:", melhor)

    def resetar_interface(self):
        for i in range(NUM_INTERVALOS):
            for j in range(NUM_MAQUINAS):
                self.maquina_labels[i][j].configure(text=f"Maq {j+1}", bg_color="green")

        for info in self.info_labels:
            info.configure(text="")

        self.aptidao_label.configure(text="Aptidão: -")
        self.geracao_label.configure(text="Geração: -")

        for i in range(NUM_MAQUINAS):
            self.capacidades_entries[i].set(CAPACIDADES[i])
            self.intervalos_entries[i].set(INTERVALOS_MANUTENCAO[i])

# Inicialização
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root = customtkinter.CTk()
interface = InterfaceAG(root)
root.mainloop()
