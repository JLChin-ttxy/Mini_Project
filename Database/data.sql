-- ============================================================================
-- UTAR Data Population Script - STREAMLINED VERSION v2
-- 6 Faculties, 30 Programs, 120 Subjects (20 per faculty)
-- Each program has 10 subjects, 5 Scholarships, 3 Trimesters, 10 Clubs
-- ============================================================================

USE university_admission_db;

-- Optional: Clear existing data (uncomment to use)
-- SET FOREIGN_KEY_CHECKS = 0;
-- TRUNCATE TABLE FEEDBACK;
-- TRUNCATE TABLE CHAT_MESSAGE;
-- TRUNCATE TABLE CHAT_SESSION;
-- TRUNCATE TABLE Users;
-- TRUNCATE TABLE FAQ;
-- TRUNCATE TABLE EVENT;
-- TRUNCATE TABLE STUDENT_CLUB;
-- TRUNCATE TABLE ACCOMMODATION;
-- TRUNCATE TABLE CAMPUS_FACILITY;
-- TRUNCATE TABLE FINANCIAL_AID;
-- TRUNCATE TABLE SCHOLARSHIP_APPLICATION;
-- TRUNCATE TABLE SCHOLARSHIP;
-- TRUNCATE TABLE TUITION_FEE;
-- TRUNCATE TABLE IMPORTANT_DATE;
-- TRUNCATE TABLE APPLICATION_DOCUMENT;
-- TRUNCATE TABLE APPLICATION_STATUS;
-- TRUNCATE TABLE DOCUMENT_CHECKLIST;
-- TRUNCATE TABLE APPLICATION;
-- TRUNCATE TABLE APPLICANT;
-- TRUNCATE TABLE ADMISSION_REQUIREMENT;
-- TRUNCATE TABLE PROGRAM_SUBJECT;
-- TRUNCATE TABLE SUBJECT;
-- TRUNCATE TABLE FACULTY_MEMBER;
-- TRUNCATE TABLE PROGRAM;
-- TRUNCATE TABLE FACULTY;
-- SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================================
-- MODULE 1: FACULTY DATA (6 Faculties)
-- ============================================================================

INSERT INTO FACULTY (faculty_name, description, contact_email, contact_phone, office_location, office_hours, location) VALUES
('Faculty of Accountancy and Management', 'Established in 2002, one of the founding faculties of UTAR. Offers comprehensive programs in accounting, finance, and business management. Recognized by professional bodies including ACCA, CIMA, CPA Australia, and ICAEW.', 'fam@utar.edu.my', '+603-9086 0288', 'Block A, Level 3', 'Mon-Fri: 9:00 AM - 5:00 PM', 'UTAR Sungai Long Campus, Kajang, Selangor'),

('Faculty of Arts and Social Science', 'Offers diverse programs in psychology, counselling, advertising, public relations, and social work. Known for producing graduates with strong communication and analytical skills.', 'fas@utar.edu.my', '+605-468 8888', 'Block D, Level 2', 'Mon-Fri: 9:00 AM - 5:00 PM', 'UTAR Kampar Campus, Perak'),

('Faculty of Business and Finance', 'Provides industry-focused programs in business administration, economics, banking, marketing, and finance. Strong industry partnerships and internship opportunities.', 'fbf@utar.edu.my', '+605-468 8888', 'Block C, Level 1', 'Mon-Fri: 9:00 AM - 5:00 PM', 'UTAR Kampar Campus, Perak'),

('Faculty of Information and Communication Technology', 'One of the three founding faculties established in 2002. Offers programs in computer science, software engineering, information systems, and data science. Recognized by Seoul Accord.', 'fict@utar.edu.my', '+605-468 8888', 'Block B, Level 3', 'Mon-Fri: 9:00 AM - 5:00 PM', 'UTAR Kampar Campus, Perak'),

('Faculty of Science', 'Offers programs in mathematical sciences, actuarial science, food science, biotechnology, agriculture, and environmental science. Strong research focus with state-of-the-art laboratories.', 'fsc@utar.edu.my', '+605-468 8888', 'Block D, Level 1', 'Mon-Fri: 9:00 AM - 5:00 PM', 'UTAR Kampar Campus, Perak'),

('Faculty of Engineering and Green Technology', 'Focus on sustainable engineering solutions. Offers programs in civil, electrical, mechanical, and mechatronics engineering with emphasis on green technology and environmental sustainability.', 'fegt@utar.edu.my', '+605-468 8888', 'Block G, Level 2', 'Mon-Fri: 9:00 AM - 5:00 PM', 'UTAR Kampar Campus, Perak');

-- ============================================================================
-- MODULE 1: PROGRAM DATA (5 Programs per Faculty = 30 Total)
-- ============================================================================

-- Faculty of Accountancy and Management Programs (Faculty ID: 1)
INSERT INTO PROGRAM (faculty_id, program_name, level, duration_years, career_prospects, description) VALUES
(1, 'Bachelor of Accounting (Honours)', 'Bachelor', 3, 'Chartered Accountant, Tax Consultant, Auditor, Financial Analyst, Management Accountant', 'Comprehensive accounting program accredited by ACCA, CIMA, CPA Australia, and MIA. Focuses on financial reporting, taxation, auditing, and corporate governance.'),
(1, 'Bachelor of Business Administration (Honours) Finance', 'Bachelor', 3, 'Financial Analyst, Investment Banker, Financial Planner, Risk Manager, Portfolio Manager', 'Specialized finance program covering investment analysis, corporate finance, financial markets, and wealth management. Recognized by FPAM and CTIM.'),
(1, 'Bachelor of Commerce (Honours) Accounting', 'Bachelor', 3, 'Public Accountant, Corporate Accountant, Tax Advisor, Financial Controller', 'Combines accounting principles with business management. Prepares students for professional accounting qualifications and managerial roles.'),
(1, 'Bachelor of International Business (Honours)', 'Bachelor', 3, 'International Business Manager, Export/Import Manager, Global Supply Chain Manager, International Marketing Executive', 'Focuses on global business strategies, international trade, cross-cultural management, and global supply chain operations.'),
(1, 'Bachelor of Banking and Finance (Honours)', 'Bachelor', 3, 'Banking Officer, Financial Consultant, Credit Analyst, Investment Advisor', 'Comprehensive program covering banking operations, financial institutions, investment strategies, and risk management.');

-- Faculty of Arts and Social Science Programs (Faculty ID: 2)
INSERT INTO PROGRAM (faculty_id, program_name, level, duration_years, career_prospects, description) VALUES
(2, 'Bachelor of Psychology (Honours)', 'Bachelor', 3, 'Clinical Psychologist, Counsellor, HR Specialist, Organizational Development Consultant', 'Comprehensive psychology program covering developmental, social, cognitive, and clinical psychology. Accredited by Malaysian Board of Counsellors.'),
(2, 'Bachelor of Arts (Honours) Advertising', 'Bachelor', 3, 'Advertising Executive, Creative Director, Brand Manager, Media Planner, Digital Marketing Specialist', 'Creative program combining advertising theory, marketing communications, digital media, and brand management.'),
(2, 'Bachelor of Arts (Honours) Public Relations', 'Bachelor', 3, 'PR Consultant, Corporate Communications Manager, Media Relations Officer, Event Manager', 'Focuses on strategic communication, media relations, crisis management, and reputation management.'),
(2, 'Bachelor of Social Science (Honours) Counselling', 'Bachelor', 3, 'Professional Counsellor, School Counsellor, Family Therapist, Career Counsellor', 'Prepares students for professional counselling practice. Recognized by Malaysian Board of Counsellors and PERKAMA.'),
(2, 'Bachelor of Arts (Honours) Journalism and Media Studies', 'Bachelor', 3, 'Journalist, News Reporter, Content Creator, Media Analyst', 'Focuses on news reporting, multimedia journalism, media ethics, and digital storytelling.');

-- Faculty of Business and Finance Programs (Faculty ID: 3)
INSERT INTO PROGRAM (faculty_id, program_name, level, duration_years, career_prospects, description) VALUES
(3, 'Bachelor of Business Administration (Honours)', 'Bachelor', 3, 'Business Manager, Entrepreneur, Management Consultant, Operations Manager', 'Comprehensive business program covering management, marketing, operations, and entrepreneurship.'),
(3, 'Bachelor of Economics (Honours) Financial Economics', 'Bachelor', 3, 'Economist, Financial Analyst, Policy Analyst, Economic Consultant', 'Combines economic theory with financial analysis. Strong focus on quantitative methods and economic modeling.'),
(3, 'Bachelor of Marketing (Honours)', 'Bachelor', 3, 'Marketing Manager, Brand Manager, Digital Marketing Specialist, Market Research Analyst', 'Comprehensive marketing program covering consumer behavior, digital marketing, brand management, and marketing analytics.'),
(3, 'Bachelor of Logistics and Supply Chain Management (Honours)', 'Bachelor', 3, 'Supply Chain Manager, Logistics Coordinator, Procurement Manager, Operations Analyst', 'Focuses on supply chain optimization, inventory management, procurement, and logistics operations.'),
(3, 'Bachelor of Entrepreneurship (Honours)', 'Bachelor', 3, 'Entrepreneur, Business Owner, Startup Consultant, Innovation Manager', 'Develops entrepreneurial mindset, business planning skills, innovation strategies, and startup management.');

-- Faculty of Information and Communication Technology Programs (Faculty ID: 4)
INSERT INTO PROGRAM (faculty_id, program_name, level, duration_years, career_prospects, description) VALUES
(4, 'Bachelor of Computer Science (Honours)', 'Bachelor', 3, 'Software Engineer, Systems Analyst, Data Scientist, AI Specialist', 'Comprehensive computing program covering algorithms, software engineering, databases, and artificial intelligence. Accredited by Seoul Accord.'),
(4, 'Bachelor of Information Systems (Honours)', 'Bachelor', 3, 'Systems Analyst, IT Consultant, Business Analyst, Project Manager', 'Combines business knowledge with IT skills. Focuses on enterprise systems, business intelligence, and IT project management.'),
(4, 'Bachelor of Software Engineering (Honours)', 'Bachelor', 3, 'Software Developer, Full-stack Developer, DevOps Engineer, Software Architect', 'Focuses on software development lifecycle, programming, software design patterns, and agile methodologies.'),
(4, 'Bachelor of Data Science and Analytics (Honours)', 'Bachelor', 3, 'Data Scientist, Data Analyst, Business Intelligence Analyst, ML Engineer', 'Covers big data technologies, statistical analysis, machine learning, and data visualization techniques.'),
(4, 'Bachelor of Computer Science (Honours) Network Security', 'Bachelor', 3, 'Cybersecurity Analyst, Network Security Engineer, Security Consultant, Penetration Tester', 'Specialized program in cybersecurity, network security, cryptography, and ethical hacking.');

