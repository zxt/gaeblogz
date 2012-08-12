import views

routes = [('/', views.BlogHandler),
    ('/admin', views.AdminHandler),
    ('/(\d+)', views.PostHandler),
    ('/new', views.NewHandler),
    ('/edit/(\d+)', views.EditHandler),
]
