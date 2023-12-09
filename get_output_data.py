
# azureml-core of version 1.0.72 or higher is required
from azureml.core import Workspace, Dataset

subscription_id = '47f8d97d-2cc4-431e-96a1-d814672a1b64'
resource_group = 'chiahui.yeh-rg'
workspace_name = 'ece1779-project'

workspace = Workspace(subscription_id, resource_group, workspace_name)

#dataset = Dataset.get_by_id(workspace, '4a2e9660-cd5e-40c0-b6fd-83c7dbdd89a6')
dataset = Dataset.get_by_name(workspace, name='MD-shipping-forecast-training-1-Train_Model-Trained_model-69f6a3eb')
dataset.download(target_path='.', overwrite=False)