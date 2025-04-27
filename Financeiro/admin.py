from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Cria a instância do Flask
app = Flask(__name__)

# Configura o banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///financeiro.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o SQLAlchemy
db = SQLAlchemy(app)

# Definição dos modelos
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # 'cliente' ou 'admin'
    contrato_id = db.Column(db.Integer, db.ForeignKey('contrato.id'), nullable=True)
    contrato = db.relationship('Contrato', back_populates='usuario')
    cobrancas = db.relationship('Cobranca', back_populates='usuario')

class Funcionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    salario = db.Column(db.Float, nullable=False)
    pagamento_data = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    status_pagamento = db.Column(db.String(50), default='Pendente')

class ContaFinanceira(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    saldo = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # 'receita' ou 'despesa'
    data = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class Mensalidade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_plano = db.Column(db.String(50), nullable=False)  # Ex: 'básico', 'premium'
    valor = db.Column(db.Float, nullable=False)

class Cobranca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    data_cobranca = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # 'manual' ou 'automática'
    usuario = db.relationship('Usuario', back_populates='cobrancas')

class Contrato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    validade = db.Column(db.Date, nullable=False)
    tipo_plano = db.Column(db.String(50), nullable=False)
    condicoes = db.Column(db.Text, nullable=False)
    usuario = db.relationship('Usuario', back_populates='contrato')

class Relatorio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)  # 'diário', 'mensal', 'anual'
    data_geracao = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False)

# Cria o banco de dados
with app.app_context():
    db.create_all()

# Rotas
@app.route('/admin')
def home():
    return render_template('admin.html')

@app.route('/pagamentos')
def pagamentos():
    funcionarios = Funcionario.query.all()
    return render_template('pagamentos.html', funcionarios=funcionarios)

@app.route('/admin/adicionar')
def adicionar():
    tipo = request.args.get('tipo')
    if tipo == 'plano':
        return render_template('adicionar_plano.html')
    elif tipo == 'funcionario':
        return render_template('adicionar_funcionario.html')
    elif tipo == 'conta':
        return render_template('adicionar_conta.html')
    else:
        return "Tipo inválido", 400

@app.route('/pagar/<int:id_funcionario>', methods=['POST'])
def pagar(id_funcionario):
    funcionario = Funcionario.query.get(id_funcionario)
    if not funcionario:
        return f"<h1>Erro 404: Funcionário não encontrado</h1>", 404

    funcionario.status_pagamento = "Pago"
    db.session.commit()
    return f"<h1>Pagamento realizado para {funcionario.nome}</h1>", 200


@app.route('/relatorios', methods=['GET'])
def relatorios():
    tipo = request.args.get('tipo')  # 'diário', 'mensal', 'anual'
    if tipo not in ['diário', 'mensal', 'anual']:
        return f"<h1>Erro: Tipo de relatório inválido</h1>", 400

    if tipo == 'diário':
        total = db.session.query(db.func.sum(Cobranca.valor)).filter(db.func.date(Cobranca.data_cobranca) == datetime.utcnow().date()).scalar()
    elif tipo == 'mensal':
        total = db.session.query(db.func.sum(Cobranca.valor)).filter(db.func.strftime('%m', Cobranca.data_cobranca) == datetime.utcnow().strftime('%m')).scalar()
    else:  # anual
        total = db.session.query(db.func.sum(Cobranca.valor)).filter(db.func.strftime('%Y', Cobranca.data_cobranca) == datetime.utcnow().strftime('%Y')).scalar()

    return f"<h1>Relatório {tipo} - Total: R${total if total else 0}</h1>", 200


@app.route('/contas/editar/<int:id>', methods=['PUT'])
def editar_conta(id):
    conta = ContaFinanceira.query.get(id)
    if not conta:
        return f"<h1>Erro 404: Conta não encontrada</h1>", 404
    
    data = request.get_json()
    conta.nome = data.get('nome', conta.nome)
    conta.saldo = data.get('saldo', conta.saldo)
    conta.tipo = data.get('tipo', conta.tipo)

    db.session.commit()
    return f"<h1>Conta {conta.nome} atualizada com sucesso</h1>", 200


@app.route('/contas/remover/<int:id>', methods=['DELETE'])
def remover_conta(id):
    conta = ContaFinanceira.query.get(id)
    if not conta:
        return f"<h1>Erro 404: Conta não encontrada</h1>", 404
    
    db.session.delete(conta)
    db.session.commit()
    return f"<h1>Conta {conta.nome} removida com sucesso</h1>", 200

# UNICO CERTO POR ENQUANTO
@app.route('/contas/adicionar', methods=['POST'])
def adicionar_conta():
    # Pegando os dados do formulário
    nome = request.form.get('nome')
    saldo = request.form.get('saldo')
    tipo = request.form.get('tipo')

    # Verificando se os dados são válidos
    if not nome or not saldo or not tipo:
        return f"<h1>Erro 400: Dados inválidos ou incompletos</h1>", 400

    # Criando uma nova conta com os dados recebidos
    nova_conta = ContaFinanceira(
        nome=nome,
        saldo=float(saldo),  # Convertendo saldo para float
        tipo=tipo
    )

    # Adicionando a conta ao banco de dados
    db.session.add(nova_conta)
    db.session.commit()

    # Retornando uma mensagem de sucesso
    return f"<h1>Conta {nova_conta.nome} adicionada com sucesso</h1>", 201



@app.route('/admin/adicionar', methods=['POST'])
def adicionar_itens():
    data = request.get_json()
    
    # Adicionar um novo plano de mensalidade
    if 'tipo_plano' in data and 'valor' in data:
        novo_plano = Mensalidade(
            tipo_plano=data['tipo_plano'],
            valor=data['valor']
        )
        db.session.add(novo_plano)
        db.session.commit()
        return f"<h1>Plano de mensalidade {novo_plano.tipo_plano} adicionado com sucesso</h1>", 201
    
    # Adicionar um novo funcionário
    if 'nome' in data and 'salario' in data:
        novo_funcionario = Funcionario(
            nome=data['nome'],
            salario=data['salario'],
            pagamento_data=datetime.utcnow()
        )
        db.session.add(novo_funcionario)
        db.session.commit()
        return f"<h1>Funcionário {novo_funcionario.nome} adicionado com sucesso</h1>", 201
    
    # Adicionar uma nova conta financeira
    if 'nome' in data and 'saldo' in data and 'tipo' in data:
        nova_conta = ContaFinanceira(
            nome=data['nome'],
            saldo=data['saldo'],
            tipo=data['tipo']  # 'receita' ou 'despesa'
        )
        db.session.add(nova_conta)
        db.session.commit()
        return f"<h1>Conta financeira {nova_conta.nome} adicionada com sucesso</h1>", 201
    
    return f"<h1>Erro: Dados inválidos ou incompletos</h1>", 400


if __name__ == '__main__':
    app.run(debug=True)