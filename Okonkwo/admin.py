from django.contrib import admin
from django.utils.html import format_html

from .models import (
    TeamMember,
    Publication,
    UpdateProfile,
    BlogPost,
    BlogComment
)



# TEAM MEMBERS


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "category",
        "position",
        "email",
        "order",
    )

    list_filter = (
        "category",
    )

    search_fields = (
        "name",
        "position",
        "email",
        "category",
    )

    list_editable = (
        "order",
    )

    ordering = (
        "category",
        "order",
        "name",
    )

    # =====================================================
    # CATEGORY SUGGESTIONS
    # =====================================================

    class Media:

        js = (
            "admin/js/team_member_category.js",
        )



# PUBLICATIONS


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "authors",
        "short_abstract",
        "date_uploaded",
        "download_count",
        "featured",
    )

    list_filter = (
        "publication_type",
        "featured",
        "date_uploaded",
    )

    search_fields = (
        "title",
        "authors",
        "abstract",
    )

    list_editable = (
        "featured",
    )

    def short_abstract(self, obj):

        if obj.abstract:

            return (
                obj.abstract[:120] + "..."
                if len(obj.abstract) > 120
                else obj.abstract
            )

        return "-"

    short_abstract.short_description = "Abstract"

    fieldsets = (

        (
            "Publication Information",
            {
                "fields": (
                    "title",
                    "authors",
                    "journal",
                    "year",
                    "publication_type",
                    "abstract",
                    "image",
                    "pdf_file",
                )
            }
        ),

        (
            "Download Statistics",
            {
                "fields": (
                    "download_count",
                ),
                "description": (
                    "The download count increases automatically "
                    "whenever a visitor downloads the full-text file."
                ),
            }
        ),

        (
            "Publication Links",
            {
                "fields": (
                    "journal_url",
                    "google_scholar_url",
                    "researchgate_url",
                    "doi",
                    "publication_url",
                ),
                "description": (
                    "Add the direct links to the journal, "
                    "Google Scholar, ResearchGate, DOI, "
                    "and publication page."
                ),
            }
        ),

        (
            "Display Options",
            {
                "fields": (
                    "featured",
                    "date_uploaded",
                )
            }
        ),

    )

    readonly_fields = (
        "download_count",
        "date_uploaded",
    )



# UPDATE PROFILE


@admin.register(UpdateProfile)
class UpdateProfileAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "title",
        "institution",
        "email",
    )



# BLOG POSTS


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):

    list_display = (
        "post_title",
        "label",
        "post_file_preview",
        "post_count",
        "date_uploaded",
    )

    list_filter = (
        "label",
        "date_uploaded",
    )

    search_fields = (
        "post_title",
        "label",
        "abstract",
    )

    ordering = (
        "-date_uploaded",
    )

    readonly_fields = (
        "date_uploaded",
        "post_file_preview",
        "post_count",
    )

    fieldsets = (

        (
            "Blog Post Information",
            {
                "fields": (
                    "post_title",
                    "label",
                    "abstract",
                    "header_picture",
                )
            }
        ),

        (
            "Post Statistics",
            {
                "fields": (
                    "post_count",
                ),
                "description": (
                    "The Post Count increases automatically "
                    "whenever a visitor opens this blog post."
                ),
            }
        ),

        (
            "Upload Information",
            {
                "fields": (
                    "date_uploaded",
                )
            }
        ),

    )

    # =====================================================
    # BLOG POST FILE PREVIEW
    # =====================================================

    def post_file_preview(self, obj):

        if not obj.header_picture:
            return "No file"

        file_name = obj.header_picture.name.lower()

        image_extensions = (
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".webp",
            ".bmp",
            ".tiff",
            ".tif",
        )

        if file_name.endswith(image_extensions):

            return format_html(
                '<img src="{}" width="120" height="80" '
                'style="object-fit: cover; border-radius: 6px;" />',
                obj.header_picture.url
            )

        return format_html(
            '<a href="{}" target="_blank">📄 Open uploaded document</a>',
            obj.header_picture.url
        )

    post_file_preview.short_description = "Post File"



# BLOG COMMENTS


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):

    list_display = (
        "blog_post",
        "name",
        "email",
        "comment_preview",
        "approved",
        "date_commented",
    )

    list_filter = (
        "approved",
        "date_commented",
    )

    search_fields = (
        "name",
        "email",
        "comment",
        "blog_post__post_title",
    )

    list_editable = (
        "approved",
    )

    readonly_fields = (
        "blog_post",
        "name",
        "email",
        "comment",
        "date_commented",
    )

    fields = (
        "blog_post",
        "name",
        "email",
        "comment",
        "approved",
        "date_commented",
    )

    ordering = (
        "-date_commented",
    )

    def comment_preview(self, obj):

        if len(obj.comment) > 25:

            return obj.comment[:25] + "..."

        return obj.comment

    comment_preview.short_description = "Comment"

    def changeform_view(
        self,
        request,
        object_id=None,
        form_url="",
        extra_context=None
    ):

        extra_context = extra_context or {}

        extra_context["show_save_and_add_another"] = False
        extra_context["show_save_and_continue"] = False

        return super().changeform_view(
            request,
            object_id,
            form_url,
            extra_context=extra_context,
        )