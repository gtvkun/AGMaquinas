# AGMaquinas



# 🧠 Algoritmo Genético para Programação de Manutenção de Máquinas

Este projeto utiliza um Algoritmo Genético (AG) com interface gráfica em Python para otimizar a programação de manutenção de um conjunto de máquinas, assegurando que a demanda de energia seja atendida em todos os intervalos.

## 📌 Objetivo

Determinar o melhor agendamento de manutenção de 7 máquinas ao longo de 4 intervalos de tempo, de forma a:
- Minimizar penalidades por não atender à demanda.
- Evitar sobreposição de manutenções que reduzam a potência total disponível.
- Garantir alta disponibilidade operacional.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- [customtkinter](https://github.com/TomSchimansky/CustomTkinter) – Interface moderna em tkinter
- Algoritmos Genéticos
- Interface Gráfica com visualização dinâmica
- Geração de relatórios em HTML (em desenvolvimento)

---

## ⚙️ Parâmetros do Problema

- **Máquinas:** 7
- **Intervalos de tempo:** 4
- **Capacidade das máquinas (MW):** `[20, 15, 35, 40, 15, 15, 10]`
- **Duração da manutenção (intervalos):** `[2, 2, 1, 1, 1, 1, 1]`
- **Demanda por intervalo (MW):** `[80, 90, 65, 70]`

---

## 🧬 Estrutura do Algoritmo Genético

- **Representação:** Vetor de 7 posições (cada posição indica quando a máquina entra em manutenção)
- **Função de Aptidão:** Média da reserva de potência – penalidades
- **Seleção:** Torneio binário
- **Crossover:** Um ponto
- **Mutação:** Aleatória com verificação de limites
- **Parâmetros configuráveis via interface:**
  - Tamanho da população
  - Número de gerações
  - Taxa de crossover
  - Taxa de mutação

---

## 🖥️ Interface Gráfica

A interface permite:
- Visualização da manutenção em tempo real (cores: verde = operando, vermelho = manutenção)
- Informações por intervalo: demanda, potência parada, total e reserva
- Ajuste dos parâmetros do AG via campos interativos

---

## ▶️ Como Executar

1. Clone este repositório:
   ```bash
   git clone https://github.com/gtvkun/AGMaquinas
   cd nome-do-repo
   ```

2. Instale as dependências:
   ```bash
   pip install customtkinter
   ```

3. Execute o programa:
   ```bash
   python main.py
   ```

---

## 📚 Autor

Desenvolvido por Gustavo Coelho Domingos  
Disciplina: Algoritmos Genéticos  
Professor: Dr. Keiji Yamanaka – FEELT/UFU  
Data: Abril de 2025

---

## 📝 Licença
Livre de Licença