-- Faculty of Science Programs (Faculty ID: 5)
INSERT INTO PROGRAM (faculty_id, program_name, level, duration_years, career_prospects, description) VALUES
(5, 'Bachelor of Science (Honours) Actuarial Science', 'Bachelor', 3, 'Actuary, Risk Analyst, Insurance Specialist, Financial Modeler', 'Comprehensive program preparing students for professional actuarial examinations. Covers risk assessment, insurance mathematics, and financial modeling.'),
(5, 'Bachelor of Science (Honours) Food Science', 'Bachelor', 3, 'Food Technologist, Quality Assurance Manager, R&D Specialist, Food Safety Officer', 'Focuses on food chemistry, food microbiology, food processing, and quality control.'),
(5, 'Bachelor of Science (Honours) Biotechnology', 'Bachelor', 3, 'Biotechnologist, Research Scientist, Laboratory Manager, Quality Control Analyst', 'Covers molecular biology, genetic engineering, bioprocessing, and bioinformatics.'),
(5, 'Bachelor of Science (Honours) Applied Mathematics with Computing', 'Bachelor', 3, 'Data Analyst, Quantitative Analyst, Operations Research Analyst, Mathematical Modeler', 'Combines mathematics with computational techniques. Focus on mathematical modeling and data analytics.'),
(5, 'Bachelor of Science (Honours) Environmental Science', 'Bachelor', 3, 'Environmental Consultant, Sustainability Officer, Environmental Analyst, Conservation Scientist', 'Focuses on environmental management, conservation, pollution control, and sustainable development.');

-- Faculty of Engineering and Green Technology Programs (Faculty ID: 6)
INSERT INTO PROGRAM (faculty_id, program_name, level, duration_years, career_prospects, description) VALUES
(6, 'Bachelor of Engineering (Honours) Civil Engineering', 'Bachelor', 4, 'Civil Engineer, Structural Engineer, Project Manager, Construction Manager', 'Accredited by BEM and recognized under Washington Accord. Covers structural design, geotechnical engineering, and construction management.'),
(6, 'Bachelor of Engineering (Honours) Electrical and Electronics Engineering', 'Bachelor', 4, 'Electrical Engineer, Electronics Engineer, Power Systems Engineer, Automation Engineer', 'Comprehensive program covering power systems, electronics, control systems, and renewable energy. BEM accredited.'),
(6, 'Bachelor of Engineering (Honours) Mechanical Engineering', 'Bachelor', 4, 'Mechanical Engineer, Design Engineer, Manufacturing Engineer, Maintenance Engineer', 'Covers thermodynamics, mechanics, materials science, and manufacturing processes. Recognized by BEM.'),
(6, 'Bachelor of Engineering (Honours) Mechatronics Engineering', 'Bachelor', 4, 'Mechatronics Engineer, Robotics Engineer, Automation Specialist, Control Systems Engineer', 'Integrates mechanical, electrical, and computer engineering. Focus on robotics, automation, and intelligent systems.'),
(6, 'Bachelor of Engineering (Honours) Chemical Engineering', 'Bachelor', 4, 'Chemical Engineer, Process Engineer, Production Manager, Environmental Engineer', 'Covers chemical processes, plant design, process control, and green chemistry. BEM accredited.');

-- ============================================================================
-- MODULE 1: FACULTY MEMBERS (Sample staff - 2 per faculty = 12 Total)
-- ============================================================================

INSERT INTO FACULTY_MEMBER (faculty_id, name, designation, specialization, email, phone, office_location) VALUES
(1, 'Prof. Dr. Lee Heng Yee', 'Dean', 'Financial Accounting, Corporate Governance', 'leehe@utar.edu.my', '+603-9086 0201', 'A301'),
(1, 'Assoc. Prof. Dr. Tan Mei Ling', 'Associate Professor', 'Management Accounting, Cost Control', 'tanml@utar.edu.my', '+603-9086 0202', 'A302'),

(2, 'Prof. Dr. Ahmad bin Hassan', 'Dean', 'Clinical Psychology, Mental Health', 'ahmad@utar.edu.my', '+605-468 1001', 'D201'),
(2, 'Dr. Lim Siew Khim', 'Senior Lecturer', 'Advertising, Media Communications', 'limsk@utar.edu.my', '+605-468 1002', 'D202'),

(3, 'Prof. Dr. Wong Chee Keong', 'Dean', 'Financial Economics, Econometrics', 'wongck@utar.edu.my', '+605-468 2001', 'C101'),
(3, 'Assoc. Prof. Dr. Siti Nurhaliza', 'Associate Professor', 'Marketing Strategy, Consumer Behavior', 'sitin@utar.edu.my', '+605-468 2002', 'C102'),

(4, 'Prof. Dr. Chong Wei Lun', 'Dean', 'Artificial Intelligence, Machine Learning', 'chongwl@utar.edu.my', '+605-468 3001', 'B301'),
(4, 'Dr. Rajesh Kumar', 'Senior Lecturer', 'Cybersecurity, Network Security', 'rajeshk@utar.edu.my', '+605-468 3002', 'B302'),

(5, 'Prof. Dr. Lau Pei San', 'Dean', 'Actuarial Science, Risk Management', 'laups@utar.edu.my', '+605-468 4001', 'D101'),
(5, 'Assoc. Prof. Dr. Mohd Azhar', 'Associate Professor', 'Biotechnology, Genetic Engineering', 'mohdaz@utar.edu.my', '+605-468 4002', 'D102'),

(6, 'Prof. Ir. Dr. Tan Kok Seng', 'Dean', 'Civil Engineering, Structural Design', 'tanks@utar.edu.my', '+605-468 5001', 'G201'),
(6, 'Ir. Dr. Nurul Ain binti Ahmad', 'Senior Lecturer', 'Electrical Engineering, Renewable Energy', 'nurula@utar.edu.my', '+605-468 5002', 'G202');

-- ============================================================================
-- MODULE 1: SUBJECTS (120 Total - 20 per Faculty)
-- ============================================================================

INSERT INTO SUBJECT (subject_code, subject_name, credit_hours, description) VALUES
('UFAM1001', 'Principles of Accounting', 3, 'Introduction to accounting principles, financial statements, and double-entry bookkeeping.'),
('UFAM1013', 'Business Mathematics', 3, 'Mathematical concepts for business including algebra, calculus, and financial mathematics.'),
('UFAM2023', 'Financial Accounting I', 3, 'Comprehensive study of financial accounting standards, asset valuation, and financial reporting.'),
('UFAM2033', 'Management Accounting', 3, 'Cost accounting, budgeting, variance analysis, and performance measurement.'),
('UFAM2043', 'Corporate Finance', 3, 'Capital structure, investment decisions, dividend policy, and financial planning.'),
('UFAM2053', 'Taxation', 3, 'Malaysian taxation system, income tax, corporate tax, and tax planning strategies.'),
('UFAM3063', 'Auditing and Assurance', 3, 'Audit principles, risk assessment, audit procedures, and professional ethics.'),
('UFAM3073', 'Financial Statement Analysis', 3, 'Ratio analysis, trend analysis, and interpretation of financial statements.'),
('UFAM3083', 'International Finance', 3, 'Foreign exchange markets, international investment, and multinational financial management.'),
('UFAM3093', 'Investment Analysis', 3, 'Portfolio theory, asset valuation, investment strategies, and market analysis.'),
('UFAM2063', 'Business Law', 3, 'Commercial law, contract law, company law, and legal aspects of business.'),
('UFAM2073', 'Organizational Behavior', 3, 'Human behavior in organizations, motivation, leadership, and team dynamics.'),
('UFAM3103', 'Strategic Management', 3, 'Strategic planning, competitive analysis, and business strategy formulation.'),
('UFAM3113', 'Risk Management', 3, 'Identification and management of financial risks, insurance, and hedging strategies.'),
('UFAM2083', 'Economics for Business', 3, 'Microeconomics and macroeconomics principles applied to business decisions.'),
('UFAM3123', 'Corporate Governance', 3, 'Board responsibilities, stakeholder management, and ethical business practices.'),
('UFAM3133', 'International Business', 3, 'Global business environment, cross-cultural management, and international trade.'),
('UFAM2093', 'Marketing Fundamentals', 3, 'Marketing concepts, consumer behavior, and marketing mix strategies.'),
('UFAM3143', 'Business Ethics', 3, 'Ethical frameworks, corporate social responsibility, and ethical decision-making.'),
('UFAM3153', 'Entrepreneurship', 3, 'Entrepreneurial mindset, business planning, and startup management.');

INSERT INTO SUBJECT (subject_code, subject_name, credit_hours, description) VALUES
('UFAS1011', 'Introduction to Psychology', 3, 'Basic psychological concepts, research methods, and major theoretical perspectives.'),
('UFAS1021', 'Communication Skills', 3, 'Effective verbal and written communication, presentation skills, and interpersonal communication.'),
('UFAS2031', 'Developmental Psychology', 3, 'Human development across lifespan, cognitive and social development theories.'),
('UFAS2041', 'Social Psychology', 3, 'Social influence, group dynamics, attitudes, and interpersonal relationships.'),
('UFAS2051', 'Cognitive Psychology', 3, 'Mental processes including perception, memory, thinking, and problem-solving.'),
('UFAS3061', 'Abnormal Psychology', 3, 'Psychological disorders, diagnosis, treatment approaches, and mental health.'),
('UFAS3071', 'Counselling Psychology', 3, 'Counselling theories, techniques, and ethical practice in counselling.'),
('UFAS2061', 'Advertising Principles', 3, 'Advertising strategies, creative development, and campaign planning.'),
('UFAS2071', 'Public Relations Theory', 3, 'PR concepts, media relations, crisis communication, and reputation management.'),
('UFAS2081', 'Digital Media', 3, 'Social media marketing, content creation, and digital communication strategies.'),
('UFAS3081', 'Media Ethics and Law', 3, 'Ethical issues in media, media regulations, and freedom of expression.'),
('UFAS3091', 'Journalism Practices', 3, 'News writing, reporting techniques, investigative journalism, and media production.'),
('UFAS2091', 'Creative Writing', 3, 'Writing techniques for various media, storytelling, and content development.'),
('UFAS3101', 'Research Methods in Social Science', 3, 'Qualitative and quantitative research methods, data collection, and analysis.'),
('UFAS3111', 'Organizational Psychology', 3, 'Workplace behavior, employee motivation, and organizational development.'),
('UFAS2101', 'Cultural Studies', 3, 'Cultural theories, identity, representation, and cultural practices.'),
('UFAS3121', 'Event Management', 3, 'Planning and executing events, logistics, budgeting, and stakeholder management.'),
('UFAS3131', 'Brand Management', 3, 'Brand strategy, brand equity, positioning, and brand communication.'),
('UFAS2111', 'Consumer Behavior', 3, 'Consumer decision-making, motivation, perception, and purchase behavior.'),
('UFAS3141', 'Crisis Communication', 3, 'Crisis management strategies, emergency response, and stakeholder communication.');

INSERT INTO SUBJECT (subject_code, subject_name, credit_hours, description) VALUES
('UFBF1001', 'Introduction to Business', 3, 'Business fundamentals, organizational structures, and business environment.'),
('UFBF1011', 'Principles of Management', 3, 'Management functions, planning, organizing, leading, and controlling.'),
('UFBF2021', 'Microeconomics', 3, 'Supply and demand, market structures, consumer theory, and production.'),
('UFBF2031', 'Macroeconomics', 3, 'National income, inflation, unemployment, fiscal and monetary policy.'),
('UFBF2041', 'Marketing Management', 3, 'Marketing strategy, segmentation, targeting, and positioning.'),
('UFBF2051', 'Operations Management', 3, 'Production systems, quality management, and supply chain optimization.'),
('UFBF3061', 'Financial Management', 3, 'Financial decision-making, capital budgeting, and cost of capital.'),
('UFBF3071', 'Human Resource Management', 3, 'Recruitment, training, performance management, and employee relations.'),
('UFBF2061', 'Business Statistics', 3, 'Statistical methods, probability, hypothesis testing, and regression analysis.'),
('UFBF3081', 'Econometrics', 3, 'Economic modeling, time series analysis, and forecasting techniques.'),
('UFBF3091', 'International Economics', 3, 'International trade theory, exchange rates, and global economic issues.'),
('UFBF2071', 'Digital Marketing', 3, 'Online marketing, SEO, social media marketing, and analytics.'),
('UFBF3101', 'Market Research', 3, 'Research design, survey methods, data analysis, and market intelligence.'),
('UFBF3111', 'Supply Chain Management', 3, 'Logistics, inventory management, procurement, and distribution.'),
('UFBF2081', 'Business Analytics', 3, 'Data-driven decision making, predictive analytics, and business intelligence.'),
('UFBF3121', 'Innovation Management', 3, 'Innovation processes, creativity, technology management, and R&D.'),
('UFBF3131', 'Business Plan Development', 3, 'Business planning, feasibility analysis, and startup strategies.'),
('UFBF2091', 'E-Commerce', 3, 'Online business models, e-commerce platforms, and digital transactions.'),
('UFBF3141', 'Project Management', 3, 'Project planning, scheduling, resource allocation, and risk management.'),
('UFBF3151', 'Negotiation and Conflict Resolution', 3, 'Negotiation strategies, conflict management, and dispute resolution.');

