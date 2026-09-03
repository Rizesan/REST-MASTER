from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from extensions import db
from models import Empleado
from schemas import empleado_schema, empleados_schema
from . import api


class Empleados(Resource):
    # GET /api/empleados
    def get(self):
        empleados = Empleado.query.order_by(Empleado.idEmpleado.asc()).all()
        return empleados_schema.dump(empleados), 200

    # POST /api/empleados
    def post(self):
        data = request.get_json()
        if not data:
            return {"message": "Cuerpo JSON requerido."}, 400
        try:
            empleado = empleado_schema.load(data)
        except ValidationError as err:
            return {"errors": err.messages}, 422
        db.session.add(empleado)
        db.session.commit()
        return empleado_schema.dump(empleado), 201

    def get(self, id):
        empleado = Empleado.query.get(id)
        if not empleado:
            return {"message": "Empleado no encontrado."}, 404
        return empleado_schema.dump(empleado), 200

    def put(self, id):
        empleado = Empleado.query.get(id)
        if not empleado:
            return {"message": "Empleado no encontrado."}, 404
        data = request.get_json()
        if not data:
            return {"message": "Cuerpo JSON requerido."}, 400
        try:
            updated_empleado = empleado_schema.load(data, instance=empleado, partial=False)
        except ValidationError as err:
            return {"errors": err.messages}, 422
        db.session.commit()
        return empleado_schema.dump(updated_empleado), 200

    def delete(self, id):
        empleado = Empleado.query.get(id)
        if not empleado:
            return {"message": "Empleado no encontrado."}, 404
        db.session.delete(empleado)
        db.session.commit()
        return {"message": "Empleado eliminado correctamente."}, 200

    api.add_resource(Empleados, '/empleados', '/api/empleados/<int:id>')
    api.add_resource(Empleados, '/empleados/<int:id>', endpoint='empleado_detail')