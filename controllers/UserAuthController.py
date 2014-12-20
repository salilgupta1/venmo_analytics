from model.database.table_managers.UserManager import UserManager
import os, requests, hashlib, time

class UserAuthController():

	def __init__(self):
		self.user = UserManager()
		self.regData = None

	def authenticateUser(self,username, password):
		result = self.user.getUserAuth(username)
		print result
		if len(result) > 0:
			db_password = result[0][0]
			db_salt = result[0][1]
			password = password + db_salt
			hashed = hashlib.sha1(password).hexdigest()
			if (hashed == db_password):
				return True
			else:
				return "Password is invalid!"
		else:
			return "Username is invalid!"

	def authorizeWithVenmo(self,code):
		data = {
			"client_id":os.environ['client_id'],
			"client_secret":os.environ['client_secret'], 
			"code":code
		}

		url = "https://api.venmo.com/v1/oauth/access_token"

		# do the actual retrieval of user information
		response = requests.post(url, data)
		response_dict = response.json()

		if 'error' in response_dict:
			print response_dict['error']
			return False
		else:
			v_id = response_dict['user']['id']
			v_user_name = response_dict['user']['username']
			v_email = response_dict['user']['email']
			v_display_name = response_dict['user']['display_name']
			v_access_token = response_dict['access_token']
			v_refresh_token = response_dict['refresh_token']
			v_auth_date = time.strftime("%Y-%m-%d %H:%M:%S")
			self.regData = (v_id,v_user_name,v_email,v_display_name,v_access_token,v_refresh_token,v_auth_date)

			return v_user_name

	def completeRegistration(self,username,password):
		salt = os.urandom(16).encode('base-64')
		password += salt
		password = hashlib.sha1(password).hexdigest()
		self.regData +=(password,salt)
		result = self.user.createUser(self.regData)

		# error handling needed
		
		self.regData.clear()
		return result
