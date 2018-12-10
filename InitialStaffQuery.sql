# Create a new user with id: 000001 and pass: password
INSERT INTO users (ID, category, pword) VALUES ('000001', 'Staff', '$2b$12$syivdenDKojWCsPxTU/q2ON2zI6BUBi6XnWXF50rclVTWklreAOci')
# Put the user into the staff table with basic informatio
INSERT INTO staff (id, fName, lName, phone, email, street, city, state, zip) VALUES ('000001', 'Bobby', 'Baylor', '2547103871', 'Bobby_Baylor@baylor.edu', 'One Bear Place #97356', 'Waco', 'TX', '76798');