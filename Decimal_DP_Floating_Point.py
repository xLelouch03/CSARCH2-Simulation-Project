'''
List of TODOs:
    1. TODO: Implement Rounding
    2. TODO: Add other special test cases for the combination field
'''
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk

#get input from user
# MAJOR FUNCTION
def get_input_from_user():
  print("Decimal: ", end = '')
  decimal_input = str(input())
  print("10 raised to: ", end = '')
  ten_raised_to = int(input())
  print("Rounding Type: ", end = '')
  rounding_type = input()

  return decimal_input, ten_raised_to, rounding_type

#limit the decimal to 16 digits by either adding leading zeroes or round off
# HELPER FUNCTION
def limit_to_16_digits(decimal_input, exponent, rounding_type, sign_bit):

  #If it's more than 16 digits, round the decimal to 16 digits
  
  if len(decimal_input) > 16:
    #increase the exponent based on the number of digits after the 16th
    exponent += (len(decimal_input) - 16)
    
    if rounding_type == 'truncate':
      decimal_input = decimal_input[:16]
    elif rounding_type == 'floor':
      
      #if sign_bit == 1 (negative)
      decimal_input = decimal_input[:16]
      
      #else sign_bit == 0 (positive)
      #truncate
    elif rounding_type == 'ceiling':
      # Adjust the exponent if rounding changes the value
      
      #if sign_bit == 0 (positive)
      decimal_input = int(decimal_input[:16]) + 1
      decimal_input = str(decimal_input)
      
      #if sign_bit == 1 (negative)
      #truncate
    elif rounding_type == 'nearest':
      original_decimal = int(decimal_input[:16])
      rounded_decimal = original_decimal + 1 if int(decimal_input[16]) >= 5 else original_decimal
      decimal_input = str(rounded_decimal)
    
  #remove trailing zeroes that was made from rounding
  decimal_input, exponent = remove_trailing_zeroes(decimal_input, exponent)
      
  #if there is less than 16 digits, add leading zeroes
  if len(decimal_input) < 16:
    number_of_missing_digits = 16 - len(decimal_input)
    for i in range(number_of_missing_digits):
      decimal_input = "0" + decimal_input

  return decimal_input, exponent

#identify the sign bit
# MAJOR FUNCTION
def get_sign_bit(decimal_input):
  if decimal_input[0] == '-':
    return "1"
  else:
    return "0"

#turn decimal to positive
# MAJOR FUNCTION
def turn_decimal_positive(decimal_input):
  decimal_input = decimal_input[1:]
  return decimal_input

def remove_trailing_zeroes(decimal_input, exponent):
  while decimal_input[len(decimal_input) - 1] == '0':
    decimal_input = decimal_input[0: len(decimal_input) - 1]
    exponent += 1
  return decimal_input, exponent

#normalize the decimal
# MAJOR FUNCTION
def normalize_decimal(decimal_input, exponent, rounding_type, sign_bit):
  decimal_point_location = decimal_input.find(".")

  #if a decimal point exists, move it to the rightmost and then remove it
  if decimal_point_location != -1:
    right_of_decimal_point = decimal_input[decimal_point_location + 1:]
    left_of_decimal_point = decimal_input[0: decimal_point_location]
    decimal_input = left_of_decimal_point + right_of_decimal_point
    exponent -= len(right_of_decimal_point)

  #remove trailing zeroes
  decimal_input, exponent = remove_trailing_zeroes(decimal_input, exponent)

  #remove leading zeroes
  while decimal_input[0] == '0':
    decimal_input = decimal_input[1:]

  #limit to 16 digits only
  decimal_input, exponent = limit_to_16_digits(decimal_input, exponent, rounding_type, sign_bit)
  
  return decimal_input, exponent

#identify the most significant digit
# HELPER FUNCTION
def get_msd(decimal_input):
  msd = decimal_input[0]
  msd = int(msd)
  return msd

#change the most significant digit to binary
# HELPER FUNCTION
def transform_msd_to_binary(msd):
  msd_binary = bin(msd)
  msd_binary = msd_binary[2:].zfill(4)
  return msd_binary

