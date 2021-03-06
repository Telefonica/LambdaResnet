import torch
import torch.nn as nn
import torch.nn.functional as F

class ClassificationModel(nn.Module):
    def __init__(self, backbone, frontend=None, head='mlp', num_labels=35):
        super(ClassificationModel, self).__init__()
        self.backbone = backbone['backbone']
        self.frontend = frontend
        self.backbone_dim = backbone['dim']
        self.head = head

        # If we don't use all the dataset: add unknown (+1)
        if num_labels != 35:
            num_labels = num_labels + 1
 
        if head == 'linear':
            self.classification_head = nn.Sequential(
                #nn.Dropout(0.5),
                nn.Linear(self.backbone_dim, num_labels)
            )

        elif head == 'mlp':
            self.classification_head = nn.Sequential(
                nn.Linear(self.backbone_dim, self.backbone_dim),
                nn.ReLU(), nn.Linear(self.backbone_dim, num_labels)
            )
        
        else:
            raise ValueError('Invalid head {}'.format(head))

    def forward(self, x):
        if self.frontend is not None:
            x = self.frontend(x)
        
        features = self.classification_head(self.backbone(x))
        features = F.normalize(features, dim = 1)
        return features