INSERT INTO SUBJECT (subject_code, subject_name, credit_hours, description) VALUES
('UECS1001', 'Introduction to Programming', 3, 'Fundamental programming concepts using Python. Variables, control structures, and functions.'),
('UECS2033', 'Data Structures and Algorithms', 3, 'Abstract data types, complexity analysis, sorting, and searching algorithms.'),
('UECS2013', 'Object-Oriented Programming', 3, 'OOP principles using Java, design patterns, and software engineering practices.'),
('UECS2063', 'Database Systems', 3, 'Database design, SQL, normalization, and DBMS implementation.'),
('UECS3033', 'Artificial Intelligence', 3, 'AI concepts, search algorithms, knowledge representation, and machine learning.'),
('UECS3043', 'Software Engineering', 3, 'SDLC, requirements analysis, system design, testing, and project management.'),
('UECS3053', 'Computer Networks', 3, 'Network protocols, TCP/IP, network security, and distributed systems.'),
('UECS3063', 'Operating Systems', 3, 'Process management, memory management, file systems, and concurrency.'),
('UECS3073', 'Web Application Development', 3, 'Full-stack development with HTML, CSS, JavaScript, and modern frameworks.'),
('UECS3083', 'Machine Learning', 3, 'Supervised/unsupervised learning, neural networks, and deep learning.'),
('UECS3093', 'Mobile Application Development', 3, 'Android and iOS app development using Kotlin and Swift.'),
('UECS3103', 'Computer Graphics', 3, '2D/3D graphics, rendering techniques, and game development fundamentals.'),
('UECS3113', 'Cybersecurity Fundamentals', 3, 'Network security, cryptography, ethical hacking, and security practices.'),
('UECS3123', 'Cloud Computing', 3, 'Cloud architectures, AWS, Azure, containerization, and microservices.'),
('UECS3133', 'Big Data Analytics', 3, 'Hadoop, Spark, NoSQL databases, and data visualization.'),
('UECS2073', 'Computer Architecture', 3, 'CPU design, memory hierarchy, I/O systems, and parallel processing.'),
('UECS2083', 'Discrete Mathematics', 3, 'Logic, set theory, graph theory, and combinatorics for computing.'),
('UECS3143', 'Human-Computer Interaction', 3, 'UI/UX design, usability testing, and interaction design principles.'),
('UECS3153', 'Information Systems', 3, 'Enterprise systems, ERP, business process modeling, and IT governance.'),
('UECS3163', 'Internet of Things', 3, 'IoT architectures, sensor networks, embedded systems, and applications.');

INSERT INTO SUBJECT (subject_code, subject_name, credit_hours, description) VALUES
('UFSC1001', 'Calculus I', 3, 'Limits, derivatives, applications of derivatives, and integration.'),
('UFSC1011', 'Linear Algebra', 3, 'Vectors, matrices, determinants, eigenvalues, and linear transformations.'),
('UFSC2021', 'Calculus II', 3, 'Multivariable calculus, partial derivatives, and multiple integrals.'),
('UFSC2031', 'Probability Theory', 3, 'Probability distributions, random variables, and expectation.'),
('UFSC2041', 'Statistical Inference', 3, 'Estimation theory, hypothesis testing, and confidence intervals.'),
('UFSC3051', 'Actuarial Mathematics', 3, 'Life contingencies, annuities, and insurance mathematics.'),
('UFSC3061', 'Financial Mathematics', 3, 'Time value of money, derivatives pricing, and portfolio theory.'),
('UFSC2051', 'Chemistry', 3, 'Atomic structure, chemical bonding, reactions, and organic chemistry.'),
('UFSC2061', 'Biology', 3, 'Cell biology, genetics, evolution, and molecular biology.'),
('UFSC3071', 'Food Chemistry', 3, 'Food composition, nutritional biochemistry, and food additives.'),
('UFSC3081', 'Food Microbiology', 3, 'Microorganisms in food, food safety, and preservation techniques.'),
('UFSC3091', 'Molecular Biology', 3, 'DNA structure, gene expression, recombinant DNA technology.'),
('UFSC3101', 'Genetic Engineering', 3, 'Gene cloning, CRISPR, and biotechnology applications.'),
('UFSC2071', 'Environmental Chemistry', 3, 'Pollution, environmental monitoring, and green chemistry.'),
('UFSC3111', 'Ecology', 3, 'Ecosystems, biodiversity, conservation biology, and sustainability.'),
('UFSC2081', 'Numerical Methods', 3, 'Computational algorithms for solving mathematical problems.'),
('UFSC3121', 'Operations Research', 3, 'Linear programming, optimization, and decision analysis.'),
('UFSC3131', 'Stochastic Processes', 3, 'Markov chains, queuing theory, and stochastic modeling.'),
('UFSC2091', 'Physics', 3, 'Mechanics, thermodynamics, electromagnetism, and optics.'),
('UFSC3141', 'Biostatistics', 3, 'Statistical methods in biological and health sciences research.');

INSERT INTO SUBJECT (subject_code, subject_name, credit_hours, description) VALUES
('UEGE1001', 'Engineering Mathematics I', 3, 'Calculus, differential equations, and vector analysis for engineers.'),
('UEGE1011', 'Engineering Mathematics II', 3, 'Laplace transforms, Fourier series, and partial differential equations.'),
('UEGE2021', 'Engineering Mechanics', 3, 'Statics, dynamics, kinematics, and kinetics of particles and rigid bodies.'),
('UEGE2031', 'Thermodynamics', 3, 'Laws of thermodynamics, energy systems, and heat transfer.'),
('UEGE2041', 'Fluid Mechanics', 3, 'Fluid statics, dynamics, flow measurement, and hydraulics.'),
('UEGE3051', 'Structural Analysis', 3, 'Stress analysis, beam theory, and structural design principles.'),
('UEGE3061', 'Geotechnical Engineering', 3, 'Soil mechanics, foundation design, and earth structures.'),
('UEGE3071', 'Electrical Circuits', 3, 'DC/AC circuits, circuit analysis, and network theorems.'),
('UEGE3081', 'Electronics', 3, 'Semiconductor devices, amplifiers, and digital electronics.'),
('UEGE3091', 'Power Systems', 3, 'Generation, transmission, distribution, and renewable energy.'),
('UEGE3101', 'Control Systems', 3, 'Feedback control, system stability, and PID controllers.'),
('UEGE2051', 'Materials Science', 3, 'Material properties, structure, processing, and selection.'),
('UEGE3111', 'Manufacturing Processes', 3, 'Machining, casting, forming, and modern manufacturing techniques.'),
('UEGE3121', 'Mechanical Design', 3, 'Design methodology, CAD, stress analysis, and machine elements.'),
('UEGE3131', 'Robotics', 3, 'Robot kinematics, dynamics, control, and industrial applications.'),
('UEGE3141', 'Chemical Process Engineering', 3, 'Process design, reactor engineering, and process control.'),
('UEGE2061', 'Environmental Engineering', 3, 'Water treatment, waste management, and pollution control.'),
('UEGE3151', 'Renewable Energy Systems', 3, 'Solar, wind, hydro energy technologies and sustainable design.'),
('UEGE3161', 'Project Engineering', 3, 'Engineering project management, cost estimation, and planning.'),
('UEGE2071', 'Engineering Drawing and CAD', 3, 'Technical drawing, orthographic projection, and CAD software.');

-- ============================================================================
-- MODULE 1: PROGRAM-SUBJECT MAPPING (30 Programs x 10 Subjects = 300 Mappings)
-- ============================================================================

-- Program 1: Bachelor of Accounting (Honours)
INSERT INTO PROGRAM_SUBJECT (program_id, subject_id, semester, is_mandatory) VALUES
(1, 1, 1, TRUE), (1, 2, 1, TRUE), (1, 3, 2, TRUE), (1, 4, 2, TRUE), (1, 5, 3, TRUE),
(1, 6, 3, TRUE), (1, 7, 4, TRUE), (1, 8, 5, TRUE), (1, 14, 6, TRUE), (1, 16, 7, TRUE);

-- Program 2: Bachelor of Business Administration (Honours) Finance
INSERT INTO PROGRAM_SUBJECT (program_id, subject_id, semester, is_mandatory) VALUES
(2, 1, 1, TRUE), (2, 2, 1, TRUE), (2, 5, 2, TRUE), (2, 9, 3, TRUE), (2, 10, 4, TRUE),
(2, 14, 4, TRUE), (2, 11, 2, TRUE), (2, 12, 3, TRUE), (2, 13, 5, TRUE), (2, 15, 5, TRUE);

-- Program 3: Bachelor of Commerce (Honours) Accounting
INSERT INTO PROGRAM_SUBJECT (program_id, subject_id, semester, is_mandatory) VALUES
(3, 1, 1, TRUE), (3, 3, 2, TRUE), (3, 4, 2, TRUE), (3, 6, 3, TRUE), (3, 7, 4, TRUE),
(3, 8, 4, TRUE), (3, 11, 3, TRUE), (3, 13, 5, TRUE), (3, 16, 6, TRUE), (3, 19, 5, TRUE);

-- Program 4: Bachelor of International Business (Honours)
INSERT INTO PROGRAM_SUBJECT (program_id, subject_id, semester, is_mandatory) VALUES
(4, 1, 1, TRUE), (4, 11, 2, TRUE), (4, 12, 2, TRUE), (4, 13, 3, TRUE), (4, 15, 3, TRUE),
(4, 17, 4, TRUE), (4, 18, 4, TRUE), (4, 9, 5, TRUE), (4, 19, 5, TRUE), (4, 20, 6, TRUE);

-- Program 5: Bachelor of Banking and Finance (Honours)
INSERT INTO PROGRAM_SUBJECT (program_id, subject_id, semester, is_mandatory) VALUES
(5, 1, 1, TRUE), (5, 2, 1, TRUE), (5, 5, 2, TRUE), (5, 9, 3, TRUE), (5, 10, 3, TRUE),
(5, 14, 4, TRUE), (5, 6, 2, TRUE), (5, 8, 4, TRUE), (5, 15, 5, TRUE), (5, 16, 5, TRUE);

-- Program 6: Bachelor of Psychology (Honours)
INSERT INTO PROGRAM_SUBJECT (program_id, subject_id, semester, is_mandatory) VALUES
(6, 21, 1, TRUE), (6, 22, 1, TRUE), (6, 23, 2, TRUE), (6, 24, 2, TRUE), (6, 25, 3, TRUE),
(6, 26, 3, TRUE), (6, 27, 4, TRUE), (6, 34, 5, TRUE), (6, 35, 5, TRUE), (6, 36, 4, TRUE);

