import views

routes = [('/', views.BlogHandler),
    ('/admin', views.AdminHandler),
    ('/new', views.NewHandler),
    ('/edit/(\d+)', views.EditHandler),
    ('/(\w+(?:-\w+)+)', views.PostHandler),
]
