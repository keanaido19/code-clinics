"""
Module that exports a Code Clinic Booking to an iCal file
"""

import os
from datetime import datetime

from icalendar import Calendar, Event, vCalAddress, vText

import helpers

calendar_booking: Event = Event()
ical_calendar_data: Calendar = Calendar()


def set_calendar_booking_start_time(event_start: str) -> None:
    """
    Sets the start time of the calendar booking
    :param str event_start: Start datetime of the event
    :return: None
    """
    global calendar_booking
    calendar_booking.add('dtstart', datetime.fromisoformat(event_start))


def set_calendar_booking_end_time(event_end: str) -> None:
    """
    Sets the end time of the calendar booking
    :param str event_end: End datetime of the event
    :return: None
    """
    global calendar_booking
    calendar_booking.add('dtend', datetime.fromisoformat(event_end))


def set_calendar_booking_organizer() -> None:
    """
    Sets the organizer of the calendar booking event
    :return: None
    """
    global calendar_booking
    organizer = vCalAddress('mailto:team.a.obliviate@gmail.com')
    organizer.params['cn'] = vText('Code Clinic')
    calendar_booking['organizer'] = organizer


def set_calendar_booking_uid(calendar_event: dict) -> None:
    """
    Sets the uid of the calendar booking event
    :param dict calendar_event: Calendar event
    :return: None
    """
    global calendar_booking
    calendar_booking['uid'] = calendar_event['iCalUID']


def set_attendee_parameters(event_attendee: dict[str, str]) -> vCalAddress:
    """
    Sets the parameters for the event attendee
    :param dict[str, str] event_attendee: Attendee from calendar event
    :return: Attendee data
    """
    attendee: vCalAddress = vCalAddress(f'mailto:{event_attendee["email"]}')
    attendee.params['cutype'] = vText('INDIVIDUAL')
    attendee.params['role'] = vText('REQ-PARTICIPANT')
    attendee.params['partstat'] = vText('ACCEPTED')
    attendee.params['cn'] = vText(f'{event_attendee["email"]}')
    attendee.params['x-num-guests'] = "0"
    attendee.params['x-response-comment'] = \
        vText(f'{event_attendee["comment"]}')

    return attendee


def set_calendar_booking_attendees(event_attendees: list[dict[str, str]]) -> \
        None:
    """
    Sets the description of the calendar booking
    :param list[dict[str, str]] event_attendees: Event attendees
    :return: None
    """
    global calendar_booking
    for event_attendee in event_attendees:
        attendee = set_attendee_parameters(event_attendee)
        calendar_booking.add('attendee', attendee)


def set_calendar_booking_description(event_description: str) -> None:
    """
    Sets the description of the calendar booking
    :param str event_description: Description of the calendar event
    :return: None
    """
    global calendar_booking
    calendar_booking.add('description', event_description)


def set_calendar_booking_extra_parameters(calendar_event: dict) -> None:
    """
    Sets the extra of the calendar booking
    :param dict calendar_event: Calendar event
    :return: None
    """
    global calendar_booking
    calendar_booking['created'] = calendar_event['created']
    calendar_booking['sequence'] = calendar_event['sequence']
    calendar_booking['status'] = calendar_event['status'].upper()


def set_calendar_booking_summary(event_summary: str) -> None:
    """
    Sets the summary of the calendar booking
    :param str event_summary: Summary of the calendar event
    :return: None
    """
    global calendar_booking
    calendar_booking.add('summary', event_summary)


def get_path_to_export_directory() -> str:
    """
    Returns the path to the export directory
    :return: Path to export directory
    """
    return os.path.join(os.environ["HOME"], 'Documents/code_clinic')


def check_export_directory_exists() -> bool:
    """
    Checks if the directory for storing the ical files exists
    :return: Path to export directory
    """
    return os.path.exists(get_path_to_export_directory())


def create_export_directory() -> None:
    """
    Creates the export directory if it does not exist
    :return: None
    """
    if not check_export_directory_exists():
        os.makedirs(get_path_to_export_directory())


def get_path_ical_file(calendar_event: dict, booking_type: str) -> str:
    """
    Returns the path to the ical file
    :param dict calendar_event: Calendar event
    :param str booking_type: Type of booking, volunteer or student
    :return: Path to the ical file
    """
    file_name: str = \
        helpers.create_file_name_from_calendar_event(calendar_event)
    return os.path.join(
        get_path_to_export_directory(),
        f'{booking_type}_Booking_{file_name}.ics'
    )


def set_calendar_booking(calendar_event: dict) -> None:
    """
    Sets the parameters of the calendar booking event
    :param dict calendar_event: Calendar event
    :return: None
    """
    global calendar_booking
    global ical_calendar_data

    set_calendar_booking_start_time(calendar_event['start']['dateTime'])
    set_calendar_booking_end_time(calendar_event['end']['dateTime'])
    set_calendar_booking_organizer()
    set_calendar_booking_uid(calendar_event)
    set_calendar_booking_attendees(calendar_event['attendees'])
    set_calendar_booking_description(calendar_event['description'])
    set_calendar_booking_summary(calendar_event['summary'])
    set_calendar_booking_extra_parameters(calendar_event)


def export_to_ical(calendar_event: dict, booking_type: str) -> None:
    """
    Exports a calendar event to an iCal file
    :param dict calendar_event: Calendar event
    :param str booking_type: Type of booking, volunteer or student
    :return: None
    """
    global calendar_booking
    global ical_calendar_data

    set_calendar_booking(calendar_event)
    ical_calendar_data.add_component(calendar_booking)
    create_export_directory()
    with open(get_path_ical_file(calendar_event, booking_type), 'wb') as \
            ical_file:
        ical_file.write(ical_calendar_data.to_ical())
