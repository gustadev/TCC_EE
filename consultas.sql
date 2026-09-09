-- Calcular a variancai dos dados
INSERT INTO estatistica_valor (
    value,
    sample_start,
    sample_end,
    estatistica,
    serie,
    sensor
)
SELECT
    variance(a.value) AS value,
    MIN(a.seq) AS sample_start,
    MAX(a.seq) AS sample_end,
    1 AS estatistica,
    a.serie,
    a.sensor
FROM amostras a
GROUP BY a.serie, a.sensor
ORDER BY a.serie, a.sensor;


-- KMedias Classificador Teste

SELECT 
	SUM(CASE WHEN Condicao=1 and Class=1 THEN 1 END) Normal_True, 
	SUM(CASE WHEN Condicao=1 and Class=2 THEN 1 END) Normal_False,
	SUM(CASE WHEN Condicao=2 and Class=2 THEN 1 END) Fault_True,
	SUM(CASE WHEN Condicao=2 and Class=1 THEN 1 END) Fault_False 
FROM 
(
	Select s.Serie, sc.condicao as Condicao, k.condicao as Class ,MIN(sqrt(power(s.A1X-k.A1X,2)+power(s.A1Y-k.A1Y,2)+power(s.A1Z-k.A1Z,2)+power(s.A2X-k.A2X,2)+power(s.A2Y-k.A2Y,2)+power(s.A2Z-k.A2Z,2)+power(s.MIC-k.MIC,2))) as Distancia
	FROM Variancia_Serie s 
	INNER JOIN serie_condicao sc ON s.Serie = sc.serie 
	INNER JOIN Variancia_Kmeans k
	WHERE sc.condicao in (1,2) and k.Condicao in (1,2)
	GROUP BY s.Serie, sc.condicao 
	ORDER BY s.Serie, sc.condicao 
)