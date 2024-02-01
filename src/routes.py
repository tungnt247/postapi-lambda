from flask_restful import Api
from views.post import ListCreatePostAPIView, RetrieveUpdateDeletePostAPIView
from views.health import HealthAPIView


def register_routes(app):
    router = Api(app)
    router.add_resource(HealthAPIView, '/')
    router.add_resource(ListCreatePostAPIView, '/api/v1/todos')
    router.add_resource(RetrieveUpdateDeletePostAPIView, '/api/v1/todos/<string:pk>')
