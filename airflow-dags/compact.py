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

with DAG('compact-01', default_args=default_args, schedule_interval=None,
         max_active_tasks=30, max_active_runs=30) as dag:
    load_resources = V1ResourceRequirements(requests={"memory": "36Gi"}, limits={"memory": "36Gi"})
    node_selector = {"loader-node": "true"}
    image_pull_secrets = [k8s.V1LocalObjectReference('falkonry-pull-secret')]

    envs = list()
    load_file = "{{ dag_run.conf['load_file'] }}"
    compact_file = "{{ dag_run.conf['compact_file'] }}"

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
        "falkonry_tiling_bulk_concurrency": "20",
        "falkonry_tiling_bulk_file_concurrency": "10",
        "falkonry_tiling_bulk_compact_parent_concurrency": "10",
        "AIOCACHE_DISABLE": "1",
        "LOG_LEVEL": "DEBUG"
    }
    for k, v in env_dict.items():
        envs.append(k8s.V1EnvVar(name=k, value=v))

    envs.append(k8s.V1EnvVar(name="falkonry_clue_livestream_non_cloud", value="true"))
    envs.append(k8s.V1EnvVar(name="falkonry_tiling_bulk_compact_concurrency", value="20"))
    envs.append(k8s.V1EnvVar(name="AWS_DYN_ENDPOINT", value="http://localhost:8000"))
    compact_resources = V1ResourceRequirements(requests={"memory": "36Gi"}, limits={"memory": "36Gi"})

    compact = KubernetesPodOperator(
        namespace='falkonry',
        image="quay.io/falkonry/tiling:issue-9965.latest",
        image_pull_secrets=image_pull_secrets,
        resources=compact_resources,
        node_selector=node_selector,
        env_vars=envs,
        image_pull_policy="Always",
        startup_timeout_seconds=60*30,
        cmds=[
            "/bin/bash",
            "-c",
            f"/jobs/buildtiles/Run.sh {compact_file}"
        ],
        labels={"purpose": "dataload", "process": "compact"},
        name="dataload-compact",
        task_id="dataload-compact",
        is_delete_operator_pod=False,
        get_logs=False,
        dag=dag
    )
    compact
