from flask import Flask
from flask_cors import CORS

from extensions import db, migrate, ma
from api import bp as api_bp
import api.empleados
import models