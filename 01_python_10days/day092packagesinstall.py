import numpy as np
from datetime import datetime

# Using datetime package
current_time = datetime.now()
print("Current Date and Time:", current_time)

# Using numpy package
numbers = np.array([10, 20, 30, 40, 50])

print("Numbers:", numbers)
print("Sum:", np.sum(numbers))
print("Average:", np.mean(numbers))
print("Maximum:", np.max(numbers))
print("Minimum:", np.min(numbers))