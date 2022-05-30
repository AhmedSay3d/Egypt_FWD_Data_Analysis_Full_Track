/* Show % of each Playlist in our store*/
WITH t1 AS (
	SELECT pl.Name AS Playlist, COUNT(t.Name) AS TrackCount
		FROM Track AS t
		JOIN PlaylistTrack AS plt
		ON t.TrackId = plt.TrackId
		JOIN Playlist AS pl
		ON plt.PlaylistId = pl.PlaylistId
		GROUP BY 1
		)
SELECT t1.Playlist, 
		/*calculating precentage rounded to 2 decimal places*/
		ROUND(
			CAST(t1.TrackCount AS FLOAT)
				/(SELECT SUM(t1.TrackCount)	FROM t1)*100
		,2) AS Precentage
		/*End of calculation*/
	FROM t1
	ORDER BY 2 DESC