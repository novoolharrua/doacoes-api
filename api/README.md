# Doações API

Folder de instruções para utilização da api

## Instalação

Para utilizar a API, basta seguir os seguintes passos no folder /api do projeto:

### Virtualenv
É interessante criar um ambiente virutal para utilização da aplicação, isso permite um controle maior das bibliotecas utilizadas: 
```
pip install virtualenv
virtualenv --python python3.5 env
```
Vale lembrar que é necessário instalar a versão 3.5 do python para que o passo acima funcione.

### Ativar e configurar ambiente
Para configurar o ambiente utilize:
```
source env/bin/activate
pip install -r requirements.txt
```

### Banco
Os comandos para configurar o banco estão na pasta /api/sql/banco.sql. Basta iniciar um sql-server, criar um schema e rodar o script de criação  das tabelas. Para que a aplicação acesse o banco é necessário configurar as seguintes variaveis de ambiente: 
```
export SQL_HOST="127.0.0.1" ou outro ip
export SQL_USER="root" ou outro user
export SQL_PASS="" a senha
export SQL_DB="donations" ou outro nome de schema
```

### Credencias
Existe um arquivo de credencial que deve ser colocado na pasta /api. Como a credencial é temporária, é só pedir para o @ferreiraalves :)


## Execução
Para rodar a aplicação, basta executar o comando:
```
python main.py
```

Lembrando que a aplicação irá rodar no localhost, porta 8080. Caso prefira executar em outro host ou porta, basta alterar os parametros no arquivo main.py:
```
app.run(debug=False, port=8080, host='0.0.0.0', use_reloader=False)
```  