#calculate for e prime
# HELPER FUNCTION
def get_exponent_prime(exponent):
  exp_prime = exponent + 398
  return exp_prime

#change e prime to binary
# HELPER FUNCTION
def transform_exponent_prime_to_binary(exp_prime):
  exp_prime_binary = bin(exp_prime)
  exp_prime_binary = exp_prime_binary[2:].zfill(10)
  return exp_prime_binary

#get the exponent extention from the e prime in binary
# HELPER FUNCTION
def get_exponent_extension(exp_prime_binary):
  exp_extension = exp_prime_binary[2:].zfill(8)
  return exp_extension

#calculate the combination field and the exponent extension
# MAJOR FUNCTION    
def get_combination_field_and_exponent_extension(decimal_input, exponent):
    
  msd = get_msd(decimal_input)
  msd_binary = transform_msd_to_binary(msd)
  exponent_prime = get_exponent_prime(exponent)
  exp_prime_binary = transform_exponent_prime_to_binary(exponent_prime)
  
  if msd >= 0 and msd <= 7:
    combi_field = exp_prime_binary[0:2] + msd_binary[1:]
  elif msd == 8 or msd == 9:
    combi_field = "11" + exp_prime_binary[0:2] + msd_binary[3]

  exponent_extension = get_exponent_extension(exp_prime_binary)
  
  return combi_field, exponent_extension

  #TODO: Add other special cases
def handle_special_cases(exponent):
    if exponent >= 398:  # Positive infinity
        sign_bit = "0"
        combination_field = "11110"
        exponent_extension = "000000000"
        coefficient_continuation = ["0000000000"] * 5
        if get_exponent_prime(exponent) > 767:
          exponent = ""
          exp_prime = ""
          exp_prime_binary = ""
          decimal_input = "inf"
    elif exponent <= -398:  # Negative infinity
        sign_bit = "1"
        combination_field = "11111"
        exponent_extension = "000000000"
        coefficient_continuation = ["0000000000"] * 5
        if get_exponent_prime(exponent) > 767:
          exponent = ""
          exp_prime = ""
          exp_prime_binary = ""
          decimal_input = "-inf"  # Set normalized decimal to "-inf"
    else:
        return None  # No special case detected, return None
    
    return sign_bit, combination_field, exponent_extension, coefficient_continuation, exp_prime, exp_prime_binary, decimal_input

#calculate for the densely packed bcd of three digits
# HELPER FUNCTION
def get_densely_packed_bcd(three_digits):
  first = int(three_digits[0]) if three_digits[0].isdigit() else 0
  second = int(three_digits[1]) if three_digits[1].isdigit() else 0
  third = int(three_digits[2]) if three_digits[2].isdigit() else 0

  first_binary = bin(first)[2:].zfill(4)
  second_binary = bin(second)[2:].zfill(4)
  third_binary = bin(third)[2:].zfill(4)

  a, b, c, d = [digit for digit in first_binary]
  e, f, g, h = [digit for digit in second_binary]
  i, j, k, m = [digit for digit in third_binary]

  r = d
  u = h
  y = m

  if a == '0' and e == '0' and i == '0':
    p = b
    q = c

    s = f
    t = g  

    v = '0'
    w = j
    x = k   

  #there is at least one digit that is 8 or 9
  else:
    v = '1'

    #if only third digit is 8 or 9
    if a == '0' and e == '0':
      p = b
      q = c

      s = f
      t = g

      w = '0'
      x = '0'

    #if only second digit is 8 or 9
    elif a == '0' and i == '0':
      p = b
      q = c
      
      s = j
      t = k

      w = '0'
      x = '1'

    #if only first digit is 8 or 9
    elif e == '0' and i == '0':
      p = j
      q = k
      
      s = f
      t = g

      w = '1'
      x = '0'

    #there is at least 2 digits that are 8 or 9
    else:
      w = '1'
      x = '1'

      #if all digits are 8 or 9
      if a == '1' and e == '1' and i == '1':
        p = '0'
        q = '0'

        s = '1'
        t = '1'

      #if only first digit is <= 7
      elif a == '0':
        p = b
        q = c

        s = '1'
        t = '0'

      #if only second digit is <= 7
      elif e == '0':
        p = f
        q = g

        s = '0'
        t = '1'

      #if only third digit is <= 7
      else:
        p = j
        q = k

        s = '0'
        t = '0'

  densely_packed_bcd = p + q + r + s + t + u + v + w + x + y
  return densely_packed_bcd

