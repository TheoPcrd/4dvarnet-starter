from src.models import Lit4dVarNet, GradSolverZero, BilinAEPriorCost, BaseObsCost, ConvLstmGradModel
from contrib.multivar.multivar_models import Multivar4dVarNet
from contrib.multivar.multivar_utils import MultivarBatchSelector
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import pandas as pd
from pathlib import Path

import sys
sys.path.append("/Odyssey/private/t22picar/4Dvarnet_uv/4dvarnet-starter/contrib/multivar/")
from contrib.multivar.parts import StandardBlock, ResBlock, Down, Up, OutConv

import kornia.filters as kfilts

class MultivarUNet(Multivar4dVarNet):

    def step(self, batch, phase=""):

        # SKIP BATCH TO IMPLEMENT #
        if self.skip_batch(batch):
            return None, None

        training_loss, out = self.multivar_step(batch, phase)

        return training_loss, out
    
    # Add dimensions 
    def forward(self, batch):
        batch_input = self.multivar_selector.multivar_prior_input(batch).nan_to_num()
        return self.solver(batch_input)
    


class UNet(nn.Module):
    def __init__(self, n_channels, n_classes, bilinear=True, block=ResBlock,
                 add_input=False):
        super(UNet, self).__init__()
        #self.block = ResBlock
        self.n_channels = n_channels
        print("n_channels")
        print(n_channels)
        self.n_classes = n_classes
        print("n_classes")
        print(n_classes)
        self.add_input = add_input
        self.bilinear = bilinear
        factor = 2 if bilinear else 1

        # block-wise weight scaling factors for stabilised gradients
        sfs = 1/torch.arange(1, 10).sqrt()
        
        # define modules
        self.inc = StandardBlock(n_channels, 64)
        self.down1 = Down(64, 128, block, sf=sfs[1])
        self.down2 = Down(128, 256, block, sf=sfs[2])
        self.down3 = Down(256, 512, block, sf=sfs[3])
        self.down4 = Down(512, 1024 // factor, block, sf=sfs[4])
        
        self.up1 = Up(1024, 512 // factor, block, bilinear, sf=sfs[5])
        self.up2 = Up(512, 256 // factor, block, bilinear, sf=sfs[6])
        self.up3 = Up(256, 128 // factor, block, bilinear, sf=sfs[7])
        self.up4 = Up(128, 64, block, bilinear, sf=sfs[8])
        self.outc = OutConv(64, n_classes)
        
    def forward(self, x):
        if self.add_input:
            inp = x[:,-1].unsqueeze(1)

        x1 = self.inc(x)
        x2 = self.down1(x1)
        x3 = self.down2(x2)
        x4 = self.down3(x3)
        x5 = self.down4(x4)
        
        x = self.up1(x5, x4)
        x = self.up2(x, x3)
        x = self.up3(x, x2)
        x = self.up4(x, x1)
        
        out = self.outc(x)
        if self.add_input:
            out += inp

        return out

def cosanneal_lr_adam_unet(lit_mod, lr, T_max=100, weight_decay=0.):
    opt = torch.optim.Adam(
        [
            {"params": lit_mod.solver.parameters(), "lr": lr},
        ], weight_decay=weight_decay
    )
    return {
        "optimizer": opt,
        "lr_scheduler": torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=T_max),
    }

def get_multivar_only_prior_dims_in(multivar_dict, channels_per_dim):

    dims_in = 0
    for var, var_info in multivar_dict.items():
        if var_info.input_arch == 'prior_input':
            dims_in+=1
    return dims_in * channels_per_dim