-- Program 7: Bachelor of Arts (Honours) Advertising
INSERT INTO PROGRAM_SUBJECT (program_id, subject_id, semester, is_mandatory) VALUES
(7, 22, 1, TRUE), (7, 28, 2, TRUE), (7, 30, 2, TRUE), (7, 33, 3, TRUE), (7, 38, 4, TRUE),
(7, 39, 4, TRUE), (7, 37, 3, TRUE), (7, 31, 5, TRUE), (7, 32, 5, TRUE), (7, 36, 1, TRUE);

-- Program 8: Bachelor of Arts (Honours) Public Relations
INSERT INTO PROGRAM_SUBJECT (program_id, subject_id, semester, is_mandatory) VALUES
(8, 22, 1, TRUE), (8, 29, 2, TRUE), (8, 30, 2, TRUE), (8, 31, 3, TRUE), (8, 40, 4, TRUE),
(8, 37, 3, TRUE), (8, 33, 4, TRUE), (8, 36, 5, TRUE), (8, 38, 5, TRUE), (8, 34, 1, TRUE);

-- Program 9: Bachelor of Social Science (Honours) Counselling
INSERT INTO PROGRAM_SUBJECT (program_id, subject_id, semester, is_mandatory) VALUES
(9, 21, 1, TRUE), (9, 22, 1, TRUE), (9, 23, 2, TRUE), (9, 24, 2, TRUE), (9, 26, 3, TRUE),
(9, 27, 3, TRUE), (9, 35, 4, TRUE), (9, 34, 4, TRUE), (9, 36, 5, TRUE), (9, 25, 5, TRUE);

-- Program 10: Bachelor of Arts (Honours) Journalism and Media Studies
INSERT INTO PROGRAM_SUBJECT (program_id, subject_id, semester, is_mandatory) VALUES
(10, 22, 1, TRUE), (10, 32, 2, TRUE), (10, 33, 2, TRUE), (10, 30, 3, TRUE), (10, 31, 3, TRUE),
(10, 34, 4, TRUE), (10, 36, 4, TRUE), (10, 37, 5, TRUE), (10, 40, 5, TRUE), (10, 28, 1, TRUE);

-- Program 11: Bachelor of Business Administration (Honours)
INSERT INTO PROGRAM_SUBJECT (program_id, subject_id, semester, is_mandatory) VALUES
(11, 41, 1, TRUE), (11, 42, 1, TRUE), (11, 43, 2, TRUE), (11, 45, 2, TRUE), (11, 46, 3, TRUE),
(11, 48, 3, TRUE), (11, 53, 4, TRUE), (11, 55, 4, TRUE), (11, 59, 5, TRUE), (11, 49, 5, TRUE);

-- Program 12: Bachelor of Economics (Honours) Financial Economics
INSERT INTO PROGRAM_SUBJECT (program_id, subject_id, semester, is_mandatory) VALUES
(12, 43, 1, TRUE), (12, 44, 1, TRUE), (12, 49, 2, TRUE), (12, 50, 2, TRUE), (12, 51, 3, TRUE),
(12, 47, 3, TRUE), (12, 55, 4, TRUE), (12, 41, 4, TRUE), (12, 42, 5, TRUE), (12, 60, 5, TRUE);

-- Program 13: Bachelor of Marketing (Honours)
INSERT INTO PROGRAM_SUBJECT (program_id, subject_id, semester, is_mandatory) VALUES
(13, 41, 1, TRUE), (13, 45, 2, TRUE), (13, 52, 2, TRUE), (13, 53, 3, TRUE), (13, 49, 3, TRUE),
(13, 55, 4, TRUE), (13, 42, 1, TRUE), (13, 58, 4, TRUE), (13, 59, 5, TRUE), (13, 48, 5, TRUE);

-- Program 14: Bachelor of Logistics and Supply Chain Management (Honours)
INSERT INTO PROGRAM_SUBJECT (program_id, subject_id, semester, is_mandatory) VALUES
(14, 41, 1, TRUE), (14, 42, 1, TRUE), (14, 46, 2, TRUE), (14, 54, 3, TRUE), (14, 55, 3, TRUE),
(14, 59, 4, TRUE), (14, 49, 2, TRUE), (14, 52, 4, TRUE), (14, 58, 5, TRUE), (14, 60, 5, TRUE);

-- Program 15: Bachelor of Entrepreneurship (Honours)
INSERT INTO PROGRAM_SUBJECT (program_id, subject_id, semester, is_mandatory) VALUES
(15, 41, 1, TRUE), (15, 42, 1, TRUE), (15, 45, 2, TRUE), (15, 56, 3, TRUE), (15, 57, 3, TRUE),
(15, 58, 4, TRUE), (15, 48, 2, TRUE), (15, 52, 4, TRUE), (15, 59, 5, TRUE), (15, 60, 5, TRUE);

-- Program 16: Bachelor of Computer Science (Honours)
INSERT INTO PROGRAM_SUBJECT (program_id, subject_id, semester, is_mandatory) VALUES
(16, 61, 1, TRUE), (16, 62, 2, TRUE), (16, 63, 2, TRUE), (16, 64, 3, TRUE), (16, 65, 4, TRUE),
(16, 66, 3, TRUE), (16, 67, 4, TRUE), (16, 68, 5, TRUE), (16, 70, 5, TRUE), (16, 77, 1, TRUE);

-- Program 17: Bachelor of Information Systems (Honours)
INSERT INTO PROGRAM_SUBJECT (program_id, subject_id, semester, is_mandatory) VALUES
(17, 61, 1, TRUE), (17, 64, 2, TRUE), (17, 66, 2, TRUE), (17, 79, 3, TRUE), (17, 69, 3, TRUE),
(17, 74, 4, TRUE), (17, 78, 4, TRUE), (17, 62, 1, TRUE), (17, 63, 5, TRUE), (17, 67, 5, TRUE);

-- Program 18: Bachelor of Software Engineering (Honours)
INSERT INTO PROGRAM_SUBJECT (program_id, subject_id, semester, is_mandatory) VALUES
(18, 61, 1, TRUE), (18, 62, 1, TRUE), (18, 63, 2, TRUE), (18, 66, 2, TRUE), (18, 69, 3, TRUE),
(18, 64, 3, TRUE), (18, 78, 4, TRUE), (18, 74, 4, TRUE), (18, 71, 5, TRUE), (18, 77, 5, TRUE);

-- Program 19: Bachelor of Data Science and Analytics (Honours)
INSERT INTO PROGRAM_SUBJECT (program_id, subject_id, semester, is_mandatory) VALUES
(19, 61, 1, TRUE), (19, 62, 2, TRUE), (19, 64, 2, TRUE), (19, 70, 3, TRUE), (19, 75, 3, TRUE),
(19, 65, 4, TRUE), (19, 77, 1, TRUE), (19, 74, 4, TRUE), (19, 78, 5, TRUE), (19, 63, 5, TRUE);

-- Program 20: Bachelor of Computer Science (Honours) Network Security
INSERT INTO PROGRAM_SUBJECT (program_id, subject_id, semester, is_mandatory) VALUES
(20, 61, 1, TRUE), (20, 62, 1, TRUE), (20, 67, 2, TRUE), (20, 73, 3, TRUE), (20, 68, 2, TRUE),
(20, 76, 3, TRUE), (20, 74, 4, TRUE), (20, 63, 4, TRUE), (20, 64, 5, TRUE), (20, 77, 5, TRUE);

-- Program 21: Bachelor of Science (Honours) Actuarial Science
INSERT INTO PROGRAM_SUBJECT (program_id, subject_id, semester, is_mandatory) VALUES
(21, 81, 1, TRUE), (21, 82, 1, TRUE), (21, 83, 2, TRUE), (21, 84, 2, TRUE), (21, 85, 3, TRUE),
(21, 86, 3, TRUE), (21, 87, 4, TRUE), (21, 96, 4, TRUE), (21, 97, 5, TRUE), (21, 98, 5, TRUE);

-- Program 22: Bachelor of Science (Honours) Food Science
INSERT INTO PROGRAM_SUBJECT (program_id, subject_id, semester, is_mandatory) VALUES
(22, 88, 1, TRUE), (22, 89, 1, TRUE), (22, 90, 2, TRUE), (22, 91, 2, TRUE), (22, 99, 3, TRUE),
(22, 94, 3, TRUE), (22, 81, 4, TRUE), (22, 100, 4, TRUE), (22, 92, 5, TRUE), (22, 93, 5, TRUE);

-- Program 23: Bachelor of Science (Honours) Biotechnology
INSERT INTO PROGRAM_SUBJECT (program_id, subject_id, semester, is_mandatory) VALUES
(23, 88, 1, TRUE), (23, 89, 1, TRUE), (23, 92, 2, TRUE), (23, 93, 2, TRUE), (23, 99, 3, TRUE),
(23, 100, 3, TRUE), (23, 81, 4, TRUE), (23, 82, 4, TRUE), (23, 94, 5, TRUE), (23, 95, 5, TRUE);

-- Program 24: Bachelor of Science (Honours) Applied Mathematics with Computing
INSERT INTO PROGRAM_SUBJECT (program_id, subject_id, semester, is_mandatory) VALUES
(24, 81, 1, TRUE), (24, 82, 1, TRUE), (24, 83, 2, TRUE), (24, 84, 2, TRUE), (24, 96, 3, TRUE),
(24, 97, 3, TRUE), (24, 98, 4, TRUE), (24, 85, 4, TRUE), (24, 87, 5, TRUE), (24, 99, 5, TRUE);

-- Program 25: Bachelor of Science (Honours) Environmental Science
INSERT INTO PROGRAM_SUBJECT (program_id, subject_id, semester, is_mandatory) VALUES
(25, 88, 1, TRUE), (25, 89, 1, TRUE), (25, 94, 2, TRUE), (25, 95, 2, TRUE), (25, 99, 3, TRUE),
(25, 81, 3, TRUE), (25, 100, 4, TRUE), (25, 84, 4, TRUE), (25, 91, 5, TRUE), (25, 92, 5, TRUE);

-- Program 26: Bachelor of Engineering (Honours) Civil Engineering
INSERT INTO PROGRAM_SUBJECT (program_id, subject_id, semester, is_mandatory) VALUES
(26, 101, 1, TRUE), (26, 102, 2, TRUE), (26, 103, 2, TRUE), (26, 105, 3, TRUE), (26, 106, 4, TRUE),
(26, 107, 4, TRUE), (26, 117, 5, TRUE), (26, 119, 6, TRUE), (26, 120, 1, TRUE), (26, 112, 3, TRUE);

-- Program 27: Bachelor of Engineering (Honours) Electrical and Electronics Engineering
INSERT INTO PROGRAM_SUBJECT (program_id, subject_id, semester, is_mandatory) VALUES
(27, 101, 1, TRUE), (27, 102, 2, TRUE), (27, 108, 2, TRUE), (27, 109, 3, TRUE), (27, 110, 3, TRUE),
(27, 111, 4, TRUE), (27, 118, 4, TRUE), (27, 119, 5, TRUE), (27, 120, 1, TRUE), (27, 103, 5, TRUE);

