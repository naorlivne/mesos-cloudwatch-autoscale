import os, requests, boto3, time
mesos_url = os.environ["MESOS_URL"]
mesos_port = os.environ["MESOS_PORT"]
metrics_prefix = os.environ["METRICS_PREFIX"]
metrics_namespace = os.environ["METRICS_NAMESPACE"]


def get_mesos_metrics(mesos_url, mesos_port):
    headers = {
        'cache-control': "no-cache"
    }
    response = requests.request("GET", mesos_url + ":" + mesos_port + "/metrics/snapshot", headers=headers, timeout=10)
    mesos_info = response.json()
    cpu_percent, mem_percent, hd_percent = (mesos_info["master/cpus_percent"] * 100.0), \
                                           (mesos_info["master/mem_percent"] * 100.0), \
                                           (mesos_info["master/disk_percent"] * 100.0)
    return cpu_percent, mem_percent, hd_percent


def send_to_cloudwatch(metrics_prefix, metrics_namespace, used_cpu_percent, used_mem_percent, used_hd_percent):
    client = boto3.client(
        'cloudwatch'
    )

    client.put_metric_data(
        Namespace=metrics_namespace,
        MetricData=[
            {
                'MetricName': metrics_prefix + "_cpu_percentage",
                'Dimensions': [
                    {
                        'Name': 'cpu_percentage',
                        'Value': 'cpu_percentage'
                    },
                ],
                'Timestamp': int(time.time()),
                'Value': used_cpu_percent,
                'Unit':  'Percent'
            },
        ]
    )

    client.put_metric_data(
        Namespace=metrics_namespace,
        MetricData=[
            {
                'MetricName': metrics_prefix + "_mem_percentage",
                'Dimensions': [
                    {
                        'Name': 'mem_percentage',
                        'Value': 'mem_percentage'
                    },
                ],
                'Timestamp': int(time.time()),
                'Value': used_mem_percent,
                'Unit':  'Percent'
            },
        ]
    )

    client.put_metric_data(
        Namespace=metrics_namespace,
        MetricData=[
            {
                'MetricName': metrics_prefix + "_hd_percentage",
                'Dimensions': [
                    {
                        'Name': 'hd_percentage',
                        'Value': 'hd_percentage'
                    },
                ],
                'Timestamp': int(time.time()),
                'Value': used_hd_percent,
                'Unit':  'Percent'
            },
        ]
    )


used_cpu_percent, used_mem_percent, used_hd_percent = get_mesos_metrics(mesos_url, mesos_port)
send_to_cloudwatch(metrics_prefix, metrics_namespace, used_cpu_percent, used_mem_percent, used_hd_percent)
