
-- -- database : Employee_Appraisal

CREATE TABLE Appraisal_cycle (
    cycle_ID SERIAL PRIMARY KEY,
    cycle_name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(20) CHECK (status IN ('active', 'inactive') ),
    start_date_of_cycle DATE NOT NULL,
    end_date_of_cycle DATE NOT NULL
);

CREATE TABLE Stages (
    stage_ID SERIAL PRIMARY KEY,
    stage_name VARCHAR(50) NOT NULL,
    cycle_ID INT REFERENCES Appraisal_cycle(cycle_ID) ON DELETE CASCADE,
    start_date_of_stage DATE NOT NULL,
    end_date_of_stage DATE NOT NULL
);

CREATE TABLE Parameters (
    parameter_ID SERIAL PRIMARY KEY,
    parameter_title VARCHAR(255) NOT NULL,
    helptext TEXT,
    cycle_ID INT REFERENCES Appraisal_cycle(cycle_ID) ON DELETE CASCADE,
    applicable_to_employee BOOLEAN,
    applicable_to_lead BOOLEAN,
    is_fixed_parameter BOOLEAN
);

CREATE TABLE Employee (
    employee_ID SERIAL PRIMARY KEY,
    employee_name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL,
    reporting_manager INT REFERENCES Employee(employee_ID) ON DELETE SET NULL,
    previous_reporting_manager INT REFERENCES Employee(employee_ID) ON DELETE SET NULL,
    password VARCHAR(10) NOT NULL
);

CREATE TABLE Employee_allocation (
    allocation_ID SERIAL PRIMARY KEY,
    cycle_ID INT REFERENCES Appraisal_cycle(cycle_ID) ON DELETE CASCADE,
    employee_ID INT REFERENCES Employee(employee_ID) ON DELETE CASCADE
);

CREATE TABLE Question (
    question_ID SERIAL PRIMARY KEY,
    question_type VARCHAR(50),
    question_text TEXT NOT NULL
);

CREATE TABLE Option (
    option_ID SERIAL PRIMARY KEY,
    question_ID INT REFERENCES Question(question_ID) ON DELETE CASCADE,
    option_text TEXT NOT NULL
);

CREATE TABLE Self_assessment_response (
    response_ID SERIAL PRIMARY KEY,
    allocation_ID INT REFERENCES Employee_allocation(allocation_ID) ON DELETE CASCADE,
    cycle_ID INT REFERENCES Appraisal_cycle(cycle_ID) ON DELETE CASCADE,
    employee_ID INT REFERENCES Employee(employee_ID) ON DELETE CASCADE,
    question_ID INT REFERENCES Question(question_ID) ON DELETE CASCADE,
    option_ID INT REFERENCES Option(option_ID) ON DELETE CASCADE,
    response_text TEXT
);

CREATE TABLE Lead_assessment_rating (
    lead_rating_ID SERIAL PRIMARY KEY,
    allocation_ID INT REFERENCES Employee_allocation(allocation_ID) ON DELETE CASCADE,
    cycle_ID INT REFERENCES Appraisal_cycle(cycle_ID) ON DELETE CASCADE,
    employee_ID INT REFERENCES Employee(employee_ID) ON DELETE CASCADE,
    parameter_ID INT REFERENCES Parameters(parameter_ID) ON DELETE CASCADE,
    parameter_rating INT CHECK (parameter_rating BETWEEN 1 AND 4),
    specific_input TEXT
);

CREATE TABLE Assigned_Questions (
    assignment_ID SERIAL PRIMARY KEY,
    cycle_ID INT REFERENCES Appraisal_cycle(cycle_ID) ON DELETE CASCADE,
    employee_ID INT REFERENCES Employee(employee_ID) ON DELETE CASCADE,
    question_ID INT REFERENCES Question(question_ID) ON DELETE CASCADE,
    UNIQUE (cycle_ID, employee_ID, question_ID) -- Ensures no duplicate question assignment
);

INSERT INTO Appraisal_cycle (cycle_name, description, status, start_date_of_cycle, end_date_of_cycle)  
VALUES  
('Annual Performance Review', 'Yearly evaluation of employee performance.', 'active', '2024-01-01', '2024-12-31'),  
('Mid-Year Performance Review', 'Half-yearly appraisal to track progress.', 'active', '2024-07-01', '2024-12-31'),  
('Quarterly Performance Review - Q1', 'First quarter performance evaluation.', 'inactive', '2024-01-01', '2024-03-31'),  
('Quarterly Performance Review - Q2', 'Second quarter performance evaluation.', 'active', '2024-04-01', '2024-06-30');  

INSERT INTO Employee (employee_name, role, reporting_manager, previous_reporting_manager, password)  
VALUES  
('Smriti mandhana', 'Team Lead', 4, 4, '1234'),
('Dipti Sharma', 'Employee', 1, 1, '1234'),
('Akshay Kumar', 'Team Lead', 4, 4, '1234'),
('Vicky Kaushal', 'Employee', 1, 1, '1234'),
('Ravindra Jadeja', 'Employee', 5, 1, '1234'),
('Hardik Pandya', 'Employee', 5, 1, '1234'),
('Krunal Pandya', 'Employee', 1, 1, '1234'),
('Ajinkya Rahane', 'Team Lead', 4, 4, '1234'),
('Virat Kohli', 'Team Lead', 4, 4, '1234'),  
('Rohit Sharma', 'Employee', 1, 1, '1234'),  
('Jasprit Bumrah', 'Employee', 5, 1, '1234'),  
('MS Dhoni', 'HR', NULL, NULL, '1234'),  
('Sachin Tendulkar', 'Team Lead', 4, 4, '1234');

