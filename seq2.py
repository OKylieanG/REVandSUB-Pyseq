import collections
import datetime
import os

def reverse_number(n):
    """
    Reverses the digits of a number.
    If the number is a single digit (0-9), it's treated as '0N'
    for reversal, e.g., 9 becomes '09' which reverses to 90.
    """
    s = str(n)
    if len(s) == 1:
        # Treat single digit 'X' as '0X' for the purpose of reversal
        s_to_reverse = "0" + s  # e.g., "9" becomes "09"
    else:
        s_to_reverse = s
    return int(s_to_reverse[::-1]) # Reverse the string and convert back to int

def get_canonical_loop(loop_list):
    """
    Converts a list representing a loop into a canonical tuple form.
    The canonical form starts with the smallest element of the loop
    and maintains the order. E.g., [63, 27, 9] -> (9, 63, 27)
    """
    if not loop_list:
        return tuple() # Should ideally not happen if a loop is found

    min_val = min(loop_list)
    min_idx = loop_list.index(min_val)
    
    # Rotate the list so that it starts with the minimum value
    canonical_loop_list = loop_list[min_idx:] + loop_list[:min_idx]
    return tuple(canonical_loop_list)

def find_ending_loop_for_number(initial_number, verbose=False):
    """
    Performs the reverse-subtract-repeat process for a single number
    and returns the canonical form of the loop it enters.

    Args:
        initial_number: The starting non-negative integer.
        verbose: If True, prints step-by-step calculations.

    Returns:
        A tuple representing the canonical form of the detected loop.
    """
    if not isinstance(initial_number, int) or initial_number < 0:
        raise ValueError("Input must be a non-negative integer.")

    seen_numbers = {}  # Stores number: index_in_sequence
    sequence = []
    current_number = initial_number
    step = 0

    if verbose:
        print(f"\nProcessing number: {initial_number}")
        print("-" * 20)

    while current_number not in seen_numbers:
        if verbose:
            print(f"  Step {step}: Current = {current_number}")

        seen_numbers[current_number] = len(sequence) # Record index before appending
        sequence.append(current_number)

        reversed_num = reverse_number(current_number)
        if verbose:
            print(f"    Reversed = {reversed_num} (single digits 'N' treated as '0N' for reversal)")

        if current_number == reversed_num:
            next_number = 0
            if verbose:
                print(f"    {current_number} == {reversed_num}, next = 0")
        elif current_number > reversed_num:
            next_number = current_number - reversed_num
            if verbose:
                print(f"    {current_number} - {reversed_num} = {next_number}")
        else: # reversed_num > current_number
            next_number = reversed_num - current_number
            if verbose:
                print(f"    {reversed_num} - {current_number} = {next_number}")
        
        current_number = next_number
        step += 1
    
    loop_start_index = seen_numbers[current_number]
    actual_loop_list = sequence[loop_start_index:]
    
    canonical_form = get_canonical_loop(actual_loop_list)
    
    if verbose:
        print(f"  Loop detected. Current number {current_number} was first seen at sequence index {loop_start_index}.")
        print(f"  Raw loop sequence: {actual_loop_list}")
        print(f"  Canonical loop: {list(canonical_form)}")
        print("-" * 20)
        
    return canonical_form

