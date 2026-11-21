
"""
validation.py
Input validation module for the Banker's Algorithm Simulator.

GUI integration:
    from validation import validate_all, ValidationError

    try:
        validate_all(
            num_processes,
            num_resources,
            total,
            allocation,
            maximum
        )
    except ValidationError as error:
        messagebox.showerror("Validation Error", str(error))

The Banker's Safety Algorithm belongs in bankers.py.
"""


class ValidationError(Exception):
    """Raised when user-provided system information is invalid."""
    pass


def _is_whole_number(value):
    """Accept integers and integral floats, but never booleans."""
    if isinstance(value, bool):
        return False

    if isinstance(value, int):
        return True

    if isinstance(value, float):
        return value.is_integer()

    return False


def _validate_non_negative_whole_number(value, location):
    """Check whether a value is a non-negative whole number."""

    if not _is_whole_number(value):
        raise ValidationError(
            f"{location} must be a whole number (got '{value}')."
        )

    if value < 0:
        raise ValidationError(
            f"{location} cannot be negative (got {value})."
        )


def validate_counts(num_processes, num_resources):
    """Ensure process and resource counts are positive whole numbers."""

    for name, value in (
        ("Number of processes", num_processes),
        ("Number of resource types", num_resources),
    ):
        if not _is_whole_number(value):
            raise ValidationError(
                f"{name} must be a whole number."
            )

        if value <= 0:
            raise ValidationError(
                f"{name} must be greater than zero."
            )

    return True


def validate_total(total, num_resources):
    """Ensure Total has one non-negative whole number per resource."""

    if not isinstance(total, (list, tuple)):
        raise ValidationError(
            "Total resources must be a list or tuple."
        )

    if len(total) != num_resources:
        raise ValidationError(
            f"Total must have {num_resources} value(s), "
            f"but {len(total)} were given."
        )

    for j, value in enumerate(total):
        _validate_non_negative_whole_number(
            value, f"Total for resource R{j}"
        )

    return True


def validate_matrix(matrix, name, num_processes, num_resources):
    """Check matrix dimensions and resource values."""

    if not isinstance(matrix, (list, tuple)):
        raise ValidationError(
            f"{name} must be a matrix (list of rows)."
        )

    if len(matrix) != num_processes:
        raise ValidationError(
            f"{name} must have {num_processes} row(s), "
            f"but {len(matrix)} were given."
        )

    for i, row in enumerate(matrix):

        if not isinstance(row, (list, tuple)):
            raise ValidationError(
                f"{name} row for P{i} must be a list or tuple of values."
            )

        if len(row) != num_resources:
            raise ValidationError(
                f"{name} row for P{i} must have {num_resources} column(s), "
                f"but {len(row)} were given."
            )

        for j, value in enumerate(row):
            _validate_non_negative_whole_number(
                value, f"{name}[P{i}][R{j}]"
            )

    return True


def validate_allocation_vs_max(allocation, maximum):
    """Ensure Allocation does not exceed Max."""

    for i, (allocation_row, maximum_row) in enumerate(
        zip(allocation, maximum)
    ):

        for j, (allocated, max_required) in enumerate(
            zip(allocation_row, maximum_row)
        ):

            if allocated > max_required:
                raise ValidationError(
                    f"Allocation[P{i}][R{j}] = {allocated} exceeds "
                    f"Max[P{i}][R{j}] = {max_required}. "
                    "Reduce Allocation or increase Max."
                )

    return True


def validate_allocation_vs_total(allocation, total):
    """Ensure total allocated units do not exceed Total resources."""

    for j, total_amount in enumerate(total):

        allocated_amount = sum(row[j] for row in allocation)

        if allocated_amount > total_amount:
            raise ValidationError(
                f"Total allocated for resource R{j} is "
                f"{allocated_amount}, which exceeds its Total "
                f"of {total_amount}. "
                "Reduce Allocation or increase Total."
            )

    return True


def validate_all(num_processes, num_resources, total, allocation, maximum):
    """
    Run all validation rules.

    Returns True if valid.
    Raises ValidationError if input is invalid.
    """

    validate_counts(num_processes, num_resources)

    num_processes = int(num_processes)
    num_resources = int(num_resources)

    validate_total(total, num_resources)

    validate_matrix(
        allocation,
        "Allocation",
        num_processes,
        num_resources
    )

    validate_matrix(
        maximum,
        "Max",
        num_processes,
        num_resources
    )

    validate_allocation_vs_max(allocation, maximum)

    validate_allocation_vs_total(allocation, total)

    return True


def is_valid(num_processes, num_resources, total, allocation, maximum):
    """GUI-friendly wrapper returning a validity result and message."""

    try:
        validate_all(
            num_processes,
            num_resources,
            total,
            allocation,
            maximum
        )

        return True, "Input is valid."

    except ValidationError as error:
        return False, str(error)


if __name__ == "__main__":

    # Classic Banker's Algorithm example

    total = [10, 5, 7]

    allocation = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2],
    ]

    maximum = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3],
    ]

    print(
        "Valid example:",
        is_valid(5, 3, total, allocation, maximum)
    )

    invalid_allocation = [
        [8, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2],
    ]

    print(
        "Invalid example:",
        is_valid(5, 3, total, invalid_allocation, maximum)
    )
