from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, Http404
from django.db import models
from django.db.models import F
from django.core.paginator import Paginator
import os
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .models import (
    UpdateProfile,
    TeamMember,
    Publication,
    BlogPost,
    BlogComment,
)



# HOME


def home(request):

    profile = UpdateProfile.objects.first()

    latest_papers = Publication.objects.all()[:3]

    featured_posts = Publication.objects.filter(
        featured=True
    ).order_by(
        "-year",
        "title"
    )[:3]

    recent_blog_posts = BlogPost.objects.all().order_by(
        "-date_uploaded"
    )[:3]

    context = {
        "profile": profile,
        "featured_posts": featured_posts,
        "latest_papers": latest_papers,
        "recent_blog_posts": recent_blog_posts,
    }

    return render(
        request,
        "home.html",
        context
    )



# ABOUT


def about(request):

    profile = UpdateProfile.objects.first()

    return render(
        request,
        "about.html",
        {
            "profile": profile
        }
    )



# POSTS


def posts_list(request):

    return render(
        request,
        "posts_list.html"
    )



# PAPERS


def papers_list(request):

    return render(
        request,
        "home.html"
    )



# FEATURED


def featured_list(request):

    return render(
        request,
        "home.html"
    )



# RESEARCH


def research(request):

    profile = UpdateProfile.objects.first()

    return render(
        request,
        "research.html",
        {
            "profile": profile
        }
    )



# FOUNDATION


def foundation(request):

    profile = UpdateProfile.objects.first()

    return render(
        request,
        "foundation.html",
        {
            "profile": profile
        }
    )



# PUBLICATIONS


def publications(request):

    query = request.GET.get(
        "q",
        ""
    ).strip()

    year = request.GET.get(
        "year",
        ""
    ).strip()

    items = Publication.objects.all()

    if query:

        items = items.filter(
            models.Q(
                title__icontains=query
            )
            |
            models.Q(
                authors__icontains=query
            )
            |
            models.Q(
                journal__icontains=query
            )
        )

    if year:

        items = items.filter(
            year=year
        )

    years = (
        Publication.objects
        .values_list(
            "year",
            flat=True
        )
        .distinct()
        .order_by(
            "-year"
        )
    )

    return render(
        request,
        "publications.html",
        {
            "publications": items,
            "years": years,
            "query": query,
            "selected_year": year,
        }
    )



# PUBLICATION FULL TEXT


def publication_download(request, pk):

    publication = get_object_or_404(
        Publication,
        pk=pk
    )

    if not publication.pdf_file:

        raise Http404(
            "The full text file for this publication is not available."
        )

    file_name = publication.pdf_file.name

    extension = os.path.splitext(
        file_name
    )[1].lower()

    if extension == ".pdf":

        content_type = "application/pdf"
        disposition = "inline"

    elif extension == ".docx":

        content_type = (
            "application/vnd.openxmlformats-officedocument."
            "wordprocessingml.document"
        )

        disposition = "attachment"

    else:

        raise Http404(
            "Unsupported publication file type. "
            "Only PDF and DOCX files are supported."
        )

    try:

        publication_file = publication.pdf_file.open(
            "rb"
        )

    except FileNotFoundError:

        raise Http404(
            "The publication file could not be found."
        )

    Publication.objects.filter(
        pk=publication.pk
    ).update(
        download_count=F(
            "download_count"
        ) + 1
    )

    response = FileResponse(
        publication_file,
        content_type=content_type,
        as_attachment=False
    )

    response["Content-Disposition"] = (
        f'{disposition}; '
        f'filename="{os.path.basename(file_name)}"'
    )

    return response



# TEAM


def team(request):

    members = TeamMember.objects.all()

    return render(
        request,
        "team.html",
        {
            "team_members": members
        }
    )



# BLOG


