from flask import request
from flask_restful import Resource

from managers.auth import auth
from managers.complaint import ComplaintManager
from models import UserRole
from schemas.requests.complaint import ComplaintSchemaRequest
from schemas.responses.complaint import ComplaintSchemaResponse
from services.s3 import S3Service
from utils.decorators import permission_required, validate_schema


class ComplaintsResource(Resource):
    @auth.login_required
    def get(self):
        user = auth.current_user()
        complaints = ComplaintManager.get_complaints(user)
        return ComplaintSchemaResponse().dump(complaints, many=True)

    @auth.login_required
    @permission_required(UserRole.complainer)
    @validate_schema(ComplaintSchemaRequest)
    def post(self):
        data = request.get_json()
        current_user = auth.current_user()
        new_complaint = ComplaintManager.create(data, current_user)
        return ComplaintSchemaResponse().dump(new_complaint), 201


class ApproveComplaintResource(Resource):
    @auth.login_required()
    def put(self, id):
        ComplaintManager.approve(id)
        return 204


class RejectComplaintResource(Resource):
    @auth.login_required()
    def put(self, id):
        ComplaintManager.reject(id)
        return 204


class DeletePhotoResource(Resource):
    @staticmethod
    @auth.login_required()
    def post():
        data = request.get_json()
        photo_name = data["key"]
        s3 = S3Service()
        s3.delete_photo(photo_name)
        return 200
