import views

routes = [('/', views.BlogHandler),
    ('/admin', views.AdminHandler),
    ('/new', views.NewHandler),
    ('/edit/(\w+(?:-\w+)*)', views.EditHandler),
    ('/(\w+(?:-\w+)*)', views.PostHandler),
]
