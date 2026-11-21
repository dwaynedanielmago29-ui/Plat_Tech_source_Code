
# ==========================================
# BANKER'S ALGORITHM
# File: bankers.py
# Purpose: Deadlock Avoidance and Safety Check
# ==========================================


def validate_algorithm_inputs(total, allocation, maximum):
    """
    Performs basic checks before running the algorithm.
    Returns the number of processes and resource types.
    """

    if not isinstance(total, (list, tuple)) or not total:
        raise ValueError("Total resources must not be empty.")

    if not isinstance(allocation, (list, tuple)) or not allocation:
        raise ValueError("Allocation matrix must not be empty.")

    if not isinstance(maximum, (list, tuple)) or not maximum:
        raise ValueError("Maximum matrix must not be empty.")

    process_count = len(allocation)
    resource_count = len(total)

    if len(maximum) != process_count:
        raise ValueError(
            "Allocation and Maximum matrices must have "
            "the same number of processes."
        )

    def check_number(value):
        return (
            isinstance(value, int)
            and not isinstance(value, bool)
            and value >= 0
        )

    for value in total:
        if not check_number(value):
            raise ValueError(
                "Total resources must contain "
                "non-negative whole numbers."
            )

    for matrix_name, matrix in (
        ("Allocation", allocation),
        ("Maximum", maximum)
    ):
        for row in matrix:
            if not isinstance(row, (list, tuple)):
                raise ValueError(
                    f"{matrix_name} must contain valid rows."
                )

            if len(row) != resource_count:
                raise ValueError(
                    f"Each {matrix_name} row must contain "
                    f"{resource_count} resource values."
                )

            for value in row:
                if not check_number(value):
                    raise ValueError(
                        f"{matrix_name} must contain "
                        "non-negative whole numbers."
                    )

    # Allocation cannot exceed maximum demand.
    for i in range(process_count):
        for j in range(resource_count):
            if allocation[i][j] > maximum[i][j]:
                raise ValueError(
                    f"Process P{i}: Allocation cannot exceed "
                    f"Maximum for resource R{j}."
                )

    # Total allocated resources cannot exceed total resources.
    for j in range(resource_count):

        allocated = sum(
            allocation[i][j]
            for i in range(process_count)
        )

        if allocated > total[j]:
            raise ValueError(
                f"Allocated amount of resource R{j} "
                "exceeds its total resources."
            )

    return process_count, resource_count


# ==========================================
# CALCULATE NEED MATRIX
# ==========================================

def calculate_need(allocation, maximum):
    """
    Need = Maximum - Allocation
    """

    need = []

    for i in range(len(allocation)):

        row = []

        for j in range(len(allocation[i])):

            required = maximum[i][j] - allocation[i][j]
            row.append(required)

        need.append(row)

    return need


# ==========================================
# CALCULATE AVAILABLE RESOURCES
# ==========================================

def calculate_available(total, allocation):
    """
    Available = Total - Sum of Allocated Resources
    """

    resource_count = len(total)

    available = []

    for j in range(resource_count):

        allocated = sum(
            allocation[i][j]
            for i in range(len(allocation))
        )

        available.append(total[j] - allocated)

    return available


# ==========================================
# BANKER'S SAFETY ALGORITHM
# ==========================================

def safety_algorithm(available, allocation, need):
    """
    Checks whether the system is in a safe state.

    Returns:
        safe
        safe_sequence
        trace
        final_work
        finish
    """

    process_count = len(allocation)

    # Initialize Work and Finish
    work = available.copy()

    finish = [False] * process_count

    safe_sequence = []

    trace = []

    step_number = 1

    trace.append({
        "step": 0,
        "event": "INITIALIZATION",
        "message": "Safety Algorithm started.",
        "work": work.copy(),
        "finish": finish.copy()
    })

    # Continue until all processes finish
    while len(safe_sequence) < process_count:

        found_process = False

        for i in range(process_count):

            if finish[i]:
                continue

            # Compare Need with Work
            can_execute = all(
                need[i][j] <= work[j]
                for j in range(len(work))
            )

            trace.append({
                "step": step_number,
                "event": "CHECK",
                "process": f"P{i}",
                "need": need[i].copy(),
                "work": work.copy(),
                "can_execute": can_execute,
                "message": (
                    f"Checking whether P{i} can execute."
                )
            })

            step_number += 1

            if can_execute:

                # Process finishes and releases resources
                previous_work = work.copy()

                for j in range(len(work)):
                    work[j] += allocation[i][j]

                finish[i] = True

                safe_sequence.append(f"P{i}")

                trace.append({
                    "step": step_number,
                    "event": "EXECUTE",
                    "process": f"P{i}",
                    "previous_work": previous_work,
                    "allocation": allocation[i].copy(),
                    "work": work.copy(),
                    "finish": finish.copy(),
                    "message": (
                        f"P{i} completed and released "
                        "its allocated resources."
                    )
                })

                step_number += 1

                found_process = True

                # Start scanning again
                break

        # No unfinished process can execute
        if not found_process:
            break

    # Check if every process has finished
    safe = all(finish)

    trace.append({
        "step": step_number,
        "event": "FINAL",
        "safe": safe,
        "sequence": safe_sequence.copy(),
        "work": work.copy(),
        "finish": finish.copy(),
        "message": (
            "System is in a SAFE state."
            if safe
            else "System is in an UNSAFE state."
        )
    })

    return {
        "safe": safe,
        "safe_sequence": safe_sequence,
        "trace": trace,
        "final_work": work,
        "finish": finish
    }


# ==========================================
# MAIN FUNCTION FOR GUI INTEGRATION
# ==========================================

def run_bankers_algorithm(total, allocation, maximum):
    """
    Main function called by main.py.

    Parameters:
        total       = Total resource vector
        allocation  = Allocation matrix
        maximum     = Maximum demand matrix

    Returns:
        Dictionary containing all calculation results.
    """

    # Validate the supplied data
    process_count, resource_count = validate_algorithm_inputs(
        total,
        allocation,
        maximum
    )

    # Calculate Need
    need = calculate_need(allocation, maximum)

    # Calculate Available
    available = calculate_available(total, allocation)

    # Run Safety Algorithm
    safety_result = safety_algorithm(
        available,
        allocation,
        need
    )

    # Return everything to the GUI
    return {
        "process_count": process_count,
        "resource_count": resource_count,
        "total": list(total),
        "allocation": [list(row) for row in allocation],
        "maximum": [list(row) for row in maximum],
        "need": need,
        "available": available,
        "safe": safety_result["safe"],
        "safe_sequence": safety_result["safe_sequence"],
        "trace": safety_result["trace"],
        "final_work": safety_result["final_work"],
        "finish": safety_result["finish"]
    }
