from geopy.distance import geodesic

from backend.sql_connection import cursor


#---- HELPER FUNCTIONS ----#

def _rows_to_dicts(rows):
    cols = [desc[0] for desc in cursor.description] if cursor.description else []
    return [dict(zip(cols, row)) for row in rows]

#---- TRAVEL FUNCTIONS ----#

def list_airports(player_id, max_distance_km):
    query = """
    SELECT 
        airport.ident,
        airport.name,
        airport.latitude_deg,
        airport.longitude_deg,
        airport.distance_km,
        (POWER(airport.distance_km, 1.25) * 0.2) AS travel_price
    FROM (
        SELECT
        airport.ident,
        airport.name,
        airport.latitude_deg,
        airport.longitude_deg,
        airport.type,
        airport.scheduled_service,
        current_airport.latitude_deg AS player_latitude_deg,
        current_airport.longitude_deg AS player_longitude_deg,
        (
            6371 * ACOS(
                COS(RADIANS(current_airport.latitude_deg)) 
                * COS(RADIANS(airport.latitude_deg)) 
                * COS(RADIANS(airport.longitude_deg) - RADIANS(current_airport.longitude_deg)) 
                + SIN(RADIANS(current_airport.latitude_deg)) 
                * SIN(RADIANS(airport.latitude_deg))
            )
        ) AS distance_km,
        player.balance AS player_balance
        FROM airport
        INNER JOIN player ON player.id = %s
        INNER JOIN airport AS current_airport ON player.location = current_airport.ident
    ) AS airport
    WHERE
        (%s IS NULL OR airport.distance_km <= %s)
        AND airport.type = 'large_airport'
        AND airport.scheduled_service = 'yes'
    ORDER BY airport.distance_km;
    """

    params = (player_id, max_distance_km, max_distance_km)

    cursor.execute(query, params)

    results = _rows_to_dicts(cursor.fetchall())

    return results
