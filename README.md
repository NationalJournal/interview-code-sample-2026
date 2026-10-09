# Django Polls — with a map of the poll choices

This extends the standard [Django tutorial Polls app](https://docs.djangoproject.com/en/5.2/intro/) with:

- Two pre-loaded polls:
  1. **"Which of these capital cities is the most populous?"** — the 10 most
     populous national capital cities (Jakarta, Dhaka, Tokyo, New Delhi,
     Cairo, Manila, Seoul, Beijing, Moscow, Kinshasa), based on UN World
     Urbanization Prospects 2025 estimates.
  2. **"Which of these top beach destinations would you most like to
     visit?"** — 10 widely recommended beach vacation spots (Maldives, Bora
     Bora, Maui, Phuket, Santorini, Cancún, Seychelles, Bali, Gold Coast,
     Amalfi Coast).
- An **optional approximate geographic location on each choice** (not on
  each vote). A `Choice` — e.g. "Tokyo, Japan" or "Bali, Indonesia" — can
  carry a latitude/longitude representing the place itself.
- A **map shown alongside the question, before anyone votes**. On the
  voting page, if any of that question's choices have a location, a
  [Leaflet](https://leafletjs.com/) map (loaded from the unpkg CDN, no API
  key or account needed) appears above the voting form with a pin for each
  located choice, using free [OpenStreetMap](https://www.openstreetmap.org/)
  tiles — so voters can see roughly where each option is before they pick.
  If no choices have a location, no map is shown. The map illustrates the
  *choices*, not where any individual voted from — the results page is a
  plain vote tally with no map.

## Setup

```bash
python -m venv venv
source venv/bin/activate        # venv\Scripts\activate on Windows
pip install "Django>=5.2,<5.3"
python manage.py migrate        # creates the DB and seeds the two polls above
python manage.py createsuperuser  # optional, for /admin/
python manage.py runserver
```

### Or with Docker

```bash
docker build -t django-polls .
docker run -p 8002:8002 django-polls
docker exec -it <container_name_or_id> python manage.py createsuperuser
```

Then visit `http://localhost:8002/polls/` or `http://localhost:8002/admin/`.
Migrations (and the two seeded polls) run automatically on container start.
Each `docker run` starts from a fresh SQLite database inside the container,
since it isn't mounted as a volume — add `-v "$(pwd)/data:/app/data"` and
point `DATABASES` at that path if you want the data to persist across restarts.

Then visit:

- `http://127.0.0.1:8000/polls/` — list of polls
- `http://127.0.0.1:8000/admin/` — manage questions and choices (including
  each choice's latitude/longitude)

## What changed from the base tutorial

- **`polls/models.py`** — `Choice` gained optional `latitude`/`longitude`
  fields for the place it represents. `Response` records a single vote for
  a `Choice` (no location data of its own). `Choice.votes` is a property
  computed from related `Response` rows.
- **`polls/migrations/0002_seed_initial_polls.py`** — a data migration that
  creates the two questions and their choices, each with an approximate
  lat/lng, automatically on `migrate`.
- **`polls/views.py`** — `detail()` collects the located choices for a
  question and passes them to the template as JSON for the map;
  `vote()` and `results()` are otherwise close to the standard tutorial.
- **`polls/templates/polls/`** — new `base.html`, `index.html`,
  `detail.html` (map of choice locations, shown above the voting form when
  applicable), and `results.html` (plain vote counts, no map).
- **`polls/admin.py`** — registers `Question` (with inline `Choice` editing,
  including lat/lng) and `Response`.

## Notes

- The capital-city population ranking and the beach destination list are
  both point-in-time/illustrative choices — edit them, or their
  coordinates, anytime via `/admin/` or by writing a new data migration.
- Leaflet displays a small "© OpenStreetMap contributors" attribution in
  the corner of the map, which is required by OSM's terms of use.
