'''
Open, read, and process the attached data file. Use the attached `junk.txt` file to:
1. Calculate and report the total number of lines in the file.
2. Add a new line at the end of the file containing exactly: `text file nanalyssis`
3. Convert all text in the `junk.txt` file to lowercase.
4. Save the processed file. Share your GitHub repository link here once you have completed the task.
'''

#SOLUTION 1
def solution_1():
    with open('resources/junk.txt', 'r') as file:
        lines = file.readlines()

    # 1. Calculate and report the total number of lines in the file.
    print(f'The total number of lines is {len(lines)}')

    # 2. Add a new line at the end of the file containing exactly: `text file nanalyssis`
    new_line = 'text file nanalyssis\n'
    lines.append(new_line)
    with open('resources/junk.txt', 'a') as file:
        file.write(new_line)

    # 3. Convert all text in the `junk.txt` file to lowercase.
    lower_lines = []
    for line in lines:
        lower_lines.append(line.lower())

    # 4. Save the processed file. Share your GitHub repository link here once you have completed the task.
    with open('resources/junk.txt', 'w') as file:
        file.writelines(lower_lines)


# SOLUTION 2
def solution_2():
    with open('resources/junk.txt', 'r+') as file:
        lines = file.readlines()
        print(f'Total number of lines is {len(lines)}')

        lines.append('text file nanalyssis')

        lower_lines = []
        for line in lines:
            lower_lines.append(line.lower())

        lower_lines.append('\n')
        # print(lower_lines)

        file.seek(0)
        file.writelines(lower_lines)
        file.truncate()

if __name__ == '__main__':
    # solution_1()
    solution_2()