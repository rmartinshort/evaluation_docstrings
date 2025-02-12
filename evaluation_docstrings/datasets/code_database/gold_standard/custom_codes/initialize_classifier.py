from torchvision import models as models
import torch.nn as nn


def initialize_model(
    model_name, num_classes, feature_extract, use_pretrained=True, final_dropout=0.2
):
    """
    Note that feature extract is bool and set to
    true of we don't want to fine-tune the hidden layers
    """

    model_ft = None

    if "resnet" in model_name:
        """ Resnet models
        See https://pytorch.org/hub/pytorch_vision_resnet/
        """
        model_size = model_name[-2:]
        if model_size == "18":
            model_ft = models.resnet18(pretrained=use_pretrained)
        elif model_size == "34":
            model_ft = models.resnet34(pretrained=use_pretrained)
        elif model_size == "50":
            model_ft = models.resnet50(pretrained=use_pretrained)
        else:
            # Default to resnet 101
            model_ft = models.resnet101(pretrained=use_pretrained)

        set_parameter_requires_grad(model_ft, feature_extract)
        num_ftrs = model_ft.fc.in_features

        # Set the final classification layer to include droput
        model_ft.fc = nn.Sequential(
            nn.Dropout(final_dropout), nn.Linear(num_ftrs, num_classes)
        )

    else:
        print("Invalid model name, exiting...")
        exit()

    return model_ft