def analyze_number_range(start_range, end_range, show_individual_progress=False, save_to_file=True):
    """
    Analyzes all numbers in a given range, tracks the loops they fall into,
    and reports the frequency of each loop type.
    
    Args:
        start_range: Starting number of the range
        end_range: Ending number of the range
        show_individual_progress: Whether to show verbose output for each number
        save_to_file: Whether to save results to a text file
    """
    print(f"\nAnalyzing numbers from {start_range} to {end_range}...")
    loop_frequencies = collections.defaultdict(int)
    total_numbers_to_process = end_range - start_range + 1

    for i in range(start_range, end_range + 1):
        # Set verbose to True here if you want to see details for each number
        # For large ranges, it's better to keep it False.
        loop = find_ending_loop_for_number(i, verbose=show_individual_progress)
        loop_frequencies[loop] += 1
        
        # Progress indicator
        current_processed_count = i - start_range + 1
        if total_numbers_to_process <= 200: # More frequent updates for small ranges
            if current_processed_count % (total_numbers_to_process // 10 + 1) == 0 or current_processed_count == total_numbers_to_process:
                 print(f"  Processed {current_processed_count}/{total_numbers_to_process} numbers (up to {i})...")
        elif current_processed_count % 100 == 0 or current_processed_count == total_numbers_to_process or current_processed_count == 1 :
            print(f"  Processed {current_processed_count}/{total_numbers_to_process} numbers (up to {i})...")

    # Prepare summary text
    summary_lines = []
    summary_lines.append("--- Loop Analysis Summary ---")
    
    if not loop_frequencies:
        summary_lines.append("No numbers were processed or no loops found.")
        print("\n" + "\n".join(summary_lines))
        return

    # Sort loops by frequency (most common first), then by the loop itself for tie-breaking
    sorted_loops = sorted(loop_frequencies.items(), key=lambda item: (item[1], item[0]), reverse=True)

    summary_lines.append(f"Analysis of numbers from {start_range} to {end_range}")
    summary_lines.append(f"Total numbers processed: {total_numbers_to_process}")
    summary_lines.append(f"Found {len(sorted_loops)} distinct loop type(s):")
    summary_lines.append("")
    
    for loop, count in sorted_loops:
        summary_lines.append(f"  Loop: {list(loop)}  <-  {count} starting number(s) ended in this loop.")
    
    summary_lines.append("--- End of Summary ---")

    # Print to console
    print("\n" + "\n".join(summary_lines))
    
    # Save to file if requested
    if save_to_file:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"loop_analysis_{start_range}_to_{end_range}_{timestamp}.txt"
        
        try:
            with open(filename, 'w') as f:
                f.write(f"Number Loop Analysis Results\n")
                f.write(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n\n")
                f.write("\n".join(summary_lines))
                f.write(f"\n\n" + "=" * 50 + "\n")
                f.write("Analysis completed successfully.\n")
            
            print(f"\nResults saved to: {filename}")
            print(f"File location: {os.path.abspath(filename)}")
            
        except Exception as e:
            print(f"\nError saving to file: {e}")
            print("Results were displayed above but not saved.")

def analyze_single_number_to_file(number, save_to_file=True):
    """
    Analyzes a single number and optionally saves the detailed results to a file.
    
    Args:
        number: The number to analyze
        save_to_file: Whether to save results to a text file
    """
    if save_to_file:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"single_number_analysis_{number}_{timestamp}.txt"
        
        try:
            # Capture the analysis output
            import io
            import sys
            
            # Redirect stdout to capture print statements
            old_stdout = sys.stdout
            sys.stdout = captured_output = io.StringIO()
            
            # Run the analysis
            result = find_ending_loop_for_number(number, verbose=True)
            
            # Get the captured output
            analysis_text = captured_output.getvalue()
            
            # Restore stdout
            sys.stdout = old_stdout
            
            # Print to console as well
            print(analysis_text)
            
            # Save to file
            with open(filename, 'w') as f:
                f.write(f"Single Number Loop Analysis\n")
                f.write(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n\n")
                f.write(analysis_text)
                f.write(f"\n" + "=" * 50 + "\n")
                f.write(f"Final canonical loop: {list(result)}\n")
                f.write("Analysis completed successfully.\n")
            
            print(f"\nDetailed analysis saved to: {filename}")
            print(f"File location: {os.path.abspath(filename)}")
            
        except Exception as e:
            print(f"\nError saving to file: {e}")
            print("Analysis was displayed above but not saved.")
            # Run analysis normally if file saving fails
            find_ending_loop_for_number(number, verbose=True)
    else:
        find_ending_loop_for_number(number, verbose=True)

# --- Main part of the program ---
if __name__ == "__main__":
    while True:
        try:
            print("\n------------------------------------------------------------")
            mode = input("Choose mode: (1) Analyze a single number with details, (2) Analyze a range of numbers, (exit) to quit: ").strip().lower()
            print("------------------------------------------------------------")

            if mode == 'exit':
                print("Exiting program.")
                break
            
            if mode == '1':
                num_str = input("Enter a non-negative integer to analyze: ")
                num = int(num_str)
                if num < 0:
                    print("Please enter a non-negative integer.")
                    continue
                
                # Ask if user wants to save to file
                save_str = input("Save detailed analysis to file? (yes/no, default: yes): ").strip().lower()
                save_file = save_str != 'no'
                
                analyze_single_number_to_file(num, save_to_file=save_file)

            elif mode == '2':
                start_str = input("Enter the start of the range (non-negative integer): ")
                start_val = int(start_str)
                end_str = input("Enter the end of the range (non-negative integer): ")
                end_val = int(end_str)

                if start_val < 0 or end_val < 0:
                    print("Range values must be non-negative integers.")
                    continue
                if end_val < start_val:
                    print("End of range cannot be less than the start of the range.")
                    continue
                
                # Ask if user wants verbose output for each number in range (usually no for large ranges)
                verbose_range_str = input("Show step-by-step for each number in range? (yes/no, default: no): ").strip().lower()
                show_steps_in_range = verbose_range_str == 'yes'
                
                # Ask if user wants to save to file
                save_str = input("Save summary results to file? (yes/no, default: yes): ").strip().lower()
                save_file = save_str != 'no'

                analyze_number_range(start_val, end_val, show_individual_progress=show_steps_in_range, save_to_file=save_file)
            
            else:
                print("Invalid mode selected. Please choose '1', '2', or 'exit'.")

        except ValueError:
            print("Invalid input. Please enter valid integers where required.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")