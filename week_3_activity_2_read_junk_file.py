'''
Open, read, and process the attached data file. Use the attached `junk.txt` file to:
1. Calculate and report the total number of lines in the file.
2. Add a new line at the end of the file containing exactly: `text file nanalyssis`
3. Convert all text in the `junk.txt` file to lowercase.
4. Save the processed file. Share your GitHub repository link here once you have completed the task.
'''

with open('resources/junk.txt', 'r+') as file:
    lines = file.readlines()
    print(f'Total number of lines is {len(lines)}')

    lines.append('text file nanalyssis')

    up_lines = []
    for line in lines:
        up_lines.append(line.upper())

    up_lines.append('\n')

    file.writelines(up_lines)

    file.close()
