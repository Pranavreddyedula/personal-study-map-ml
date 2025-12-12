from ics import Calendar, Event
from datetime import date, timedelta
from utils import ensure_dir, timestamp_str, logger

def export_ics(study_items, path):
    """
    study_items: list of dicts with 'topic' and optionally 'weight'
    path: full path to write .ics file
    """
    out_dir = path.rsplit("/",1)[0] if "/" in path else "."
    ensure_dir(out_dir)
    cal = Calendar()
    start = date.today()
    for i, it in enumerate(study_items):
        e = Event()
        e.name = f"Study: {it.get('topic')}"
        e.begin = (start + timedelta(days=i)).isoformat()
        e.make_all_day()
        e.description = f"Priority score: {it.get('weight')}"
        cal.events.add(e)
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(cal)
        logger.info("Exported ICS to %s", path)
    except Exception as e:
        logger.error("Failed to write ICS file: %s", e)
        raise
