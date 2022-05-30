WITH t2 AS (
	WITH t1 AS (
		SELECT  c.Country,g.Name AS Genre, COUNT(*) AS Count
			FROM Customer AS c
			JOIN Invoice AS i
			ON i.CustomerId = c.CustomerId
			JOIN InvoiceLine AS il
			ON il.InvoiceId = i.InvoiceId
			JOIN Track AS t
			ON il.TrackId = t.TrackId
			JOIN Genre AS g
			ON t.GenreId = g.GenreId
			GROUP BY 1, 2)
			
	SELECT t1.Country, MAX(t1.Count) AS Max_Purchases
		FROM t1
		GROUP BY 1),
		
	t3 AS (
		SELECT  c.Country,g.Name AS Genre, COUNT(*) AS Purchases
			FROM Customer AS c
			JOIN Invoice AS i
			ON i.CustomerId = c.CustomerId
			JOIN InvoiceLine AS il
			ON il.InvoiceId = i.InvoiceId
			JOIN Track AS t
			ON il.TrackId = t.TrackId
			JOIN Genre AS g
			ON t.GenreId = g.GenreId
			GROUP BY 1,2)
		
SELECT t3.Country, t3.Genre, t3.Purchases
	FROM t3
	JOIN t2
	ON t3.Country = t2.Country AND t3.Purchases = t2.Max_Purchases