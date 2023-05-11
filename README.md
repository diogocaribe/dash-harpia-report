**Harpia DashBoard Project**

* Criando a tabela de cruzamentos entre municipio e desmatamento

'''sql
CREATE OR REPLACE VIEW public.vw_decremento_municipio
AS 
SELECT row_number() OVER () AS id, nome, view_date, round(((st_area(st_transform(t.geom, 5555)))/10000)::numeric, 2) AS area_ha
FROM (
	SELECT ms.nome AS nome,
		md.view_date,
		st_union(st_intersection(ms.geom, md.geom)) AS geom
	FROM limite.municipio_sei_2018 ms,
	monitoramento_dissolve md
	WHERE st_intersects(md.geom, ms.geom)
	GROUP BY nome, view_date
) t;
'''
