from ics import Calendar, Event
from datetime import date, timedelta

def export_ics(study_items, path):
    cal = Calendar()
    start = date.today()

    for i, item in enumerate(study_items):
        e = Event()
        e.name = f"Study: {item['topic']}"
        e.begin = (start + timedelta(days=i)).isoformat()
        e.make_all_day()
        e.description = f"Score: {item['weight']}"
        cal.events.add(e)

    with open(path, "w") as f:
        f.writelines(cal)
