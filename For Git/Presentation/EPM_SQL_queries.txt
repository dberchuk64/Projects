-- SQL-запросы в DBeaver
-- База Education01.db

--1.1 Количество студентов
SELECT 	count(student_id) AS students_quantity
FROM logs

--1.2 Количество записей процесса сдачи
SELECT COUNT(*)
FROM processes


--2. Период обучения, - от начала первой сессии до конца последней сессии
-- Дата и время предобработаны в Python
WITH session_time_CTE AS (
	SELECT 	p."session",
			p.start_time, 
			SUBSTR(p.start_time, 1, INSTR(p.start_time, ' ') - 1) as dt,
			JULIANDAY(SUBSTR(p.start_time, 1, INSTR(p.start_time, ' ') - 1)) AS jd 
	FROM processes p 
	)
SELECT 	"session",
		start_time,
		dt,
		DATE(MIN(jd)) AS min_max_time 
FROM session_time_CTE	
UNION
SELECT 	"session",
		start_time,
		dt,
		DATE(MAX(jd)) AS min_max_time 
FROM session_time_CTE	
	

--3. Топ 10 студентов по успеваемости
SELECT *
FROM (
	SELECT 	student_id,
			"total_(100_points)",
			ROW_NUMBER() OVER(ORDER BY "total_(100_points)" DESC) AS rating
	FROM (		
		SELECT 	student_id,
				"total_(100_points)"		
		FROM final_grades_first fgf
		UNION
		SELECT 	student_id,
				"total_(100_points)"		
		FROM final_grades_second fgs 
		)
	)
WHERE rating <= 10


-- 4. Статистика по успеваемости
-- Среднее, мода, медиана, дисперсия

WITH fga AS (
	SELECT 	student_id, 
			max("total_(100_points)") as student_total,
			ROW_NUMBER() OVER ( ORDER BY "total_(100_points)" DESC) AS total_rating
	FROM (
			SELECT 	student_id,
					"total_(100_points)"	
			FROM final_grades_first fgf
			UNION
			SELECT 	student_id,
					"total_(100_points)"	
			FROM final_grades_second fgs 	
			)
	GROUP BY student_id
		)