-- Program 28: Bachelor of Engineering (Honours) Mechanical Engineering
INSERT INTO PROGRAM_SUBJECT (program_id, subject_id, semester, is_mandatory) VALUES
(28, 101, 1, TRUE), (28, 102, 2, TRUE), (28, 103, 2, TRUE), (28, 104, 3, TRUE), (28, 105, 3, TRUE),
(28, 112, 4, TRUE), (28, 113, 4, TRUE), (28, 114, 5, TRUE), (28, 119, 5, TRUE), (28, 120, 1, TRUE);

-- Program 29: Bachelor of Engineering (Honours) Mechatronics Engineering
INSERT INTO PROGRAM_SUBJECT (program_id, subject_id, semester, is_mandatory) VALUES
(29, 101, 1, TRUE), (29, 102, 2, TRUE), (29, 108, 2, TRUE), (29, 109, 3, TRUE), (29, 111, 3, TRUE),
(29, 115, 4, TRUE), (29, 114, 4, TRUE), (29, 119, 5, TRUE), (29, 120, 1, TRUE), (29, 112, 5, TRUE);

-- Program 30: Bachelor of Engineering (Honours) Chemical Engineering
INSERT INTO PROGRAM_SUBJECT (program_id, subject_id, semester, is_mandatory) VALUES
(30, 101, 1, TRUE), (30, 102, 2, TRUE), (30, 104, 2, TRUE), (30, 105, 3, TRUE), (30, 116, 3, TRUE),
(30, 117, 4, TRUE), (30, 118, 4, TRUE), (30, 119, 5, TRUE), (30, 120, 1, TRUE), (30, 112, 5, TRUE);

-- ============================================================================
-- MODULE 2: ADMISSION REQUIREMENTS (One per program = 30 requirements)
-- ============================================================================

INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info) VALUES
(1, 'STPM', 'Minimum CGPA 2.00 with a pass in Mathematics at SPM level', 'Credit in Mathematics at SPM level', 'No entrance exam required'),
(1, 'A-Level', 'Minimum 2 passes', 'Grade C in Mathematics at O-Level or equivalent', NULL),
(1, 'UEC', 'Minimum 5Bs including Mathematics', NULL, NULL),

(2, 'STPM', 'Minimum CGPA 2.00', 'Credit in Mathematics at SPM level', 'No entrance exam required'),
(2, 'Matriculation', 'Minimum CGPA 2.00', NULL, NULL),

(3, 'STPM', 'Minimum CGPA 2.00', 'Credit in Mathematics at SPM level', NULL),
(3, 'Foundation', 'Minimum CGPA 2.00 in relevant field', NULL, NULL),

(4, 'STPM', 'Minimum CGPA 2.00', 'Credit in Mathematics and English at SPM level', NULL),
(4, 'A-Level', 'Minimum 2 passes', NULL, NULL),

(5, 'STPM', 'Minimum CGPA 2.00', 'Credit in Mathematics at SPM level', NULL),
(5, 'Diploma', 'Minimum CGPA 2.50 in Finance/Banking', 'Credit transfer available', NULL);

INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info) VALUES
(6, 'STPM', 'Minimum CGPA 2.50', 'Credit in English at SPM level', 'Possible interview required'),
(6, 'A-Level', 'Minimum 2 passes', 'Strong academic background preferred', 'Psychological assessment may be required'),

(7, 'STPM', 'Minimum CGPA 2.00', 'Credit in English at SPM level', NULL),
(7, 'Diploma', 'Minimum CGPA 2.50 in Mass Communication/Marketing', NULL, NULL),

(8, 'STPM', 'Minimum CGPA 2.00', 'Credit in English at SPM level', NULL),
(8, 'Foundation', 'Minimum CGPA 2.00', NULL, NULL),

(9, 'STPM', 'Minimum CGPA 2.50', 'Credit in English at SPM level', 'Interview may be required'),
(9, 'A-Level', 'Minimum 2 passes', NULL, NULL),

(10, 'STPM', 'Minimum CGPA 2.00', 'Credit in English and Bahasa Malaysia at SPM level', NULL),
(10, 'Diploma', 'Minimum CGPA 2.50 in Mass Communication', NULL, NULL);

INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info) VALUES
(11, 'STPM', 'Minimum CGPA 2.00', 'Credit in Mathematics at SPM level', NULL),
(11, 'Foundation', 'Minimum CGPA 2.00 in business studies', NULL, NULL),

(12, 'STPM', 'Minimum CGPA 2.33 with Mathematics', 'Credit in Mathematics at SPM level', NULL),
(12, 'A-Level', 'Minimum 2Cs including Mathematics', NULL, NULL),

(13, 'STPM', 'Minimum CGPA 2.00', 'Credit in English at SPM level', NULL),
(13, 'Diploma', 'Minimum CGPA 2.50 in Marketing/Business', 'Credit transfer may be available', NULL),

(14, 'STPM', 'Minimum CGPA 2.00', 'Credit in Mathematics at SPM level', NULL),
(14, 'Foundation', 'Minimum CGPA 2.00', NULL, NULL),

(15, 'STPM', 'Minimum CGPA 2.00', 'Strong interest in entrepreneurship', NULL),
(15, 'Diploma', 'Minimum CGPA 2.50 in any business-related field', 'Portfolio of business ideas preferred', NULL);

INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info) VALUES
(16, 'STPM', 'Minimum CGPA 2.00 with Mathematics', 'Credit in Mathematics and Additional Mathematics at SPM level', NULL),
(16, 'A-Level', 'Minimum 2 passes including Mathematics', NULL, NULL),
(16, 'UEC', 'Minimum 5Bs including Mathematics', NULL, NULL),

(17, 'STPM', 'Minimum CGPA 2.00', 'Credit in Mathematics at SPM level', NULL),
(17, 'Diploma', 'Minimum CGPA 2.50 in IT/Computer Science', 'Credit transfer available for relevant subjects', NULL),

(18, 'STPM', 'Minimum CGPA 2.00 with Mathematics', 'Credit in Mathematics at SPM level', NULL),
(18, 'Foundation', 'Minimum CGPA 2.00 in IT/Engineering', NULL, NULL),

(19, 'STPM', 'Minimum CGPA 2.00 with Mathematics', 'Credit in Mathematics and Additional Mathematics at SPM level', NULL),
(19, 'A-Level', 'Minimum 2 passes including Mathematics', 'Strong analytical skills required', NULL),

(20, 'STPM', 'Minimum CGPA 2.00 with Mathematics', 'Credit in Mathematics at SPM level', NULL),
(20, 'Diploma', 'Minimum CGPA 2.50 in IT/Computer Science', 'Basic programming knowledge preferred', NULL);

INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info) VALUES
(21, 'STPM', 'Minimum CGPA 3.00 with A in Mathematics', 'A in Additional Mathematics at SPM level', 'Strong mathematical background essential'),
(21, 'A-Level', 'Minimum A in Mathematics', 'Excellent mathematical aptitude required', NULL),

(22, 'STPM', 'Minimum CGPA 2.00 with passes in Chemistry and Biology', 'Credit in Mathematics, Chemistry, Biology at SPM level', NULL),
(22, 'Matriculation', 'Minimum CGPA 2.00 in Science stream', NULL, NULL),

(23, 'STPM', 'Minimum CGPA 2.00 with passes in Biology and Chemistry', 'Credit in Biology, Chemistry at SPM level', NULL),
(23, 'A-Level', 'Minimum 2 passes including Biology/Chemistry', NULL, NULL),

(24, 'STPM', 'Minimum CGPA 2.33 with Mathematics', 'Credit in Mathematics and Additional Mathematics at SPM level', NULL),
(24, 'Foundation', 'Minimum CGPA 2.50 in Science/Computing', NULL, NULL),

(25, 'STPM', 'Minimum CGPA 2.00 with passes in Biology/Chemistry', 'Credit in Science subjects at SPM level', NULL),
(25, 'Matriculation', 'Minimum CGPA 2.00 in Science stream', NULL, NULL);

INSERT INTO ADMISSION_REQUIREMENT (program_id, qualification_type, minimum_grade, additional_requirements, entrance_exam_info) VALUES
(26, 'STPM', 'Minimum CGPA 2.00 with passes in Mathematics and Physics', 'Credit in Mathematics, Additional Mathematics, Physics at SPM level', NULL),
(26, 'A-Level', 'Minimum 2 passes including Mathematics and Physics', NULL, NULL),
(26, 'UEC', 'Minimum 5Bs including Mathematics and Physics', NULL, NULL),

(27, 'STPM', 'Minimum CGPA 2.00 with passes in Mathematics and Physics', 'Credit in Mathematics, Additional Mathematics, Physics at SPM level', 'BEM accreditation requirement'),
(27, 'Foundation', 'Minimum CGPA 2.00 in Engineering', NULL, NULL),

(28, 'STPM', 'Minimum CGPA 2.00 with passes in Mathematics and Physics', 'Credit in Mathematics, Additional Mathematics, Physics at SPM level', NULL),
(28, 'A-Level', 'Minimum 2 passes including Mathematics and Physics', NULL, NULL),

(29, 'STPM', 'Minimum CGPA 2.00 with passes in Mathematics and Physics', 'Credit in Mathematics, Additional Mathematics, Physics at SPM level', NULL),
(29, 'Diploma', 'Minimum CGPA 2.50 in Mechatronics/Electronics', 'Credit transfer available', NULL),

(30, 'STPM', 'Minimum CGPA 2.00 with passes in Mathematics, Physics, Chemistry', 'Credit in Mathematics, Additional Mathematics, Physics, Chemistry at SPM level', 'BEM accreditation requirement'),
(30, 'Foundation', 'Minimum CGPA 2.00 in Engineering/Science', NULL, NULL);

-- ============================================================================
-- MODULE 2: DOCUMENT CHECKLIST (Common documents for all programs)
-- ============================================================================

INSERT INTO DOCUMENT_CHECKLIST (program_id, document_name, is_mandatory, description) VALUES
(1, 'SPM Certificate', TRUE, 'Original and photocopy of SPM certificate'),
(1, 'STPM/A-Level/UEC Certificate', TRUE, 'Original and photocopy of highest qualification'),
(1, 'Birth Certificate', TRUE, 'Original and photocopy'),
(1, 'Identity Card', TRUE, 'Photocopy of MyKad (front and back)'),
(1, 'Passport Size Photos', TRUE, '4 recent passport-sized photographs'),
(1, 'Medical Report', FALSE, 'General health examination report'),
(2, 'SPM Certificate', TRUE, 'Original and photocopy'), (2, 'STPM/A-Level Certificate', TRUE, 'Original and photocopy'), (2, 'Identity Card', TRUE, 'Photocopy of MyKad'),
(3, 'SPM Certificate', TRUE, 'Original and photocopy'), (3, 'STPM/UEC Certificate', TRUE, 'Original and photocopy'), (3, 'Identity Card', TRUE, 'Photocopy of MyKad'),
(4, 'SPM Certificate', TRUE, 'Original and photocopy'), (4, 'STPM/A-Level Certificate', TRUE, 'Original and photocopy'), (4, 'Identity Card', TRUE, 'Photocopy of MyKad'),
(5, 'SPM Certificate', TRUE, 'Original and photocopy'), (5, 'Diploma Certificate', TRUE, 'If applicable'), (5, 'Identity Card', TRUE, 'Photocopy of MyKad'),
(6, 'SPM Certificate', TRUE, 'Original and photocopy'), (6, 'STPM/A-Level Certificate', TRUE, 'Original and photocopy'), (6, 'Identity Card', TRUE, 'Photocopy of MyKad'),
(7, 'SPM Certificate', TRUE, 'Original and photocopy'), (7, 'STPM/Diploma Certificate', TRUE, 'Original and photocopy'), (7, 'Portfolio', FALSE, 'Creative work samples'),
(8, 'SPM Certificate', TRUE, 'Original and photocopy'), (8, 'STPM Certificate', TRUE, 'Original and photocopy'), (8, 'Identity Card', TRUE, 'Photocopy of MyKad'),
(9, 'SPM Certificate', TRUE, 'Original and photocopy'), (9, 'STPM/A-Level Certificate', TRUE, 'Original and photocopy'), (9, 'Identity Card', TRUE, 'Photocopy of MyKad'),
(10, 'SPM Certificate', TRUE, 'Original and photocopy'), (10, 'STPM/Diploma Certificate', TRUE, 'Original and photocopy'), (10, 'Identity Card', TRUE, 'Photocopy of MyKad');

