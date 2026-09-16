from django.db.models import Sum

from .models import (
    Publication,
    BlogPost,
)


def admin_dashboard(request):

    # =========================================================
    # PUBLICATIONS
    # =========================================================

    publications = Publication.objects.all()

    latest_publication = publications.order_by(
        "-date_uploaded"
    ).first()


    # =========================================================
    # TOTAL PUBLICATION DOWNLOADS
    # =========================================================

    total_downloads = publications.aggregate(
        total=Sum("download_count")
    )["total"] or 0


    # =========================================================
    # TOTAL BLOG POSTS
    # =========================================================

    total_blog_posts = BlogPost.objects.count()


    # =========================================================
    # DASHBOARD DATA
    # =========================================================

    return {

        "total_publications":
            publications.count(),

        "total_downloads":
            total_downloads,

        "latest_publication":
            latest_publication,

        "total_blog_posts":
            total_blog_posts,

    }
