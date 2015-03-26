import calendar

def get_last_date_of_previous_month(in_date):
    date = in_date
    if(date.month == 1):
        current_year = date.year
        date = date.replace(year=current_year-1, month=12)
    else:
        date = date.replace(month=date.month-1)
    
    last_day_in_month = calendar.monthrange(date.year, date.month)[1]
    date = date.replace(day=last_day_in_month)
    
    return date