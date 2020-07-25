def average():
    total = count = 0

    def avg(new_var):
        nonlocal total, count
        total += new_var
        count += 1
        return total / count

    return avg


avg = average()
avg(2)
print(avg(8))
