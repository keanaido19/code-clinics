"""
Additional functions to assist other modules.
"""

from __future__ import annotations
import datetime

from pytz import timezone


def get_current_utc_date():
    """
    Get the current date in utc format
    """
    return datetime.datetime.utcnow()


def get_new_utc_date(days):
    """
    Returns current utc date plus number of specified days
    """
    new_date = get_current_utc_date().date() + datetime.timedelta(days=days + 1)
    new_time = datetime.datetime.min.time()
    new_datetime = datetime.datetime.combine(new_date, new_time)
    return new_datetime


def get_date_range(days):
    """
    Returns a range of how many days will be displayed in the calendar
    """
    start_date = get_current_utc_date().isoformat() + 'Z'
    end_date = get_new_utc_date(days).isoformat() + 'Z'
    return start_date, end_date


def convert_to_local_timezone(date):
    '''
    Converts date to local timezone
    '''
    timestamp = date.timestamp()
    utc_date = datetime.datetime.utcfromtimestamp(timestamp)
    return timezone('UTC').localize(utc_date).astimezone(
        timezone('Africa/Johannesburg'))


def get_calendar_event_start(calendar_event):
    '''
    Get the calendar event start date
    '''
    dt = datetime.datetime
    start_time = \
        calendar_event['start'] \
        .get('dateTime', calendar_event['start'].get('date'))
    return convert_to_local_timezone(dt.fromisoformat(start_time))


def get_calendar_event_end(calendar_event):
    '''
    Get the calendar event start date
    '''
    dt = datetime.datetime
    end_time = calendar_event['end'].get('dateTime',
                                         calendar_event['end'].get('date'))
    return convert_to_local_timezone(dt.fromisoformat(end_time))


def format_calendar_event_start(calendar_event):
    '''
    formats the  calendar event start date
    '''
    event_start = get_calendar_event_start(calendar_event)
    calendar_event['start']['event_date'] = event_start.strftime('%a %d-%b-%Y')
    calendar_event['start']['event_time'] = event_start.strftime('%H:%M')


def format_calendar_event_end(calendar_event):
    '''
    formats the  calendar event start date
    '''
    event_end = get_calendar_event_end(calendar_event)
    calendar_event['end']['event_date'] = event_end.strftime('%a %d-%b-%Y')
    calendar_event['end']['event_time'] = event_end.strftime('%H:%M %p')


def get_current_datetime_timestamp() -> float:
    """
    Returns the current datetime as a timestamp float
    :return: Current datetime as a timestamp float
    """
    current_datetime_as_string: str = \
        datetime.datetime.now().isoformat() + '+02:00'
    return \
        datetime.datetime.fromisoformat(current_datetime_as_string).timestamp()


def check_calendar_event_not_expired(calendar_event: dict) -> bool:
    """
    Checks if the given calendar event has expired
    :param dict calendar_event: Calendar event
    :return: Boolean value
    """
    current_datetime_timestamp: float = get_current_datetime_timestamp()
    return get_calendar_event_start(
        calendar_event).timestamp() > current_datetime_timestamp


def remove_expired_calendar_events(calendar_events: list[dict]) -> list[dict]:
    """
    Removes any expired calendar events from the given list of calendar events
    :param list[dict] calendar_events: List of calendar events from Google
    Calendar
    :return: List of calendar events with expired events removed
    """
    return [
        calendar_event
        for calendar_event in calendar_events
        if check_calendar_event_not_expired(calendar_event)
    ]


def format_calendar_event(calendar_event):
    '''
    formats the  calendar event start and end date
    '''
    format_calendar_event_start(calendar_event)
    format_calendar_event_end(calendar_event)


def get_event_time_period(calendar_event: dict) -> str:
    """
    Returns the time period from the calendar event
    :param dict calendar_event: Calendar event
    :return: Calendar event time period
    """
    event_start = calendar_event['start']['event_time']
    event_end = calendar_event['end']['event_time']
    return f'{event_start} - {event_end}'


def get_event_summary(calendar_event: dict) -> str:
    """
    Returns the event summary from the calendar event
    :param dict calendar_event: Calendar event
    :return: Calendar event summary
    """
    return calendar_event['summary']


