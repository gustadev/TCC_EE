with series as (
	select distinct serie_id
	from caracteristicas_limpo cl
	INNER JOIN condicao c ON c.id = cl.condicao_id
	where c.name IN ('normal', 'underhang ball fault')
),
treino as (
	select serie_id, 1 as treino
	from series
	order by RANDOM()
	limit (select count(*) * 0.8 from series)
),
teste as (
	select serie_id, 0 as treino
	from series
	where serie_id not in (select serie_id from treino)
	order by RANDOM()
),
series_rotuladas as (
	select * from treino
	union all
	select * from teste
)
SELECT treino,condicao_id,acel_x1_energia, acel_y1_energia, acel_z1_energia, acel_x2_energia, acel_y2_energia, acel_z2_energia, mic_energia
FROM caracteristicas_limpo cl
INNER JOIN condicao c ON c.id = cl.condicao_id
inner join series_rotuladas sr on sr.serie_id = cl.serie_id