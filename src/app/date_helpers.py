import calendar, datetime

def get_last_date_of_previous_month(in_date):
    date = in_date
    date = date.replace(day=1) #every month has a first
    
    if(date.month == 1):
        current_year = date.year
        date = date.replace(year=current_year-1, month=12)
    else:
        date = date.replace(month=date.month-1)
    
    last_day_in_month = calendar.monthrange(date.year, date.month)[1]
    date = date.replace(day=last_day_in_month)
    
    return date

def string_to_date(date_string):
    date_parse_string = "%Y-%m-%d"
    
    return datetime.datetime.strptime(date_string, date_parse_string).date()