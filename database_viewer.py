import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """Cria uma conexão com o banco de dados SQLite especificado pelo arquivo."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(f"O erro '{e}' ocorreu ao tentar conectar.")
        return None

def view_data(conn, query, title):
    """
    Executa uma consulta e exibe os resultados em um formato de tabela.
    """
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute(query)
            rows = c.fetchall()
            
            print(f"\n--- {title} ---")
            if not rows:
                print("Nenhum dado encontrado.")
                return

            # Imprime os cabeçalhos das colunas
            columns = [description[0] for description in c.description]
            print(" | ".join(columns))
            print("-" * (len(" | ".join(columns)) + len(columns) * 2))

            # Imprime as linhas de dados
            for row in rows:
                print(" | ".join(str(item) for item in row))
            print("-" * (len(" | ".join(columns)) + len(columns) * 2))

        except Error as e:
            print(f"O erro '{e}' ocorreu ao tentar visualizar os dados.")
    else:
        print("Conexão com o banco de dados não estabelecida.")

# --- Exemplo de uso ---
if __name__ == '__main__':
    # Define o nome do arquivo do seu banco de dados
    db_file_name = "financas_pessoais.db"
    
    # 1. Conecta ao banco de dados
    conn = create_connection(db_file_name)

    if conn:
        # 2. Visualiza os usuários
        view_data(conn, "SELECT id, username, email FROM users", "USUÁRIOS")

        # 3. Visualiza as contas
        view_data(conn, "SELECT id, account_name, current_balance, created_at FROM accounts", "CONTAS")
        
        # 4. Visualiza as transações (limitando para evitar uma saída muito longa)
        view_data(conn, "SELECT id, transaction_date, amount, description FROM transactions LIMIT 20", "TRANSAÇÕES (Amostra de 20)")
        
        # 5. Fecha a conexão
        conn.close()