def blog(request):

    blog_posts = BlogPost.objects.all().order_by(
        "-date_uploaded"
    )

    paginator = Paginator(
        blog_posts,
        10
    )

    page_number = request.GET.get(
        "page"
    )

    page_obj = paginator.get_page(
        page_number
    )

    recent_posts = BlogPost.objects.all().order_by(
        "-date_uploaded"
    )[:3]

    context = {
        "blog_posts": page_obj,
        "page_obj": page_obj,
        "recent_posts": recent_posts,
    }

    return render(
        request,
        "blog.html",
        context
    )



# BLOG DETAIL


def blog_detail(request, pk):

    post = get_object_or_404(
        BlogPost,
        pk=pk
    )



   
    # HANDLE COMMENT SUBMISSION
   

    if request.method == "POST":

        name = request.POST.get(
            "name",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        comment_text = request.POST.get(
            "comment",
            ""
        ).strip()

        if name and email and comment_text:

            BlogComment.objects.create(
                blog_post=post,
                name=name,
                email=email,
                comment=comment_text,
                approved=False,
            )

            return redirect(
                "blog_detail",
                pk=post.pk
            )

   
    # ONLY APPROVED COMMENTS ARE SHOWN
   

    comments = BlogComment.objects.filter(
        blog_post=post,
        approved=True
    ).order_by(
        "date_commented"
    )

    comment_count = comments.count()

   
    # RECENT BLOG POSTS
   

    recent_posts = BlogPost.objects.all().order_by(
        "-date_uploaded"
    )[:3]

   
    # CONTEXT
   

    context = {

        "post": post,

        "recent_posts": recent_posts,

        "comments": comments,

        "comment_count": comment_count,

    }

    return render(
        request,
        "blog_detail.html",
        context
    )



# CONTACT


def contact(request):

   
    # DISPLAY CONTACT PAGE
   

    if request.method != "POST":

        return render(
            request,
            "contact.html"
        )

   
    # GET FORM DATA
   

    name = request.POST.get(
        "name",
        ""
    ).strip()

    email = request.POST.get(
        "email",
        ""
    ).strip()

    phone = request.POST.get(
        "phone",
        ""
    ).strip()

    message = request.POST.get(
        "message",
        ""
    ).strip()

   
    # VALIDATE REQUIRED FIELDS
   

    if not name or not email or not message:

        messages.error(
            request,
            "Please fill in all required fields."
        )

        return redirect(
            "contact"
        )

   
    # VALIDATE EMAIL ADDRESS
   

    try:

        validate_email(
            email
        )

    except ValidationError:

        messages.error(
            request,
            "Invalid email address provided."
        )

        return redirect(
            "contact"
        )

   
    # EMAIL SUBJECT
   

    subject = (
        "Contact Form Submission - "
        "Prof. Wilfred I. Okonkwo "
    )

   
    # EMAIL CONTENT
   

    email_content = f"""
You have received a new message from the
Prof. Wilfred I. Okonkwo  website.


CONTACT FORM DETAILS


Name:
{name}

Email:
{email}

Phone:
{phone}

Message:
{message}


This message was submitted through the website.

"""

   
    # RECEIVING EMAIL ADDRESS
   

    to_email = "Your emailaddress.com"  # Replace with your email address

   
    # SEND EMAIL
   

    try:

        email_message = EmailMessage(
            subject=subject,
            body=email_content,
            from_email=None,
            to=[to_email],
            reply_to=[email],
        )

        email_message.send(
            fail_silently=False
        )

        messages.success(
            request,
            "Thanks for contacting us. We will get back to you soon!"
        )

        print(
            "CONTACT EMAIL SENT SUCCESSFULLY"
        )

    except Exception as e:

        # -------------------------------------------------
        # PRINT THE REAL ERROR IN TERMINAL
        # -------------------------------------------------

        print(
            ""
        )

        print(
            "EMAIL ERROR:"
        )

        print(
            repr(e)
        )

        print(
            ""
        )

        messages.error(
            request,
            "Sorry, your message could not be sent. Please try again later."
        )

    return redirect(
        "contact"
    )