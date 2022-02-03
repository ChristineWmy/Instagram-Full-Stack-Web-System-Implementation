import pathlib
import os
import json
import shutil
import sys
import pdb

# ========================= TESTS ============================

def test_print_schedule():
    output = output_schedules("config.json")
    assert output == "Spongebob Squarepants is taking:\n101\n183\n280\n281\n\nWonder Woman is taking:\n370\n481\n482\n484\n\n"
    

def test_partition_courses():
    # brekapoint()
    output_dir = "output"
    partition_courses("config.json", output_dir)

    # check that output dir has been created
    assert pathlib.Path(output_dir).exists()

    path_100 = f"{output_dir}/courses_100.txt"
    path_200 = f"{output_dir}/courses_200.txt"
    path_300 = f"{output_dir}/courses_300.txt"
    path_400 = f"{output_dir}/courses_400.txt"

    # check that partitions have been created
    assert pathlib.Path(path_100).exists()
    assert pathlib.Path(path_200).exists()
    assert pathlib.Path(path_300).exists()
    assert pathlib.Path(path_400).exists()

    # check that partitions contain correct courses
    with open(path_100) as f1: 
        s = f1.read()
        assert "101" in s
        assert "183" in s

    with open(path_200) as f2: 
        s = f2.read()
        assert "280" in s
        assert "281" in s
    
    with open(path_300) as f3: 
        s = f3.read()
        assert "370" in s
    
    with open(path_400) as f4: 
        s = f4.read()
        assert "481" in s
        assert "482" in s
        assert "484" in s


# ========================= BUGGY FUNCTIONS ============================

def output_schedules(path):
    # brekapoint()
    infile_path = pathlib.Path(path)
    output = ""
    with infile_path.open() as fh:
        data = json.loads(fh)
        for student in data:
            output += f"{student['name']} is taking:\n"
            allCourses = student['courses']
            for i in range(len(allCourses)):
                output += f"{allCourses[i]}\n"
            output += "\n"
    return output


def partition_courses(path, output_dir):
    infile_path = pathlib.Path(path)
    with infile_path.open() as fh:
        data = json.load(fh)

    if not pathlib.Path(output_dir).exists():
        os.mkdir(output_dir)

    f1 = open(f"{output_dir}/courses_100.txt", "w")
    f2 = open(f"{output_dir}/courses_200.txt", "w")
    f3 = open(f"{output_dir}/courses_300.txt", "w")
    f4 = open(f"{output_dir}/courses_400.txt", "w")

    for student in data:
        for course in student['courses']:
            course_level = course % 10
            if course_level == 1:
                f1.write(f"{course}\n")
            elif course_level == 2:
                f2.write(f"{course}\n")
            elif course_level == 3:
                f3.write(f"{course}\n")
            elif course_level == 4:
                f4.write(f"{course}\n")


# ========================= MAIN ============================

if __name__ == '__main__':
    test_partition_courses()