# project/server/auth/views.py

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from project.server import bcrypt, db
from project.server.models import User

auth_blueprint = Blueprint('auth', __name__)

class RegisterAPI(MethodView):
    """
    User Registration Resource
    """

    def get(self):
    	responseObject = {
    		'status': 'success',
    		'message': 'Request successful but please send an HTTP POST request to register the user.'
    	}
    	return make_response(jsonify(responseObject)), 201

    def post(self):
        # get the post data
        post_data = request.get_json(); print(request)
        # check if user already exists
        user = User.query.filter_by(email=post_data.get('email')).first()
        if not user:
            try:
                user = User(
                    email=post_data.get('email'),
                    password=post_data.get('password')
                )

                # insert the user
                db.session.add(user)
                db.session.commit()
                # generate the auth token
                auth_token = user.encode_auth_token(user.id)
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return make_response(jsonify(responseObject)), 202



#code from https://github.com/adoval12/cs501_t1_diagnostic_test/blob/test/project/server/auth/views.py 
# and https://github.com/aeram0/cs501_t1_diagnostic_test/blob/test/project/server/auth/views.py 
class UserListAPI(MethodView):
    def get(self):
        user_arr = []
        user = db.session.query(User.email)
        for i in user:
            user_arr.append(i[0])
        return make_response(jsonify(user_arr)), 201




# define the API resources
registration_view = RegisterAPI.as_view('register_api')
userList_view = UserListAPI.as_view('userList_api')

# add Rules for API Endpoints
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST', 'GET']
)

auth_blueprint.add_url_rule(
    '/users/index',
    view_func=userList_view,
    methods=['POST', 'GET']
)