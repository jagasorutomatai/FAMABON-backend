from apiv1.tests import factories
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken


class TestBookViews(APITestCase):

    # ===============================
    # 正常系テスト　　　　　　　　　|
    # ===============================
    def setUp(self):
        # テスト用のデータ作成
        self.login_user = factories.AccountFactory(
            username="anotheruser", email="anotheruser@sample.com", password="anotheruserpassword")
        self.another_user = factories.AccountFactory(
            username="loginuser", email="loginuser@sample.com", password="loginuserpassword")

        # ログイン処理
        token = str(AccessToken.for_user(self.login_user))
        self.client.credentials(HTTP_AUTHORIZATION='jwt {0}'.format(token))

    def test_get_book_list(self):
        # テスト用データの作成
        tag = factories.TagFactory(account=self.login_user)
        factories.BookFactory(account=self.login_user, tag=tag)
        factories.BookFactory(account=self.login_user, tag=tag)

        # APIの実行
        url = "/api/v1/household/books/"
        response = self.client.get(url)

        # レスポンスの評価
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK, "HTTPレスポンスステータスコードが200のとき")
        self.assertEqual(len(response.data), 2, "取得した帳簿が2件のとき")

    def test_get_filter_book_list(self):
        # テスト用データの作成
        tag_tag1 = factories.TagFactory(name="tag1", account=self.login_user)
        tag_tag2 = factories.TagFactory(name="tag2", account=self.login_user)
        factories.BookFactory(title="test title 2020-02-15",
                              date="2020-02-15", account=self.login_user, tag=tag_tag1)
        factories.BookFactory(title="test title 2020-03-15",
                              date="2020-03-15", account=self.login_user, tag=tag_tag1)
        factories.BookFactory(title="test title 2020-04-15",
                              date="2020-04-15", account=self.login_user, tag=tag_tag2)

        # APIの実行
        url = "/api/v1/household/books/"
        data = {"date_after": "2020-02-14", "date_before": "2020-02-16"}
        filterd_date_response = self.client.get(url, data)
        data = {"title": "test title 2020-03-15"}
        filterd_title_response = self.client.get(url, data)
        data = {"tag": tag_tag2.name}
        filterd_tag_response = self.client.get(url, data)

        # レスポンスの評価(filterd_date_response)
        self.assertEqual(filterd_date_response.status_code,
                         status.HTTP_200_OK, "HTTPレスポンスステータスコードが200のとき")
        self.assertEqual(len(filterd_date_response.data),
                         1, "取得した帳簿が1件のとき")
        self.assertEqual(filterd_date_response.data[0]["date"], "2020-02-15",
                         "帳簿の日付が2020-02-15のとき")

        # レスポンスの評価(filterd_title_response)
        self.assertEqual(filterd_title_response.status_code,
                         status.HTTP_200_OK, "HTTPレスポンスステータスコードが200のとき")
        self.assertEqual(len(filterd_title_response.data),
                         1, "取得した帳簿が1件のとき")
        self.assertEqual(filterd_title_response.data[0]["title"], "test title 2020-03-15",
                         "帳簿のタイトルが「test title 2020-03-15」のとき")

        # レスポンスの評価(filterd_tag_response)
        self.assertEqual(filterd_tag_response.status_code,
                         status.HTTP_200_OK, "HTTPレスポンスステータスコードが200のとき")
        self.assertEqual(len(filterd_tag_response.data),
                         1, "取得した帳簿が1件のとき")
        self.assertEqual(filterd_tag_response.data[0]["tag"]["name"], "tag2",
                         "帳簿のタグの名前が「tag2」のとき")

    def test_get_book_detail(self):
        # テスト用データの作成
        tag_tag1 = factories.TagFactory(name="tag1", account=self.login_user)
        book = factories.BookFactory(title="test title", description="test description", money=1000,
                                     date="2020-02-15", account=self.login_user, tag=tag_tag1)

        # APIの実行
        url = "/api/v1/household/books/{}/".format(book.uuid)
        response = self.client.get(url)

        # レスポンスの評価(filterd_tag_response)
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK, "HTTPレスポンスステータスコードが200のとき")
        self.assertEqual(response.data["title"],
                         "test title", "帳簿のタイトルが「test title」のとき")
        self.assertEqual(response.data["description"],
                         "test description", "帳簿の説明が「test description」のとき")
        self.assertEqual(response.data["money"],
                         1000, "帳簿の金額が「1000」のとき")
        self.assertEqual(response.data["date"],
                         "2020-02-15", "帳簿の日付が「2020-02-15」のとき")
        self.assertEqual(response.data["account"],
                         self.login_user.uuid, "帳簿のアカウントが「{}」のとき".format(self.login_user.uuid))
        self.assertEqual(response.data["tag"]["name"],
                         tag_tag1.name, "帳簿のタグの名前が「tag1」のとき")

    def test_create_book(self):
        # テスト用データの作成
        tag_tag1 = factories.TagFactory(name="tag1", account=self.login_user)

        # APIの実行
        url = "/api/v1/household/books/"
        data = {"title": "test title", "description": "test description",
                "money": 1000, "date": "2020-02-15", "tag_uuid": tag_tag1.uuid, "account_uuid": self.login_user.uuid}
        response = self.client.post(url, data)

        # レスポンスの評価(filterd_tag_response)
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED, "HTTPレスポンスステータスコードが200のとき")
        self.assertEqual(response.data["title"],
                         "test title", "帳簿のタイトルが「test title」のとき")
        self.assertEqual(response.data["description"],
                         "test description", "帳簿の説明が「test description」のとき")
        self.assertEqual(response.data["money"],
                         1000, "帳簿の金額が「1000」のとき")
        self.assertEqual(response.data["date"],
                         "2020-02-15", "帳簿の日付が「2020-02-15」のとき")
        self.assertEqual(response.data["account"],
                         self.login_user.uuid, "帳簿のアカウントが「{}」のとき".format(self.login_user.uuid))
        self.assertEqual(response.data["tag"]["name"],
                         tag_tag1.name, "帳簿のタグの名前が「tag1」のとき")

    def test_update_book(self):
        # テスト用データの作成
        tag_tag1 = factories.TagFactory(name="tag1", account=self.login_user)
        tag_tag2 = factories.TagFactory(name="tag2", account=self.login_user)
        book = factories.BookFactory(title="test title", description="test description", money=1000,
                                     date="2020-02-15", account=self.login_user, tag=tag_tag1)

        # APIの実行
        url = "/api/v1/household/books/{}/".format(book.uuid)
        data = {"title": "updated test title", "description": "updated test description",
                "money": 2000, "date": "2020-03-15", "tag_uuid": tag_tag2.uuid, "account_uuid": self.login_user.uuid}
        response = self.client.put(url, data)

        # レスポンスの評価(filterd_tag_response)
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK, "HTTPレスポンスステータスコードが200のとき")
        self.assertEqual(response.data["title"],
                         "updated test title", "帳簿のタイトルが「updated test title」のとき")
        self.assertEqual(response.data["description"],
                         "updated test description", "帳簿の説明が「updated test description」のとき")
        self.assertEqual(response.data["money"],
                         2000, "帳簿の金額が「1000」のとき")
        self.assertEqual(response.data["date"],
                         "2020-03-15", "帳簿の日付が「2020-03-15」のとき")
        self.assertEqual(response.data["tag"]["name"],
                         tag_tag2.name, "帳簿のタグの名前が「tag2」のとき")

    def test_get_book_total(self):
        # テスト用データの作成
        tag_tag1 = factories.TagFactory(name="tag1", account=self.login_user)
        factories.BookFactory(title="title login_user", money=1000,
                              account=self.login_user, tag=tag_tag1)
        factories.BookFactory(title="title another_user", money=2000,
                              account=self.login_user, tag=tag_tag1)

        # APIの実行
        url = "/api/v1/household/books/total/"
        response = self.client.get(url)

        # レスポンスの評価
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK, "HTTPレスポンスステータスコードが200のとき")
        self.assertEqual(response.data["total"],
                         3000, "帳簿の金額の合計が「3000」のとき")

    def test_get_filter_book_total(self):
        # テスト用データの作成
        tag_tag1 = factories.TagFactory(name="tag1", account=self.login_user)
        factories.BookFactory(money=1000, date="2020-02-15",
                              account=self.login_user, tag=tag_tag1)
        factories.BookFactory(money=2000, date="2020-03-15",
                              account=self.login_user, tag=tag_tag1)
        factories.BookFactory(money=3000, date="2020-04-15",
                              account=self.login_user, tag=tag_tag1)

        # APIの実行
        url = "/api/v1/household/books/total/"
        data = {"date_after": "2020-02-16", "date_before": "2020-04-16"}
        response = self.client.get(url, data)

        # レスポンスの評価
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK, "HTTPレスポンスステータスコードが200のとき")
        self.assertEqual(response.data["total"],
                         5000, "帳簿の金額の合計が「3000」のとき")

    def test_get_book_totalByDate(self):
        tag_tag1 = factories.TagFactory(name="tag1", account=self.login_user)
        factories.BookFactory(money=1000, date="2020-02-15",
                              account=self.login_user, tag=tag_tag1)
        factories.BookFactory(money=2000, date="2020-02-15",
                              account=self.login_user, tag=tag_tag1)
        factories.BookFactory(money=3000, date="2020-03-15",
                              account=self.login_user, tag=tag_tag1)
        factories.BookFactory(money=4000, date="2020-03-15",
                              account=self.login_user, tag=tag_tag1)
        factories.BookFactory(money=5000, date="2020-03-15",
                              account=self.login_user, tag=tag_tag1)
        factories.BookFactory(money=6000, date="2020-04-15",
                              account=self.login_user, tag=tag_tag1)

        # APIの実行
        url = "/api/v1/household/books/totalByDate/"
        response = self.client.get(url)

        # レスポンスの評価
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK, "HTTPレスポンスステータスコードが200のとき")
        self.assertEqual(len(response.data),
                         3, "取得した帳簿の合計データ数が3件のとき")
        self.assertEqual(response.data[0],
                         {"date": "2020-02-15", "total": 3000}, "帳簿の「2020-02-15」の合計が3000のとき")
        self.assertEqual(response.data[1],
                         {"date": "2020-03-15", "total": 12000}, "帳簿の「2020-03-15」の合計が12000のとき")
        self.assertEqual(response.data[2],
                         {"date": "2020-04-15", "total": 6000}, "帳簿の「2020-04-15」の合計が6000のとき")

    def test_get_filter_book_totalByDate(self):
        tag_tag1 = factories.TagFactory(name="tag1", account=self.login_user)
        factories.BookFactory(money=1000, date="2020-02-15",
                              account=self.login_user, tag=tag_tag1)
        factories.BookFactory(money=2000, date="2020-02-15",
                              account=self.login_user, tag=tag_tag1)
        factories.BookFactory(money=3000, date="2020-03-15",
                              account=self.login_user, tag=tag_tag1)
        factories.BookFactory(money=4000, date="2020-03-15",
                              account=self.login_user, tag=tag_tag1)
        factories.BookFactory(money=5000, date="2020-03-15",
                              account=self.login_user, tag=tag_tag1)
        factories.BookFactory(money=6000, date="2020-04-15",
                              account=self.login_user, tag=tag_tag1)

        # APIの実行
        url = "/api/v1/household/books/totalByDate/"
        data = {"date_after": "2020-02-14", "date_before": "2020-03-16"}
        response = self.client.get(url, data)

        # レスポンスの評価
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK, "HTTPレスポンスステータスコードが200のとき")
        self.assertEqual(len(response.data),
                         2, "取得した帳簿の合計データ数が2件のとき")
        self.assertEqual(response.data[0],
                         {"date": "2020-02-15", "total": 3000}, "帳簿の「2020-02-15」の合計が3000のとき")
        self.assertEqual(response.data[1],
                         {"date": "2020-03-15", "total": 12000}, "帳簿の「2020-03-15」の合計が12000のとき")

    def test_get_book_totalByTag(self):
        tag_tag1 = factories.TagFactory(name="tag1", account=self.login_user)
        tag_tag2 = factories.TagFactory(name="tag2", account=self.login_user)
        tag_tag3 = factories.TagFactory(name="tag3", account=self.login_user)

        factories.BookFactory(money=1000, date="2020-02-15",
                              account=self.login_user, tag=tag_tag1)
        factories.BookFactory(money=2000, date="2020-02-16",
                              account=self.login_user, tag=tag_tag2)
        factories.BookFactory(money=3000, date="2020-02-17",
                              account=self.login_user, tag=tag_tag3)
        factories.BookFactory(money=4000, date="2020-02-18",
                              account=self.login_user, tag=tag_tag1)
        factories.BookFactory(money=5000, date="2020-02-19",
                              account=self.login_user, tag=tag_tag2)
        factories.BookFactory(money=6000, date="2020-02-20",
                              account=self.login_user, tag=tag_tag3)

        # APIの実行
        url = "/api/v1/household/books/totalByTag/"
        response = self.client.get(url)

        # レスポンスの評価
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK, "HTTPレスポンスステータスコードが200のとき")
        self.assertEqual(response.data[0],
                         {"tag__name": "tag3", "tag__color": "grey", "total": 9000}, "タグ「tag3」の合計が9000のとき")
        self.assertEqual(response.data[1],
                         {"tag__name": "tag2", "tag__color": "grey", "total": 7000}, "タグ「tag3」の合計が9000のとき")
        self.assertEqual(response.data[2],
                         {"tag__name": "tag1", "tag__color": "grey", "total": 5000}, "タグ「tag3」の合計が9000のとき")

    def test_get_filter_book_totalByTag(self):
        tag_tag1 = factories.TagFactory(name="tag1", account=self.login_user)
        tag_tag2 = factories.TagFactory(name="tag2", account=self.login_user)
        tag_tag3 = factories.TagFactory(name="tag3", account=self.login_user)

        factories.BookFactory(money=1000, date="2020-02-15",
                              account=self.login_user, tag=tag_tag1)
        factories.BookFactory(money=2000, date="2020-02-16",
                              account=self.login_user, tag=tag_tag2)
        factories.BookFactory(money=3000, date="2020-02-17",
                              account=self.login_user, tag=tag_tag3)
        factories.BookFactory(money=4000, date="2020-02-18",
                              account=self.login_user, tag=tag_tag1)
        factories.BookFactory(money=5000, date="2020-02-19",
                              account=self.login_user, tag=tag_tag2)
        factories.BookFactory(money=6000, date="2020-02-20",
                              account=self.login_user, tag=tag_tag3)

        # APIの実行
        url = "/api/v1/household/books/totalByTag/"
        data = {"date_after": "2020-02-16", "date_before": "2020-02-19"}
        response = self.client.get(url, data)

        # レスポンスの評価
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK, "HTTPレスポンスステータスコードが200のとき")
        self.assertEqual(response.data[0],
                         {"tag__name": "tag2", "tag__color": "grey", "total": 7000}, "タグ「tag3」の合計が9000のとき")
        self.assertEqual(response.data[1],
                         {"tag__name": "tag1", "tag__color": "grey", "total": 4000}, "タグ「tag3」の合計が9000のとき")
        self.assertEqual(response.data[2],
                         {"tag__name": "tag3", "tag__color": "grey", "total": 3000}, "タグ「tag3」の合計が9000のとき")

    # ===============================
    # 異常系テスト　　　　　　　　　|
    # ===============================

    def test_get_book_list_anotheruser(self):
        # テスト用データの作成
        tag_tag1 = factories.TagFactory(name="tag1", account=self.login_user)
        tag_tag2 = factories.TagFactory(name="tag2", account=self.another_user)
        factories.BookFactory(title="title login_user",
                              account=self.login_user, tag=tag_tag1)
        factories.BookFactory(title="title another_user",
                              account=self.another_user, tag=tag_tag2)

        # APIの実行
        url = "/api/v1/household/books/"
        response = self.client.get(url)

        # レスポンスの評価
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK, "HTTPレスポンスステータスコードが200のとき")
        self.assertEqual(len(response.data), 1, "取得した帳簿が1件のとき")
        self.assertEqual(response.data[0]["title"],
                         "title login_user", "帳簿のタイトルが「title another_user」のとき")

    def test_get_book_detail_anotheruser(self):
        # テスト用データの作成
        tag = factories.TagFactory(account=self.another_user)
        book = factories.BookFactory(title="title another_user",
                                     account=self.another_user, tag=tag)

        # APIの実行
        url = "/api/v1/household/books/{}/".format(book.uuid)
        response = self.client.get(url)

        # レスポンスの評価
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST, "HTTPレスポンスステータスコードが400のとき")

    def test_update_book_anotheruser(self):
        # テスト用データの作成
        tag = factories.TagFactory(account=self.login_user)
        book = factories.BookFactory(title="title another_user",
                                     account=self.another_user, tag=tag)

        # APIの実行
        url = "/api/v1/household/books/{}/".format(book.uuid)
        data = {"title": "updated test title", "description": "updated test description",
                "money": 2000, "date": "2020-03-15", "tag_uuid": tag.uuid, "account_uuid": self.another_user.uuid}
        response = self.client.put(url, data)

        # レスポンスの評価
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST, "HTTPレスポンスステータスコードが400のとき")

    def test_create_book_empty_input(self):
        # APIの実行
        url = "/api/v1/household/books/"
        data = {}
        response = self.client.post(url, data)

        # レスポンスの評価
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST, "HTTPレスポンスステータスコードが400のとき")
        self.assertEqual(response.data["title"][0],
                         "この項目は必須です。", "帳簿のタイトルが空のとき")
        self.assertEqual(response.data["money"][0],
                         "この項目は必須です。", "帳簿の金額が空のとき")
        self.assertEqual(response.data["date"][0],
                         "この項目は必須です。", "帳簿の日付が空のとき")
        self.assertEqual(response.data["tag_uuid"][0],
                         "この項目は必須です。", "帳簿のタグが空のとき")
        self.assertEqual(response.data["account_uuid"][0],
                         "この項目は必須です。", "帳簿のアカウントが空のとき")

    def test_create_book_illegal_input(self):
        # テスト用データの作成
        tag_tag1 = factories.TagFactory(name="tag1", account=self.login_user)

        # 不正な入力値を作成
        title = "a" * 51
        money = 2147483648
        date = "2020-02-21-00:00"

        # APIの実行
        url = "/api/v1/household/books/"
        data = {"title": title,
                "money": money, "date": date, "tag_uuid": tag_tag1.uuid, "account_uuid": self.login_user.uuid}
        response = self.client.post(url, data)

        # レスポンスの評価
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST, "HTTPレスポンスステータスコードが400のとき")
        self.assertEqual(response.data["title"][0],
                         "この項目が50文字より長くならないようにしてください。", "帳簿のタイトルが50文字以上のとき")
        self.assertEqual(response.data["money"][0],
                         "この値は2147483647以下にしてください。", "帳簿の金額が2147483648以上のとき")
        self.assertEqual(response.data["date"][0],
                         "日付の形式が違います。以下のどれかの形式にしてください: YYYY-MM-DD。", "帳簿の日付が不正なフォーマットのとき")

        # 不正な入力値を作成
        title = "a" * 51
        money = "string"
        date = "2020-02-21-00:00"

        # APIの実行
        data = {"title": title,
                "money": money, "date": date, "tag_uuid": tag_tag1.uuid, "account_uuid": self.login_user.uuid}
        response = self.client.post(url, data)

        # レスポンスの評価
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST, "HTTPレスポンスステータスコードが400のとき")
        self.assertEqual(response.data["money"][0],
                         "有効な整数を入力してください。", "帳簿の金額が文字列のとき")
