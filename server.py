# AI agent have tools, resources (knowledge), and prompts.
import os
from mcp.server.fastmcp import FastMCP 
from typing import List, Optional, Dict
from hrms import *
from utils import seed_services
from emails import *

from dotenv import load_dotenv
load_dotenv()

mcp = FastMCP("hr-assistant")

employee_manager = EmployeeManager()
leave_manager = LeaveManager()
meeting_manager = MeetingManager()
ticket_manager = TicketManager()

seed_services(employee_manager, leave_manager, meeting_manager, ticket_manager)

emailer = EmailSender(
    smtp_server="smtp.gmail.com",
    port=587,
    username=os.getenv("CB_EMAIL"),
    password=os.getenv("CB_EMAIL_PWD"),
    use_tls=True
)

@mcp.tool()
def add_employee(name: str, manager_id: str, email: str) -> str:
    """
    Add a new employee to the system.
    
    Args:
        name (str): Employee name.
        manager_id (str): Manager's employee ID.
        email (str): Employee email address.
        
    Returns:
        str: Confirmation message.
    """
    emp = EmployeeCreate(
        emp_id=employee_manager.get_next_emp_id(),
        name=name,
        manager_id=manager_id,
        email=email
    )
    employee_manager.add_employee(emp)
    return f"Employee {name} added successfully."

@mcp.tool()
def get_employee_details(name:str) -> Dict[str, str]:
    """
    Get details of an employee by name.
    
    Args:
        name (str): Employee name.
        
    Returns:
        Optional[Dict[str, str]]: Employee details or None if not found.
    """
    matches = employee_manager.search_employee_by_name(name)
    if len(matches) == 0:
        raise ValueError(f"No employee found with name '{name}'")
    
    emp_id = matches[0] 
    return employee_manager.get_employee_details(emp_id)

@mcp.tool()
def send_email(to_emails: List[str], subject: str, body: str, html: bool = False) -> str:
    """
    Send an email to specified recipients.
    
    Args:
        to_emails (List[str]): List of recipient email addresses.
        subject (str): Email subject.
        body (str): Email body content.
        html (bool): Whether the body is HTML formatted.
        
    Returns:
        str: Confirmation message.
    """
    emailer.send_email(
        subject=subject,
        body=body,
        to_emails=to_emails,
        html=html
    )
    return f"Email sent successfully to {', '.join(to_emails)}."

@mcp.tool()
def create_ticket(emp_id: str, item: str, reason: str) -> str:
    """
    Create a new ticket for an employee.
    
    Args:
        emp_id (str): Employee ID.
        item (str): Item requested.
        reason (str): Reason for the ticket.
        
    Returns:
        str: Confirmation message.
    """
    if not employee_manager.get_employee_details(emp_id):
        raise ValueError(f"Employee with ID '{emp_id}' does not exist.")
    
    ticket_req = TicketCreate(
        emp_id=emp_id,
        item=item,
        reason=reason
    )
    return ticket_manager.create_ticket(ticket_req)

@mcp.tool()
def update_ticket_status(ticket_id: str, status: str) -> str:
    """
    Update the status of an existing ticket.

    Args:
        ticket_id (str): Ticket ID.
        status (str): New status for the ticket.
    
    Returns:
        str: Confirmation message.
    """
    if not ticket_manager.get_ticket(ticket_id):
        raise ValueError(f"Ticket with ID '{ticket_id}' does not exist.")
    
    ticket_update_status = TicketStatusUpdate(status=status)
    return ticket_manager.update_ticket_status(ticket_update_status, ticket_id)

@mcp.tool()
def list_tickets(emp_id: str, status: Optional[str] = None) -> List[Dict[str, str]]:
    """
    List all tickets for a specific employee with optional status filter.
    
    Args:
        emp_id (str): Employee ID.
        status (str): Optional status to filter tickets by.
        
    Returns:
        List of tickets or a message if no tickets found.
    """
    if not employee_manager.get_employee_details(emp_id):
        raise ValueError(f"Employee with ID '{emp_id}' does not exist.")
    
    return ticket_manager.list_tickets(employee_id=emp_id, status=status)

