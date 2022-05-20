CREATE SCHEMA spotimonitor;

CREATE TABLE spotimonitor.artist(
    id VARCHAR(50) PRIMARY KEY,
    artist_name VARCHAR(50)
);

-- could be normalized into track & track-artist
CREATE TABLE spotimonitor.track(
    id VARCHAR(50) PRIMARY KEY,
    danceability NUMERIC,
    energy NUMERIC,
    track_key INTEGER,
    loudness NUMERIC,
    mode INTEGER,
    speechiness NUMERIC,
    acousticness NUMERIC,
    instrumentalness NUMERIC,
    liveness NUMERIC,
    valence NUMERIC,
    tempo NUMERIC,
    duration_ms INTEGER,
    id_artist VARCHAR(50) REFERENCES spotimonitor.artist(id)
);

CREATE TABLE spotimonitor.top_tracks (
    id VARCHAR(50) REFERENCES spotimonitor.track(id),
    date_added TIMESTAMP not null default CURRENT_TIMESTAMP,
    popularity INT,
    time_range VARCHAR(20)
);

CREATE TABLE spotimonitor.top_artists(
    id VARCHAR(50) REFERENCES spotimonitor.artist,
    date_added TIMESTAMP not null default CURRENT_TIMESTAMP,
    popularity INT
);

CREATE TABLE spotimonitor.track_artist(
    track_id VARCHAR(50),
    artist_id VARCHAR(50)
);

-- CREATE TABLE spotimonitor.artist(
--     id VARCHAR(50) PRIMARY KEY,
--     artist_name VARCHAR(50),
--     genre VARCHAR(50)
-- );

CREATE TABLE spotimonitor.genre(
    genre VARCHAR(50) PRIMARY KEY
);


CREATE TABLE spotimonitor.artist_genre(
    id VARCHAR(50) REFERENCES spotimonitor.artist(id),
    genre VARCHAR(50) REFERENCES spotimonitor.genre(genre)
);