def get_event_volunteer_location(calendar_event: dict) -> str:
    """
    Returns the volunteer's campus location from the calendar event
    :param dict calendar_event: Calendar event
    :return: Calendar event summary
    """
    volunteer_comment: str = next(
        (
            attendee['comment']
            for attendee in calendar_event['attendees']
            if 'Volunteer' in attendee['comment']
        ), 'Unknown - Unknown')
    return volunteer_comment.split(' - ')[1]


def format_calendar_events_to_table(
        calendar_event_data: dict[str, list[dict]]) \
        -> list[list[str]]:
    """
    Converts the calendar event data into a printable table format
    :param dict[str, list[dict]] calendar_event_data: Calendar event data
    :return: None
    """
    output_table: list[list[str]] = []
    table_row: list[str]

    for date, events in calendar_event_data.items():
        for event in events:
            table_row = [date, get_event_time_period(event),
                         get_event_summary(event)]
            output_table.append(table_row)

    return output_table


def get_available_volunteer_slots(calendar_event_data):
    """Checks for available volunteer slots. Returns available_slots[dict]

    """
    available_slots = {}
    indexing = 1

    for date, events in calendar_event_data.items():
        for event in events:
            if not check_volunteer_slot_booked(event):
                available_slots[str(indexing)] = \
                    get_volunteer_slot_information(event)
            indexing += 1
    return available_slots


def check_volunteer_slot_booked(calendar_event):
    """Checks if a slot is booked. Returns[bool]

    """
    try:
        if calendar_event['summary'] == 'Code Clinic':
            return len(calendar_event['attendees']) > 0
        return False
    except KeyError:
        return False


def get_volunteer_slot_information(calendar_event):
    """It gets information about a volunteer slot.
    Returns volunteer_slot_info[dict]
    """
    volunteer_slot_info = {}
    volunteer_slot_info['event_id'] = calendar_event['id']
    volunteer_slot_info['datetime'] = \
        calendar_event['start']['event_date'] + \
        ' (' + calendar_event['start']['event_time'] + \
        ' - ' + calendar_event['end']['event_time'] + ')'

    return volunteer_slot_info


def get_volunteer_slot_table_row_index(calendar_event: dict) -> int:
    """
    Returns the volunteer slot table row index for the given calendar event time
    :param dict calendar_event: Calendar event
    :return: Volunteer slot table row index
    """
    dt = datetime.time
    time_key: datetime.time = get_calendar_event_start(calendar_event).time()
    table_row_index_dict: dict[datetime.time, int] = \
        {
            dt(9, 0): 1, dt(9, 30): 2, dt(10, 0): 3, dt(10, 30): 4,
            dt(11, 0): 5, dt(11, 30): 6, dt(12, 0): 7, dt(12, 30): 8,
            dt(13, 0): 9, dt(13, 30): 10, dt(14, 0): 11, dt(14, 30): 12,
            dt(15, 0): 13, dt(15, 30): 14, dt(16, 0): 15, dt(16, 30): 16,
            dt(17, 0): 17, dt(17, 30): 18
        }
    return table_row_index_dict[time_key]


def format_clinic_time_slots_to_table(
        calendar_event_data: dict[str, list[dict]]) \
        -> list[list[str, str, str]]:
    """
    Converts the clinic calendar time slots into a printable table format
    :param dict[str, list[dict]] calendar_event_data: Calendar event data
    :return: None
    """
    output_table: list[list[str, str, str]] = []
    table_row: list[str, str, str]
    table_row_index: int
    index: int = 1

    for date, events in calendar_event_data.items():
        table_row = [date] + ['-'] * 18
        for event in events:
            table_row_index = get_volunteer_slot_table_row_index(event)
            if check_volunteer_slot_booked(event):
                table_row[table_row_index] = 'BOOKED'
            else:
                table_row[table_row_index] = f'({index})'
            index += 1
        output_table.append(table_row)
    return output_table


def check_dictionary_key_is_valid(
        key: str, dictionary: dict) -> bool:
    """
    Checks if the dictionary key exists in the dictionary
    :param str key: Dictionary key
    :param dict dictionary: Dictionary
    :return: Boolean value
    """
    try:
        dictionary[key]
        return True
    except KeyError:
        return False


