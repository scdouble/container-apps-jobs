#!/bin/bash
source ./src/var.sh

QUEUE_CONNECTION_STRING=$(az storage account show-connection-string -g containerappjobtest-rg --name cajobtestst --query connectionString --output tsv)

az containerapp job create --name "cajobreceiver" \
    --resource-group containerappjobtest-rg \
    --environment managedEnvironment-containerappjob-975a  \
    --trigger-type "Event"  \
    --replica-timeout "1800"  \
    --replica-retry-limit "1"  \
    --replica-completion-count "1"  \
    --parallelism "1"  \
    --min-executions "0"  \
    --max-executions "10"  \
    --polling-interval "60"  \
    --scale-rule-name "queue"  \
    --scale-rule-type "azure-queue"  \
    --scale-rule-metadata "accountName=cajobtestst" \
                            "queueName=outputqueue" \
                            "queueLength=1"  \
    --scale-rule-auth "connection=connection-string-secret"  \
    --image "cajobtestacr.azurecr.io/cajobreceiver:v1"  \
    --registry-password "ZWevcyBtNkkQ9lFVi1Cb55Eqi67ARWRxxpQiIr6SdK+ACRDR3ZyO" \
    --registry-username "cajobtestacr" \
    --cpu "0.5"  \
    --memory "1Gi"  \
    --secrets "connection-string-secret=$QUEUE_CONNECTION_STRING"  \
    --registry-server "cajobtestacr.azurecr.io"  \
    --env-vars "OUTPUT_QUEUE_NAME=outputqueue" \
                "AZURE_STORAGE_CONNECTION_STRING=secretref:connection-string-secret" \
                "FULLY_QUALIFIED_NAMESPACE=cajobtestst.queue.core.windows.net"


az containerapp job create -n MyContainerappsjob  \
    -g containerappjobtest-rg  \
    --environment managedEnvironment-containerappjob-975a  \
    --trigger-type Manual  \
    --replica-timeout 5  \
    --replica-retry-limit 2  \
    --replica-completion-count 1  \
    --parallelism 1  \
    --image "cajobtestacr.azurecr.io/cajobreceiver:v1"  \
    --registry-server "cajobtestacr.azurecr.io"  \
    --registry-password "ZWevcyBtNkkQ9lFVi1Cb55Eqi67ARWRxxpQiIr6SdK+ACRDR3ZyO" \
    --registry-username "cajobtestacr" \
