INSERT INTO Category (mainCategory, subCategory, catNotes) VALUES
('Furniture', 'Chair', 'Seating furniture'),
('Furniture', 'Table', 'Flat-surface furniture'),
('Electronics', 'Laptop', 'Portable computers'),
('Electronics', 'Smartphone', 'Mobile phones with smart features'),
('Clothing', 'Shirt', 'Upper-body wear');

-- Need to edit paths to include resources folder for images - refer to example python script to connect

INSERT INTO Item (iDescription, photo, color, isNew, hasPieces, material, mainCategory, subCategory) VALUES
('Office Chair', 'resources/officechair.jpeg', 'Black', TRUE, FALSE, 'Plastic', 'Furniture', 'Chair'),
('Dining Table', 'resources/diningtable.jpeg', 'Brown', TRUE, FALSE, 'Wood', 'Furniture', 'Table'),
('Gaming Laptop', 'resources/gaminglaptop.jpeg', 'Black', TRUE, FALSE, 'Metal', 'Electronics', 'Laptop'),
('iPhone', 'resources/iphone.jpeg', 'Silver', TRUE, FALSE, 'Glass', 'Electronics', 'Smartphone'),
('T-shirt', 'resources/tshirt.jpeg', 'Blue', TRUE, FALSE, 'Cotton', 'Clothing', 'Shirt');

INSERT INTO Person (userName, password, fname, lname, email) VALUES
('jdoe', 'hashed_password_1', 'John', 'Doe', 'john.doe@example.com'),
('asmith', 'hashed_password_2', 'Alice', 'Smith', 'alice.smith@example.com'),
('bwong', 'hashed_password_3', 'Brian', 'Wong', 'brian.wong@example.com'),
('ckim', 'hashed_password_4', 'Chris', 'Kim', 'chris.kim@example.com'),
('djohnson', 'hashed_password_5', 'Diana', 'Johnson', 'diana.johnson@example.com');

INSERT INTO PersonPhone (userName, phone) VALUES
('jdoe', '555-1234'),
('asmith', '555-5678'),
('bwong', '555-8765'),
('ckim', '555-4321'),
('djohnson', '555-6789');

INSERT INTO DonatedBy (ItemID, userName, donateDate) VALUES
(1, 'jdoe', '2024-01-01'),
(2, 'asmith', '2024-01-02'),
(3, 'bwong', '2024-01-03'),
(4, 'ckim', '2024-01-04'),
(5, 'djohnson', '2024-01-05');

INSERT INTO Role (roleID, rDescription) VALUES
('staff', 'Staff Member'),
('volunteer', 'Volunteer Worker'),
('admin', 'Administrator'),
('client', 'Client'),
('donor', 'Donor');

INSERT INTO Act (userName, roleID) VALUES
('jdoe', 'staff'),
('asmith', 'volunteer'),
('bwong', 'admin'),
('ckim', 'client'),
('djohnson', 'donor');

INSERT INTO Location (roomNum, shelfNum, shelf, shelfDescription) VALUES
(1, 1, 'A1', 'Top shelf in Room 1'),
(1, 2, 'A2', 'Middle shelf in Room 1'),
(2, 1, 'B1', 'Top shelf in Room 2'),
(2, 2, 'B2', 'Middle shelf in Room 2'),
(3, 1, 'C1', 'Top shelf in Room 3');

INSERT INTO Piece (ItemID, pieceNum, pDescription, length, width, height, roomNum, shelfNum, pNotes) VALUES
(1, 1, 'Chair Back', 20, 15, 5, 1, 1, 'Back piece of the chair'),
(1, 2, 'Chair Leg', 30, 5, 5, 1, 2, 'Leg piece of the chair'),
(2, 1, 'Table Top', 60, 30, 5, 2, 1, 'Top piece of the table'),
(2, 2, 'Table Leg', 40, 5, 5, 2, 2, 'Leg piece of the table'),
(3, 1, 'Laptop Cover', 15, 10, 1, 3, 1, 'Cover piece of the laptop');

INSERT INTO Ordered (orderDate, orderNotes, supervisor, client) VALUES
('2024-01-06', 'Urgent delivery', 'jdoe', 'ckim'),
('2024-01-07', 'Regular order', 'asmith', 'djohnson'),
('2024-01-08', 'Priority order', 'bwong', 'jdoe'),
('2024-01-09', 'Bulk order', 'ckim', 'asmith'),
('2024-01-10', 'Special request', 'djohnson', 'bwong');


INSERT INTO ItemIn (ItemID, orderID, found) VALUES
(1, 1, TRUE),
(2, 2, FALSE),
(3, 3, TRUE),
(4, 4, TRUE),
(5, 5, FALSE);


INSERT INTO Delivered (userName, orderID, status, date) VALUES
('jdoe', 1, 'Delivered', '2024-01-11'),
('asmith', 2, 'In Progress', '2024-01-12'),
('bwong', 3, 'Delivered', '2024-01-13'),
('ckim', 4, 'Pending', '2024-01-14'),
('djohnson', 5, 'Delivered', '2024-01-15');

