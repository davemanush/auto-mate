from datetime import datetime, timedelta


def default_render(value):
    return value

def delay_render(value):
    return value + " seconds"

def datetime_render(value: datetime):
    now = datetime.now()
    diff = now - value

    if diff < timedelta(minutes=1):
        return "less than a minute ago"
    elif diff < timedelta(hours=1):
        minutes = diff.seconds // 60
        return f"{minutes} minutes ago"
    elif diff < timedelta(days=1):
        hours = diff.seconds // 3600
        return f"{hours} hours ago"
    elif diff < timedelta(days=now.day):
        days = diff.days
        return f"{days} days ago"
    else:
        months = (now.year - value.year) * 12 + now.month - value.month
        return f"more than {months} months ago"