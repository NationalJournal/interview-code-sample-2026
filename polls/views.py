import json

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Choice, Question, Response


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")
    return render(request, "polls/index.html", {"latest_question_list": latest_question_list})


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    # Pins for any choices that have an approximate location, so voters can
    # see where each option is before they pick one.
    pins = [
        {"lat": choice.latitude, "lng": choice.longitude, "label": choice.choice_text}
        for choice in question.choices.all()
        if choice.has_location()
    ]

    return render(
        request,
        "polls/detail.html",
        {
            "question": question,
            "pins_json": json.dumps(pins),
            "has_pins": bool(pins),
        },
    )


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = list(question.choices.all())
    total_votes = sum(choice.votes for choice in choices)

    choice_data = [
        {
            "choice": choice,
            "votes": choice.votes,
            "percent": round((choice.votes / total_votes) * 100) if total_votes else 0,
        }
        for choice in choices
    ]

    return render(
        request,
        "polls/results.html",
        {
            "question": question,
            "choice_data": choice_data,
            "total_votes": total_votes,
        },
    )


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choices.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        pins = [
            {"lat": choice.latitude, "lng": choice.longitude, "label": choice.choice_text}
            for choice in question.choices.all()
            if choice.has_location()
        ]
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
                "pins_json": json.dumps(pins),
                "has_pins": bool(pins),
            },
        )

    Response.objects.create(choice=selected_choice)
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
