/* Show how many Tracks in each Playlist*/
SELECT pl.Name AS Playlist, COUNT(t.Name) AS TrackCount
	FROM Track AS t
	JOIN PlaylistTrack AS plt
	ON t.TrackId = plt.TrackId
	JOIN Playlist AS pl
	ON plt.PlaylistId = pl.PlaylistId
	GROUP BY 1
	ORDER BY 2 DESC