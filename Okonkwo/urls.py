from django.urls import path

from . import views


urlpatterns = [

    # HOME

    path(
        "",
        views.home,
        name="home",
    ),

    # ABOUT

    path(
        "about/",
        views.about,
        name="about",
    ),

    # RESEARCH

    path(
        "research/",
        views.research,
        name="research",
    ),

       # PUBLICATIONS

    path(
        "publications/",
        views.publications,
        name="publications",
    ),

    # PUBLICATION PDF DOWNLOAD

    path(
        "publications/<int:pk>/download/",
        views.publication_download,
        name="publication_download",
    ),
    # TEAM

    path(
        "team/",
        views.team,
        name="team",
    ),

    # Foundation

    path("foundation/", views.foundation, name="foundation"),
    # CONTACT

    path(
        "contact/",
        views.contact,
        name="contact",
    ),

    # OTHER PAGES

    path(
        "posts/",
        views.posts_list,
        name="posts_list",
    ),

    path(
        "papers_list/",
        views.papers_list,
        name="papers_list",
    ),

    path(
        "featured_list/",
        views.featured_list,
        name="featured_list",
    ),
    path(
    "blog/",
    views.blog,
    name="blog"
    ),

path(
    "blog/<int:pk>/",
    views.blog_detail,
    name="blog_detail"
    ),

]