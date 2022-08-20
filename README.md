# Django Backend with Swagger UI
- 安裝套件
- 建立 Model 和 ORM 操作
- 建立 API
- drf-yasg swagger UI


## 安裝套件
主要使用到的套件為
- Django
- djangorestframework
- django-cors-headers
- drf-yasg
- mysqlclient

建議使用 virtualenv 之類的虛擬環間安裝套件，避免影響到本地端的其他專案

套件安裝方法為 requirements.txt 或是可以透過 pip 逐一根據需求安裝
```
pip3 install -r requirements.txt
```

套件安裝好後須先建立 Django 專案 `startproject app` 和服務 `startapp core`
```
.
├── app
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── main.py
├── manage.py
└── requirements.txt
```

需要加入到 /app/settings.py 中
```python
...

SECRET_KEY = 'django-insecure-+c@1nds$p9yfw26#^+&a#asv)p-oizr)lrsmbl&bow!#=!qd4y'

...

INSTALLED_APPS = [
    ...,

    # REST API
    'rest_framework',

    # Cross-Origin Resource Sharing
    'corsheaders',

    # Swagger UId
    'drf_yasg',

    # core app
    'core',
]

...

MIDDLEWARE = [
    ...,
    
    "corsheaders.middleware.CorsMiddleware",
]

...

# If True, all origins will be allowed
CORS_ALLOW_ALL_ORIGINS = True
```

建立一個 mysql 資料庫 "order_ms" ，並且設定與資料庫的連接，請參考 https://www.delftstack.com/zh-tw/howto/django/django-mysqldb/ 設定

## 建立 Model 和 ORM 操作
根據物件導向程式設計，大多數時候都是對物件進行操作，因此我們會將物件寫在 core/models.py 中，而在 models.py 的物件時常都和資料表有所關聯，例如 User 資料表與 User 物件有強烈關係
因此透過物件關聯對映 (ORM) 可以幫助我們將建立好的物件直接轉換成資料表，並且若底層資料庫有需要替換時，也可透過 ORM 自動生成，減少手動創建的成本，也可解決資料庫與物件無法對應的錯誤
![image](https://user-images.githubusercontent.com/22998999/185399594-7ab34333-b35a-4968-9947-61556b1142d0.png)

ORM 介紹：https://medium.com/tds-note/orm-v-s-sql-91e003089a61

Django 只要設定好上面的資料庫連線，就會自動進行 ORM，因此我們需先在 core/models.py 中建立一個 Order 的物件 (id、建立時間、最後修改時間及訂單中的物品)

```python
class Order(models.Model):
    
    order_id = models.AutoField(auto_created=True, primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)
    list_of_items = models.TextField(max_length=1000)
```

執行 makemigrations 在 migrations 目錄下生成紀錄 models 變動的 .py 檔，完成後再執行 migrate 操作將改動寫入資料庫
```shell
python manage.py makemigrations
python manage.py migrate
```

若過程沒有錯誤訊息則可以看到

![](https://i.imgur.com/7qbnspf.png)

## 建立 API

當我們收到 Request 中帶有 Order 的 JSON 時，我們需要透過 Serializer 幫助我們做 JSON 與 Order 物件之間的轉換，或是在 Response 時需要把 Order 物件轉成 JSON 回傳時，也會需要 Serializer，
因此我們需要建立 core/serializers.py
```
core
|-- migrations
|-- __init__.py
|-- admin.py
|-- apps.py
|-- models.py
|-- serializers.py (新增)
|-- tests.py
|-- urls.py
|-- views.py
```

serializers.py 貼上以下程式碼
```python
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
```

view 是 API request 進來時會呼叫的 function，主要處理業務邏輯以及回傳資料
我們在 core/views.py 建立了一個 view class，並且繼承了 viewsets.ModelViewSet，即可自動對應至 RESTful API 的各個 Request type
```python
class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
```
rest-framework 也有提供其他種 API 接口可以繼承，細節可參考 https://www.django-rest-framework.org/

完成以上之後，只差 URL 的建立，需在 core/urls.py 增加以下程式碼
- orders/: 代表建立或取得所有的 order
- orders/<int:pk>: 因為有帶入特定的 id，因此可查/修/刪特定的 order
```python
order_list = OrdersViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
order_detail = OrdersViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('orders/', order_list, name='order-list'),
    path('orders/<int:pk>/', order_detail, name='order-detail'),

]
```

最後在 app/urls.py 加上 core 服務的 API 路徑
```python
...

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # core 服務的 API 路徑
    path('core/', include('core.urls'))
]
...

```

完成後執行專案
```shell
python manage.py runserver
```
![](https://i.imgur.com/pDuHY2P.png)

執行成功後顯示可以在 http://127.0.0.1:8000 訪問網頁，那我們根據剛剛的設定可以到 http://127.0.0.1:8000/core/orders/ 查看服務是不是正常運作，若沒有問題則可以看到以下畫面
![](https://i.imgur.com/BvPj88Z.png)

## drf-yasg Swagger UI
我們採用 drf-yasg 來實現 Swagger UI https://drf-yasg.readthedocs.io/en/stable/

到 app/urls.py 中加上 drf-yasg 的設定，除了設定版本之外，之後可以透過 127.0.0.1:8000/swagger 以及 127.0.0.1:8000/redoc 得到可操作的文件
```python
schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls'))
]

urlpatterns += [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

```

完成後透過指令啟動 server
```shell
python manage.py runserver
```

到 http://127.0.0.1:8000/swagger/ 即可得到一個網頁包含所有可以操作的 API
![](https://i.imgur.com/kMgyOe2.jpg)

或是到 http://127.0.0.1:8000/redoc/ 也可以得到類似的網頁
![](https://i.imgur.com/xBxQKlC.jpg)
