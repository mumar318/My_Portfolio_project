from django import forms

from .models import BlogPost, ContactMessage


_DISPOSABLE_DOMAINS = {
    "mailinator.com",
    "tempmail.com",
    "10minutemail.com",
    "guerrillamail.com",
}


class ContactForm(forms.Form):
    """Contact form with basic spam and quality validation."""

    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(
        max_length=200,
        required=False,
        help_text="Optional subject; defaults to a generic contact line if left blank.",
    )
    message = forms.CharField(widget=forms.Textarea, required=True)

    def clean_email(self):
        email = self.cleaned_data["email"].strip()
        domain = email.split("@")[-1].lower()
        if domain in _DISPOSABLE_DOMAINS:
            raise forms.ValidationError(
                "Please use a professional email address (disposable emails are not allowed)."
            )
        return email

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if len(message) < 10:
            raise forms.ValidationError(
                "Your message is a bit too short. Please provide at least a couple of sentences."
            )
        if "http://" in message or "https://" in message:
            # Very light anti-spam heuristic
            raise forms.ValidationError(
                "Links are not allowed in the message. Please describe your request in plain text."
            )
        return message

    def save(self, request=None) -> ContactMessage:
        """Persist a ContactMessage instance based on validated data."""

        if not self.is_valid():  # pragma: no cover - guard
            raise ValueError("Cannot save an invalid form")

        ip = None
        user_agent = ""
        if request is not None:
            ip = request.META.get("REMOTE_ADDR")
            user_agent = request.META.get("HTTP_USER_AGENT", "")[:500]

        data = self.cleaned_data
        subject = data.get("subject") or "New portfolio contact message"

        return ContactMessage.objects.create(
            name=data["name"],
            email=data["email"],
            subject=subject,
            message=data["message"],
            ip_address=ip,
            user_agent=user_agent,
        )


class BlogPostForm(forms.ModelForm):
    """Admin-facing blog post form with rich content widgets."""

    class Meta:
        model = BlogPost
        fields = "__all__"
        widgets = {
            "content": forms.Textarea(attrs={"class": "markdown-editor", "rows": 18}),
            "excerpt": forms.Textarea(attrs={"rows": 3}),
        }
