with series as (
	select distinct serie_id
	from caracteristicas_limpo cl
	INNER JOIN condicao c ON c.id = cl.condicao_id
	-- where c.name IN ('normal', 'underhang ball fault') 
	-- where c.name IN ('normal', 'underhang outer race') 
	-- where c.name IN ('normal', 'underhang cage fault') 
	-- where c.name IN ('normal', 'overhang ball fault') 
	-- where c.name IN ('normal', 'overhang outer race') 
	-- where c.name IN ('normal', 'overhang cage fault') 
	-- where c.name IN ('normal', 'horizontal misalignment') 
	-- where c.name IN ('normal', 'vertical misalignment') 
	where c.name IN ('normal', 'imbalance') 

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
SELECT treino,condicao_id,
-- Acelerometro 1
-- X
acel_x1_energia, 
acel_x1_variancia,
acel_x1_rms,
acel_x1_obliquidade,
acel_x1_curtose,
acel_x1_fator_crista,
-- Y
acel_y1_energia, 
acel_y1_variancia,
acel_y1_rms,
acel_y1_obliquidade,
acel_y1_curtose,
acel_y1_fator_crista,
-- Z
acel_z1_energia, 
acel_z1_variancia,
acel_z1_rms,
acel_z1_obliquidade,
acel_z1_curtose,
acel_z1_fator_crista,
-- Acelerometro 2
-- X
acel_x2_energia, 
acel_x2_variancia,
acel_x2_rms,
acel_x2_obliquidade,
acel_x2_curtose,
acel_x2_fator_crista,
-- Y
acel_y2_energia, 
acel_y2_variancia,
acel_y2_rms,
acel_y2_obliquidade,
acel_y2_curtose,
acel_y2_fator_crista,
-- Z
acel_z2_energia, 
acel_z2_variancia,
acel_z2_rms,
acel_z2_obliquidade,
acel_z2_curtose,
acel_z2_fator_crista,
-- Microfone
mic_energia,
mic_variancia,
mic_rms,
mic_obliquidade,
mic_curtose,
mic_fator_crista
FROM caracteristicas_limpo cl
INNER JOIN condicao c ON c.id = cl.condicao_id
inner join series_rotuladas sr on sr.serie_id = cl.serie_id