#get the densely packed bcd of all the coefficient digits
# MAJOR FUNCTION
def get_coefficient_continuation(decimal_input):
  coefficient_digits = decimal_input[1:]
  coefficient_binary = []
  for i in range(5):
    three_digits = coefficient_digits[i * 3: (i+1) * 3]
    coefficient_binary.append(get_densely_packed_bcd(three_digits))
  return coefficient_binary

#multiply binary digits to their place value and return its corresponding hexadecimal value
# HELPER FUNCTION
def convert_four_binary_to_hexadecimal(four_binary_digits):
  if len(four_binary_digits) != 4:
        return '0'
      
  eight, four, two, one = [int(digit) for digit in four_binary_digits]
  eight *= 8
  four *= 4
  two *= 2
  
  total = eight + four + two + one
  hexadecimal_equivalent = ""
  
  if total < 10:
    hexadecimal_equivalent = str(total)
  elif total == 10:
    hexadecimal_equivalent = "A"
  elif total == 11:
    hexadecimal_equivalent = "B"
  elif total == 12:
    hexadecimal_equivalent = "C"
  elif total == 13:
    hexadecimal_equivalent = "D"
  elif total == 14:
    hexadecimal_equivalent = "E"
  else:
    hexadecimal_equivalent = "F"
    
  return hexadecimal_equivalent

#convert binary to hexadecimal
# MAJOR FUNCTION
def convert_output_to_hexadecimal(binary_output):
  hexadecimal_digits = ""
  for i in range(16):
    four_binary_digits = binary_output[i * 4: (i+1) * 4]
    hexadecimal_digits = hexadecimal_digits + convert_four_binary_to_hexadecimal(four_binary_digits)
  return hexadecimal_digits

# BEGIN

def validate_decimal_input(decimal_input):
    if not decimal_input:
        messagebox.showerror("Error", "Decimal input cannot be empty")
        return False
    return True

def validate_ten_raised_to_input(ten_raised_to):
    if not ten_raised_to:
        messagebox.showerror("Error", "Exponent field cannot be empty")
        return False
    return True
#
# Function to get input from the GUI
def get_input_from_gui():
    decimal_input = decimal_entry.get()
    ten_raised_to = exponent_entry.get()
    rounding_type = rounding_combobox.get()
    
    if decimal_input == "0" or decimal_input == "-0":
      display_output_in_gui("0", "0000000000000000", "0", "01000", "00000000", ["00000000"]*5, "398", "10001110")
      return None, None, None
      
    if not all(char.isdigit() or char == '-' for char in decimal_input):
        # Set output fields for non-numeric input
      display_output_in_gui("0", "", "", "11111", "00000000", ["00000000"]*5, "", "")
      
      return None, None, None

    if not validate_decimal_input(decimal_input):
        return None, None, None
    if not validate_ten_raised_to_input(ten_raised_to):
        return None, None, None
      
    try:
        ten_raised_to_int = int(ten_raised_to)
    except ValueError:
        messagebox.showerror("Error", "Fields must be numeric")
        return None, None, None  
    return decimal_input, int(ten_raised_to), rounding_type

