import sqlite3
from sqlite3 import Error
from datetime import datetime
from faker import Faker
import random
import uuid

# Inicializa o Faker para gerar dados em português do Brasil
fake = Faker('pt_BR')

def create_connection(db_file):
    """Cria uma conexão com o banco de dados SQLite especificado pelo arquivo."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(f"O erro '{e}' ocorreu ao tentar conectar.")
        return None

def insert_user(conn, username, email, password_hash):
    """Insere um novo usuário na tabela 'users'."""
    sql = """
    INSERT INTO users (username, email, password_hash, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?)
    """
    try:
        c = conn.cursor()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute(sql, (username, email, password_hash, current_time, current_time))
        conn.commit()
        return c.lastrowid
    except Error as e:
        print(f"O erro '{e}' ocorreu ao inserir o usuário '{username}'.")
        return None

def insert_account(conn, user_id, account_name, account_type_id):
    """Insere uma nova conta na tabela 'accounts'."""
    sql = """
    INSERT INTO accounts (user_id, account_name, account_type_id, current_balance, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    try:
        c = conn.cursor()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current_balance = round(random.uniform(500.0, 50000.0), 2)
        c.execute(sql, (user_id, account_name, account_type_id, current_balance, current_time, current_time))
        conn.commit()
        return c.lastrowid
    except Error as e:
        print(f"O erro '{e}' ocorreu ao inserir a conta '{account_name}'.")
        return None

def insert_category(conn, user_id, category_name, category_type_id):
    """Insere uma nova categoria na tabela 'categories'."""
    sql = """
    INSERT INTO categories (user_id, category_name, category_type_id, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?)
    """
    try:
        c = conn.cursor()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute(sql, (user_id, category_name, category_type_id, current_time, current_time))
        conn.commit()
        return c.lastrowid
    except Error as e:
        print(f"O erro '{e}' ocorreu ao inserir a categoria '{category_name}'.")
        return None

def insert_transaction(conn, user_id, account_id, category_id, amount, transaction_type_id, description):
    """Insere uma nova transação na tabela 'transactions'."""
    sql = """
    INSERT INTO transactions (user_id, account_id, category_id, transaction_date, amount, transaction_type_id, description, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    try:
        c = conn.cursor()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Correção: Agora usamos fake.date_object() para retornar um objeto datetime.date
        c.execute(sql, (user_id, account_id, category_id, fake.date_object(), amount, transaction_type_id, description, current_time, current_time))
        conn.commit()
        return c.lastrowid
    except Error as e:
        print(f"O erro '{e}' ocorreu ao inserir a transação.")
        return None

def get_enum_id(conn, table_name, value):
    """Busca o ID de um valor em uma tabela de enum."""
    # Mapeia os nomes das tabelas para as colunas corretas
    column_map = {
        'account_type_enum': 'account_type',
        'category_type_enum': 'category_type',
        'transaction_type_enum': 'transaction_type',
        'investment_type_enum': 'investment_type',
        'investment_transaction_type_enum': 'transaction_type',
    }
    column_name = column_map.get(table_name)
    if not column_name:
        print(f"Erro: Tabela de enum '{table_name}' não reconhecida.")
        return None

    sql = f"SELECT id FROM {table_name} WHERE {column_name} = ?"
    try:
        c = conn.cursor()
        c.execute(sql, (value,))
        result = c.fetchone()
        return result[0] if result else None
    except Error as e:
        print(f"O erro '{e}' ocorreu ao buscar o ID na tabela '{table_name}'.")
        return None

# --- Funções para popular o banco de dados ---

def populate_database(conn):
    """Função principal para popular o banco de dados com dados fictícios."""
    # IDs das tabelas de enum
    account_types = ['Checking', 'Savings', 'Credit Card', 'Investment']
    category_types = ['Income', 'Expense']
    transaction_types = ['Income', 'Expense', 'Transfer']

    # Geração de usuários
    print("Populating users...")
    user_ids = []
    for _ in range(5): # Cria 5 usuários fictícios
        username = fake.user_name()
        email = fake.email()
        password_hash = str(uuid.uuid4()) # Hash de senha fictício
        user_id = insert_user(conn, username, email, password_hash)
        if user_id:
            user_ids.append(user_id)

    # Geração de contas e categorias para cada usuário
    print("Populating accounts and categories...")
    for user_id in user_ids:
        # Contas
        for i in range(2): # 2 contas por usuário
            account_type = random.choice(account_types)
            account_type_id = get_enum_id(conn, 'account_type_enum', account_type)
            if account_type_id:
                insert_account(conn, user_id, f"{account_type} Account {i+1}", account_type_id)

        # Categorias
        for _ in range(3): # 3 categorias por tipo (Receita/Despesa)
            category_type = random.choice(category_types)
            category_type_id = get_enum_id(conn, 'category_type_enum', category_type)
            if category_type_id:
                category_name = fake.word()
                insert_category(conn, user_id, category_name, category_type_id)

    # Geração de transações
    print("Populating transactions...")
    for user_id in user_ids:
        c = conn.cursor()
        c.execute("SELECT id FROM accounts WHERE user_id = ?", (user_id,))
        account_ids = [row[0] for row in c.fetchall()]
        
        c.execute("SELECT id FROM categories WHERE user_id = ? OR user_id IS NULL", (user_id,))
        category_ids = [row[0] for row in c.fetchall()]

        if account_ids and category_ids:
            for _ in range(50): # 50 transações por usuário
                account_id = random.choice(account_ids)
                category_id = random.choice(category_ids)
                
                amount = round(random.uniform(1.0, 1000.0), 2)
                transaction_type = random.choice(transaction_types)
                transaction_type_id = get_enum_id(conn, 'transaction_type_enum', transaction_type)
                
                description = fake.sentence(nb_words=5)
                insert_transaction(conn, user_id, account_id, category_id, amount, transaction_type_id, description)

    print("\nBanco de dados populado com sucesso!")


# --- Exemplo de uso ---
if __name__ == '__main__':
    # Define o nome do arquivo do seu banco de dados
    db_file_name = "financas_pessoais.db"
    
    # Primeiro, execute o script de setup para criar as tabelas
    # O arquivo database_setup.py precisa estar no mesmo diretório
    import database_setup
    database_setup.setup_database(db_file_name)
    
    # 2. Conecta ao banco de dados
    conn = create_connection(db_file_name)

    if conn:
        # 3. Chama a função para popular o banco de dados
        populate_database(conn)
        
        # 4. Fecha a conexão
        conn.close()
