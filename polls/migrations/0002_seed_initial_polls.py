from django.db import migrations

# Top 10 most populous capital cities (city-proper population, based on
# UN World Urbanization Prospects 2025 estimates and similar sources),
# each with an approximate lat/lng.
CAPITAL_CITIES = [
    ("Jakarta, Indonesia", -6.2088, 106.8456),
    ("Dhaka, Bangladesh", 23.8103, 90.4125),
    ("Tokyo, Japan", 35.6762, 139.6503),
    ("New Delhi, India", 28.6139, 77.2090),
    ("Cairo, Egypt", 30.0444, 31.2357),
    ("Manila, Philippines", 14.5995, 120.9842),
    ("Seoul, South Korea", 37.5665, 126.9780),
    ("Beijing, China", 39.9042, 116.4074),
    ("Moscow, Russia", 55.7558, 37.6173),
    ("Kinshasa, DR Congo", -4.4419, 15.2663),
]

# Ten widely recommended beach vacation destinations (subjective/illustrative
# list drawn from popular travel round-ups), each with an approximate lat/lng.
BEACH_DESTINATIONS = [
    ("Maldives", 4.1755, 73.5093),
    ("Bora Bora, French Polynesia", -16.5004, -151.7415),
    ("Maui, Hawaii (USA)", 20.7984, -156.3319),
    ("Phuket, Thailand", 7.8804, 98.3923),
    ("Santorini, Greece", 36.3932, 25.4615),
    ("Cancún, Mexico", 21.1619, -86.8515),
    ("Seychelles", -4.6191, 55.4513),
    ("Bali, Indonesia", -8.3405, 115.0920),
    ("Gold Coast, Australia", -28.0167, 153.4000),
    ("Amalfi Coast, Italy", 40.6340, 14.6027),
]

QUESTION_TEXTS = [
    "Which of these capital cities is the most populous?",
    "Which of these top beach destinations would you most like to visit?",
]


def seed_polls(apps, schema_editor):
    Question = apps.get_model("polls", "Question")
    Choice = apps.get_model("polls", "Choice")

    capitals_question = Question.objects.create(question_text=QUESTION_TEXTS[0])
    Choice.objects.bulk_create(
        [
            Choice(question=capitals_question, choice_text=city, latitude=lat, longitude=lng)
            for city, lat, lng in CAPITAL_CITIES
        ]
    )

    beaches_question = Question.objects.create(question_text=QUESTION_TEXTS[1])
    Choice.objects.bulk_create(
        [
            Choice(question=beaches_question, choice_text=destination, latitude=lat, longitude=lng)
            for destination, lat, lng in BEACH_DESTINATIONS
        ]
    )


def remove_seeded_polls(apps, schema_editor):
    Question = apps.get_model("polls", "Question")
    Question.objects.filter(question_text__in=QUESTION_TEXTS).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_polls, remove_seeded_polls),
    ]