# Function to display the output in the GUI text widget
def display_output_in_gui(sign_bit, decimal_input, exponent, combination_field, exponent_extension, coefficient_continuation, exp_prime, exp_prime_binary):
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Normalized Decimal: {'-' if sign_bit == '1' else ''}{decimal_input}\n")
    output_text.insert(tk.END, f"Normalized Exponent: {exponent}\n")
    output_text.insert(tk.END, f"Exponent Prime: {exp_prime}\n") 
    output_text.insert(tk.END, f"Exponent Prime Binary: {exp_prime_binary}\n")  
    output_text.insert(tk.END, f"Sign Bit: {sign_bit}\n")
    output_text.insert(tk.END, f"Combination Field: {combination_field}\n")
    output_text.insert(tk.END, f"Exponent Extension: {exponent_extension}\n")
    output_text.insert(tk.END, "Coefficient Continuation: " + ' '.join(coefficient_continuation) + "\n")
    
    binary_output = sign_bit + combination_field + exponent_extension + ''.join(coefficient_continuation)
    hexadecimal_output = convert_output_to_hexadecimal(binary_output)
    binary_output_with_spaces = sign_bit + " " +  combination_field + " " + exponent_extension + " " + ''.join([' '.join(bits) for bits in [coefficient_continuation[i:i+10] for i in range(0, len(coefficient_continuation), 10)]])
    
    output_text.insert(tk.END, f"Binary Output: {binary_output_with_spaces}\n")
    output_text.insert(tk.END, f"Hexadecimal Output: {hexadecimal_output}\n")

# Function to convert and display output when Convert button is clicked
def convert_and_display_output():
    decimal_input, ten_raised_to, rounding_type = get_input_from_gui()  
    if decimal_input is None or ten_raised_to is None or rounding_type is None:
        return
    sign_bit = get_sign_bit(decimal_input)
    if sign_bit == "1": 
        decimal_input = turn_decimal_positive(decimal_input)
    decimal_input, exponent = normalize_decimal(decimal_input, ten_raised_to, rounding_type, sign_bit)
    
    special_case_result = handle_special_cases(exponent)
    if special_case_result:
        sign_bit, combination_field, exponent_extension, coefficient_continuation, exp_prime, exp_prime_binary, decimal_input = special_case_result
    else:
      combination_field, exponent_extension = get_combination_field_and_exponent_extension(decimal_input, exponent)
      coefficient_continuation = get_coefficient_continuation(decimal_input)
      exp_prime = get_exponent_prime(exponent) 
      exp_prime_binary = transform_exponent_prime_to_binary(exp_prime) 
      
    display_output_in_gui(sign_bit, decimal_input, exponent, combination_field, exponent_extension, coefficient_continuation, exp_prime, exp_prime_binary)

# Function to save the output when Save Output button is clicked
def save_output():
    output_text_content = output_text.get(1.0, tk.END)
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(output_text_content)
        messagebox.showinfo("Success", "Output saved successfully!")

# Create the root window
root = tk.Tk()
root.title("Decimal Converter")

# Set the size of the window
root.geometry("900x500") 

# Input GUI elements
decimal_label = tk.Label(root, text="Decimal:")
decimal_label.grid(row=0, column=3)

decimal_entry = tk.Entry(root)
decimal_entry.grid(row=0, column=4)

exponent_label = tk.Label(root, text="10 raised to:")
exponent_label.grid(row=1, column=3)

exponent_entry = tk.Entry(root)
exponent_entry.grid(row=1, column=4)

rounding_label = tk.Label(root, text="Rounding Type:")
rounding_label.grid(row=2, column=3)

# Rounding type dropdown
rounding_combobox = ttk.Combobox(root, values=["truncate", "floor", "ceiling", "nearest"])
rounding_combobox.grid(row=2, column=4)
rounding_combobox.current(0)  # Set the default value to "truncate"

# Convert button for conversion and display output
convert_button = tk.Button(root, text="Convert", command=convert_and_display_output)
convert_button.grid(row=3, column=4)

# Save Output button to save the output
save_button = tk.Button(root, text="Save Output", command=save_output)
save_button.grid(row=4, column=4)

# GUI element for output
output_text = tk.Text(root, height=10, width=100)  
output_text.grid(row=5, columnspan=10)

root.mainloop()
