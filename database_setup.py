import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """Cria uma conexão com o banco de dados SQLite especificado pelo arquivo."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Conexão bem-sucedida ao banco de dados '{db_file}'")
        return conn
    except Error as e:
        print(f"O erro '{e}' ocorreu ao tentar conectar.")
        return None

def execute_query(conn, query):
    """Executa uma query SQL."""
    if conn is not None:
        try:
            c = conn.cursor()
            c.executescript(query)  # Use executescript para múltiplas queries
            conn.commit()
            print("Queries executadas com sucesso.")
        except Error as e:
            print(f"O erro '{e}' ocorreu ao executar as queries.")
    else:
        print("Conexão com o banco de dados não estabelecida.")

def setup_database(db_file):
    """
    Função principal para configurar o banco de dados.
    Ela se conecta ao arquivo, cria todas as tabelas e popula os dados iniciais.
    """
    # SQL para criar e popular todas as tabelas
    sql_script = """
    -- Criação das tabelas "enum" para simular os tipos de dados ENUM do DBML
    CREATE TABLE IF NOT EXISTS account_type_enum (
        id INTEGER PRIMARY KEY,
        account_type TEXT NOT NULL UNIQUE
    );
    INSERT INTO account_type_enum (account_type) VALUES 
        ('Checking'), 
        ('Savings'), 
        ('Credit Card'), 
        ('Investment'), 
        ('Other')
    ON CONFLICT(account_type) DO NOTHING;

    CREATE TABLE IF NOT EXISTS category_type_enum (
        id INTEGER PRIMARY KEY,
        category_type TEXT NOT NULL UNIQUE
    );
    INSERT INTO category_type_enum (category_type) VALUES 
        ('Income'), 
        ('Expense')
    ON CONFLICT(category_type) DO NOTHING;

    CREATE TABLE IF NOT EXISTS transaction_type_enum (
        id INTEGER PRIMARY KEY,
        transaction_type TEXT NOT NULL UNIQUE
    );
    INSERT INTO transaction_type_enum (transaction_type) VALUES 
        ('Income'), 
        ('Expense'), 
        ('Transfer')
    ON CONFLICT(transaction_type) DO NOTHING;

    CREATE TABLE IF NOT EXISTS investment_type_enum (
        id INTEGER PRIMARY KEY,
        investment_type TEXT NOT NULL UNIQUE
    );
    INSERT INTO investment_type_enum (investment_type) VALUES 
        ('Stock'), 
        ('Bond'), 
        ('Mutual Fund'), 
        ('ETF'), 
        ('Cryptocurrency'), 
        ('Real Estate'), 
        ('Other')
    ON CONFLICT(investment_type) DO NOTHING;

    CREATE TABLE IF NOT EXISTS investment_transaction_type_enum (
        id INTEGER PRIMARY KEY,
        transaction_type TEXT NOT NULL UNIQUE
    );
    INSERT INTO investment_transaction_type_enum (transaction_type) VALUES 
        ('Buy'), 
        ('Sell'), 
        ('Dividend'), 
        ('Interest'), 
        ('Fee')
    ON CONFLICT(transaction_type) DO NOTHING;

    -- Tabela de usuários (users)
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    );

    -- Tabela de contas (accounts)
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        account_name TEXT NOT NULL,
        account_type_id INTEGER NOT NULL,
        current_balance REAL NOT NULL DEFAULT 0.00,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UNIQUE (user_id, account_name),
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (account_type_id) REFERENCES account_type_enum(id)
    );

    -- Tabela de categorias (categories)
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        category_name TEXT NOT NULL,
        category_type_id INTEGER NOT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UNIQUE (user_id, category_name, category_type_id),
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (category_type_id) REFERENCES category_type_enum(id)
    );

    -- Tabela de transações (transactions)
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        account_id INTEGER NOT NULL,
        category_id INTEGER NOT NULL,
        transaction_date TEXT NOT NULL, -- Use TEXT para o tipo DATE
        amount REAL NOT NULL,
        transaction_type_id INTEGER NOT NULL,
        description TEXT,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (account_id) REFERENCES accounts(id),
        FOREIGN KEY (category_id) REFERENCES categories(id),
        FOREIGN KEY (transaction_type_id) REFERENCES transaction_type_enum(id)
    );

    -- Tabela de orçamentos (budgets)
    CREATE TABLE IF NOT EXISTS budgets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        category_id INTEGER NOT NULL,
        budget_month TEXT NOT NULL, -- Use TEXT para o tipo DATE
        budget_amount REAL NOT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UNIQUE (user_id, category_id, budget_month),
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (category_id) REFERENCES categories(id)
    );

    -- Tabela de investimentos (investments)
    CREATE TABLE IF NOT EXISTS investments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        account_id INTEGER,
        investment_name TEXT NOT NULL,
        symbol TEXT,
        investment_type_id INTEGER NOT NULL,
        current_value REAL NOT NULL DEFAULT 0.00,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UNIQUE (user_id, symbol),
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (account_id) REFERENCES accounts(id),
        FOREIGN KEY (investment_type_id) REFERENCES investment_type_enum(id)
    );

    -- Tabela de transações de investimento (investment_transactions)
    CREATE TABLE IF NOT EXISTS investment_transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        investment_id INTEGER NOT NULL,
        transaction_date TEXT NOT NULL, -- Use TEXT para o tipo DATE
        transaction_type_id INTEGER NOT NULL,
        quantity REAL,
        price_per_unit REAL,
        total_amount REAL NOT NULL,
        description TEXT,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (investment_id) REFERENCES investments(id),
        FOREIGN KEY (transaction_type_id) REFERENCES investment_transaction_type_enum(id)
    );
    """
    
    conn = create_connection(db_file)
    if conn:
        execute_query(conn, sql_script)
        conn.close()

if __name__ == '__main__':
    # Define o nome do arquivo do seu banco de dados
    db_file_name = "financas_pessoais.db"

    # Chama a função para configurar o banco de dados
    setup_database(db_file_name)
