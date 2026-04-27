class AppError(Exception):
    """Base application exception.
    Args:
        """
    status_code: int = 500
    detail: str = 'Application error.'

    def __init__(self, detail: str | None = None) -> None:
        """Initialize application exception.
        Args:
            detail (str | None): Custom exception detail."""
        if detail is not None:
            self.detail = detail

        super().__init__(self.detail)


class MissingFileNameError(AppError):
    """Raise when uploaded file name is missing.
    Args:
        """
    status_code = 400
    detail = 'Uploaded file name is missing.'


class InvalidFileExtensionError(AppError):
    """Raise when uploaded file extension is invalid.
    Args:
        """
    status_code = 400
    detail = 'Only .xlsx files are allowed.'


class FileReadError(AppError):
    """Raise when uploaded file cannot be read.
    Args:
        """
    status_code = 400
    detail = 'Failed to read uploaded xlsx file.'


class PipelineExecutionError(AppError):
    """Raise when pipeline execution fails.
    Args:
        """
    status_code = 500
    detail = 'Pipeline execution failed.'


class ValidationExecutionError(AppError):
    """Raise when validation execution fails.
    Args:
        """
    status_code = 500
    detail = 'Validation execution failed.'
