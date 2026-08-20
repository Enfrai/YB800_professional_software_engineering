This is database design for a college/university enrollment system where describs some main entities, such as Student, Enrollment, Lecturer, Subjects and Lecture, and the relationship between them, just as shown as the picture:
![ER Diagram](../images/ER-sample.png)
From this picture, we can see there are two clear relationships:
1. A `Student` can enroll a college/university by this sytem, and when finish the `Enrollment`, they can join `Lectures`. BUT there missed a relationship between a `Course_name` and a `Subject` since a `Student` can know how many `Lectures` they have only if they finished the `Enrollment` for a course (`Course_name`) and related `Subjects. 
2. And also, this diagram shows the relationship of each `Subject` has what `Lectures` and a `Lecture` relatively belonges to what `Subjects`, and each `Lecture` is given by who, means `Lecturer`.

## Entities
- Student
    - **attributes**: F_name, L_name, NID, B_date,
    - **also needed**: 
- Enrollment
- Lecturer
- Subjects
- Lecture

## 