-- Continue for remaining programs (11-30) with standard documents
INSERT INTO DOCUMENT_CHECKLIST (program_id, document_name, is_mandatory, description)
SELECT program_id, 'SPM Certificate', TRUE, 'Original and photocopy of SPM certificate'
FROM PROGRAM WHERE program_id BETWEEN 11 AND 30;

INSERT INTO DOCUMENT_CHECKLIST (program_id, document_name, is_mandatory, description)
SELECT program_id, 'Higher Education Certificate', TRUE, 'STPM/A-Level/Diploma/Foundation certificate'
FROM PROGRAM WHERE program_id BETWEEN 11 AND 30;

INSERT INTO DOCUMENT_CHECKLIST (program_id, document_name, is_mandatory, description)
SELECT program_id, 'Identity Card', TRUE, 'Photocopy of MyKad or passport for international students'
FROM PROGRAM WHERE program_id BETWEEN 11 AND 30;

-- ============================================================================
-- MODULE 2: IMPORTANT DATES (2025 Academic Year - 3 Trimesters)
-- ============================================================================

INSERT INTO IMPORTANT_DATE (program_id, event_type, start_date, end_date, description) VALUES
(1, 'Application Period', '2024-10-01', '2024-12-31', 'Application window for January 2025 intake'),
(1, 'Trimester Start', '2025-01-13', NULL, 'First day of Trimester 1'),
(1, 'Trimester End', '2025-04-25', NULL, 'Last day of Trimester 1'),

(1, 'Application Period', '2025-02-01', '2025-04-30', 'Application window for May 2025 intake'),
(1, 'Trimester Start', '2025-05-19', NULL, 'First day of Trimester 2'),
(1, 'Trimester End', '2025-08-29', NULL, 'Last day of Trimester 2'),

(1, 'Application Period', '2025-06-01', '2025-08-31', 'Application window for September 2025 intake'),
(1, 'Trimester Start', '2025-09-08', NULL, 'First day of Trimester 3'),
(1, 'Trimester End', '2025-12-19', NULL, 'Last day of Trimester 3');

-- ============================================================================
-- MODULE 2: SAMPLE APPLICANTS
-- ============================================================================

INSERT INTO APPLICANT (full_name, email, phone, nationality, date_of_birth, address) VALUES
('Tan Wei Jian', 'tanweijian@gmail.com', '+6012-345 6789', 'Malaysian', '2005-03-15', 'No. 123, Jalan Bukit, 43000 Kajang, Selangor'),
('Nurul Aisyah binti Abdullah', 'nurul@gmail.com', '+6013-456 7890', 'Malaysian', '2005-07-22', 'No. 456, Taman Bunga, 31900 Kampar, Perak'),
('Lim Kai Xuan', 'limkaixuan@gmail.com', '+6014-567 8901', 'Malaysian', '2005-01-10', 'No. 789, Jalan Raya, 50000 Kuala Lumpur'),
('Siti Nur Haziqah', 'siti@gmail.com', '+6015-678 9012', 'Malaysian', '2005-09-05', 'No. 321, Taman Permai, 43000 Kajang, Selangor'),
('Wong Jun Ming', 'wongjunming@gmail.com', '+6016-789 0123', 'Malaysian', '2005-11-18', 'No. 654, Jalan Putra, 31900 Kampar, Perak');

-- ============================================================================
-- MODULE 2: SAMPLE APPLICATIONS
-- ============================================================================

INSERT INTO APPLICATION (applicant_id, program_id, reference_number, status, submission_date, remarks) VALUES
(1, 16, 'UTAR2025010001', 'Accepted', '2024-11-01', 'Excellent academic background. Accepted for January 2025 intake.'),
(2, 1, 'UTAR2025010002', 'Under Review', '2024-11-05', 'Documents under verification.'),
(3, 27, 'UTAR2025010003', 'Interview Scheduled', '2024-11-08', 'Interview scheduled for December 15, 2024.'),
(4, 6, 'UTAR2025010004', 'Submitted', '2024-11-10', 'Application received. Pending review.'),
(5, 11, 'UTAR2025010005', 'Accepted', '2024-10-28', 'Accepted with merit scholarship. January 2025 intake.');

-- ============================================================================
-- MODULE 2: APPLICATION STATUS HISTORY
-- ============================================================================

INSERT INTO APPLICATION_STATUS (application_id, status, remarks) VALUES
(1, 'Submitted', 'Application submitted online'),
(1, 'Under Review', 'Documents verified'),
(1, 'Accepted', 'Offer letter issued'),

(2, 'Submitted', 'Application submitted online'),
(2, 'Under Review', 'Reviewing academic qualifications'),

(3, 'Submitted', 'Application submitted online'),
(3, 'Interview Scheduled', 'Interview date confirmed'),

(4, 'Submitted', 'Application received and logged'),

(5, 'Submitted', 'Application submitted online'),
(5, 'Accepted', 'Accepted with scholarship');

-- ============================================================================
-- MODULE 3: TUITION FEES (All 30 Programs x 3 Trimesters = 90 Entries)
-- ============================================================================

INSERT INTO TUITION_FEE (program_id, semester, amount, currency, academic_year, payment_deadline, late_fee) VALUES
(1, 1, 6800.00, 'MYR', '2025', '2025-01-10', 50.00),
(1, 2, 6800.00, 'MYR', '2025', '2025-05-15', 50.00),
(1, 3, 6800.00, 'MYR', '2025', '2025-09-05', 50.00),

(2, 1, 6800.00, 'MYR', '2025', '2025-01-10', 50.00),
(2, 2, 6800.00, 'MYR', '2025', '2025-05-15', 50.00),
(2, 3, 6800.00, 'MYR', '2025', '2025-09-05', 50.00),

(3, 1, 6800.00, 'MYR', '2025', '2025-01-10', 50.00),
(3, 2, 6800.00, 'MYR', '2025', '2025-05-15', 50.00),
(3, 3, 6800.00, 'MYR', '2025', '2025-09-05', 50.00),

(4, 1, 6900.00, 'MYR', '2025', '2025-01-10', 50.00),
(4, 2, 6900.00, 'MYR', '2025', '2025-05-15', 50.00),
(4, 3, 6900.00, 'MYR', '2025', '2025-09-05', 50.00),

(5, 1, 6800.00, 'MYR', '2025', '2025-01-10', 50.00),
(5, 2, 6800.00, 'MYR', '2025', '2025-05-15', 50.00),
(5, 3, 6800.00, 'MYR', '2025', '2025-09-05', 50.00);

-- FAS Programs (Programs 6-10) - Arts & Social Science
-- Tuition: RM 6,500 - RM 6,600 per trimester

INSERT INTO TUITION_FEE (program_id, semester, amount, currency, academic_year, payment_deadline, late_fee) VALUES
(6, 1, 6500.00, 'MYR', '2025', '2025-01-10', 50.00),
(6, 2, 6500.00, 'MYR', '2025', '2025-05-15', 50.00),
(6, 3, 6500.00, 'MYR', '2025', '2025-09-05', 50.00),

(7, 1, 6500.00, 'MYR', '2025', '2025-01-10', 50.00),
(7, 2, 6500.00, 'MYR', '2025', '2025-05-15', 50.00),
(7, 3, 6500.00, 'MYR', '2025', '2025-09-05', 50.00),

(8, 1, 6500.00, 'MYR', '2025', '2025-01-10', 50.00),
(8, 2, 6500.00, 'MYR', '2025', '2025-05-15', 50.00),
(8, 3, 6500.00, 'MYR', '2025', '2025-09-05', 50.00),

(9, 1, 6600.00, 'MYR', '2025', '2025-01-10', 50.00),
(9, 2, 6600.00, 'MYR', '2025', '2025-05-15', 50.00),
(9, 3, 6600.00, 'MYR', '2025', '2025-09-05', 50.00),

(10, 1, 6500.00, 'MYR', '2025', '2025-01-10', 50.00),
(10, 2, 6500.00, 'MYR', '2025', '2025-05-15', 50.00),
(10, 3, 6500.00, 'MYR', '2025', '2025-09-05', 50.00);

-- FBF Programs (Programs 11-15) - Business & Finance
-- Tuition: RM 6,700 - RM 6,900 per trimester

INSERT INTO TUITION_FEE (program_id, semester, amount, currency, academic_year, payment_deadline, late_fee) VALUES
(11, 1, 6700.00, 'MYR', '2025', '2025-01-10', 50.00),
(11, 2, 6700.00, 'MYR', '2025', '2025-05-15', 50.00),
(11, 3, 6700.00, 'MYR', '2025', '2025-09-05', 50.00),

(12, 1, 6900.00, 'MYR', '2025', '2025-01-10', 50.00),
(12, 2, 6900.00, 'MYR', '2025', '2025-05-15', 50.00),
(12, 3, 6900.00, 'MYR', '2025', '2025-09-05', 50.00),

(13, 1, 6700.00, 'MYR', '2025', '2025-01-10', 50.00),
(13, 2, 6700.00, 'MYR', '2025', '2025-05-15', 50.00),
(13, 3, 6700.00, 'MYR', '2025', '2025-09-05', 50.00),

(14, 1, 6700.00, 'MYR', '2025', '2025-01-10', 50.00),
(14, 2, 6700.00, 'MYR', '2025', '2025-05-15', 50.00),
(14, 3, 6700.00, 'MYR', '2025', '2025-09-05', 50.00),

(15, 1, 6700.00, 'MYR', '2025', '2025-01-10', 50.00),
(15, 2, 6700.00, 'MYR', '2025', '2025-05-15', 50.00),
(15, 3, 6700.00, 'MYR', '2025', '2025-09-05', 50.00);

-- FICT Programs (Programs 16-20) - Information & Communication Technology
-- Tuition: RM 7,200 - RM 7,400 per trimester

INSERT INTO TUITION_FEE (program_id, semester, amount, currency, academic_year, payment_deadline, late_fee) VALUES
(16, 1, 7200.00, 'MYR', '2025', '2025-01-10', 50.00),
(16, 2, 7200.00, 'MYR', '2025', '2025-05-15', 50.00),
(16, 3, 7200.00, 'MYR', '2025', '2025-09-05', 50.00),

(17, 1, 7200.00, 'MYR', '2025', '2025-01-10', 50.00),
(17, 2, 7200.00, 'MYR', '2025', '2025-05-15', 50.00),
(17, 3, 7200.00, 'MYR', '2025', '2025-09-05', 50.00),

(18, 1, 7200.00, 'MYR', '2025', '2025-01-10', 50.00),
(18, 2, 7200.00, 'MYR', '2025', '2025-05-15', 50.00),
(18, 3, 7200.00, 'MYR', '2025', '2025-09-05', 50.00),

