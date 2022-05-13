from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from kubernetes.client import models as k8s
from kubernetes.client import V1ResourceRequirements

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.utcnow()
}

with DAG('load_opt2', default_args=default_args, schedule_interval=None,
         max_active_tasks=20, max_active_runs=20) as dag:
    load_resources = V1ResourceRequirements(requests={"memory": "18Gi"}, limits={"memory": "18Gi"})
    node_selector = {"loader-node": "true"}
    image_pull_secrets = [k8s.V1LocalObjectReference('falkonry-pull-secret')]

    envs = list()
    load_file = "{{ dag_run.conf['load_file'] }}"
    compact_file = "{{ dag_run.conf['compact_file'] }}"
    task_id = "{{ dag_run.conf['task_id'] }}"

    envs.append(k8s.V1EnvVar(name="AWS_SECRET_ACCESS_KEY",
                             value_from=k8s.V1EnvVarSource(
                                 secret_key_ref=k8s.V1SecretKeySelector(key="secret-id", name="aws-key-prod"))
                             )
                )
    envs.append(k8s.V1EnvVar(name="AWS_DEFAULT_REGION",
                             value_from=k8s.V1EnvVarSource(
                                 secret_key_ref=k8s.V1SecretKeySelector(key="region-w2", name="aws-key-prod"))
                             )
                )
    envs.append(k8s.V1EnvVar(name="AWS_REGION",
                             value_from=k8s.V1EnvVarSource(
                                 secret_key_ref=k8s.V1SecretKeySelector(key="region-w2", name="aws-key-prod"))
                             )
                )
    envs.append(k8s.V1EnvVar(name="AWS_ACCESS_KEY_ID",
                             value_from=k8s.V1EnvVarSource(
                                 secret_key_ref=k8s.V1SecretKeySelector(key="key-id", name="aws-key-prod"))
                             )
                )
    env_dict = {
        "DEST_BUCKET_NAME": "falkonry-prod-backend",
        "falkonry_clue_livestream_aws_dynamodb_context_source_tablename": "H8W8864TVLFOSQ1V-master-ContextMetadata",
        "falkonry_clue_livestream_aws_dynamodb_tilemetadata_tablename": "H8W8864TVLFOSQ1V-master-TileMetadata-v01-01",
        "falkonry_clue_livestream_non_cloud": "true",
        "falkonry_tiling_bulk_concurrency": "5",
        "falkonry_tiling_bulk_file_concurrency": "5",
        "falkonry_tiling_bulk_metadata_read_concurrency": "50",
        "falkonry_tiling_bulk_task_row_count_limit": "1000000",
        "falkonry_tiling_bulk_split_reader_batch_size": "500000",
        "falkonry_tiling_bulk_db_concurrency": "10",
        "AIOCACHE_DISABLE": "1",
        "S3FS_LOGGING_LEVEL": "DEBUG"
    }
    for k, v in env_dict.items():
        envs.append(k8s.V1EnvVar(name=k, value=v))

    data_load = KubernetesPodOperator(
        namespace='falkonry',
        image="quay.io/falkonry/tiling:issue-9965.latest",
        image_pull_secrets=image_pull_secrets,
        resources=load_resources,
        node_selector=node_selector,
        env_vars=envs,
        image_pull_policy="Always",
        startup_timeout_seconds=60 * 30,
        cmds=[
            "/bin/bash",
            "-c",
            f"/jobs/buildtiles/Run.sh {load_file}"
        ],
        labels={"purpose": "dataload", "process": "split"},
        name=f"split",
        task_id=f"split",
        get_logs=False,
        is_delete_operator_pod=False,
        dag=dag
    )
    data_load
