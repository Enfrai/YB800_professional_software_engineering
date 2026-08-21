According to the ER diagram, it describes a relation in which a `Student` enrols a course identified by `CC#` and `Course_name`. Once who enrolled can know what `Lectures` are contained in their course learning. Each `Lecture` refers to the course identified by `CC#` and the subject identified by `Subject`. And also each `Lecture` has a `Lecturer`.

- add more one/ two attributes for any of the entities?
    - The entity `Lecture` should have an attribute `Lecture_id` refers to which `Lecturer` will teach in the lecture. And
    - The entity `Subjects` should have an attribute `Subject_name`.
    - The attribute `Subject` of the entity `Lecture` should be changed to `Subject_code`

- Write the type of relationship between the entities and describe it.
    - A `Student` can do `Enrollment` for a course (`CC#` & `Course_name`).
    - Once did that, the enrolled `Students` would be distributed to the `Lectures` they should complete.
    - And also, they will be aware of the `Subjects` are contained in their courses because each `Lecture` has an attribute `Subject`.
    - Moreover, each `Lecture` has a `Lecturer` (`Lecture_id`)