SELECT DISTINCT user.first_name, user.last_name
FROM user
LEFT JOIN reservation ON user.user_id = reservation.user_id
WHERE reservation.status != 'paid' OR reservation.user_id IS NULL;
