#bin/bash

source ./src/var.sh

az group create --name $resourceGroup --location $location
az containerapp env create -n ${prefix}cae -g $resourceGroup --location $location
az acr create --resource-group $resourceGroup --name $acrName --sku Basic
az storage account create -n $storageNme -g $resourceGroup -l $location --sku Standard_LRS