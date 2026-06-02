-- ================================================
-- Database: hotel_bookings.db
-- Tables: bookings, customers, reservations
-- ================================================

-- Q1: Which hotel type has the higher cancellation rate?
-- Business context: Understanding which hotel format struggles more with cancellations helps management apply targeted deposit policies and overbooking strategies to protect revenue.

SELECT 
    hotel,
    COUNT(*) AS total_bookings,
    SUM(is_canceled) AS total_cancellations,
    ROUND(SUM(is_canceled) * 100.0 / COUNT(*), 2) AS cancellation_rate_pct
FROM bookings
GROUP BY hotel
ORDER BY cancellation_rate_pct DESC;

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Q2: How has average daily rate changed year over year by hotel type?
-- Business context: Tracking ADR trends reveals pricing power and demand growth. Declining ADR may indicate increased competition or weaker demand requiring promotional intervention.

SELECT 
    hotel,
    arrival_date_year,
    COUNT(*) AS total_bookings,
    ROUND(AVG(adr), 2) AS avg_daily_rate
FROM bookings
GROUP BY hotel, arrival_date_year
ORDER BY hotel, arrival_date_year;
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Q3: Which market segment loses the most revenue due to cancellations?
-- Business context: Identifying which segments drive the most lost revenue helps management prioritize where to tighten deposit policies, improve confirmation processes, or apply overbooking strategies.

SELECT 
    r.market_segment,
    COUNT(*) AS total_bookings,
    SUM(b.is_canceled) AS total_cancellations,
    ROUND(SUM(b.is_canceled) * 100.0 / COUNT(*), 2) AS cancellation_rate_pct,
    ROUND(AVG(b.adr), 2) AS avg_daily_rate,
    ROUND(SUM(CASE WHEN b.is_canceled = 1 
        THEN b.adr * (b.stays_in_weekend_nights + b.stays_in_week_nights) 
        ELSE 0 END), 2) AS lost_revenue
FROM bookings b
JOIN reservations r ON b.booking_id = r.booking_id
GROUP BY r.market_segment
ORDER BY lost_revenue DESC;
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
-- Q4: Top 10 countries by bookings with cancellation rate and ADR
-- Business context: Understanding which markets generate the most bookings and which have problematic cancellation rates helps prioritizemarket-specific pricing and deposit policies.

SELECT 
    c.country,
    COUNT(*) AS total_bookings,
    SUM(b.is_canceled) AS total_cancellations,
    ROUND(SUM(b.is_canceled) * 100.0 / COUNT(*), 2) AS cancellation_rate_pct,
    ROUND(AVG(b.adr), 2) AS avg_daily_rate
FROM bookings b
JOIN customers c ON b.booking_id = c.booking_id
WHERE c.country IS NOT NULL
GROUP BY c.country
ORDER BY total_bookings DESC
LIMIT 10;          
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Q5: Which deposit type has the highest cancellation rate?
-- Business context: Understanding the relationship between deposit policy and cancellation behaviour helps management design smarter deposit requirements that reduce cancellations without deterring bookings.

SELECT 
    r.deposit_type,
    COUNT(*) AS total_bookings,
    SUM(b.is_canceled) AS total_cancellations,
    ROUND(SUM(b.is_canceled) * 100.0 / COUNT(*), 2) AS cancellation_rate_pct
FROM bookings b
JOIN reservations r ON b.booking_id = r.booking_id
GROUP BY r.deposit_type
ORDER BY cancellation_rate_pct DESC;
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Q6: Monthly booking trends across 2015-2017
-- Business context: Identifying seasonal patterns in bookings, cancellations and ADR helps management plan staffing, inventory, and promotional strategies around peak and low demand periods.

SELECT 
    arrival_date_year,
    arrival_date_month,
    CASE arrival_date_month
        WHEN 'January' THEN 1 WHEN 'February' THEN 2
        WHEN 'March' THEN 3 WHEN 'April' THEN 4
        WHEN 'May' THEN 5 WHEN 'June' THEN 6
        WHEN 'July' THEN 7 WHEN 'August' THEN 8
        WHEN 'September' THEN 9 WHEN 'October' THEN 10
        WHEN 'November' THEN 11 WHEN 'December' THEN 12
    END AS month_num,
    COUNT(*) AS total_bookings,
    SUM(is_canceled) AS total_cancellations,
    ROUND(SUM(is_canceled) * 100.0 / COUNT(*), 2) AS cancellation_rate_pct,
    ROUND(AVG(adr), 2) AS avg_daily_rate,
    SUM(COUNT(*)) OVER (
        PARTITION BY arrival_date_year
        ORDER BY CASE arrival_date_month
            WHEN 'January' THEN 1 WHEN 'February' THEN 2
            WHEN 'March' THEN 3 WHEN 'April' THEN 4
            WHEN 'May' THEN 5 WHEN 'June' THEN 6
            WHEN 'July' THEN 7 WHEN 'August' THEN 8
            WHEN 'September' THEN 9 WHEN 'October' THEN 10
            WHEN 'November' THEN 11 WHEN 'December' THEN 12
        END
    ) AS running_total_bookings