select * from Employee;

INSERT INTO Question (question_type, question_text)
VALUES 
('MCQ', 'Which of the following are programming languages?'),
('Single choice', 'What is the capital of Japan?'),
('True/false', 'The sun rises in the east.'),
('True/false', 'Penguins can fly.'),
('Descriptive', 'List down your strengths and weaknesses');

INSERT INTO Option (question_ID, option_text)
VALUES
(1, 'Python'),
(1, 'HTML'),
(1, 'C++'),
(1, 'Photoshop'),
(2, 'Tokyo'),
(2, 'Beijing'),
(2, 'Seoul'),
(2, 'Bangkok'),
(3, 'True'),
(3, 'False'),
(4, 'True'),
(4, 'False');

INSERT INTO Stages (stage_name, cycle_ID, start_date_of_stage, end_date_of_stage) 
VALUES 
    -- Annual Performance Review (Cycle 1: 2024-01-01 to 2024-12-31)
    ('Setup', 1, '2024-01-05', '2024-01-10'),
    ('Self Assessment', 1, '2024-02-01', '2024-02-10'),
    ('Lead Assessment', 1, '2024-03-01', '2024-03-10'),
    ('HR/VL Validation', 1, '2024-04-01', '2024-04-07'),
    ('Closure', 1, '2024-05-01', '2024-05-05'),

    -- Mid-Year Performance Review (Cycle 2: 2024-07-01 to 2024-12-31)
    ('Setup', 2, '2024-07-05', '2024-07-10'),
    ('Self Assessment', 2, '2024-08-01', '2024-08-07'),
    ('Lead Assessment', 2, '2024-09-01', '2024-09-07'),
    ('HR/VL Validation', 2, '2024-10-01', '2024-10-05'),
    ('Closure', 2, '2024-11-01', '2024-11-05'),

    -- Quarterly Performance Review - Q1 (Cycle 3: 2024-01-01 to 2024-03-31)
    ('Setup', 3, '2024-01-02', '2024-01-05'),
    ('Self Assessment', 3, '2024-01-10', '2024-01-15'),
    ('Lead Assessment', 3, '2024-02-01', '2024-02-05'),
    ('HR/VL Validation', 3, '2024-02-20', '2024-02-25'),
    ('Closure', 3, '2024-03-10', '2024-03-15'),

    -- Quarterly Performance Review - Q2 (Cycle 4: 2024-04-01 to 2024-06-30)
    ('Setup', 4, '2024-04-02', '2024-04-05'),
    ('Self Assessment', 4, '2024-04-10', '2024-04-15'),
    ('Lead Assessment', 4, '2024-05-01', '2024-05-05'),
    ('HR/VL Validation', 4, '2024-05-20', '2024-05-25'),
    ('Closure', 4, '2024-06-15', '2024-06-20');


INSERT INTO Parameters (parameter_title, helptext, cycle_ID, applicable_to_employee, applicable_to_lead, is_fixed_parameter) 
VALUES 
    -- Annual Performance Review (Cycle 1)
    ('Job Knowledge', 'Understanding of job roles and responsibilities.', 1, TRUE, TRUE, FALSE),
    ('Communication Skills', 'Ability to effectively communicate within the team and with stakeholders.', 1, TRUE, TRUE, FALSE),
    ('Team Collaboration', 'Effectiveness in working with colleagues and contributing to team goals.', 1, TRUE, TRUE, FALSE),
    ('Overall Performance Rating', 'Overall performance', 1, TRUE, TRUE, TRUE),
    -- Mid-Year Performance Review (Cycle 2)
    ('Innovation', 'Initiative in bringing new ideas and improvements.', 2, TRUE, FALSE, FALSE),
    ('Leadership Potential', 'Ability to take ownership and guide teams effectively.', 2, FALSE, TRUE, FALSE),
    ('Overall Performance Rating', 'Overall performance', 2, TRUE, TRUE, TRUE),
    -- Quarterly Performance Review - Q1 (Cycle 3)
    ('Customer Focus', 'Ability to understand and meet customer expectations.', 3, TRUE, TRUE, FALSE),
    ('Problem-Solving', 'Skill in identifying and resolving work-related challenges.', 3, TRUE, TRUE, FALSE),
    ('Overall Performance Rating', 'Overall performance', 3, TRUE, TRUE, TRUE),
    -- Quarterly Performance Review - Q2 (Cycle 4)
    ('Time Management', 'Effectiveness in prioritizing and completing tasks on time.', 4, TRUE, FALSE, FALSE),
    ('Decision Making', 'Ability to make well-informed, effective, and timely decisions.', 4, FALSE, TRUE, FALSE),
    ('Overall Performance Rating', 'Overall performance', 4, TRUE, TRUE, TRUE);


