
from apiv1.tests import factories
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken


class TestBookGetAPIView(APITestCase):

    def test_get_user(self):
        # テスト用のデータ作成
        login_user = factories.AccountFactory(
            username="loginuser", email="loginuser@sample.com", password="loginuserpassword")

        # ログイン処理
        token = str(AccessToken.for_user(login_user))
        self.client.credentials(HTTP_AUTHORIZATION='jwt {0}'.format(token))

        # APIの実行
        url = "/api/v1/account/auth/users/me/"
        response = self.client.get(url)

        # レスポンスの評価
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK, "HTTPレスポンスステータスコードが200のとき")
        self.assertEqual(response.data["username"],
                         "loginuser", "アカウントのユーザー名が「loginuser」のとき")
        self.assertEqual(response.data["email"],
                         "loginuser@sample.com", "アカウントのメールアドレスが「loginuser@sample.com」のとき")

    def test_create_user(self):
        # APIの実行
        url = "/api/v1/account/auth/users/"
        data = {
            "username": "testuser",
            "email": "testuser@sample.com",
            "password": "testuserpassword",
            "re_password": "testuserpassword"
        }
        response = self.client.post(url, data)

        # レスポンスの評価
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED, "HTTPレスポンスステータスコードが201のとき")
        self.assertEqual(response.data["username"],
                         "testuser", "アカウントのユーザー名が「testuser」のとき")
        self.assertEqual(response.data["email"],
                         "testuser@sample.com", "アカウントのメールアドレスが「testuser@sample.com」のとき")

    def test_change_password(self):
        # テスト用のデータ作成
        login_user = factories.AccountFactory(
            username="loginuser", email="loginuser@sample.com", password="loginuserpassword")

        # ログイン処理
        token = str(AccessToken.for_user(login_user))
        self.client.credentials(HTTP_AUTHORIZATION='jwt {0}'.format(token))

        # APIの実行 changedpassword
        url = "/api/v1/account/auth/users/set_password/"
        data = {
            "new_password": "new password",
            "re_new_password": "new password",
            "current_password": "loginuserpassword",
        }
        response = self.client.post(url, data)

        # レスポンスの評価
        # set_passwordの成功時はHTTP_400_BAD_REQUEST
        # https://djoser.readthedocs.io/en/latest/base_endpoints.html#set-password
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST, "HTTPレスポンスステータスコードが400のとき")
