from backend.backend_functions import get_player
from backend.helper_functions import rows_to_dicts, is_ident
from backend.sql_connection import cursor

#---- TRAVEL FUNCTIONS ----#

def list_airports(player_id, max_distance_km):
    query = """
    SELECT 
        airport.ident,
        airport.name,
        airport.latitude_deg,
        airport.longitude_deg,
        airport.distance_km,
        ROUND((POWER(airport.distance_km, 1.25) * 0.2), 2) AS travel_price
    FROM (
        SELECT
        airport.ident,
        airport.name,
        airport.latitude_deg,
        airport.longitude_deg,
        airport.type,
        airport.scheduled_service,
        ROUND((
            6371 * ACOS(
                COS(RADIANS(current_airport.latitude_deg)) 
                * COS(RADIANS(airport.latitude_deg)) 
                * COS(RADIANS(airport.longitude_deg) - RADIANS(current_airport.longitude_deg)) 
                + SIN(RADIANS(current_airport.latitude_deg)) 
                * SIN(RADIANS(airport.latitude_deg))
            )
        ), 2) AS distance_km
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

    results = rows_to_dicts(cursor.fetchall())

    return results

def fetch_travel_details(player_id, arr_ident):
    # Find out if player has enough money to travel
    cursor.execute(
        """                
        SELECT 
            airport.ident,
            airport.distance_km,
            ROUND((POWER(airport.distance_km, 1.25) * 0.2), 2) AS travel_price
        FROM (
            SELECT
            airport.ident,
            airport.type,
            airport.scheduled_service,
            ROUND((
                6371 * ACOS(
                    COS(RADIANS(current_airport.latitude_deg)) 
                    * COS(RADIANS(airport.latitude_deg)) 
                    * COS(RADIANS(airport.longitude_deg) - RADIANS(current_airport.longitude_deg)) 
                    + SIN(RADIANS(current_airport.latitude_deg)) 
                    * SIN(RADIANS(airport.latitude_deg))
                )
            ), 2) AS distance_km
            FROM airport
            INNER JOIN player ON player.id = %s
            INNER JOIN airport AS current_airport ON player.location = current_airport.ident
            WHERE airport.ident = %s
        ) AS airport
        WHERE
            airport.ident = %s
            AND airport.type = 'large_airport'
            AND airport.scheduled_service = 'yes';
        """
        , (player_id, arr_ident, arr_ident))
    results = rows_to_dicts(cursor.fetchall())
    return results

def travel(player_id, arr_ident, travel_price):
    cursor.execute(
        """
        UPDATE player
        SET location = %s, balance = balance - %s
        WHERE id = %s
        """,
        (arr_ident, travel_price, player_id)
    )