FROM bookings
GROUP BY arrival_date_year, arrival_date_month
ORDER BY arrival_date_year, month_num;
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Q7: Does booking lead time affect cancellation rate?
-- Business context: Understanding whether advance bookings cancel more helps management apply different deposit policies based on how far in advance a booking is made — protecting revenue from high-risk long lead-time reservations.

SELECT 
    CASE 
        WHEN lead_time = 0 THEN '1. Same day'
        WHEN lead_time <= 7 THEN '2. 1-7 days'
        WHEN lead_time <= 30 THEN '3. 8-30 days'
        WHEN lead_time <= 90 THEN '4. 31-90 days'
        WHEN lead_time <= 180 THEN '5. 91-180 days'
        ELSE '6. 180+ days'
    END AS lead_time_bucket,
    COUNT(*) AS total_bookings,
    SUM(is_canceled) AS total_cancellations,
    ROUND(SUM(is_canceled) * 100.0 / COUNT(*), 2) AS cancellation_rate_pct,
    ROUND(AVG(adr), 2) AS avg_daily_rate
FROM bookings
GROUP BY lead_time_bucket
ORDER BY cancellation_rate_pct DESC;
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Q8: Do repeat guests behave differently from new guests?
-- Business context: Comparing repeat vs new guest behaviour quantifies the value of customer loyalty. If repeat guests cancel less and spend more, loyalty programs deliver measurable ROI.

WITH guest_stats AS (
    SELECT 
        c.is_repeated_guest,
        COUNT(*) AS total_bookings,
        SUM(b.is_canceled) AS total_cancellations,
        ROUND(SUM(b.is_canceled) * 100.0 / COUNT(*), 2) AS cancellation_rate_pct,
        ROUND(AVG(b.adr), 2) AS avg_daily_rate,
        ROUND(AVG(b.total_of_special_requests), 2) AS avg_special_requests
    FROM bookings b
    JOIN customers c ON b.booking_id = c.booking_id
    GROUP BY c.is_repeated_guest
)
SELECT 
    CASE WHEN is_repeated_guest = 1 
         THEN 'Repeat Guest' 
         ELSE 'New Guest' 
    END AS guest_type,
    total_bookings,
    total_cancellations,
    cancellation_rate_pct,
    avg_daily_rate,
    avg_special_requests
FROM guest_stats
ORDER BY is_repeated_guest DESC;
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Q9: Does getting a different room than reserved affect cancellation?
-- Business context: Understanding whether room changes drive cancellations helps management decide whether to compensate guests who receive different rooms or improve room assignment accuracy to protect revenue.

SELECT 
    CASE WHEN r.reserved_room_type = r.assigned_room_type 
         THEN 'Room Matched' 
         ELSE 'Room Changed' 
    END AS room_match_status,
    COUNT(*) AS total_bookings,
    SUM(b.is_canceled) AS total_cancellations,
    ROUND(SUM(b.is_canceled) * 100.0 / COUNT(*), 2) AS cancellation_rate_pct,
    ROUND(AVG(b.adr), 2) AS avg_daily_rate
FROM reservations r
JOIN bookings b ON r.booking_id = b.booking_id
GROUP BY room_match_status
ORDER BY cancellation_rate_pct DESC;
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Q10: Do high-value bookings cancel more or less than low-value ones?
-- Business context: Understanding whether cancellation risk correlates with booking value helps management apply value-based deposit policies requiring stricter terms for high-value bookings if they cancel more, or for low-value bookings if they represent higher volume risk.

WITH booking_revenue AS (
    -- Step 1: Calculate revenue and assign quartile to every booking
    SELECT 
        booking_id,
        hotel,
        is_canceled,
        adr,
        (stays_in_weekend_nights + stays_in_week_nights) AS total_nights,
        ROUND(adr * (stays_in_weekend_nights + stays_in_week_nights), 2) AS total_revenue,
        NTILE(4) OVER (
            ORDER BY adr * (stays_in_weekend_nights + stays_in_week_nights)
        ) AS revenue_quartile
    FROM bookings
    WHERE adr > 0  -- exclude zero-rate bookings
)
-- Step 2: Group by quartile and calculate cancellation metrics
SELECT 
    CASE revenue_quartile
        WHEN 1 THEN 'Q1 - Low Value'
        WHEN 2 THEN 'Q2 - Mid-Low Value'
        WHEN 3 THEN 'Q3 - Mid-High Value'
        WHEN 4 THEN 'Q4 - High Value'
    END AS booking_tier,
    COUNT(*) AS total_bookings,
    SUM(is_canceled) AS total_cancellations,
    ROUND(SUM(is_canceled) * 100.0 / COUNT(*), 2) AS cancellation_rate_pct,
    ROUND(AVG(adr), 2) AS avg_daily_rate,
    ROUND(AVG(total_nights), 1) AS avg_nights,
    ROUND(AVG(total_revenue), 2) AS avg_revenue
FROM booking_revenue
GROUP BY revenue_quartile
ORDER BY revenue_quartile;
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------