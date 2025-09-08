# Gestão de Economia$ 💰

Sistema completo de controle financeiro pessoal desenvolvido em Python.

## 🎯 Funcionalidades

- **Autenticação**: Cadastro e login seguro de usuários
- **Categorias**: Gestão de receitas, despesas, investimentos e lazer
- **Movimentações**: CRUD completo de transações financeiras
- **Dashboards**: Relatórios e gráficos interativos
- **Projeções**: Previsão de cenários financeiros
- **Exportação**: Relatórios em Excel e PDF
- **Interface Web**: Responsiva e moderna, com gráficos interativos e filtros dinâmicos

## 🚀 Instalação

```bash
pip install -r requirements.txt
python app.py
```

## 📁 Estrutura do Projeto

```
Iconomy/
├── app.py                 # Aplicação principal
├── config.py             # Configurações
├── requirements.txt      # Dependências
├── models/              # Modelos de dados
├── services/            # Lógica de negócio
├── api/                 # Endpoints da API
├── utils/               # Utilitários
├── cli/                 # Interface de linha de comando
├── templates/           # Templates HTML
├── static/             # CSS, JS, imagens
│   ├── css/
│   └── js/
├── instance/           # Banco de dados
└── exports/             # Arquivos exportados
```

## 🛠️ Tecnologias

- **Backend**: Flask + SQLAlchemy
- **Banco**: SQLite (desenvolvimento) / PostgreSQL (produção)
- **Autenticação**: JWT + Bcrypt
- **Gráficos**: Matplotlib, Seaborn, Plotly
- **Exportação**: Pandas, OpenPyXL, ReportLab
- **Frontend**: Bootstrap 5, Font Awesome 6, Chart.js, JavaScript ES6

## 📊 Banco de Dados

- **Users**: Gerenciamento de usuários
- **Categories**: Categorias financeiras
- **Transactions**: Movimentações financeiras

## 📈 Recursos Avançados

### 🔄 AJAX e Interatividade
- Formulários assíncronos
- Notificações em tempo real
- Validação dinâmica
- Loading states

### 📊 Visualizações
- Gráficos responsivos
- Dados em tempo real
- Filtros dinâmicos
- Exportação de dados

## 🎯 Comandos Úteis

```bash
# Desenvolvimento
python app.py                    # Servidor web padrão
python app.py --port 8080       # Porta customizada
python app.py cli               # Interface CLI

# Produção
python app.py --no-debug        # Sem modo debug
python app.py --host 0.0.0.0    # Aceitar conexões externas
```

---

**🎉 Desenvolvido com ❤️ para controle financeiro pessoal eficiente!**
