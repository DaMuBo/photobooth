import pathlib
import time
import cups
import logging
from flask import current_app

def create_cups_connection():
    """
    Creates a new CUPS connection.

    Returns:
        cups.Connection: A new CUPS connection object.
    """
    return cups.Connection()

def check_printer_error(conn, printer_name):
    jobs = conn.getJobs()
    for job_id, _job in jobs.items():
        job_info = conn.getJobAttributes(job_id)
        job_state_reasons = job_info.get('job-state-reasons', [])
        if 'media-empty' in job_state_reasons or 'No Paper Tray' in job_state_reasons:
            return job_id, f"Printer error: {', '.join(job_state_reasons)}"
    return None, None

def check_printer_status(printer_name: str) -> tuple[str, int]:
    """
    Check the status of the specified printer.

    Args:
        printer_name (str): The name of the printer to check.

    Returns:
        tuple[str, int]: A tuple containing the status message and status code.
    """
    conn = create_cups_connection()
    printer_info = conn.getPrinterAttributes(printer_name)
    state_reasons = printer_info.get("printer-state-reasons", [])
    
    if "media-jam" in state_reasons:
        return "Papierstau", 501
    elif "media-empty" in state_reasons:
        return "Kein Papier", 502
    elif "toner-low" in state_reasons or "ink-low" in state_reasons:
        return "Wenig Toner/Tinte", 503
    return "OK", 200

def restart_printer(printer_name: str) -> bool:
    """
    Restart the specified printer.

    Args:
        printer_name (str): The name of the printer to restart.

    Returns:
        bool: True if the printer was successfully restarted, False otherwise.
    """
    conn = create_cups_connection()
    try:
        conn.cancelAllJobs(printer_name)
        conn.disablePrinter(printer_name)
        conn.enablePrinter(printer_name)
        time.sleep(5)
        return True
    except cups.IPPError:
        current_app.logger.error("Failed to restart printer %s", printer_name)
        return False

def cancel_all_jobs(printer_name: str):
    """
    Cancel all print jobs for the specified printer.

    Args:
        printer_name (str): The name of the printer.
    """
    conn = create_cups_connection()
    jobs = conn.getJobs()
    for job_id in jobs:
        conn.cancelJob(job_id, purge_job=True)


def log_printer_state(printer_name: str):
    """
    Log the current state of the printer.

    Args:
        printer_name (str): The name of the printer.
    """
    conn = create_cups_connection()
    printer_info = conn.getPrinterAttributes(printer_name)
    current_app.logger.debug("Printer state: %s", printer_info['printer-state'])
    current_app.logger.debug("State reasons: %s", printer_info.get('printer-state-reasons', []))

def print_image_cups(image_path: pathlib.Path, printer_name: str = "your_printer_name") -> int:
    conn = create_cups_connection()
    printers = conn.getPrinters()

    if printer_name not in printers:
        current_app.logger.error("Printer %s not found", printer_name)
        return 400

    try:
        job_id = conn.printFile(printer_name, str(image_path), "Python Image", {})
        current_app.logger.info("Print job %s sent to queue", job_id)

        # Wait and check status multiple times
        for _ in range(5):  # Check 5 times
            time.sleep(2)  # Wait 2 seconds between checks
            error_job_id, error_message = check_printer_error(conn, printer_name)
            status_info, status_code = check_printer_status(printer_name)
            print(error_job_id, error_message, status_code)
            if status_info != "OK":
                current_app.logger.error(status_info)
                conn.cancelJob(job_id)
                restart_printer(printer_name=printer_name)
                return status_code  # Use your specific error code for printer errors

            job_info = conn.getJobAttributes(job_id)
            job_state = job_info.get('job-state')

            if job_state == cups.IPP_JOB_COMPLETED:
                current_app.logger.info("Print job %s completed successfully", job_id)
                return 200

        current_app.logger.warning("Job status unclear after multiple checks")
        conn.cancelJob(job_id)
        restart_printer(printer_name=printer_name)
        return 500  # Unknown status after checks

    except cups.IPPError as e:
        current_app.logger.error("IPP Error: %s - %s", e.message, e.description)
        return 505

    except Exception as e:
        current_app.logger.error("Unexpected error: %s", str(e))
        return 500

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    status = print_image_cups(pathlib.Path("src/functions/test_qr.jpg").resolve(), "Canon_SELPHY_CP1500")
    print(f"Print status: {status}")