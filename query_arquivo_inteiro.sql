with 
series_normal as (
	select distinct serie_id,s.ensaio 
	from caracteristicas_limpo_inteiro cl
	INNER JOIN condicao c ON c.id = cl.condicao_id
	inner join serie s on s.id = cl.serie_id 
	where c.name = 'normal'
),
series_falha as (
	select distinct cl.serie_id,s.ensaio 
	from caracteristicas_limpo_inteiro cl
	INNER JOIN condicao c ON c.id = cl.condicao_id
	inner join serie s on s.id = cl.serie_id 
	inner join series_normal sn on sn.ensaio = s.ensaio  
	where c.name in (<lista_de_condicoes>) and c.name <> 'normal'
),
series as (
	select serie_id from series_normal 
	union all 
	select serie_id from series_falha 
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
SELECT 
treino,
condicao_id,
-- Acelerometro 1
-- X
acel_x1_variancia,
acel_x1_rms,
acel_x1_obliquidade,
acel_x1_curtose,
acel_x1_fator_crista,
-- Y
acel_y1_variancia,
acel_y1_rms,
acel_y1_obliquidade,
acel_y1_curtose,
acel_y1_fator_crista,
-- Z
acel_z1_variancia,
acel_z1_rms,
acel_z1_obliquidade,
acel_z1_curtose,
acel_z1_fator_crista,
-- Acelerometro 2
-- X
acel_x2_variancia,
acel_x2_rms,
acel_x2_obliquidade,
acel_x2_curtose,
acel_x2_fator_crista,
-- Y
acel_y2_variancia,
acel_y2_rms,
acel_y2_obliquidade,
acel_y2_curtose,
acel_y2_fator_crista,
-- Z
acel_z2_variancia,
acel_z2_rms,
acel_z2_obliquidade,
acel_z2_curtose,
acel_z2_fator_crista,
-- Microfone
mic_variancia,
mic_rms,
mic_obliquidade,
mic_curtose,
mic_fator_crista
FROM caracteristicas_limpo_inteiro cl
INNER JOIN condicao c ON c.id = cl.condicao_id
inner join series_rotuladas sr on sr.serie_id = cl.serie_id
