from django.db import models
from django.core.exceptions import ValidationError


# PUBLICATION FILE VALIDATION

def validate_publication_file(value):

    allowed_extensions = [
        ".pdf",
        ".docx",
    ]

    file_name = value.name.lower()

    if not any(
        file_name.endswith(extension)
        for extension in allowed_extensions
    ):
        raise ValidationError(
            "Only PDF (.pdf) and Microsoft Word (.docx) files are allowed."
        )


# TEAM MEMBERS

class TeamMember(models.Model):

    CATEGORY_CHOICES = [
        ("director", "Director"),
        ("professor", "Professor"),
        ("postdoc", "Postdoctoral Researcher"),
        ("phd", "PhD Student"),
        ("masters", "Master's Student"),
        ("undergraduate", "Undergraduate Student"),
        ("research_assistant", "Research Assistant"),
        ("visiting_scholar", "Visiting Scholar"),
        ("visiting_student", "Visiting Student"),
        ("alumni", "Alumni"),
        ("other", "Other"),
    ]

    name = models.CharField(
        max_length=200
    )

    position = models.CharField(
        max_length=200
    )

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default="other"
    )

    photo = models.ImageField(
        upload_to="team/",
        blank=True,
        null=True
    )

    email = models.EmailField(
        blank=True
    )

    linkedin = models.URLField(
        blank=True
    )

    order = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = [
            "order",
            "name"
        ]

    def __str__(self):
        return self.name


# PUBLICATIONS

class Publication(models.Model):

    PUBLICATION_TYPES = [
        ("journal", "Journal Article"),
        ("conference", "Conference Paper"),
        ("book", "Book / Book Chapter"),
        ("report", "Research Report"),
        ("working", "Working Paper"),
        ("other", "Other"),
    ]

    # PUBLICATION INFORMATION

    title = models.CharField(
        max_length=500
    )

    authors = models.CharField(
        max_length=500
    )

    journal = models.CharField(
        max_length=300,
        blank=True
    )

    year = models.PositiveIntegerField()

    publication_type = models.CharField(
        max_length=20,
        choices=PUBLICATION_TYPES,
        default="journal"
    )

    abstract = models.TextField(
        blank=True
    )

    # PUBLICATION IMAGE

    image = models.ImageField(
        upload_to="publications/",
        blank=True,
        null=True
    )

    # FULL TEXT FILE
    # PDF OR DOCX

    pdf_file = models.FileField(
        upload_to="publications/pdfs/",
        blank=True,
        null=True,
        verbose_name="Full Text File",
        validators=[
            validate_publication_file
        ]
    )

    # DOWNLOAD COUNTER

    download_count = models.PositiveIntegerField(
        default=0,
        editable=False
    )

    # PUBLICATION LINKS

    journal_url = models.URLField(
        blank=True,
        verbose_name="Journal Link"
    )

    google_scholar_url = models.URLField(
        blank=True,
        verbose_name="Google Scholar Link"
    )

    researchgate_url = models.URLField(
        blank=True,
        verbose_name="ResearchGate Link"
    )

    doi = models.URLField(
        blank=True,
        verbose_name="DOI Link"
    )

    publication_url = models.URLField(
        blank=True,
        verbose_name="Publication Link"
    )

    # DISPLAY OPTIONS

    featured = models.BooleanField(
        default=False
    )

    date_uploaded = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date of Upload"
    )

    class Meta:
        ordering = [
            "-year",
            "title"
        ]

    def __str__(self):
        return self.title




# UPDATE PROFILE

class UpdateProfile(models.Model):

    name = models.CharField(
        max_length=200,
        blank=False
    )

    title = models.CharField(
        max_length=300,
        blank=False
    )

    department = models.CharField(
        max_length=300,
        blank=True
    )

    institution = models.CharField(
        max_length=300,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    photo = models.ImageField(
        upload_to="profile/",
        blank=True,
        null=True
    )

    bio = models.TextField(
        blank=True
    )

    google_scholar = models.URLField(
        blank=True
    )

    live_DNA = models.URLField(
        blank=True
    )

    linkedin = models.URLField(
        blank=True
    )

    ORCID = models.URLField(
        blank=True
    )

    ResearchGate = models.URLField(
        blank=True
    )

    def __str__(self):
        return self.name


# BLOG POSTS

class BlogPost(models.Model):

    post_title = models.CharField(
        max_length=300,
        verbose_name="Post Title"
    )

    label = models.CharField(
        max_length=100
    )

    # BLOG POST ABSTRACT

    abstract = models.TextField(
        blank=False,
        verbose_name="Abstract"
    )

    # HEADER PICTURE

    header_picture = models.ImageField(
        upload_to="blog/",
        blank=True,
        null=True,
        verbose_name="Header Picture"
    )

    # POST VIEW COUNTER

    post_count = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name="Post Count"
    )

    # DATE

    date_uploaded = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date of Upload"
    )

    class Meta:
        ordering = [
            "-date_uploaded"
        ]

        verbose_name = "Blog Post"

        verbose_name_plural = "Blog Posts"

    post_title = models.CharField(
        max_length=300,
        verbose_name="Post Title"
    )

    label = models.CharField(
        max_length=100
    )

    abstract = models.TextField(
        blank=True,
        verbose_name="Abstract"
    )

    header_picture = models.ImageField(
        upload_to="blog/",
        blank=True,
        null=True,
        verbose_name="Header Picture"
    )

    date_uploaded = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date of Upload"
    )

    post_count = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name="Post Count"
    )

    class Meta:
        ordering = ["-date_uploaded"]
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

    def __str__(self):
        return self.post_title


# BLOG COMMENT

class BlogComment(models.Model):

    blog_post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Blog Post"
    )

    name = models.CharField(
        max_length=150,
        verbose_name="Name"
    )

    email = models.EmailField(
        verbose_name="Email"
    )

    comment = models.TextField(
        verbose_name="Comment"
    )

    approved = models.BooleanField(
        default=False,
        verbose_name="Approved"
    )

    date_commented = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date of Comment"
    )

    class Meta:
        ordering = ["date_commented"]
        verbose_name = "Blog Comment"
        verbose_name_plural = "Blog Comments"

    def __str__(self):
        return f"{self.name} - {self.blog_post.post_title}"

