from db_utils import query_data


series_fatias = query_data("SELECT DISTINCT serie, fatia from amostras where fatia is not null")

for s,f in series_fatias:
    [seq, acel_x1, acel_y1, acel_z1, acel_x2, acel_y2, acel_z2, mic] = query_data(f"SELECT seq, acel_x1, acel_y1, acel_z1, acel_x2, acel_y2, acel_z2, mic from amostras where serie = {s} and fatia={f} order by seq")

    print(acel_x1)


