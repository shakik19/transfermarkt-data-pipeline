SELECT
  dc.club_id,
  dc.name AS club_name,
  dgi.season,
  fcg.own_manager_name AS manager,
  COUNT(1) AS matches,
  SUM(fcg.own_goals) AS goals_scored,
  SUM(fcg.opponent_goals) AS goals_conceded,
  SUM(CASE WHEN fcg.opponent_goals = 0 THEN 1 ELSE 0 END) AS clean_sheets,
  SUM(CASE WHEN fcg.is_win = 1 THEN 1 ELSE 0 END) AS wins,
  SUM(CASE WHEN fcg.is_win = 0 THEN 1 ELSE 0 END) AS draws,
  SUM(CASE WHEN fcg.is_win = -1 THEN 1 ELSE 0 END) AS losses,
  SUM(CASE WHEN dgi.round != "final" AND fcg.game_location = "home" AND fcg.is_win = 1 THEN 1 ELSE 0 END) AS home_wins,
  SUM(CASE WHEN dgi.round != "final" AND fcg.game_location = "home" AND fcg.is_win = -1 THEN 1 ELSE 0 END) AS home_losses,
  SUM(CASE WHEN dgi.round != "final" AND fcg.game_location = "away" AND fcg.is_win = 1 THEN 1 ELSE 0 END) AS away_wins,
  SUM(CASE WHEN dgi.round != "final" AND fcg.game_location = "away" AND fcg.is_win = -1 THEN 1 ELSE 0 END) AS away_losses,
  AVG(CASE WHEN fcg.game_location = "home" THEN dgi.attendance END) AS avg_home_attendance,
  AVG(CASE WHEN fcg.game_location = "away" THEN dgi.attendance END) AS avg_away_attendance
FROM
  {{ ref("fact_club_games") }} fcg
  LEFT JOIN {{ ref("dim_game_info") }} dgi USING(game_id)
  LEFT JOIN {{ ref("dim_clubs") }} dc ON dc.club_id = fcg.own_id
GROUP BY
  1, 2, 3, 4