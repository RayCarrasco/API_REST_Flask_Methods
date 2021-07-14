# Código modificado del curso
#  Creación de API REST Web Service con Python y MySQL
# API REST Web Service con Python y MySQL
# Raymundo Carrasco 

#jsonify permite convertir a Json
from flask import Flask, jsonify, request
# Documentación https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/
from flask_sqlalchemy import SQLAlchemy
# Documentación https://marshmallow.readthedocs.io/en/stable/
from flask_marshmallow import Marshmallow

# se crea una instancia de Flask y se configura la conexión con la base de datos
#se puede revizar la documentación en: https://docs.sqlalchemy.org/en/14/dialects/mysql.html#dialect-mysql
app = Flask(__name__)
# "mariadb+pymysql://user:pass@some_mariadb/dbname?charset=utf8mb4"
# con anterioridad en PHP Admin con el nombre dbpythonapi
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost:3306/python_api_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db =SQLAlchemy(app)
ma = Marshmallow(app)

# Creación del esquema para la base de datos, La base de datos fue creada
class Categoria(db.Model):
    cat_id = db.Column(db.Integer, primary_key = True)
    cat_nombre = db.Column(db.String(100))
    cat_descripcion = db.Column(db.String(100))

    def __init__(self, cat_nombre, cat_descripcion):
        self.cat_nombre = cat_nombre
        self.cat_descripcion = cat_descripcion

# Se actualizan los cambios de db
db.create_all()

# Este equema permitirá la interacción con el servicio
class CategoriaSchema(ma.Schema):
    class Meta:
        fields = ('cat_id', 'cat_nombre', 'cat_descripcion')

# Este esquema permite manipular una única categoría
esquema_de_categoria = CategoriaSchema()

# Este esquema es utilizado para manejar varias categorías
esquema_de_categoria_plural = CategoriaSchema(many=True)

# GET Obtiene la información de todas las categorías
@app.route('/categoria', methods=['GET'])
def get_categorias():
    # se obtienen los resultados
    all_categorias = Categoria.query.all()
    #los resultados se estructuran en el esquema y se guardan
    result = esquema_de_categoria.dump(all_categorias)
    
    # se comunican en fromato Json
    return jsonify(result)

# GET Obtiene toda la información de una categoría al id que corresponda
@app.route('/categoria/<id>', methods=['GET'])
def get_categoria_id(id):
    una_categoria = Categoria.query.get(id)

    return esquema_de_categoria.jsonify(una_categoria)

# POST Permite crear una nueva categoría especificando nombre y 
# descripción en formato Json
@app.route('/categoria', methods=['POST'])
def insert_categoria():
    data = request.get_json(force=True)
    cat_nombre = data['cat_nombre']
    cat_descripcion = data['cat_descripcion']

    nueva_categoria = Categoria(cat_nombre, cat_descripcion)

    db.session.add(nueva_categoria)
    db.session.commit()

    return esquema_de_categoria.jsonify(nueva_categoria)

#PUT Actualiza un registro en la BD con el correspondiente id
@app.route('/categoria/<id>', methods=['PUT'])
def update_categoria(id):
    actualizar_categoria = Categoria.query.get(id)

    cat_nombre = request.json['cat_nombre']
    cat_descripcion = request.json['cat_descripcion']

    actualizar_categoria.cat_nom = cat_nombre
    actualizar_categoria.cat_desp = cat_descripcion

    db.session.commit()

    return esquema_de_categoria.jsonify(actualizar_categoria)

# DLETE Eliminar un registro de la BD con el respectivo id
# Esta es una forma ilustrativa de realizar esta operación, nunca debe
# implementarse de esta forma en producción
@app.route('/categoria/<id>', methods=['DELETE'])
def delete_categoria(id):
    eliminar_categoria = Categoria.query.get(id)
    db.session.delete(eliminar_categoria)
    db.session.commit()

    return esquema_de_categoria.jsonify(eliminar_categoria)

#Mensaje de bienvenida en index
@app.route('/', methods=['GET'])
def index():
    return jsonify({'Mensaje': 'Bienvenido'})

if __name__ == '__main__':
    app.run(debug=True)
