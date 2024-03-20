# Variables
prefix="cajobtest"
acrName=${prefix}acr
location="japaneast"
resourceGroup=${prefix}rg
storageNme=${prefix}st

attachAcr=false
senderImageName="cajobsender"
processorImageName="cajobprocessor"
receiverImageName="cajobreceiver"
images=($senderImageName $processorImageName $receiverImageName)
filenames=(cajobsender.py cajobprocessor.py cajobreceiver.py)


tag="latest"
# Azure Subscription and Tenant
subscriptionId=$(az account show --query id --output tsv)
subscriptionName=$(az account show --query name --output tsv)
tenantId=$(az account show --query tenantId --output tsv)