def get_event_volunteer_email(calendar_event: dict) -> str:
    """
    Returns the volunteer's email address from the calendar event
    :param dict calendar_event: Calendar event
    :return: Volunteer's email address
    """
    return next(
        (
            attendee['email']
            for attendee in calendar_event['attendees']
            if 'Volunteer' in attendee['comment']
        ), '-')


def get_event_student_email(calendar_event: dict) -> str:
    """
    Returns the student's email address from the calendar event
    :param dict calendar_event: Calendar event
    :return: Student's email address
    """
    return next(
            (
                attendee['email']
                for attendee in calendar_event['attendees']
                if 'Student' in attendee['comment']
            ), '-')


def check_code_clinic_slot_booked_by_volunteer_only(
        username: str, calendar_event: dict) -> bool:
    """
    Checks if the calendar event has only been booked by a volunteer
    :param str username: Current user's username
    :param dict calendar_event: Calendar event
    :return: Boolean value
    """
    try:
        if calendar_event['summary'] == 'Code Clinic':
            attendees: list[dict[str, str]] = calendar_event['attendees']
            if len(attendees) == 1:
                return attendees[0]['email'] != username \
                       and 'Volunteer' in attendees[0]['comment']
        return False
    except KeyError:
        return False


def check_code_clinic_slot_booked_by_user_as_volunteer_only(
        username: str, calendar_event: dict) -> bool:
    """
    Checks if the calendar event has only been booked by the user as a volunteer
    :param str username: Current user's username
    :param dict calendar_event: Calendar event
    :return: Boolean value
    """
    try:
        if calendar_event['summary'] == 'Code Clinic':
            attendees: list[dict[str, str]] = calendar_event['attendees']
            if len(attendees) == 1:
                return attendees[0]['email'] == username \
                       and 'Volunteer' in attendees[0]['comment']
        return False
    except KeyError:
        return False


def check_code_clinic_slot_booked_by_user_as_volunteer(
        username: str, calendar_event: dict) -> bool:
    """
    Checks if the calendar event has been booked by the user as a volunteer
    :param str username: Current user's username
    :param dict calendar_event: Calendar event
    :return: Boolean value
    """
    try:
        if calendar_event['summary'] == 'Code Clinic':
            attendees: list[dict[str, str]] = calendar_event['attendees']
            if attendees:
                return any(username == attendee['email'] and 'Volunteer' in
                           attendee['comment'] for attendee in attendees)
        return False
    except KeyError:
        return False


def get_time_slot_information(calendar_event: dict) -> dict[str, str]:
    """
    Returns information about the calendar event's time slot
    :param dict calendar_event: Calendar event
    :return: Calendar event time slot information
    """
    return \
        {
            'event_id': calendar_event['id'],
            'datetime': f"{calendar_event['start']['event_date']} "
                        f"({calendar_event['start']['event_time']} - "
                        f"{calendar_event['end']['event_time']})"
        }


def get_available_student_slots(
        username: str,
        calendar_event_data: dict[str, list[dict]]) \
        -> dict[str, dict[str, str]]:
    """
    Returns a dictionary of available student slots that can be booked
    :param str username: Current user's username
    :param dict[str, list[dict]] calendar_event_data: Calendar event data
    :return: Available student slots that can be booked
    """
    available_slots: dict[str, dict[str, str]] = {}
    index: int = 1

    for date, events in calendar_event_data.items():
        for event in events:
            if check_code_clinic_slot_booked_by_volunteer_only(username, event):
                available_slots[str(index)] = \
                    get_time_slot_information(event)
            index += 1
    return available_slots


def check_code_clinic_time_slot_booked_by_user_as_student(
        username: str, calendar_event: dict) -> bool:
    """
    Checks if the calendar event has been booked by the user as a student
    :param str username: Current user's username
    :param dict calendar_event: Calendar event
    :return: Boolean value
    """
    try:
        if calendar_event['summary'] == 'Code Clinic':
            attendees: list[dict[str, str]] = calendar_event['attendees']
            if len(attendees) == 2:
                return any(
                    username == attendee['email'] and 'Student' in
                    attendee['comment'] for attendee in attendees
                )
        return False
    except KeyError:
        return False


