from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Nome do arquivo do banco de dados
DATABASE = 'financas_pessoais.db'

def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row # Permite acessar as colunas como um dicionário
    return conn

@app.route('/transacoes', methods=['GET', 'POST'])
def transacoes():
    conn = get_db_connection()
    
    if request.method == 'POST':
        # Adiciona uma nova transação
        data = request.json
        descricao = data.get('descricao')
        valor = data.get('valor')
        tipo = data.get('tipo') # Deve ser 'receita' ou 'despesa'
        
        # A data de hoje
        import datetime
        data_hoje = datetime.date.today().isoformat()
        
        try:
            conn.execute('INSERT INTO transacoes (descricao, valor, tipo, data) VALUES (?, ?, ?, ?)',
                         (descricao, valor, tipo, data_hoje))
            conn.commit()
            return jsonify({'message': 'Transação adicionada com sucesso!'}), 201
        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 400
        finally:
            conn.close()

    elif request.method == 'GET':
        # Lista todas as transações
        cursor = conn.execute('SELECT * FROM transacoes')
        transacoes = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(transacoes)

if __name__ == '__main__':
    # Certifique-se de que o banco de dados e a tabela 'transacoes' existem
    # Antes de rodar a aplicação Flask.
    # Você já tem o seu script para isso.
    app.run(debug=True)
