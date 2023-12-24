from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Books


def index(request):
    return render(request, "mlak/index.html")

class BooksView(View):
    """Books view
    """

    def get(self, request):
        """Get all books"""
        books = Books.objects.all().values()

        return render(
            request,
            "mlak/index.html",
            {"books": books, },
                )


class SignUpView(View):
    """Signup view
    """
    def get(self, request):
        """Render form
        """
        return render(
            request,
            "mlap/sign.html",
            {"form": UserCreationForm(), },
                )


def post(self, request):
    """Get signup
    """
    form = UserCreationForm(request.POST)

    if form.is_valid():
        form.save()

        username = form.data["username"]
        password = form.data["password1"]

        user = authenticate(
                request,
                username=username,
                password=password,
                    )

        if user:
            login(request, user)

        return redirect("/")

    return render(
        request,
        "giffy_app/sign.html",
        {"form": form, },
            )