@mcp.tool()
def schedule_meeting(emp_id: str, meeting_dt: datetime, topic: str) -> str:
    """
    Schedule a meeting for an employee.
    
    Args:
        emp_id (str): Employee ID.
        meeting_dt (datetime): Scheduled date and time of the meeting.
        topic (str): Topic or subject of the meeting.
        
    Returns:
        str: Confirmation message.
    """
    if not employee_manager.get_employee_details(emp_id):
        raise ValueError(f"Employee with ID '{emp_id}' does not exist.")
    
    meeting_req = MeetingCreate(
        emp_id=emp_id,
        meeting_dt=meeting_dt,
        topic=topic
    )
    return meeting_manager.schedule_meeting(meeting_req)

@mcp.tool()
def get_meetings(emp_id: str) -> List[Dict[str, str]]:
    """
    Get all scheduled meetings for an employee.
    
    Args:
        emp_id (str): Employee ID.
        
    Returns:
        str: List of meetings or a message if no meetings found.
    """
    if not employee_manager.get_employee_details(emp_id):
        raise ValueError(f"Employee with ID '{emp_id}' does not exist.")
    
    meetings = meeting_manager.get_meetings(emp_id)
    if not meetings:
        return f"No meetings scheduled for employee {emp_id}."
    
    return meetings

@mcp.tool()
def cancel_meeting(emp_id: str, meeting_dt: datetime, topic: Optional[str] = None) -> str:
    """
    Cancel a scheduled meeting for an employee.
    
    Args:
        emp_id (str): Employee ID.
        meeting_dt (datetime): Date and time of the meeting to cancel.
        topic (str): Optional topic of the meeting to cancel.
        
    Returns:
        str: Confirmation message.
    """
    if not employee_manager.get_employee_details(emp_id):
        raise ValueError(f"Employee with ID '{emp_id}' does not exist.")
    
    cancel_req = MeetingCancelRequest(
        emp_id=emp_id,
        meeting_dt=meeting_dt,
        topic=topic
    )
    return meeting_manager.cancel_meeting(cancel_req)

@mcp.tool()
def get_employee_leave_balance(emp_id: str) -> str:
    """
    Get the leave balance for an employee.
    
    Args:
        emp_id (str): Employee ID.
        
    Returns:
        str: Leave balance or a message if employee not found.
    """
    return leave_manager.get_leave_balance(emp_id)

@mcp.tool()
def apply_leave(emp_id: str, leave_dates: list) -> str:
    """
    Apply for leave for an employee.
    
    Args:
        emp_id (str): Employee ID.
        leave_dates (list): List of dates for which leave is requested.
        
    Returns:
        str: Confirmation message or error if leave cannot be applied.
    """
    leave_req = LeaveApplyRequest(
        emp_id=emp_id,
        leave_dates=leave_dates
    )
    return leave_manager.apply_leave(leave_req)

@mcp.tool()
def get_leave_history(emp_id: str) -> str:
    """
    Get the leave history for an employee.
    
    Args:
        emp_id (str): Employee ID.
        
    Returns:
        str: Leave history or a message if employee not found.
    """
    return leave_manager.get_leave_history(emp_id)

@mcp.prompt()
def onboard_new_employee(employee_name: str, manager_name: str, email: str) -> str:
    """
    Onboard a new employee by adding them to the system and sending a welcome email.
    
    Args:
        employee_name (str): Name of the new employee.
        manager_name (str): Name of the manager for the new employee.
        email (str): Email address of the new employee.
        
    Returns:
        str: Confirmation message.
    """
    return f"""
    onboard new employee {employee_name} under manager {manager_name} with email {email}
    steps to follow:
        1. Add employee to the HRMS system
        2. send a welcome email to employee with the new credentials (employee_name@curefit.com, employee_password)
        3. notify the manager {manager_name} about the new employee
        4. Raise tickets for a new laptop, id card, and other necessary equipment.
        5. Schedule an introductory meeting between the employee and the manager.
    """

if __name__ == "__main__":
    mcp.run(transport="stdio")   