(19, 1, 7400.00, 'MYR', '2025', '2025-01-10', 50.00),
(19, 2, 7400.00, 'MYR', '2025', '2025-05-15', 50.00),
(19, 3, 7400.00, 'MYR', '2025', '2025-09-05', 50.00),

(20, 1, 7300.00, 'MYR', '2025', '2025-01-10', 50.00),
(20, 2, 7300.00, 'MYR', '2025', '2025-05-15', 50.00),
(20, 3, 7300.00, 'MYR', '2025', '2025-09-05', 50.00);

-- FSc Programs (Programs 21-25) - Science
-- Tuition: RM 7,000 - RM 7,500 per trimester

INSERT INTO TUITION_FEE (program_id, semester, amount, currency, academic_year, payment_deadline, late_fee) VALUES
(21, 1, 7500.00, 'MYR', '2025', '2025-01-10', 50.00),
(21, 2, 7500.00, 'MYR', '2025', '2025-05-15', 50.00),
(21, 3, 7500.00, 'MYR', '2025', '2025-09-05', 50.00),

(22, 1, 7000.00, 'MYR', '2025', '2025-01-10', 50.00),
(22, 2, 7000.00, 'MYR', '2025', '2025-05-15', 50.00),
(22, 3, 7000.00, 'MYR', '2025', '2025-09-05', 50.00),

(23, 1, 7000.00, 'MYR', '2025', '2025-01-10', 50.00),
(23, 2, 7000.00, 'MYR', '2025', '2025-05-15', 50.00),
(23, 3, 7000.00, 'MYR', '2025', '2025-09-05', 50.00),

(24, 1, 7200.00, 'MYR', '2025', '2025-01-10', 50.00),
(24, 2, 7200.00, 'MYR', '2025', '2025-05-15', 50.00),
(24, 3, 7200.00, 'MYR', '2025', '2025-09-05', 50.00),

(25, 1, 7000.00, 'MYR', '2025', '2025-01-10', 50.00),
(25, 2, 7000.00, 'MYR', '2025', '2025-05-15', 50.00),
(25, 3, 7000.00, 'MYR', '2025', '2025-09-05', 50.00);

-- FEGT Programs (Programs 26-30) - Engineering & Green Technology
-- Tuition: RM 8,200 - RM 8,400 per trimester (4-year programs)

INSERT INTO TUITION_FEE (program_id, semester, amount, currency, academic_year, payment_deadline, late_fee) VALUES
(26, 1, 8200.00, 'MYR', '2025', '2025-01-10', 50.00),
(26, 2, 8200.00, 'MYR', '2025', '2025-05-15', 50.00),
(26, 3, 8200.00, 'MYR', '2025', '2025-09-05', 50.00),

(27, 1, 8200.00, 'MYR', '2025', '2025-01-10', 50.00),
(27, 2, 8200.00, 'MYR', '2025', '2025-05-15', 50.00),
(27, 3, 8200.00, 'MYR', '2025', '2025-09-05', 50.00),

(28, 1, 8200.00, 'MYR', '2025', '2025-01-10', 50.00),
(28, 2, 8200.00, 'MYR', '2025', '2025-05-15', 50.00),
(28, 3, 8200.00, 'MYR', '2025', '2025-09-05', 50.00),

(29, 1, 8300.00, 'MYR', '2025', '2025-01-10', 50.00),
(29, 2, 8300.00, 'MYR', '2025', '2025-05-15', 50.00),
(29, 3, 8300.00, 'MYR', '2025', '2025-09-05', 50.00),

(30, 1, 8400.00, 'MYR', '2025', '2025-01-10', 50.00),
(30, 2, 8400.00, 'MYR', '2025', '2025-05-15', 50.00),
(30, 3, 8400.00, 'MYR', '2025', '2025-09-05', 50.00);

-- ============================================================================
-- MODULE 3: SCHOLARSHIPS (5 Top Scholarships)
-- ============================================================================

INSERT INTO SCHOLARSHIP (scholarship_name, eligibility_criteria, amount, type, application_deadline, available_slots, description) VALUES

('UTAR Academic Excellence Scholarship', 
'STPM CGPA 4.00 or A-Level 3As or SPM 10As or above. Full tuition fee waiver for entire program (3 years x 3 trimesters). Malaysian and international students eligible.',
40800.00, 
'Merit-based', 
'2025-01-31',
10,
'Full 100% tuition waiver scholarship for the entire program duration. Covers 3 years (9 trimesters) for Bachelor programs. Automatic consideration upon admission based on entry qualifications. No separate application required. Recipients must maintain minimum CGPA of 3.50 to retain scholarship.'),

('UTAR High Achievers Scholarship', 
'STPM CGPA 3.67 or A-Level 2As 1B or SPM 8As or above. 50% tuition fee waiver for entire program. Must maintain CGPA 3.00 to retain scholarship.',
20400.00, 
'Merit-based', 
'2025-01-31',
30,
'50% tuition waiver for entire program duration. Automatic consideration upon admission. No separate application required. Renewable each semester based on academic performance. Must achieve minimum CGPA 3.00 to continue receiving scholarship.'),

('UTAR Education Foundation Scholarship', 
'Household income below RM 5,000/month. Minimum CGPA 3.00 or equivalent. Malaysian citizens only. Demonstrate financial need with supporting documents.',
10000.00, 
'Need-based + Merit', 
'2025-03-31',
50,
'Annual scholarship of RM 10,000 to support students from low-income families. Renewable annually based on maintaining CGPA 3.00 and continued financial need. Application requires income proof (parents payslips, EPF statements), academic transcripts, and personal statement. Interview may be required.'),

('Industry Partner Scholarship (IT & Engineering)', 
'For FICT and FEGT students only. STPM CGPA 3.50 or equivalent. Strong interest in technology and engineering. Includes mandatory internship placement with partner companies.',
25000.00, 
'Merit-based', 
'2025-02-28',
15,
'One-time scholarship of RM 25,000 sponsored by industry partners including tech companies and engineering firms. Includes guaranteed internship placement (3-6 months) with sponsoring company. Apply through respective faculty office. Submit resume, academic transcript, personal statement, and letter of recommendation.'),

('Women in STEM Scholarship', 
'For female students in Science, Technology, Engineering programs (FSc, FICT, FEGT). STPM CGPA 3.33 or equivalent. Malaysian citizens only.',
12000.00, 
'Merit-based + Gender', 
'2025-04-30',
25,
'Annual scholarship to encourage female participation in STEM fields. Renewable for up to 3 years based on CGPA 3.00. Online application required with 500-word essay on "Why I chose STEM and my career aspirations". Academic transcript and proof of citizenship required.');
-- ============================================================================
-- MODULE 3: FINANCIAL AID OPTIONS
-- ============================================================================

INSERT INTO FINANCIAL_AID (aid_name, aid_type, eligibility_criteria, application_process, deadline) VALUES
('PTPTN (Perbadanan Tabung Pendidikan Tinggi Nasional)', 'Student Loan', 'Malaysian citizens, family income below RM 100,000/year, enrolled in accredited programs', 'Apply online at ptptn.gov.my. Submit income documents, academic transcript, offer letter.', '2025-02-28'),

('MARA Education Loan', 'Student Loan', 'Bumiputera Malaysian citizens, demonstrated financial need', 'Apply at MARA offices. Submit application form and supporting documents.', '2025-03-15'),

('UTAR Installment Payment Plan', 'Payment Plan', 'Open to all students. Break down tuition into monthly installments with no interest', 'Apply at Finance Office. RM 200 processing fee. Automatic approval.', '2025-01-05'),

('EPF Education Withdrawal', 'Withdrawal Scheme', 'Parents can withdraw from EPF Account 2 for children''s education', 'Apply at EPF offices with university offer letter and identity documents.', NULL);

-- ============================================================================
-- MODULE 4: CAMPUS FACILITIES (8 Key Facilities)
-- ============================================================================

INSERT INTO CAMPUS_FACILITY (facility_name, facility_type, description, location, operating_hours) VALUES
('Perpustakaan Tun Dr Ling Liong Sik', 'Library', 'Main library with over 400,000 books, journals, and digital resources. Study rooms, computer labs, and multimedia facilities available.', 'UTAR Kampar Campus, Main Building', 'Mon-Fri: 8:00 AM - 10:00 PM, Sat-Sun: 9:00 AM - 6:00 PM'),

('Mary KUOK Pick Hoo Library', 'Library', 'Modern library facility with extensive collection of academic resources, group study rooms, and digital learning center.', 'UTAR Sungai Long Campus, Block A', 'Mon-Fri: 8:00 AM - 10:00 PM, Sat-Sun: 9:00 AM - 6:00 PM'),

('Dewan Tun Dr Ling Liong Sik (Grand Hall)', 'Auditorium', 'Main auditorium with seating capacity of 3,000. Used for convocations, ceremonies, and major events.', 'UTAR Kampar Campus', 'By reservation only'),

('Sports Complex Kampar', 'Sports Facility', 'Indoor sports hall, gymnasium, badminton courts, basketball courts, and fitness center. Olympic-size swimming pool.', 'UTAR Kampar Campus, Block F', 'Mon-Fri: 7:00 AM - 10:00 PM, Weekends: 8:00 AM - 8:00 PM'),

('Engineering Laboratories', 'Laboratory', 'State-of-the-art engineering labs including CAD/CAM lab, robotics lab, electronics lab, and materials testing facilities.', 'UTAR Kampar Campus, Block G', 'Mon-Fri: 8:00 AM - 6:00 PM'),

('Clinical Skills & Simulation Centre', 'Medical Facility', 'Medical training facility with simulation mannequins, clinical skills labs, and anatomy labs for medical and health sciences students.', 'UTAR Sungai Long Campus, Medical Block', 'Mon-Fri: 8:00 AM - 6:00 PM'),

('Cafeteria & Food Court', 'Dining', 'Multiple food outlets serving local and international cuisine. Halal and vegetarian options available.', 'Both Campuses - Multiple Locations', 'Mon-Sun: 7:00 AM - 9:00 PM'),

('Student Activity Center', 'Recreation', 'Hub for student clubs and societies. Meeting rooms, performance spaces, and lounge areas.', 'Both Campuses', 'Mon-Fri: 9:00 AM - 10:00 PM, Weekends: 10:00 AM - 8:00 PM');

-- ============================================================================
-- MODULE 4: ACCOMMODATION (4 Options)
-- ============================================================================

INSERT INTO ACCOMMODATION (hostel_name, room_type, monthly_fee, capacity, available_slots, facilities, contact_info) VALUES
('UTAR Kampar Hostel Block A', 'Twin Sharing', 350.00, 2, 50, 'Air-conditioned, attached bathroom, study desk, bed, wardrobe, WiFi, common room, laundry', '+605-468 8800'),
('UTAR Kampar Hostel Block A', 'Single Room', 550.00, 1, 20, 'Air-conditioned, attached bathroom, study desk, bed, wardrobe, WiFi, common room, laundry', '+605-468 8800'),
('UTAR Sungai Long Hostel', 'Twin Sharing', 380.00, 2, 75, 'Air-conditioned, attached bathroom, study desk, bed, wardrobe, WiFi, pantry, laundry', '+603-9086 0289'),
('UTAR Sungai Long Hostel', 'Single Room', 600.00, 1, 25, 'Air-conditioned, attached bathroom, study desk, bed, wardrobe, WiFi, pantry, laundry', '+603-9086 0289');

-- ============================================================================
-- MODULE 4: STUDENT CLUBS (10 Clubs)
-- ============================================================================

