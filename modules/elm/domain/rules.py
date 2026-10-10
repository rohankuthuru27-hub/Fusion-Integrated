EL = 30
VL = 60
COL = 20
CL = 8
SCL = 15
RH = 2

def count_leave_days(start_date, end_date, leave_type):
    if leave_type == 'CL' and start_date.day == 15 and end_date.day == 15:
        return 0.5
    return (end_date - start_date).days

def detect_overlap(leave_requests):
    for i in range(len(leave_requests) - 1):
        if leave_requests[i].end_date > leave_requests[i + 1].start_date:
            return True
    return False