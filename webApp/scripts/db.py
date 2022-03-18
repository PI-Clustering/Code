from django.db import connection
from collections import defaultdict


def get_data():

    query_string = '''select b.algo_type, b.data_set, b.size, d.iteration_no,b.n_iterations,  b.t_cluster as t_cluster_whole, d.t_cluster as t_cluster_cumulative,  d.f_score as adj_random_index, d.ami
    from webApp_datapoint as d join webApp_benchmark as b on d.benchmark_id == b.id
    where d.benchmark_id in (
        select max(b.id)
        from webApp_datapoint as d join webApp_benchmark as b on d.benchmark_id == b.id
        where d.id not NULL
        group by b.algo_type)'''

    with connection.cursor() as cursor:
        data = cursor.execute(query_string, []).fetchall()

    series_by_dataset = defaultdict(list)
    for iteration in data:
        key, value = iteration[0:3], iteration[3:]
        series_by_dataset[key].append(value)

    time_series = []
    ami_series = []
    ari_series = []
    for key in series_by_dataset.keys():
        t = {
            'name': str(key),
            'data': []
        }
        ar = {
            'name': "ARI " + str(key),
            'data': []
        }
        am = {
            'name':  "AMI " + str(key),
            'data': []
        }
        for value in series_by_dataset[key]:
            print(value)
            t['data'].append((value[0], value[3]))  # it_no,t_cum
            ar['data'].append((value[0], value[4]))  # it_no,ari
            am['data'].append((value[0], value[5]))  # it_no,ari
        time_series.append(t)
        ari_series.append(ar)
        ami_series.append(am)

    series = {
        "time": time_series,
        "ari": ari_series,
        "ami": ami_series
    }

    return series