'''
List of TODOs:
    1. TODO: Implement Rounding
    2. TODO: Add other special test cases for the combination field
    3. TODO: Provide an option for the user to download the output
    4. TODO: Implement GUI
'''

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
def limit_to_16_digits(decimal_input, exponent, rounding_type):

  #if there is less than 16 digits, add leading zeroes
  if len(decimal_input) < 16:
    number_of_missing_digits = 16 - len(decimal_input)
    for i in range(number_of_missing_digits):
      decimal_input = "0" + decimal_input

  #NOTE: else if it is more than 16 digits, round the decimal to 16 digits
  
  else:
        # Implement rounding if the input decimal has more than 16 digits
        if rounding_type == 'truncate':
            decimal_input = decimal_input[:16]
        elif rounding_type == 'floor':
            decimal_input = decimal_input[:16]
        elif rounding_type == 'ceiling':
            # Adjust the exponent if rounding changes the value
            original_decimal = int(decimal_input[:16])
            rounded_decimal = original_decimal + 1
            if rounded_decimal % 10 == 0:
                exponent += 1
            decimal_input = str(rounded_decimal)
        elif rounding_type == 'nearest':
            original_decimal = int(decimal_input[:16])
            rounded_decimal = original_decimal + 1 if int(decimal_input[16]) >= 5 else original_decimal
            if rounded_decimal % 10 == 0 and original_decimal % 10 != 9:
                exponent += 1
            decimal_input = str(rounded_decimal)

    #TODO:Implement Rounding
  # Ensure that the decimal is limited to 16 digits
  if len(decimal_input) > 16:
      decimal_input = decimal_input[:16]

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

#normalize the decimal
# MAJOR FUNCTION
def normalize_decimal(decimal_input, exponent, rounding_type):
  decimal_point_location = decimal_input.find(".")

  #if a decimal point exists, move it to the rightmost and then remove it
  if decimal_point_location != -1:
    right_of_decimal_point = decimal_input[decimal_point_location + 1:]
    left_of_decimal_point = decimal_input[0: decimal_point_location]
    decimal_input = left_of_decimal_point + right_of_decimal_point
    exponent -= len(right_of_decimal_point)

  #remove trailing zeroes
  while decimal_input[len(decimal_input) - 1] == '0':
    decimal_input = decimal_input[0: len(decimal_input) - 1]
    exponent += 1

  #remove leading zeroes
  while decimal_input[0] == '0':
    decimal_input = decimal_input[1:]

  #limit to 16 digits only
  decimal_input, exponent = limit_to_16_digits(decimal_input, exponent, rounding_type)
  
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
  print("Exponent Prime: ", exp_prime)
  return exp_prime

#change e prime to binary
# HELPER FUNCTION
def transform_exponent_prime_to_binary(exp_prime):
  exp_prime_binary = bin(exp_prime)
  exp_prime_binary = exp_prime_binary[2:].zfill(10)
  print("Exponent Prime Binary: ", exp_prime_binary)
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

  #TODO: Add other special cases

  return combi_field, exponent_extension

#calculate for the densely packed bcd of three digits
# HELPER FUNCTION
def get_densely_packed_bcd(three_digits):
  first = int(three_digits[0])
  second = int(three_digits[1])
  third = int(three_digits[2])

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

#get input from user for the decimal_input, exponent of 10, and how the user wants the number to be rounded
decimal_input, ten_raised_to, rounding_type = get_input_from_user()

#first obtain the sign bit
sign_bit = get_sign_bit(decimal_input)

#if it is negative, we change it to positive for the next calculations
if sign_bit == "1":
  decimal_input = turn_decimal_positive(decimal_input)

#normalize the decimal by removing the decimal point, adding trailing zeroes if needed, and round off if needed
decimal_input, exponent = normalize_decimal(decimal_input, ten_raised_to, rounding_type)

#get the combination field (5 bits) and the exponent extension (8 bits)
#this PRINTS Exponent Prime and Exponent Prime in Binary
combination_field, exponent_extension = get_combination_field_and_exponent_extension(decimal_input, exponent)

#get the coefficient continuation in bcd format of the remaining digits
coefficient_continuation = get_coefficient_continuation(decimal_input)

#print out the output

#Exponent Prime and Exponent Prime in Binary (output from above)

#Normalized Decimal
print("Normalized Decimal: ", end = '')
if sign_bit == '1':
  print("-", end = '')
print(decimal_input)

#Normalized Exponent
print("Normalized Exponent: ", exponent)

#Sign Bit
print("Sign Bit: ", sign_bit)

#Combination Field
print("Combination Field: ", combination_field)

#Exponent Extension
print("Exponent Extension: ", exponent_extension)

#Coefficient Continuation
print("Coefficient Continuation: ", end = '')
for bcd in coefficient_continuation:
  print(bcd, end = ' ')

print()

#Print all into one binary output
print("Binary Output: " + sign_bit + " " + combination_field + " " + exponent_extension + " ", end = '')
for bcd in coefficient_continuation:
  print(bcd, end = ' ')

print()

binary_output = sign_bit + combination_field + exponent_extension
for bcd in coefficient_continuation:
  binary_output = binary_output + bcd

hexadecimal_output = convert_output_to_hexadecimal(binary_output)
print("Hexadecimal Output: " + hexadecimal_output)

#TODO: Provide an option for the user to download the output
