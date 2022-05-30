SELECT a.Title AS Album, SUM(il.Quantity*il.UnitPrice) AS Total_Profit
	FROM Album AS a
	JOIN Track AS t
	ON t.AlbumId = a.AlbumId
	JOIN InvoiceLine AS il
	ON il.TrackId = t.TrackId
	GROUP BY 1
	ORDER BY 2 DESC
	LIMIT 20