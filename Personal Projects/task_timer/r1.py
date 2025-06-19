
import datetime as dt

class TaskTimer:
    def __init__(self):
        # Initialize with placeholder values for demonstration
        self.task_start_time = None
        self.task_end_time = None
        self.work_seconds = 0 # This is assumed to be an integer, accumulated from int(segment.total_seconds())

    def set_times_for_demo(self, start_str, end_str, work_s):
        """Helper to set times for testing the function."""
        # Assuming times are in a consistent format like "YYYY-MM-DD HH:MM:SS"
        # For simplicity, using a dummy date for time-only examples, but dt.datetime handles cross-day fine.
        dummy_date = "2025-06-18 " # Or "2025-06-19 " for cross-day if needed
        if " " not in start_str: # Assume only time is given if no space
             start_str = dummy_date + start_str
        if " " not in end_str:
            end_str = dummy_date + end_str

        # Handle cross-day scenario for example setting
        start_dt = dt.datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")
        end_dt = dt.datetime.strptime(end_str, "%Y-%m-%d %H:%M:%S")

        # If end time is earlier than start time, assume it crosses midnight
        if end_dt < start_dt:
            end_dt += dt.timedelta(days=1)

        self.task_start_time = start_dt
        self.task_end_time = end_dt
        self.work_seconds = work_s # This is already assumed to be an integer

    def _calculate_duration(self):
        """
        Calculates work_minutes, pause_minutes, and total_task_minutes based on specific rules:
        1. total_task_minutes aligns with Excel's visual minute boundaries (e.g., 10:30:44 -> 10:30:00).
        2. pause_minutes is derived from the actual precise pause duration, truncated to whole minutes.
        3. work_minutes is derived to ensure work_minutes + pause_minutes == total_task_minutes.

        Assumes self.work_seconds is an integer, accumulated by truncating fractional seconds
        from individual work segments.
        """

        # 1. Calculate total_task_minutes (the 'Excel visual' duration)
        # This aligns with how Excel typically calculates duration between timestamps when displayed as HH:MM.
        # It involves trimming seconds/microseconds to the beginning of the minute.
        task_start_trimmed = self.task_start_time.replace(second=0, microsecond=0)
        task_end_trimmed = self.task_end_time.replace(second=0, microsecond=0)

        # Calculate total seconds between the trimmed minute boundaries.
        # This will always be an exact multiple of 60 seconds.
        total_task_seconds = (task_end_trimmed - task_start_trimmed).total_seconds()

        # Convert to minutes using integer division.
        # Since total_task_seconds is always a multiple of 60 here, round(), int(), and // 60
        # will yield the same correct integer result for total minutes.
        total_task_minutes = int(total_task_seconds) // 60

        # 2. Calculate the actual wall-clock duration of the task.
        # This is the precise time from start to end, including all seconds and microseconds.
        # We then explicitly cast it to an integer to ensure consistency with self.work_seconds,
        # which is also accumulated as an integer (due to truncation of fractional seconds).
        total_actual_seconds_int = int((self.task_end_time - self.task_start_time).total_seconds())

        # 3. Calculate the true pause duration in seconds.
        # This is the difference between the total wall-clock time and the actual accumulated work time.
        # Using max(0, ...) ensures pause time is never negative if work_seconds slightly exceeds total_actual_seconds
        # due to precision differences or very minor overlaps.
        true_pause_seconds_int = max(0, total_actual_seconds_int - self.work_seconds)

        # 4. Convert the true pause seconds to pause minutes.
        # We use integer division (truncation) to get whole minutes for pause.
        pause_minutes = true_pause_seconds_int // 60

        # 5. Derive work_minutes to ensure the sum consistency.
        # This is the key step to meet the requirement: work_minutes + pause_minutes = total_task_minutes.
        # By deriving work_minutes this way, it 'fills the gap' to make the equation balance,
        # resolving the 'ghost pause' issue when work_seconds don't perfectly align with minute boundaries.
        work_minutes = total_task_minutes - pause_minutes
        work_minutes = max(0, work_minutes) # Ensure work_minutes is not negative

        # For debugging/verification:
        print(f"{self.work_seconds=} {work_minutes=} || "
              f"{self.task_start_time=} {self.task_end_time} | "
              f"{total_actual_seconds_int=} || "
              f"{task_start_trimmed=} {task_end_trimmed=} | "
              f"{total_task_minutes=} {pause_minutes=}")

        return work_minutes, pause_minutes, total_task_minutes

# --- Demonstration of Usage ---
if __name__ == "__main__":
    timer = TaskTimer()

    print("--- Scenario 1: Original 'Ghost Pause' Example ---")
    timer.set_times_for_demo("2025-06-18 10:30:44", "2025-06-18 10:31:33", 49) # 49 actual seconds, no pause
    work_m, pause_m, total_m = timer._calculate_duration()
    print(f"Result: Work: {work_m}m, Pause: {pause_m}m, Total: {total_m}m")
    # Expected: Work: 1m, Pause: 0m, Total: 1m (matches user's goal)

    print("\n--- Scenario 2: Cross-Midnight Example (2 work mins) ---")
    timer.set_times_for_demo("2025-06-18 23:59:35", "2025-06-19 00:01:59", 144) # 144 actual seconds, no pause
    work_m, pause_m, total_m = timer._calculate_duration()
    print(f"Result: Work: {work_m}m, Pause: {pause_m}m, Total: {total_m}m")
    # Expected: Work: 2m, Pause: 0m, Total: 2m

    print("\n--- Scenario 3: Task with actual pause ---")
    timer.set_times_for_demo("2025-06-18 10:00:00", "2025-06-18 10:05:00", 60) # 300 actual seconds, 60 work seconds (4 mins pause)
    work_m, pause_m, total_m = timer._calculate_duration()
    print(f"Result: Work: {work_m}m, Pause: {pause_m}m, Total: {total_m}m")
    # Expected: Work: 1m, Pause: 4m, Total: 5m

    print("\n--- Scenario 4: Very short task (less than 1 minute) ---")
    timer.set_times_for_demo("2025-06-18 10:00:10", "2025-06-18 10:00:25", 15) # 15 actual seconds, no pause
    work_m, pause_m, total_m = timer._calculate_duration()
    print(f"Result: Work: {work_m}m, Pause: {pause_m}m, Total: {total_m}m")
    # Expected: Work: 0m, Pause: 0m, Total: 0m

    print("\n--- Scenario 5: Task exactly on minute boundaries ---")
    timer.set_times_for_demo("2025-06-18 10:00:00", "2025-06-18 10:01:00", 60) # 60 actual seconds, no pause
    work_m, pause_m, total_m = timer._calculate_duration()
    print(f"Result: Work: {work_m}m, Pause: {pause_m}m, Total: {total_m}m")
    # Expected: Work: 1m, Pause: 0m, Total: 1m
