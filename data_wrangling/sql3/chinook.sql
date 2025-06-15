-- CREATE VIEW Q1 AS
-- SELECT InvoiceId, InvoiceDate, Total FROM invoices ORDER BY InvoiceDate DESC LIMIT 10

-- CREATE VIEW Q2 AS 
-- SELECT FirstName || " " || LastName AS Name, Address, City, State, PostalCode FROM customers WHERE Country='USA'
-- -- https://a-gentle-introduction-to-sql.readthedocs.io/en/latest/part2/concatenate.html

-- CREATE VIEW Q3 AS
-- SELECT Name, Composer FROM tracks WHERE Composer REGEXP 'Samuel Rosa'

-- CREATE VIEW Q4 AS 
-- SELECT Country, count(*) FROM customers GROUP BY Country
-- -- https://www.sqlitetutorial.net/sqlite-count-function/

-- CREATE VIEW Q5 AS 
-- SELECT Name, round(CAST(Milliseconds as REAL)/(60*1000), 1) as "Duration (min.)", round(CAST(Bytes as REAL)/1024, 0) as "Size (KB)" FROM tracks
-- -- https://datacomy.com/sql/sqlite/division/
-- -- https://www.w3resource.com/sqlite/core-functions-round.php

-- CREATE VIEW Q6 AS
-- SELECT count(*) AS "No. of '(Live)' tracks" FROM tracks WHERE Name REGEXP "\(Live\)"

-- CREATE VIEW Q7 AS
-- SELECT FirstName || " " || LastName AS Name, coalesce(Fax, Phone) AS Number, iif(Fax IS NOT NULL, 'Fax', 'Phone') as Type FROM customers
-- https://www.sqlitetutorial.net/sqlite-functions/sqlite-iif/

-- CREATE VIEW Q8 AS
-- SELECT EmployeeId, FirstName || " " || LastName AS Name, CAST(substr(timediff(HireDate, BirthDate), 2, 4) AS INT) AS "Age at hiring", Email FROM employees
-- https://www.sqlite.org/lang_datefunc.html
-- https://www.sqlitetutorial.net/sqlite-functions/sqlite-substr/

-- CREATE VIEW Q9 AS
-- SELECT BillingCountry, count(*) AS num_orders, round(sum(Total)/count(*), 2) as ave_cost FROM invoices GROUP BY BillingCountry

-- CREATE VIEW Q10 AS
-- SELECT (CAST(count(*) AS REAL)/(SELECT count(*) FROM artists WHERE Name REGEXP 'Feat\.')) as Percentage FROM artists

-- CREATE VIEW Q11 AS
-- SELECT substr(Name, 0, 2) as Alphabet, count(*) as "Count" FROM artists GROUP BY substr(Name, 0, 2)

-- CREATE VIEW Q12 AS
-- SELECT Name, round(CAST(Milliseconds as REAL)/(60*1000), 1) as "Duration (min.)", round(CAST(Bytes as REAL)/1024, 0) as "Size (KB)", Type FROM tracks INNER JOIN media_types ON tracks.MediaTypeId=media_types.MediaTypeId;
-- ALTER TABLE media_types RENAME COLUMN Name TO Type
-- https://stackoverflow.com/questions/805363/how-do-i-rename-a-column-in-an-sqlite-database-table

-- CREATE VIEW Q13 AS
-- SELECT Type AS "Genre Type", count(*) AS num_tracks FROM tracks INNER JOIN genres ON tracks.GenreId=genres.GenreId GROUP BY Type ORDER BY count(*) DESC
-- ALTER TABLE genres RENAME COLUMN Name TO Type

-- CREATE VIEW Q14 AS
-- SELECT
-- 	Name AS TrackName, AlbumTitle, ArtistName
-- FROM tracks
-- INNER JOIN albums ON tracks.AlbumId=albums.AlbumId
-- INNER JOIN artists ON albums.ArtistId=artists.ArtistId
-- ALTER TABLE albums RENAME COLUMN Title TO AlbumTitle
-- ALTER TABLE artists RENAME COLUMN Name TO ArtistName

-- CREATE VIEW Q15 AS
-- SELECT
-- 	FirstName || " " || LastName AS Name, Address, sum(Total)
-- FROM customers
-- INNER JOIN invoices ON customers.CustomerId=invoices.CustomerId
-- GROUP BY Name


-- DROP VIEW IF EXISTS Q1;