INSERT INTO STUDENT_CLUB (club_name, category, description, contact_person, contact_email) VALUES
('UTAR Computer Science Society', 'Academic', 'Organizes hackathons, coding competitions, workshops on latest technologies, and industry talks. Open to all FICT students.', 'Lee Jun Wei', '[email protected]'),

('UTAR Business Club', 'Academic', 'Focuses on entrepreneurship, business case competitions, networking events with industry leaders, and business seminars.', 'Sarah Tan', '[email protected]'),

('UTAR Accounting & Finance Club', 'Academic', 'Professional development activities, CPA/ACCA exam preparation workshops, corporate visits, and accounting competitions.', 'Mohammad Faiz', '[email protected]'),

('UTAR Photography Club', 'Arts & Culture', 'Photography workshops, exhibitions, photo walks, and competitions. All skill levels welcome.', 'Lim Mei Ying', '[email protected]'),

('UTAR Badminton Club', 'Sports', 'Regular training sessions, inter-university competitions, friendly matches. Equipment available for members.', 'Wong Kar Mun', '[email protected]'),

('UTAR Chinese Cultural Society', 'Arts & Culture', 'Promotes Chinese culture through language classes, cultural performances, calligraphy workshops, and festive celebrations.', 'Tan Xiao Ming', '[email protected]'),

('UTAR Environmental Club', 'Community Service', 'Environmental awareness campaigns, recycling initiatives, tree planting, beach cleanups, and sustainability projects.', 'Nurul Ain', '[email protected]'),

('UTAR Debate & Public Speaking Society', 'Academic', 'Debate training, public speaking workshops, inter-university debate competitions, and mock parliament sessions.', 'Rajesh Kumar', '[email protected]'),

('UTAR Robotics & Maker Club', 'Academic', 'Robotics competitions, Arduino/Raspberry Pi workshops, 3D printing projects, and tech innovation challenges.', 'Chong Wei Lun', '[email protected]'),

('UTAR Volunteer Club', 'Community Service', 'Organizes community outreach programs, charity drives, visits to orphanages and elderly homes, and disaster relief efforts.', 'Siti Fatimah', '[email protected]');

-- ============================================================================
-- MODULE 4: CAMPUS EVENTS (8 Events for 2025)
-- ============================================================================

INSERT INTO EVENT (event_name, event_type, event_date, location, description, organizer) VALUES
('UTAR Orientation Week 2025', 'Academic', '2025-01-06', 'Both Campuses', 'Welcome program for new students. Campus tours, faculty introductions, ice-breaking activities, and registration assistance.', 'Student Affairs Division'),

('UTAR Career Fair 2025', 'Career', '2025-03-15', 'Kampar Campus - Grand Hall', 'Major career fair with 100+ companies. Job opportunities, internships, career talks, and resume clinics.', 'Career Development Centre'),

('UTAR Convocation 2025', 'Ceremony', '2025-10-18', 'Kampar Campus - Grand Hall', 'Graduation ceremony for Class of 2025. Conferment of degrees and awards.', 'Registry Department'),

('Innovation & Technology Expo', 'Academic', '2025-04-20', 'Both Campuses', 'Showcase of student projects, research posters, and innovative solutions. Industry judging panel.', 'FICT & FEGT'),

('UTAR Sports Carnival', 'Sports', '2025-05-25', 'Kampar Campus - Sports Complex', 'Inter-faculty sports competition. Events include badminton, basketball, futsal, and track & field.', 'Sports & Recreation Unit'),

('Cultural Night 2025', 'Arts & Culture', '2025-08-15', 'Sungai Long Campus', 'Multicultural celebration with performances, food stalls, and cultural exhibitions from various student societies.', 'Student Union'),

('Entrepreneurship Summit', 'Career', '2025-06-10', 'Kampar Campus', 'Talks by successful entrepreneurs, startup pitching competition, networking sessions, and business plan workshops.', 'FBF & Business Club'),

('Blood Donation Drive', 'Community Service', '2025-07-20', 'Both Campuses', 'Organized in collaboration with National Blood Bank. Free health screening and blood donation.', 'UTAR Volunteer Club');

-- ============================================================================
-- MODULE 6: FAQ (12 Common Questions)
-- ============================================================================

INSERT INTO FAQ (category, question, answer, view_count) VALUES
('General', 'What programs does UTAR offer?', 'UTAR offers over 110 programs across 10 faculties in various fields including Engineering, Computing, Business, Science, Arts, Medicine, and more at Diploma, Bachelor, Master, and PhD levels.', 150),

('Admission', 'What are the admission requirements for undergraduate programs?', 'General requirements include STPM (min CGPA 2.00), A-Level (min 2 passes), UEC (min 5Bs), Foundation/Matriculation (min CGPA 2.00), or Diploma (min CGPA 2.50). Specific programs may have additional requirements. Credit in SPM Mathematics and English is typically required.', 230),

('Admission', 'How do I apply for admission?', 'Apply online through study.utar.edu.my. Create an account, select your program, fill in personal details, upload required documents (IC, certificates, passport photos), and pay RM 50 application fee. Application deadlines vary by intake.', 180),

('Admission', 'When are the intakes?', 'UTAR has 3 intakes per year: January (Trimester 1), May (Trimester 2), and September (Trimester 3). Application periods typically open 3 months before each intake.', 200),

('Fees', 'How much are the tuition fees?', 'Tuition fees vary by program. Arts/Business programs: ~RM 6,500-6,900 per trimester. Computing/Science: ~RM 7,000-7,500 per trimester. Engineering (4 years): ~RM 8,200-8,400 per trimester. Total program costs range from RM 40,000 to RM 98,000 for 3-4 year programs.', 320),

('Fees', 'Are there payment plans available?', 'Yes, UTAR offers installment payment plans with no interest. Pay tuition in monthly installments throughout the trimester. RM 200 processing fee applies. Apply at the Finance Office before semester starts.', 145),

('Scholarship', 'What scholarships are available?', 'UTAR offers merit-based scholarships (Academic Excellence: 100% waiver, High Achievers: 50% waiver), need-based scholarships (Education Foundation), and specialized scholarships (Women in STEM, Industry Partner). External scholarships include PTPTN loans and MARA financing.', 275),

('Scholarship', 'How do I apply for scholarships?', 'Merit scholarships (Academic Excellence, High Achievers) are automatically considered upon admission. For need-based scholarships, submit application form with supporting documents (income proof, transcripts) through the Student Affairs portal. Deadlines vary by scholarship type.', 165),

('Campus Life', 'What facilities are available on campus?', 'UTAR campuses feature modern libraries, sports complexes with swimming pools, engineering and science labs, medical simulation centers, cafeterias, student activity centers, auditoriums, and on-campus hostels. WiFi is available throughout campus.', 190),

('Campus Life', 'Is accommodation available?', 'Yes, both Kampar and Sungai Long campuses offer on-campus hostel accommodation. Twin-sharing rooms: RM 350-380/month. Single rooms: RM 550-600/month. All rooms are air-conditioned with attached bathrooms, study desks, and WiFi. Limited spaces available - apply early.', 210),

('Campus Life', 'What student clubs can I join?', 'UTAR has 60+ clubs including academic clubs (Computer Science Society, Business Club), sports clubs (Badminton, Basketball), cultural societies (Chinese Cultural Society), and community service clubs (Volunteer Club, Environmental Club). Join during orientation or contact the Student Union.', 95),

('General', 'Where is UTAR located?', 'UTAR has two main campuses: Kampar Campus in Perak (1,300 acres, main programs: Science, Engineering, Business, ICT) and Sungai Long Campus in Kajang, Selangor (programs: Medicine, Engineering, Accountancy, Creative Industries). Both are accessible by public transport and private vehicles.', 175);

-- ============================================================================
-- MODULE 6: USERS (Sample users for testing)
-- ============================================================================

INSERT INTO Users (username, email, user_type, last_login) VALUES
('tanweijian', 'tanweijian@gmail.com', 'Applicant', '2024-11-12 14:30:00'),
('nurulaisyah', 'nurulaisyah@gmail.', 'Applicant', '2024-11-11 09:15:00'),
('limkaixuan', 'limkaixuan@gmail.com', 'Prospective Student', '2024-11-10 16:45:00'),
('admin_utar', 'admin_utar@gmail.com', 'Admin', '2024-11-12 08:00:00');

-- ============================================================================
-- DATA VERIFICATION QUERIES
-- ============================================================================

-- Quick summary of inserted data
SELECT 'FACULTIES' as Category, COUNT(*) as Count FROM FACULTY
UNION ALL SELECT 'PROGRAMS', COUNT(*) FROM PROGRAM
UNION ALL SELECT 'FACULTY MEMBERS', COUNT(*) FROM FACULTY_MEMBER
UNION ALL SELECT 'SUBJECTS', COUNT(*) FROM SUBJECT
UNION ALL SELECT 'PROGRAM-SUBJECT MAPPINGS', COUNT(*) FROM PROGRAM_SUBJECT
UNION ALL SELECT 'ADMISSION REQUIREMENTS', COUNT(*) FROM ADMISSION_REQUIREMENT
UNION ALL SELECT 'TUITION FEES', COUNT(*) FROM TUITION_FEE
UNION ALL SELECT 'SCHOLARSHIPS', COUNT(*) FROM SCHOLARSHIP
UNION ALL SELECT 'FINANCIAL AID OPTIONS', COUNT(*) FROM FINANCIAL_AID
UNION ALL SELECT 'CAMPUS FACILITIES', COUNT(*) FROM CAMPUS_FACILITY
UNION ALL SELECT 'ACCOMMODATIONS', COUNT(*) FROM ACCOMMODATION
UNION ALL SELECT 'STUDENT CLUBS', COUNT(*) FROM STUDENT_CLUB
UNION ALL SELECT 'CAMPUS EVENTS', COUNT(*) FROM EVENT
UNION ALL SELECT 'FAQs', COUNT(*) FROM FAQ
UNION ALL SELECT 'USERS', COUNT(*) FROM Users
UNION ALL SELECT 'APPLICANTS', COUNT(*) FROM APPLICANT
UNION ALL SELECT 'APPLICATIONS', COUNT(*) FROM APPLICATION;

-- Verify subjects per faculty
SELECT 
    'FAM Subjects (1-20)' as Faculty,
    COUNT(*) as Subject_Count
FROM SUBJECT WHERE subject_id BETWEEN 1 AND 20
UNION ALL
SELECT 'FAS Subjects (21-40)', COUNT(*) FROM SUBJECT WHERE subject_id BETWEEN 21 AND 40
UNION ALL
SELECT 'FBF Subjects (41-60)', COUNT(*) FROM SUBJECT WHERE subject_id BETWEEN 41 AND 60
UNION ALL
SELECT 'FICT Subjects (61-80)', COUNT(*) FROM SUBJECT WHERE subject_id BETWEEN 61 AND 80
UNION ALL
SELECT 'FSc Subjects (81-100)', COUNT(*) FROM SUBJECT WHERE subject_id BETWEEN 81 AND 100
UNION ALL
SELECT 'FEGT Subjects (101-120)', COUNT(*) FROM SUBJECT WHERE subject_id BETWEEN 101 AND 120;

-- Verify program-subject mappings
SELECT 
    p.program_id,
    p.program_name,
    COUNT(ps.subject_id) as subjects_assigned
FROM PROGRAM p
LEFT JOIN PROGRAM_SUBJECT ps ON p.program_id = ps.program_id
GROUP BY p.program_id, p.program_name
ORDER BY p.program_id;