def get_user_booked_student_slots(
        username: str,
        calendar_event_data: dict[str, list[dict]]) \
        -> dict[str, dict[str, str]]:
    """
    Returns a dictionary of student slots that have booked by the user
    :param str username: The current user's username
    :param dict[str, list[dict]] calendar_event_data: Calendar event data
    :return: Dictionary of student slots that have booked by the user
    """
    user_booked_student_slots: dict[str, dict[str, str]] = {}
    index: int = 1

    for date, events in calendar_event_data.items():
        for event in events:
            if check_code_clinic_time_slot_booked_by_user_as_student(
                    username, event):
                user_booked_student_slots[str(index)] = \
                    get_time_slot_information(event)
            index += 1
    return user_booked_student_slots


def format_calendar_events_to_available_student_bookings(
        username: str,
        calendar_event_data: dict[str, list[dict]]) \
        -> list[list[str]]:
    """
    Extracts the available student bookings from the calendar event data and
    converts it into a table format
    :param str username: Current user's username
    :param dict[str, list[dict]] calendar_event_data: Calendar event data
    :return: Available student bookings in table format
    """
    output_table: list[list[str]] = []
    table_row: list[str]
    index: int = 1

    for date, events in calendar_event_data.items():
        for event in events:
            if check_code_clinic_slot_booked_by_volunteer_only(username, event):
                table_row = \
                    [f'({index})', date, get_event_time_period(event),
                     get_event_volunteer_location(event),
                     get_event_volunteer_email(event)]
                output_table.append(table_row)
            index += 1
    return output_table


def get_retractable_volunteer_slots(
        username: str,
        calendar_event_data: dict[str, list[dict]]) \
        -> dict[str, dict[str, str]]:
    """
    Retrieves the user's booked volunteer slots that can be cancelled
    :param str username: The current user's username
    :param dict[str, list[dict]] calendar_event_data: Calendar event data
    :return: User's booked volunteer slots that can be cancelled
    """
    retractable_volunteer_slots = {}
    indexing = 1

    for date, events in calendar_event_data.items():
        for event in events:
            if check_code_clinic_slot_booked_by_user_as_volunteer_only(
                    username, event):
                retractable_volunteer_slots[str(indexing)] = \
                    get_volunteer_slot_information(event)
            indexing += 1
    return retractable_volunteer_slots


def format_user_booked_volunteer_slots_to_table(
        calendar_event_data: dict[str, list[dict]], username: str) \
        -> list[list[str]]:
    """
    Extracts the user's booked volunteer slots from their calendar even data
    and converts it into table format
    :param dict[str, list[dict]] calendar_event_data: Calendar event data
    :param str username: The current user's username
    :return: User's booked volunteer slots as table format
    """
    output_table: list[list[str]] = []
    table_row: list[str]
    index: int = 1

    for date, events in calendar_event_data.items():
        for event in events:
            if check_code_clinic_slot_booked_by_user_as_volunteer(
                    username, event):
                if check_code_clinic_slot_booked_by_user_as_volunteer_only(
                        username, event):
                    table_row = [f'({index})']
                else:
                    table_row = ['-']
                table_row += [date, get_event_time_period(event),
                              get_event_student_email(event)]
                output_table.append(table_row)
            index += 1
    return output_table


def format_user_booked_student_slots_to_table(
        calendar_event_data: dict[str, list[dict]], username: str) \
        -> list[list[str]]:
    """
    Extracts the user's booked student slots from their calendar even data
    and converts it into table format
    :param dict[str, list[dict]] calendar_event_data: Calendar event data
    :param str username: The current user's username
    :return: User's booked volunteer slots as table format
    """
    output_table: list[list[str]] = []
    table_row: list[str]
    index: int = 1

    for date, events in calendar_event_data.items():
        for event in events:
            if check_code_clinic_time_slot_booked_by_user_as_student(
                    username, event):
                table_row = [f'({index})', date, get_event_time_period(event),
                             get_event_volunteer_location(event),
                             get_event_volunteer_email(event)]
                output_table.append(table_row)
            index += 1
    return output_table
