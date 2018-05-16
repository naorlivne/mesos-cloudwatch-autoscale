# mesos-cloudwatch-autoscale

simple container which designed to run inside metronome (or other cron like mesos framework) which takes the current CPU\mem\HD percentage and exports it to cloudwatch every X minutes in order to allow that metrics to be used to autoscale the mesos cluster workers according to current use percentage.

required envs:
* AWS_ACCESS_KEY_ID (or IAM role)
* AWS_SECRET_ACCESS_KEY (or IAM role)
* AWS_DEFAULT_REGION (example: us-east-1)
* MESOS_URL (example: leader.mesos for use inside mesos)
* MESOS_PORT (example: 5050)
* METRICS_PREFIX (example: mesos_)
* METRICS_NAMESPCE (example: mesos/)

the script will then create 3 new cloudwatch metrics named:
* metrics_prefix_mem_percentage
* metrics_prefix_cpu_percentage
* metrics_prefix_hd_percentage

example metronome job config:
``````
{
  "id": "mesos-cloudwatch-autoscale",
  "run": {
    "cmd": "docker pull naorlivne/mesos-cloudwatch-autoscale:latest && docker run --rm  -e METRICS_NAMESPACE=mesos/ -e AWS_ACCESS_KEY_ID=your_aws_Key -e AWS_SECRET_ACCESS_KEY=your_aws_secret -e MESOS_URL=http://leader.mesos -e AWS_DEFAULT_REGION=us-east-1 -e MESOS_PORT=5050 -e METRICS_PREFIX=vidazoo_dcos naorlivne/mesos-cloudwatch-autoscale:latest",
    "cpus": 0.1,
    "mem": 256,
    "disk": 100
  },
  "schedules": [
    {
      "id": "default",
      "enabled": true,
      "cron": "*/5 * * * *",
      "timezone": "UTC",
      "concurrencyPolicy": "ALLOW",
      "startingDeadlineSeconds": 30
    }
  ]
}
````````