import uuid
from dataclasses import asdict
from flask import request
from flask_restful import Resource, reqparse
from models.post import Post


class ListCreatePostAPIView(Resource):
    def get(self):
        return {'statusCode': 200, 'body': Post.all()}, 200

    def post(self):
        try:
            post_data = request.json.copy()
            post_data['id'] = uuid.uuid4().hex
            post = Post(**post_data)
            post.save()
            return {'statusCode': 201, 'message': asdict(post)}, 201
        except Exception as e:
            return {'statusCode': 400, 'message': e.args[0]}, 400


class RetrieveUpdateDeletePostAPIView(Resource):
    def get(self, pk):
        try:
            post = self.__get_post(pk)
            return {'statusCode': 200, 'message': post}, 200
        except Exception as e:
            return {'statusCode': 404, 'message': e.args[0]}, 404

    def put(self, pk):
        try:
            self._set_post_params()
            self.__get_post(pk)
            updating_data = {
                'title': request.form.to_dict().get('title'),
                'content': request.form.to_dict().get('content'),
                'image': request.files.get('image'),
            }
            Post.update(pk, **updating_data)
            return {'statusCode': 200, 'message': f'post with id {pk} is updated!'}, 200
        except Exception as e:
            return {'statusCode': 400, 'message': e.args[0]}, 400

    def delete(self, pk):
        try:
            self.__get_post(pk)
            Post.delete(pk)
            return {'statusCode': 200, 'message': f'post with id {pk} is deleted!'}, 200
        except Exception as e:
            return {'statusCode': 404, 'message': e.args[0]}, 404

    def __get_post(self, pk):
        post = Post.retrieve(pk)
        if not post:
            raise ValueError(f'Post with id {pk} is not exist!')
        return post

    def _set_post_params(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=False, location='form')
        parser.add_argument('content', type=str,
                            required=False, location='form')
        parser.add_argument('images', type=str,
                            required=False, location='form')


class UploadPostImageAPIView(Resource):
    def post(self, pk):
        self.__get_post(pk)

    def __get_post(self, pk):
        post = Post.retrieve(pk)
        if not post:
            raise ValueError(f'Post with id {pk} is not exist!')
        return post

    def _set_post_params(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=False, location='form')
        parser.add_argument('content', type=str,
                            required=False, location='form')
        parser.add_argument('images', type=str,
                            required=False, location='form')
