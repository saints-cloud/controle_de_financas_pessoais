import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date

# Importe os modelos, enums e funções do seu projeto
from models import Conta, Historico, Bancos, Tipos
from view import (
    criar_conta,
    listar_contas,
    desativar_conta,
    transferir_saldo,
    movimentar_saldo,
    total_contas,
    buscar_historicos_entre_datas,
    gerar_grafico_historico
)

# Classe principal da aplicação Tkinter
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplicativo Bancário")
        self.geometry("600x400")
        self.create_widgets()

    def create_widgets(self):
        # Cria um frame principal para organizar os botões
        frame = ttk.Frame(self)
        frame.pack(padx=10, pady=10, fill='both', expand=True)

        # Botão para criar conta
        btn_criar = ttk.Button(frame, text="Criar Conta", command=self.abrir_criar_conta)
        btn_criar.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        # Botão para desativar conta
        btn_desativar = ttk.Button(frame, text="Desativar Conta", command=self.abrir_desativar_conta)
        btn_desativar.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

        # Botão para transferir dinheiro
        btn_transferir = ttk.Button(frame, text="Transferir Dinheiro", command=self.abrir_transferir)
        btn_transferir.grid(row=2, column=0, padx=5, pady=5, sticky='ew')

        # Botão para movimentar dinheiro (registrar transação)
        btn_movimentar = ttk.Button(frame, text="Movimentar Dinheiro", command=self.abrir_movimentar)
        btn_movimentar.grid(row=3, column=0, padx=5, pady=5, sticky='ew')

        # Botão para exibir o total de contas
        btn_total = ttk.Button(frame, text="Total de Contas", command=self.mostrar_total_contas)
        btn_total.grid(row=4, column=0, padx=5, pady=5, sticky='ew')

        # Botão para filtrar histórico de transações
        btn_filtrar = ttk.Button(frame, text="Filtrar Histórico", command=self.abrir_filtrar_historico)
        btn_filtrar.grid(row=5, column=0, padx=5, pady=5, sticky='ew')

        # Botão para gerar gráfico (chama função que gera o gráfico)
        btn_grafico = ttk.Button(frame, text="Mostrar Gráfico", command=self.abrir_grafico)
        btn_grafico.grid(row=6, column=0, padx=5, pady=5, sticky='ew')

    def abrir_criar_conta(self):
        """Janela para criação de uma nova conta"""
        window = tk.Toplevel(self)
        window.title("Criar Conta")
        window.geometry("300x300")

        # Seleção do banco (usando Combobox)
        ttk.Label(window, text="Banco:").pack(padx=5, pady=5)
        banco_values = [banco.value for banco in Bancos]
        banco_var = tk.StringVar(window)
        banco_var.set(banco_values[0])
        combo_banco = ttk.Combobox(window, textvariable=banco_var, values=banco_values, state="readonly")
        combo_banco.pack(padx=5, pady=5)

        # Entrada para a agência
        ttk.Label(window, text="Agência:").pack(padx=5, pady=5)
        entry_agencia = ttk.Entry(window)
        entry_agencia.pack(padx=5, pady=5)

        # Entrada para o número da conta
        ttk.Label(window, text="Número:").pack(padx=5, pady=5)
        entry_numero = ttk.Entry(window)
        entry_numero.pack(padx=5, pady=5)

        # Entrada para o saldo inicial
        ttk.Label(window, text="Saldo Inicial:").pack(padx=5, pady=5)
        entry_saldo = ttk.Entry(window)
        entry_saldo.pack(padx=5, pady=5)

        def submit():
            try:
                banco_str = banco_var.get()
                banco_enum = Bancos(banco_str)
                agencia = int(entry_agencia.get())
                numero = int(entry_numero.get())
                saldo = float(entry_saldo.get())
                # Cria o objeto Conta e chama a função de criação
                conta = Conta(banco=banco_enum, agencia=agencia, numero=numero, saldo=saldo)
                resultado = criar_conta(conta)
                messagebox.showinfo("Info", resultado)
                window.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro: {str(e)}")

        ttk.Button(window, text="Criar Conta", command=submit).pack(padx=5, pady=10)

    def abrir_desativar_conta(self):
        """Janela para desativar uma conta com saldo 0"""
        window = tk.Toplevel(self)
        window.title("Desativar Conta")
        window.geometry("300x300")

        contas = listar_contas()
        listbox = tk.Listbox(window)
        for conta in contas:
            # Exibe apenas contas com saldo 0
            if conta['saldo'] == 0:
                listbox.insert(tk.END, f"{conta['id']} - {conta['banco']} - R$ {conta['saldo']}")
        listbox.pack(padx=5, pady=5, fill='both', expand=True)

        def submit():
            try:
                selection = listbox.curselection()
                if not selection:
                    messagebox.showwarning("Aviso", "Selecione uma conta!")
                    return
                item = listbox.get(selection[0])
                conta_id = int(item.split(" - ")[0])
                resultado = desativar_conta(conta_id)
                messagebox.showinfo("Info", resultado)
                window.destroy()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        ttk.Button(window, text="Desativar Conta", command=submit).pack(padx=5, pady=10)

    def abrir_transferir(self):
        """Janela para transferência de dinheiro entre contas"""
        window = tk.Toplevel(self)
        window.title("Transferir Dinheiro")
        window.geometry("300x400")

        contas = listar_contas()

        # Listbox para seleção da conta de origem
        ttk.Label(window, text="Conta Origem:").pack(padx=5, pady=5)
        listbox_origem = tk.Listbox(window)
        for conta in contas:
            listbox_origem.insert(tk.END, f"{conta['id']} - {conta['banco']} - R$ {conta['saldo']}")
        listbox_origem.pack(padx=5, pady=5, fill='both', expand=True)

        # Listbox para seleção da conta de destino
        ttk.Label(window, text="Conta Destino:").pack(padx=5, pady=5)
        listbox_destino = tk.Listbox(window)
        for conta in contas:
            listbox_destino.insert(tk.END, f"{conta['id']} - {conta['banco']} - R$ {conta['saldo']}")
        listbox_destino.pack(padx=5, pady=5, fill='both', expand=True)

        ttk.Label(window, text="Valor para Transferir:").pack(padx=5, pady=5)
        entry_valor = ttk.Entry(window)
        entry_valor.pack(padx=5, pady=5)

        def submit():
            try:
                idx_origem = listbox_origem.curselection()
                idx_destino = listbox_destino.curselection()
                if not idx_origem or not idx_destino:
                    messagebox.showwarning("Aviso", "Selecione as duas contas!")
                    return
                item_origem = listbox_origem.get(idx_origem[0])
                item_destino = listbox_destino.get(idx_destino[0])
                conta_origem = int(item_origem.split(" - ")[0])
                conta_destino = int(item_destino.split(" - ")[0])
                valor = float(entry_valor.get())
                resultado = transferir_saldo(conta_origem, conta_destino, valor)
                messagebox.showinfo("Info", resultado)
                window.destroy()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        ttk.Button(window, text="Transferir", command=submit).pack(padx=5, pady=10)

    def abrir_movimentar(self):
        """Janela para registrar movimentação (transação) em uma conta"""
        window = tk.Toplevel(self)
        window.title("Movimentar Dinheiro")
        window.geometry("300x350")

        contas = listar_contas()
        ttk.Label(window, text="Selecione a Conta:").pack(padx=5, pady=5)
        conta_values = [f"{conta['id']} - {conta['banco']} - R$ {conta['saldo']}" for conta in contas]
        conta_var = tk.StringVar(window)
        combo_conta = ttk.Combobox(window, textvariable=conta_var, values=conta_values, state="readonly")
        combo_conta.pack(padx=5, pady=5)

        ttk.Label(window, text="Valor da Movimentação:").pack(padx=5, pady=5)
        entry_valor = ttk.Entry(window)
        entry_valor.pack(padx=5, pady=5)

        ttk.Label(window, text="Tipo de Movimentação:").pack(padx=5, pady=5)
        tipo_values = [tipo.value for tipo in Tipos]
        tipo_var = tk.StringVar(window)
        combo_tipo = ttk.Combobox(window, textvariable=tipo_var, values=tipo_values, state="readonly")
        combo_tipo.pack(padx=5, pady=5)

        def submit():
            try:
                if not combo_conta.get():
                    messagebox.showwarning("Aviso", "Selecione uma conta!")
                    return
                conta_id = int(combo_conta.get().split(" - ")[0])
                valor = float(entry_valor.get())
                tipo_enum = Tipos(combo_tipo.get())
                # Cria um objeto Historico (a descrição pode ser adicionada conforme necessário)
                historico = Historico(conta_id=conta_id, tipo=tipo_enum, valor=valor, data=date.today(), descricao="")
                resultado = movimentar_saldo(historico)
                messagebox.showinfo("Info", resultado)
                window.destroy()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        ttk.Button(window, text="Registrar Movimentação", command=submit).pack(padx=5, pady=10)

    def mostrar_total_contas(self):
        """Exibe o total (soma dos saldos) de todas as contas cadastradas"""
        try:
            total = total_contas()
            messagebox.showinfo("Total de Contas", f"R$ {total}")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def abrir_filtrar_historico(self):
        """Janela para filtrar o histórico de transações por data"""
        window = tk.Toplevel(self)
        window.title("Filtrar Histórico")
        window.geometry("300x250")

        ttk.Label(window, text="Data de Início (dd/mm/aaaa):").pack(padx=5, pady=5)
        entry_inicio = ttk.Entry(window)
        entry_inicio.pack(padx=5, pady=5)

        ttk.Label(window, text="Data Final (dd/mm/aaaa):").pack(padx=5, pady=5)
        entry_fim = ttk.Entry(window)
        entry_fim.pack(padx=5, pady=5)

        def submit():
            try:
                data_inicio = datetime.strptime(entry_inicio.get(), '%d/%m/%Y').date()
                data_fim = datetime.strptime(entry_fim.get(), '%d/%m/%Y').date()
                historicos = buscar_historicos_entre_datas(data_inicio, data_fim)
                # Exibe os resultados em uma nova janela
                result_window = tk.Toplevel(window)
                result_window.title("Histórico Filtrado")
                result_window.geometry("400x300")
                text = tk.Text(result_window)
                text.pack(fill='both', expand=True)
                for hist in historicos:
                    text.insert(tk.END, f"{hist.valor} - {hist.tipo.value}\n")
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        ttk.Button(window, text="Filtrar", command=submit).pack(padx=5, pady=10)

    def abrir_grafico(self):
        """Chama a função que gera o gráfico e exibe-o (por exemplo, usando matplotlib)"""
        try:
            gerar_grafico_historico()  # Sua função que gera o gráfico
        except Exception as e:
            messagebox.showerror("Erro", str(e))

# Execução da aplicação
if __name__ == "__main__":
    app = App()
    app.mainloop()
