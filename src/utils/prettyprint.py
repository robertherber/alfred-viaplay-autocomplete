def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    from datetime import datetime
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time 
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff == 0 and second_diff < 0:
        if second_diff > -10:
            return "any moment"
        if second_diff > -60:
            return "in " + str(-second_diff) + " seconds"
        if second_diff > -120:
            return "in a minute"
        if second_diff > -3600:
            return "in " + str( -second_diff / 60 ) + " minutes"
        if second_diff > -86400:
            return "Today at " + time.strftime("%H:%M")
            #return "in " + str( -second_diff / 3600 ) + " hours"
    
    if day_diff == 0 and second_diff >= 0:
        if second_diff < 10:
            return "a moment ago"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return  "a minute ago"
        if second_diff < 3600:
            return str( second_diff / 60 ) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str( second_diff / 3600 ) + " hours ago"
        
    if day_diff == -1:
        return "Tomorrow at " + time.strftime("%H:%M")
    if day_diff > -7:
        return "in " + str(-day_diff) + " days"
    if day_diff > -31:
        return "in " + str(-day_diff/7) + " weeks"
    if day_diff > -365:
        return "in " + str(-day_diff/30) + " months"

    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff/7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff/30) + " months ago"
    return str(day_diff/365) + " years ago"