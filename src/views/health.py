from flask_restful import Resource

class HealthAPIView(Resource):
    def get(self):
        return {'message': 'ok'}
