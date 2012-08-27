import os

import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.api import memcache

from models import *
import utils

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                              autoescape=True)

class BaseHandler(webapp2.RequestHandler):
    def error(self, code, page):
        super(BaseHandler, self).error(code)
        if code == 404:
            self.render("404.html",
                         page=page)
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **kw):
        t = jinja_env.get_template(template)
        return t.render(kw)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class BlogHandler(BaseHandler):
    def get(self):
        posts = get_published_posts()
        for p in posts:
            p.content = utils.md_to_html(p.content)
        self.render("blog.html",
                     blog_posts=posts)

class PostHandler(BaseHandler):
    def get(self, slug):
        post = memcache.get("post_"+slug) or \
               Post.gql("WHERE slug = :1", slug).get()
        if post is None:
            self.error(404, slug)
        else:
            memcache.set("post_"+slug, post)
            post.content = utils.md_to_html(post.content)
            self.render("post.html",
                         post=post)

class NewHandler(BaseHandler):
    def render_page(self, subject="", content="", draft=False, error=""):
        self.render("newpost.html",
                    subject=subject,
                    content=utils.md_to_html(content),
                    draft=draft,
                    error=error)

    def get(self):
        if users.is_current_user_admin():
            self.render_page()
        else:
            self.redirect(login("/new"))

    def post(self):
        subject = self.request.get("subject")
        slug = utils.unique_slugify(" ".join(subject.split()[:10]),
                                    get_all_slugs())
        content = self.request.get("content")
        draft = True if self.request.get("draft-checkbox") else False

        if subject:
            post = Post(subject=subject,
                        slug=slug,
                        content=content,
                        draft=draft)
            post.put()
            memcache.delete("posts")
            self.redirect('/%s' % post.slug)
        else:
            error = "Your post needs title!"
            self.render_page(subject, content, draft, error)

class EditHandler(BaseHandler):
    def render_page(self, subject="", content="",
                    draft=False, error=""):
        self.render("edit.html",
                     subject=subject,
                     content=content,
                     draft=draft,
                     error=error)

    def get(self, slug):
        post = memcache.get("post_"+slug) or \
               Post.gql("WHERE slug = :1", slug).get()
        if post is None:
            self.error(404, slug)
        else:
            memcache.set("post_"+slug, post)
            subject = post.subject
            content = post.content
            draft = post.draft
            self.render_page(subject, content, draft)

    def post(self, slug):
        subject = self.request.get("subject")
        content = self.request.get("content")
        draft = True if self.request.get("draft-checkbox") else False

        if subject:
            post = Post.gql("WHERE slug = :1", slug).get()
            post.subject = subject
            post.content = content
            post.draft = draft
            post.put()
            memcache.set("post_"+post.slug, post)
            memcache.delete("posts")
            self.redirect('/%s' % post.slug)
        else:
            error = "Your post needs a title!"
            self.render_page(subject, content, draft, error)

def login(dest_url=None):
    return users.create_login_url(dest_url)

def logout(dest_url):
    return users.create_logout_url(dest_url)

class AdminHandler(BaseHandler):
    def render_page(self, prev_draft_page=0, next_draft_page=0,
                    prev_pub_page=0, next_pub_page=0,
                    drafts=None, published=None):
        self.render("admin.html",
                     prev_draft_page=prev_draft_page,
                     next_draft_page=next_draft_page,
                     prev_pub_page=prev_pub_page,
                     next_pub_page=next_pub_page,
                     drafts=drafts,
                     published=published)

    def get(self):
        limit = 10

        draft_page = self.request.get("draft_page")
        draft_page = int(draft_page) if draft_page.isdigit() else 0
        drafts = get_draft_posts(draft_page*limit, limit)

        prev_draft_page = draft_page - 1
        ndp = get_draft_posts((draft_page+1)*limit, limit)
        if ndp:
            next_draft_page = draft_page + 1
        else:
            next_draft_page = -1

        pub_page = self.request.get("pub_page")
        pub_page = int(pub_page) if pub_page.isdigit() else 0
        published = get_published_posts(pub_page*limit, limit)

        prev_pub_page = pub_page - 1
        npp = get_published_posts((pub_page+1)*limit, limit)
        if npp:
            next_pub_page = pub_page + 1
        else:
            next_pub_page = -1

        self.render_page(prev_draft_page,
                         next_draft_page,
                         prev_pub_page,
                         next_pub_page,
                         drafts,
                         published)
