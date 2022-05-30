WITH t1 As (
		/*Table contains the total_profit of each track*/
		SELECT TrackId, SUM(UnitPrice*Quantity) As Total_Track_Profit
		FROM InvoiceLine
		GROUP BY 1),
	t2 AS (
		/*Table contains all tracks in each genre*/
		SELECT g.Name As Genre,t.Name As Track, t.TrackId
		FROM Genre As g
		JOIN Track As t
		ON t.GenreId = g.GenreId
		GROUP BY 1,2)
/*Calculate the total profit of each genre*/
SELECT t2.Genre, 
		ROUND(SUM(t1.Total_Track_Profit),2) AS Total_Genre_Profit
	FROM t2
	JOIN t1
	ON t2.TrackId = t1.TrackId
	GROUP BY 1
	ORDER BY 2 DESC