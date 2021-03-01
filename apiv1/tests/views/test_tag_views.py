
from apiv1.tests import factories
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken


class TestBookGetAPIView(APITestCase):

    def setUp(self):
        # テスト用のデータ作成
        self.login_user = factories.AccountFactory(
            username="anotheruser", email="anotheruser@sample.com", password="anotheruserpassword")
        self.another_user = factories.AccountFactory(
            username="loginuser", email="loginuser@sample.com", password="loginuserpassword")

        # ログイン処理
        token = str(AccessToken.for_user(self.login_user))
        self.client.credentials(HTTP_AUTHORIZATION='jwt {0}'.format(token))

    def test_get_tag_list(self):
        # テスト用のデータ作成
        factories.TagFactory(account=self.login_user)
        factories.TagFactory(account=self.login_user)

        # APIの実行
        url = "/api/v1/household/tags/"
        response = self.client.get(url)

        # レスポンスの評価
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK, "HTTPレスポンスステータスコードが200のとき")
        self.assertEqual(len(response.data), 2, "取得したタグが1件のとき")

    def test_create_tag(self):
        # APIの実行
        url = "/api/v1/household/tags/"
        data = {"name": "new tag", "color": "grey",
                "account_uuid": self.login_user.uuid}
        response = self.client.post(url, data)

        # レスポンスの評価
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED, "HTTPレスポンスステータスコードが200のとき")
        self.assertEqual(response.data["name"],
                         "new tag", "タグの名前が「new tag」のとき")
        self.assertEqual(response.data["color"],
                         "grey", "タグの色が「grey」のとき")

    def test_update_tag(self):
        # テスト用のデータ作成
        tag = factories.TagFactory(account=self.login_user)

        # APIの実行
        url = "/api/v1/household/tags/{}/".format(tag.uuid)
        data = {"name": "updated tag", "color": "red",
                "account_uuid": self.login_user.uuid}
        response = self.client.put(url, data)

        # レスポンスの評価
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK, "HTTPレスポンスステータスコードが200のとき")
        self.assertEqual(response.data["name"],
                         "updated tag", "タグの名前が「updated tag」のとき")
        self.assertEqual(response.data["color"],
                         "red", "タグの色が「red」のとき")

    def test_delete_tag(self):
        # テスト用のデータ作成
        tag = factories.TagFactory(account=self.login_user)

        # APIの実行
        url = "/api/v1/household/tags/{}/".format(tag.uuid)
        response = self.client.delete(url)

        # レスポンスの評価
        self.assertEqual(response.status_code,
                         status.HTTP_204_NO_CONTENT, "HTTPレスポンスステータスコードが204のとき")

    def test_get_list_anotheruser(self):
        # テスト用のデータ作成
        factories.TagFactory(name="tag1", account=self.login_user)
        factories.TagFactory(name="tag2", account=self.another_user)

        # APIの実行
        url = "/api/v1/household/tags/"
        response = self.client.get(url)

        # レスポンスの評価
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK, "HTTPレスポンスステータスコードが200のとき")
        self.assertEqual(len(response.data), 1, "取得したタグが1件のとき")
        self.assertEqual(response.data[0]["name"],
                         "tag1", "タグの名前が「tag1」のとき")

    def test_update_tag_anotheruser(self):
        # テスト用のデータ作成
        tag = factories.TagFactory(account=self.another_user)

        # APIの実行
        url = "/api/v1/household/tags/{}/".format(tag.uuid)
        data = {"name": "updated tag", "color": "red",
                "account_uuid": self.login_user.uuid}
        response = self.client.put(url, data)

        # レスポンスの評価
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST, "HTTPレスポンスステータスコードが200のとき")

    def test_create_tag_empty_input(self):
        # APIの実行
        url = "/api/v1/household/tags/"
        data = {}
        response = self.client.post(url, data)

        # レスポンスの評価
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST, "HTTPレスポンスステータスコードが200のとき")
        self.assertEqual(response.data["name"][0],
                         "この項目は必須です。", "タグの名前が空のとき")
        self.assertEqual(response.data["account_uuid"][0],
                         "この項目は必須です。", "タグのアカウントが空のとき")

    def test_create_book_illegal_input(self):
        # 不正な入力値を作成
        name = "a" * 51
        color = "a" * 21

        # APIの実行
        url = "/api/v1/household/tags/"
        data = {"name": name, "color": color,
                "account_uuid": self.login_user.uuid}
        response = self.client.post(url, data)

        # レスポンスの評価
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST, "HTTPレスポンスステータスコードが200のとき")
        self.assertEqual(response.data["name"][0],
                         "この項目が50文字より長くならないようにしてください。", "タグの名前が51文字以上のとき")
        self.assertEqual(response.data["color"][0],
                         "この項目が20文字より長くならないようにしてください。", "タグの色が21文字以上のとき")