SELECT 	*,
		max(fga.student_total) OVER w_all AS total_max,
		min(fga.student_total) OVER w_all AS total_min,
		round( avg(fga.student_total) OVER w_all, 2) AS total_avg,
		(SELECT	student_total --max(freq)
	      FROM (SELECT 	fga.student_id,
						fga.student_total,
						COUNT(fga.student_id) AS freq
				FROM fga
				GROUP BY fga.student_total
				ORDER BY COUNT(fga.student_id) DESC 
				LIMIT 1
				) 
		) AS total_moda,
		(SELECT AVG(student_id) --as total_median
		FROM (SELECT student_id
		      FROM fga
		      ORDER BY student_id
		      LIMIT 2 - (SELECT COUNT(*) FROM fga) % 2    -- odd 1, even 2
		      OFFSET (SELECT (COUNT(*) - 1) / 2
              FROM fga))
         ) AS total_mean,
         (SELECT	ROUND( AVG(sq_div) OVER(ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING), 2 ) AS dispersion_tst
			FROM (
				SELECT 	fga.student_id,
				fga.student_total,		
				avg(fga.student_total) OVER(ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS t_avg,
				ABS( ( fga.student_total - (avg(fga.student_total) OVER(ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)) ) * 2 ) AS sq_div
				FROM fga
				GROUP BY fga.student_id
				) 
		) AS dispersion
FROM fga
WINDOW w_all AS (ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)


--Мода отдельным запросом
SELECT 	fga.student_id,
		fga.student_total,
		COUNT(fga.student_id) AS freq
FROM fga
GROUP BY fga.student_total
ORDER BY COUNT(fga.student_id) DESC 
--LIMIT 1


--Медиана отдельным запросом
SELECT AVG(student_id) as total_median
FROM (SELECT student_id
      FROM fga
      ORDER BY student_id
      LIMIT 2 - (SELECT COUNT(*) FROM fga) % 2    -- odd 1, even 2
      OFFSET (SELECT (COUNT(*) - 1) / 2
              FROM fga))
              
		
--Дисперсия отдельным запросом
SELECT	*,
		AVG(sq_div) OVER(ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS dispersion
FROM (
		SELECT 	fga.student_id,
		fga.student_total,		
		avg(fga.student_total) OVER(ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS t_avg,
		ABS( ( fga.student_total - (avg(fga.student_total) OVER(ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)) ) * 2 ) AS sq_div		FROM fga
		GROUP BY fga.student_id
	)



--5. Количество законченных сессий 
SELECT 	lg.student_id,
		(session_1 + session_2 + session_3 + session_4 + session_5 + session_6) AS sessions_finished
FROM logs lg
LEFT JOIN (
		SELECT 	student_id, 
				max("total_(100_points)") as student_total,
				ROW_NUMBER() OVER ( ORDER BY "total_(100_points)" DESC) AS total_rating
		FROM (
				SELECT 	student_id,
						"total_(100_points)"	
				FROM final_grades_first fgf
				UNION
				SELECT 	student_id,
						"total_(100_points)"	
				FROM final_grades_second fgs 	
				)
		GROUP BY student_id
		) AS fg
ON lg.student_id = fg.student_id


--6. Время выполнения заданий
SELECT 	sp."session",
		sp.student_id,
		sp.exercise,
		sp.activity,
		sp.start_time,
		sp.end_time,
		sp.act_time,
		strftime('%H:%M:%S',
                CAST((JULIANDAY(ex_sum_time2)) AS REAL),
                '12:00') AS ex_sum_time			
FROM (
		SELECT 	"session",
				student_id,
				exercise,
				activity,
				start_time,
				end_time,
				strftime('%H:%M:%S',
                CAST((JULIANDAY(end_time) - JULIANDAY(start_time)) AS REAL),
                '12:00') AS act_time,
				TIME( JULIANDAY(end_time)  - JULIANDAY(start_time) ) AS t_diff,
				JULIANDAY(end_time)  - JULIANDAY(start_time) AS t_diff_code,
				SUM( JULIANDAY(end_time)  - JULIANDAY(start_time) ) OVER w AS ex_sum_time2		
		FROM processes p 
		WINDOW w AS (PARTITION BY p."session", p.student_id, p.exercise ORDER BY p.student_id)  -- Время на задания за всё упражнение
		) AS sp

		
-- 7. Максимальное и минимальное время выполнения заданий
WITH session_ex_CTE  AS (		
	SELECT 	sp."session",
			sp.student_id,
			sp.exercise,
			sp.activity,
			sp.start_time,
			sp.end_time,
			sp.act_time,
			strftime('%H:%M:%S',
	                CAST((JULIANDAY(ex_sum_time2)) AS REAL),
	                '12:00') AS ex_sum_time,
	        ex_sum_time2
	FROM (
			SELECT 	"session",
					student_id,
					exercise,
					activity,
					start_time,
					end_time,
					strftime('%H:%M:%S',
	                CAST((JULIANDAY(end_time) - JULIANDAY(start_time)) AS REAL),
	                '12:00') AS act_time,
					TIME( JULIANDAY(end_time)  - JULIANDAY(start_time) ) AS t_diff,
					JULIANDAY(end_time)  - JULIANDAY(start_time) AS t_diff_code,
					SUM( JULIANDAY(end_time)  - JULIANDAY(start_time) ) OVER w AS ex_sum_time2		
			FROM processes p 
			WINDOW w AS (PARTITION BY p."session", p.student_id, p.exercise ORDER BY p.student_id)  -- Время на задания за всё упражнение
			) AS sp		
	)
	SELECT 	*,
			strftime('%H:%M:%S',
	                CAST((MIN(ex_sum_time2)) AS REAL),
	                '12:00') AS min_max_time
	FROM session_ex_CTE
	UNION
	SELECT 	*,
			strftime('%H:%M:%S',
	                CAST((MAX(ex_sum_time2)) AS REAL),
	                '12:00') AS min_max_time2
	FROM session_ex_CTE
	
